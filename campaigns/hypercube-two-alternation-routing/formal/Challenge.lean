module

public import Mathlib.Computability.TuringMachine.Computable

@[expose] public section

namespace HypercubeTwoAlternationRouting

/-- Q001's self-delimiting binary natural; length is logarithmic, not unary. -/
def encodeNat (n : Nat) : List Bool :=
  let bits := (Nat.toDigits 2 n).map (fun c => c == '1')
  List.replicate bits.length true ++ [false] ++ bits

def encodeList {α : Type} (encode : α → List Bool) (xs : List α) : List Bool :=
  encodeNat xs.length ++ xs.flatMap encode

def encodeOption {α : Type} (encode : α → List Bool) : Option α → List Bool
  | none => [false]
  | some x => true :: encode x

/-- None denotes mathematical nonexistence, never an execution error. -/
def searchOutput {I W : Type} (legal : I → Bool) (witness : I → W → Bool)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w = true
  | none => legal x = true ∧ ¬ ∃ w, witness x w = true

/-- Relational version for witnesses with quantified real or optimality conditions. -/
def relationalOutput {I W : Type} (legal : I → Bool) (witness : I → W → Prop)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w
  | none => legal x = true ∧ ¬ ∃ w, witness x w


def cubeAdjacent (dimension u v : Nat) : Bool :=
  ((List.range dimension).filter (fun i => u.testBit i != v.testBit i)).length == 1
structure Source where
  dimension : Nat
  active : List Bool
  budget : Nat
  deriving Repr
def legalSource (x : Source) : Bool := x.dimension ≥ 1 && x.active.length == 2^x.dimension
def sourceWitness (x : Source) (chosen : List Nat) : Bool :=
  decide chosen.Nodup && chosen.length ≤ x.budget && chosen.all (fun v => x.active[v]? == some true) &&
  (List.range x.active.length).all (fun v => x.active[v]? != some true ||
    chosen.any (fun u => u == v || cubeAdjacent x.dimension u v))
structure Demand where
  start : Nat
  finish : Nat
  weight : Nat
  deriving Repr
structure Instance where
  dimension : Nat
  demands : List Demand
  bound : Nat
  deriving Repr
def legalTarget (x : Instance) : Bool := x.dimension ≥ 1 &&
  x.demands.all (fun d => d.start < 2^x.dimension && d.finish < 2^x.dimension && d.start != d.finish && d.weight > 0)
abbrev Matching := List (Nat × Nat)
def matching (x : Instance) (m : Matching) : Bool :=
  m.all (fun e => e.1 < 2^x.dimension && e.2 < 2^x.dimension) &&
  decide ((m.flatMap (fun e => [e.1,e.2])).Nodup)
structure Route where
  vertices : List Nat
  medium : List Bool
  deriving Repr
def route (x : Instance) (m : Matching) (d : Demand) (r : Route) : Bool :=
  r.vertices.head? == some d.start && r.vertices.getLast? == some d.finish &&
  r.vertices.length == r.medium.length+1 && r.vertices.all (· < 2^x.dimension) &&
  ((r.vertices.zip r.vertices.tail).zip r.medium).all (fun ((u,v),dynamic) =>
    if dynamic then m.contains (u,v) || m.contains (v,u) else cubeAdjacent x.dimension u v) &&
  ((r.medium.zip r.medium.tail).filter (fun (a,b) => a != b)).length ≤ 2
def twiceCost (r : Route) : Nat := (r.medium.map (fun b => if b then 1 else 2)).sum
def targetWitness (x : Instance) (m : Matching) : Prop := matching x m = true ∧
  ∃ routes : List Route, routes.length = x.demands.length ∧
    (x.demands.zip routes).all (fun (d,r) => route x m d r) = true ∧
    ((x.demands.zip routes).map (fun (d,r) => d.weight*twiceCost r)).sum ≤ x.bound
def validSourceOutput := searchOutput legalSource sourceWitness
def validTargetOutput := relationalOutput legalTarget targetWitness
def encodeSource (x : Source) := encodeNat x.dimension ++ encodeList (fun b => [b]) x.active ++ encodeNat x.budget
def encodeTarget (x : Instance) := List.replicate x.dimension true ++ [false] ++
  encodeList (fun d => encodeNat d.start ++ encodeNat d.finish ++ encodeNat d.weight) x.demands ++ encodeNat x.bound
def encodeMatching := encodeList (fun e : Nat × Nat => encodeNat e.1 ++ encodeNat e.2)

/-- Both algorithms use Q001's explicit bit encoding and TM2 cost model.
Recovery receives the full pair of source instance and target output. -/
def Reduction (forward : Source → Instance)
    (recover : Source × Option Matching → Option (List Nat)) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime encodeSource encodeTarget forward) ∧
  Nonempty (Turing.TM2ComputableInPolyTime
    (fun input => encodeSource input.1 ++ (encodeOption encodeMatching) input.2)
    (encodeOption (encodeList encodeNat)) recover) ∧
  (∃ bound : Polynomial Nat, ∀ x,
    (encodeTarget (forward x)).length ≤ bound.eval (encodeSource x).length) ∧
  (∃ bound : Polynomial Nat, ∀ input,
    ((encodeOption (encodeList encodeNat)) (recover input)).length ≤
      bound.eval (encodeSource input.1 ++ (encodeOption encodeMatching) input.2).length) ∧
  (∀ x, legalSource x = true → legalTarget (forward x) = true) ∧
  (∀ x, legalSource x = true → ∀ y, validTargetOutput (forward x) y →
    validSourceOutput x (recover (x, y)))


def Goal : Prop :=
  ∃ (forward : Source → Instance)
    (recover : Source × Option Matching → Option (List Nat)), Reduction forward recover

/-- Open question only; this placeholder is not a solution. -/
theorem solve : Goal := by
  sorry

end HypercubeTwoAlternationRouting
