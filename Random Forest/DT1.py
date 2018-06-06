import math

class Node:
   def __init__(self, left, right, feature, threshold, decision):
      self.left=left
      self.right=right
      self.feature=feature
      self.threshold=threshold
      self.decision=decision

#change name of file to load in data from a different file.
#for testing data (no labels)
def getDataUnlabeled():
    x = []
    input = open("testing.csv").read().split("\n")
    for index, i in enumerate(input):
        inputArray = i.split(",")
        if(index==0):
            inputArray[0] = '4'
        if(len(inputArray)==9): #number of features           
            x.append(inputArray)
        else:
            print(len(inputArray))
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
            exp = inputArray.pop(len(inputArray)-1)
            x.append(inputArray)
            y.append(exp)
        else:
            print(len(inputArray))
    return x,y

#pass array of labels and method will generate output txt
def generateOutputFile(y_test):
	with open('out.txt', 'w') as f:
	    f.write("id,solution\n")
	    for i in range(len(y_test)):
	        f.write(str(i+1)+","+str(str(y_test[i])+"\n"))
           
x_train, y_train = getDataLabeled()
x_train2 = x_train[:]
for i in range(0, len(x_train)):
   x_train[i].append(y_train[i][0])
for i in range(0, len(x_train)):
   for j in range(0, 10):
      x_train[i][j]=int(x_train[i][j])
      
#print type(x_train[0][0])
x_test = getDataUnlabeled()
for i in range(0, len(x_test)):
   for j in range(0, 9):
      x_test[i][j]=int(x_test[i][j])
   
# TODO: Write some ML
# TODO: use model to generate y_test from X_test
# generateOutputFile(y_test)
def caculateImpurity(matrix):
   b = 0.0
   m = 0.0
   for sample in matrix:
      if (sample[9]==0):
         b+=1
      else:
         m+=1
   p1 = b/(b+m)
   p2 = m/(b+m)
   if (p1==0 or p2==0):
      return 1
   return -1*(p1*math.log(p1, 2) + p2*math.log(p2, 2))

def infoGain(parent, leftchild, rightchild):
   p = float(len(parent))
   infogain = caculateImpurity(parent)
   infogain-=len(leftchild)/p*caculateImpurity(leftchild)
   infogain-=len(rightchild)/p*caculateImpurity(rightchild)
   return infogain    

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
   max=-1
   t=-1
   f=-1
   l=[]
   r=[]
   for feature in range(0, 9): #9 features
      for threshold in range(0, 10): #check kaggle
         lchild, rchild = splitMatrix(parent, feature, threshold)
         if (lchild==[] or rchild==[]):
            continue
         igain = infoGain(parent, lchild, rchild)
         if (igain>max):
            max=igain
            t=threshold
            f=feature
            l=lchild
            r=rchild
   #print depth
   #print f
   #print t
   if (max<0.00001):
      b = 0
      m = 0
      for sample in parent:
         if (sample[9]==0):
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
   
n = bestSplit(x_train, 0)
res = []
for test in x_test:
   #print test
   temp = n
   while(temp.decision==-1):
      if (test[temp.feature]<temp.threshold):
         temp=temp.left
      else:
         temp=temp.right
   res.append(temp.decision)  
count = 0
for i in range(0, len(res)):
   if (res[i]==int(y_train[i])):
      count+=1
print count/533.0  
generateOutputFile(res)