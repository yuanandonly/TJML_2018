import random, math

class Node:
   def __init__(self, left, right, feature, threshold, decision):
      self.left=left
      self.right=right
      self.feature=feature
      self.threshold=threshold
      self.decision=decision

def buildRandomForest(x_train, d, s, k):
    #hyperparameters to tune


    trees = []
    for i in range(k):
        x_bootstrap = []
        # for p in range(len(x_train)):
        #     x_bootstrap.append(x_train[random.randint(0, len(x_train) - 1)])
        for val in x_train:
            if( random.uniform(0, 1) < s):
                x_bootstrap.append(val)

        rl = set()
        while len(rl) < d:
            rl.add(random.randint(0, len(x_bootstrap[0]) - 1))
        #print(rl)
        remcol = [i for i in range(len(x_bootstrap[0]) - 1) if i not in rl]
        newmatrix = remove_from_matrix(x_bootstrap, remcol, [])
        trees.append(bestSplit(newmatrix, 0))
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

def caculateImpurity(matrix):
   b = 0.0
   m = 0.0
   for sample in matrix:
      if (sample[len(sample) - 1]==0):
         b+=1
      else:
         m+=1
   p1 = b/(b+m)
   p2 = m/(b+m)
   if (p1==0 or p2==0):
      return 1
   return -1*(p1*math.log(p1, 2) + p2*math.log(p2, 2))

def informationGain(parent, leftchild, rightchild):
    np = len(parent)
    infoGain = caculateImpurity(parent) - (len(leftchild)/np)*caculateImpurity(leftchild) - (len(rightchild)/np)*caculateImpurity(rightchild)
    return infoGain

def splitMatrix(matrix, feature, threshold):
   leftchild = []
   rightchild = []
   for sample in matrix:
      if (sample[feature]<threshold):
         leftchild.append(sample)
      else:
         rightchild.append(sample)
   return leftchild, rightchild

def bestSplit(parent, depth):
   maxig=-1
   t=-1
   f=-1
   l=[]
   r=[]
   for feature in range(len(parent[0])): #9 features
      for x in parent:
          threshold = float(x[feature])
          lchild, rchild = splitMatrix(parent, feature, threshold)
          if (lchild==[] or rchild==[]):
             continue
          igain = informationGain(parent, lchild, rchild)
          if igain > maxig:
              maxig = igain
              l = lchild
              r = rchild
              f = feature
              t = threshold
   #print depth
   #print f
   #print t
   if (maxig <0.05):
      b = 0
      m = 0
      for sample in parent:
         if (sample[len(parent[0]) - 1]==0):
            b+=1
         else:
            m+=1
      d = 0
      if (m>=b):
         d = 1
      n = Node(None, None, -1, -1, d)
      #print d
      #print ""
      return n
   #print ""
   ln = bestSplit(l, depth+1)
   rn = bestSplit(r, depth+1)
   n = Node(ln, rn, f, t, -1)
   return n

def traverse(tree, test):
       #print test
       temp = tree
       while(temp.decision==-1):
          if (test[temp.feature]<temp.threshold):
             temp=temp.left
          else:
             temp=temp.right
       return temp.decision

def main(d, s, k):
    x_train = getDataLabeled()
    for i in range(0, len(x_train)):
       for j in range(0, len(x_train[0])):
          x_train[i][j]=float(x_train[i][j])

    #print type(x_train[0][0])
    x_test = getDataUnlabeled()
    for i in range(0, len(x_test)):
       for j in range(0, len(x_test[0])):
          x_test[i][j]=float(x_test[i][j])

    # x_train = getDataLabeled()
    # print(len(x_train))
    # x_test = getDataUnlabeled()
    #print(x_train)
    trees = buildRandomForest(x_train, d, s, k)
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

if __name__ == "__main__":
    d = 6 #features from sample, w/o replacement
    s = 0.55 #split
    k = 55 #number of decision trees
    main(d, s, k)
