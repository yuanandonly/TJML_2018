import random

def generateOutputFile(x_test):
	with open('out.csv', 'w') as file:
	    file.write("id,solution\n")
	    for i in range(len(x_test)):
	        file.write(str(i+1)+ ","+ str(random.randint(0, 1)) + "\n")

def getDataUnlabeled():
    x = []
    input = open("test.csv").read().split("\n")
    for index, i in enumerate(input):
        inputArray = i.split(",")
        if(len(inputArray)==7): #number of features
            x.append(inputArray)
        # else:
        #     print(len(inputArray))
    return x

if __name__ == "__main__":
    x_test = getDataUnlabeled()
    generateOutputFile(x_test)
