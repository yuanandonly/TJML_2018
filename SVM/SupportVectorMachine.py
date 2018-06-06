import random, math
from sklearn import svm

#0.76757 c = 1, del 3, 4, 6, 7

def getDataUnlabeled(delcolumns):
    x = []
    ainput = open("testing.csv").read().split("\n")
    for index, i in enumerate(ainput):
        inputArray = i.split(",")
        if(len(inputArray)==12): #number of features
            # finangling
            del inputArray[2:4]  # name
            del inputArray[6]  # ticket
            del inputArray[7]  # cabin
            #print(inputArray)
            # number, class, sex, income, siblings, parent/children, fare, port: 0 s = Southampton, 1 c = Cherbourg, 2 q = Queenstown
            if inputArray[2] == 'male':
                inputArray[2] = 0
            else:
                inputArray[2] = 1
            if inputArray[7] == 'S':
                inputArray[7] = 0
            elif inputArray[7] == 'C':
                inputArray[7] = 1
            else:
                inputArray[7] = 2
            delcolumns.sort()
            minus = 0
            for d in delcolumns:
                del inputArray[d - minus]
                minus+=1
            bruh = list()
            for a in inputArray:
                if a != '':
                    bruh.append(float(a))
                else:
                    bruh.append(0.0)
            x.append(bruh)
        # else:
        #     print(len(inputArray))
    return x

def getDataLabeled(delcolumns):
    x = []
    y = []
    ainput = open("training.csv").read().split("\n")
    for i in ainput:
        inputArray = i.split(",")
        if(len(inputArray)==13): #number of features + number of labels
            exp = inputArray.pop(1)
            #finangling
            del inputArray[2:4]#name
            del inputArray[6]#ticket
            del inputArray[7]#cabin
            #number, class, sex, income, siblings, parent/children, fare, port: 0 s = Southampton, 1 c = Cherbourg, 2 q = Queenstown
            if inputArray[2] == 'male':
                inputArray[2] = 0
            else:
                inputArray[2] = 1
            if inputArray[7] == 'S':
                inputArray[7] = 0
            elif inputArray[7] == 'C':
                inputArray[7] = 1
            else:
                inputArray[7] = 2
            minus = 0
            for d in delcolumns:
                del inputArray[d - minus]
                minus+=1
            bruh = list()
            for a in inputArray:
                if a != '':
                    bruh.append(float(a))
                else:
                    bruh.append(0.0)
            x.append(bruh)
            y.append(int(exp))
        # else:
        #     print(len(inputArray))
    # meancol = list()
    # for a in range(len(x[0])):
    #     sum = 0
    #     count = 0
    #     for point in x:
    #         if isinstance(point[a], float):
    #             sum += point[a]
    #             count += 1
    #     meancol.append(sum/count)
    # print(meancol)
    # for i in x:
    #     for j in range(len(x[0])):
    #         if i[j] == '':
    #            i[j] = float(int(meancol[j]))
    return x, y

def generateOutputFile(y_test):
    with open('out.csv', 'w') as file:
        file.write("id,solution\n")
        for i in range(len(y_test)):
            file.write(str(i+1)+ ","+ (str(y_test[i])+"\n"))

def main(cval, choose):
    x_train, y_train = getDataLabeled(choose)
    x_test = getDataUnlabeled(choose)
    clf = svm.SVC(kernel = 'poly', degree = 4, decision_function_shape = 'ovo', C = 10**cval)
    #clf = svm.LinearSVC(C = 10**cval)
    clf.fit(x_train, y_train)
    #test
    y_test = clf.predict(x_test)
    generateOutputFile(y_test)

if __name__ == "__main__":
    main(1, [0, 3, 4, 6, 7])
