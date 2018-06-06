class TreeNode():
    def __init__(self, f, t, v):
      self.left = None
      self.right = None
      self.value = v
      self.feature = f
      self.threshold = t
    def getLeft(self):
        return self.left
    def getRight(self):
        return self.right
    def setLeft(self, v):
        self.left = v
    def setRight(self, v):
        self.right = v
    def getFeat(self):
        return self.feature
    def getThresh(self):
        return self.threshold
    def getValue(self):
        return self.value

def getDataUnlabeled():
    x = []
    input = open("testing.csv").read().split("\n")
    for index, i in enumerate(input):
        inputArray = i.split(",")
        if(index==0):
            inputArray[0] = '4'
        if(len(inputArray)==9): #number of features
            x.append(inputArray)
        # else:
        #     print(len(inputArray))
    return x

 #change name of file to load in data from a different file.
 #for training data (with labels)

def getDataLabeled():
    x = []
    y = []
    input = open("training.csv").read().split("\n")
    for i in input:
        inputArray = i.split(",")
        if(len(inputArray)==10): #number of features + number of labels
            # exp = inputArray.pop(len(inputArray)-1)
            x.append(inputArray)
            # y.append(exp)
        # else:
        #     print(len(inputArray))
    return x,y

def generateOutputFile(y_test):
	with open('out.csv', 'w') as file:
	    file.write("id,solution\n")
	    for i in range(len(y_test)):
	        file.write(str(i+1)+ ","+ (str(y_test[i])+"\n"))

def impurity(matrix):
    if len(matrix) == 0:
        return 0
    zc = 0
    oc = 0
    for x in matrix:
        if x[len(x) - 1] == '0':
            zc +=1
        else:
            oc +=1

    return 1 - (zc/len(matrix))**2 - (oc/len(matrix))**2

def split(matrix, feature, threshold):
   #split matrix into leftchild, rightchild
   lchild, rchild = list(), list()
   for x in matrix:
    #    print(x[feature])
       if int(x[feature]) < threshold:
           lchild.append(x)
       else:
           rchild.append(x)
   return lchild, rchild

def informationGain(parent, leftchild, rightchild):
    np = len(parent)
    infoGain = impurity(parent) - (len(leftchild)/np)*impurity(leftchild) - (len(rightchild)/np)*impurity(rightchild)
    return infoGain

def bestsplit(parent, depth):
    maxig = 0
    left, right = [], []
    feat = -1
    thresh = -1
    for feature in range(len(parent[1]) - 1):
        for x in parent:
            threshold = int(x[feature])
            lchild, rchild = split(parent, feature, threshold)
            igain = informationGain(parent, lchild, rchild)
            if igain > maxig:
                maxig = igain
                left = lchild
                right = rchild
                feat = feature
                thresh = threshold
    return maxig, feat, thresh, left, right

def buildtree(parent, val):
    m, f, t, l, r = bestsplit(parent, 0)
    head = TreeNode(f, t, val)
    #print (impurity(parent))
    if m < 0.07 or  len(l) < 2 or len(r) < 2:
        return head
    head.setLeft(buildtree(l, 0))
    head.setRight(buildtree(r, 1))
    return head

def traverse(tree, ds):
    while tree.getRight() != None:
        if int(ds[tree.getFeat()]) < int(tree.getThresh()):
            tree = tree.getLeft()
        else:
            tree= tree.getRight()
    return tree.getValue()

if __name__ == "__main__":
    x_train, y_train = getDataLabeled()
    x_test = getDataUnlabeled()

    parent = x_train
    tree = buildtree(parent, 0)

    y_test = list()
    for x in x_test:
        y_test.append(traverse(tree, x))

    # print(y_test)
    generateOutputFile(y_test)
