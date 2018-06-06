import random, time
import RandomForestGeorge as forest
import compare as comp

d, s, k, maxd, maxs, maxk = 0, 0, 0, 6, 0.35, 65
maxaccuracy = 0.0
count = 0
for d in range(3, 7):
    for s in range(30, 75, 5):
        for k in range(45, 70, 5):
            forest.main(d, s/100, k)
            accuracy = comp.main()
            if(accuracy > maxaccuracy):
                maxd = d
                maxs = s/100
                maxk = k
            print(count)
            if count % 9 == 0:
                print("D: ", maxd)
                print("S: ", maxs)
                print("K: ", maxk)
            count += 1
print("D: ", maxd)
print("S: ", maxs)
print("K: ", maxk)
