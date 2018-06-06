def getTrain():
    x = []
    input = open("train.csv").read().split("\n")
    count = 0
    for index, i in enumerate(input):
        inputArray = i.split(",")
        if(len(inputArray)==8): #number of features
            x.append([count, inputArray[7]])
        count+=1
        # else:
        #     print(len(inputArray))
    return x

def getOut():
    x = []
    input = open("out.csv").read().split("\n")
    for index, i in enumerate(input):
        inputArray = i.split(",")
        if inputArray[0]!="id" and len(inputArray) == 2: #number of features
            x.append(inputArray)
        # else:
        #     print(len(inputArray))
    return x

if __name__ == "__main__":
    main()

def main():
    train = getTrain()
    out = getOut()
    tot = 0
    for x in range(len(out)):
        if out[x][1] == train[x][1]:
            tot += 1
    return(tot/len(out))
