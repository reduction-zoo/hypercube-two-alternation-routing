import Challenge
open HypercubeTwoAlternationRouting
example : cubeAdjacent 3 0 4 = true := by native_decide
example : cubeAdjacent 3 0 3 = false := by native_decide
example : sourceWitness ⟨2,[true,false,false,true],1⟩ [0] = false := by native_decide
example : route ⟨2,[⟨0,3,1⟩],1⟩ [(0,3)] ⟨0,3,1⟩ ⟨[0,3],[true]⟩ = true := by native_decide
example : twiceCost ⟨[0,1,3],[false,true]⟩ = 3 := by native_decide
