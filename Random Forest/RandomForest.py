import random

class TreeNode():
    def __init__(self, f, t, v):
      self.left = None
      self.right = None
      self.value = v
      self.feature = f
      self.threshold = t

def buildRandomForest(x_train):
    #hyperparameters to tune
    d = (len(x_train[0]) - 1)*0.7 #features from sample, w/o replacement
    s = 0.6 #split
    k = 50 #number of decision trees

    trees = []
    for i in range(k):
        x_bootstrap = []
        for p in range(len(x_train)):
            x_bootstrap.append(x_train[random.randint(0, len(x_train) - 1)])

        rl = set()
        while len(rl) < d:
            rl.add(random.randint(0, len(x_bootstrap[0]) - 1))
        #print(rl)
        remcol = [i for i in range(len(x_bootstrap[0]) - 1) if i not in rl]
        newmatrix = remove_from_matrix(x_bootstrap, remcol, [])
        tree = buildtree(newmatrix, 0)
        trees.append(tree)
    # train decision tree with X_bootstrap
    return trees

def most_common(lst):
    if lst.count(1) > lst.count(0):
        return 1
    return 0

def remove_from_matrix(matrix, columns, rows):
    return [
           [float(matrix[row_num][col_num])
           for col_num in range(len(matrix[row_num]))
           if not col_num in columns]
           for row_num in range(len(matrix))
           if not row_num in rows]

def testRandomForest(trees, x_test):
   y_test = []
   for x_t in x_test:
      votes = []
      for tree in trees:
         votes.append(traverse(tree, x_t))
      #print(votes)
      y_test.append(most_common(votes))
   return y_test

def getDataUnlabeled():
    x = []
    ainput = open("test.csv").read().split("\n")
    for index, i in enumerate(ainput):
        inputArray = i.split(",")
        if(len(inputArray)==7): #number of features
            x.append(inputArray)
        # else:
        #     print(len(inputArray))
    return x

 #change name of file to load in data from a different file.
 #for training data (with labels)

def getDataLabeled():
    x = []
    ainput = open("train.csv").read().split("\n")
    for i in ainput:
        inputArray = i.split(",")
        if(len(inputArray)==8): #number of features + number of labels
            # exp = inputArray.pop(len(inputArray)-1)
            x.append(inputArray)
            # y.append(exp)
        # else:
        #     print(len(inputArray))
    return x

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
        if int(x[len(x) - 1]) == 0:
            zc +=1
        else:
            oc +=1
    return 1 - (zc/len(matrix))**2 - (oc/len(matrix))**2

def informationGain(parent, leftchild, rightchild):
    np = len(parent)
    infoGain = impurity(parent) - (len(leftchild)/np)*impurity(leftchild) - (len(rightchild)/np)*impurity(rightchild)
    return infoGain

def split(matrix, feature, threshold):
   #split matrix into leftchild, rightchild
   lchild, rchild = list(), list()
   for x in matrix:
    #    print(x[feature])
       if float(x[feature]) < threshold:
           lchild.append(x)
       else:
           rchild.append(x)
   return lchild, rchild

def bestsplit(parent):
    maxig = 0.0
    left, right = [], []
    feat = 9999
    thresh = 9999
    for feature in range(len(parent[1]) - 1):
        for x in parent:
            threshold = float(x[feature])
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
    m, f, t, l, r = bestsplit(parent)
    head = TreeNode(f, t, val)
    # print(m)
    if m < 0.05 or  len(l) < 2 or len(r) < 2:
        return head
    head.left = (buildtree(l, 0))
    head.right = (buildtree(r, 1))
    return head

def traverse(tree, ds):
    while tree.right != None and tree.left != None:
        if float(ds[tree.feature]) < float(tree.threshold):
            tree = tree.left
        else:
            tree = tree.right
    return tree.value

if __name__ == "__main__":
    x_train = getDataLabeled()
    print(len(x_train))
    x_test = getDataUnlabeled()
    #print(x_train)
    trees = buildRandomForest(x_train)
    y_test = testRandomForest(trees, x_test)

    # x_traintest = []
    # for i in range(len(x_train)):
    #     x_traintest.append([x_train[i][j] for j in range(7)])
    # print(len(x_traintest))
    # trees = buildRandomForest(x_train)
    # y_test = testRandomForest(trees, x_traintest)
    # tree = buildtree(x_train, 0)
    # y_test = list()
    # for x in x_test:
    #     y_test.append(traverse(tree, x))
    # print(y_test)
    generateOutputFile(y_test)
