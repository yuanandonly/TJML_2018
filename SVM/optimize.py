import random, time
import SupportVectorMachine as svm
import compare as comp
from itertools import combinations

maxc, maxcol = -3, []
maxaccuracy = 0.0
for c in range(-3, 3):
    for choose in combinations([x for x in range(0, 8)], 3):
        #print(list(choose))
        svm.main(c, list(choose))
        accuracy = comp.main()
        if(accuracy > maxaccuracy):
            maxc = c
            maxcol = choose
    for choose in combinations([x for x in range(0, 8)], 4):
        #print(list(choose))
        svm.main(c, list(choose))
        accuracy = comp.main()
        if(accuracy > maxaccuracy):
            maxc = c
            maxcol = choose
print("C: ", maxc)
print("Columns: ", maxcol)
