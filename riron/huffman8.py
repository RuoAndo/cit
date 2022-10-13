import numpy as np
import random as rm
import sys

# The statespace
states = ["Chabudai","Husuma","TV"]

transitionName = [["CC","CT","CH"],["HH","HT","HC"],["TT","TH","TC"]]
transitionMatrix = [[0.2,0.6,0.2],[0.1,0.6,0.3],[0.2,0.7,0.1]]

if sum(transitionMatrix[0])+sum(transitionMatrix[1])+sum(transitionMatrix[1]) != 3:
    print("Transition matrix is wrong.")
else: print("OK.")

alist = []
rndstr = []

def randstr(length,b,e):
    return ''.join([chr(rm.randint(b, e)) for _ in range(length)])

def generate_sequence(days, cPos):
    # Choose the starting state
    currentPosition = cPos
    alist.append(currentPosition)
    print("Start state: " + currentPosition)
    # Shall store the sequence of states taken. So, this only has the starting state for now.
    activityList = [currentPosition]
    i = 0
    # To calculate the probability of the activityList
    prob = 1
    while i != days:
        if currentPosition == "Chabudai":
            change = np.random.choice(transitionName[0],replace=True,p=transitionMatrix[0])
            if change == "CC":
                prob = prob * 0.2
                activityList.append("Chabudai")
                alist.append("Chabudai")
                rndstr.append(randstr(10,75,85))
                pass
            elif change == "CT":
                prob = prob * 0.6
                currentPosition = "TV"
                activityList.append("TV")
                alist.append("TV")
                rndstr.append(randstr(10,65,75))
            else:
                prob = prob * 0.2
                currentPosition = "Husuma"
                activityList.append("Husuma")
                alist.append("Husuma")
                rndstr.append(randstr(10,85,90))
                
        elif currentPosition == "Husuma":
            change = np.random.choice(transitionName[1],replace=True,p=transitionMatrix[1])
            if change == "HC":
                prob = prob * 0.5
                activityList.append("Chabudai")
                alist.append("Chabudai")
                rndstr.append(randstr(10,75,85))
                pass
            elif change == "HT":
                prob = prob * 0.2
                currentPosition = "TV"
                activityList.append("TV")
                alist.append("TV")
                rndstr.append(randstr(10,75,85))
            else:
                prob = prob * 0.3
                currentPosition = "Husuma"
                activityList.append("Husuma")
                alist.append("Husuma")
                rndstr.append(randstr(10,85,90))
                
        elif currentPosition == "TV":
            change = np.random.choice(transitionName[2],replace=True,p=transitionMatrix[2])
            if change == "TC":
                prob = prob * 0.1
                activityList.append("Chabudai")
                alist.append("Chabudai")
                rndstr.append(randstr(10,75,85))
                pass
            elif change == "TH":
                prob = prob * 0.2
                currentPosition = "Husuma"
                activityList.append("Husuma")
                alist.append("Husuma")
                rndstr.append(randstr(10,85,90))
            else:
                prob = prob * 0.7
                currentPosition = "TV"
                activityList.append("TV")
                alist.append("TV")
                rndstr.append(randstr(10,65,75))
        i += 1  


#args = sys.argv
startPosition="TV"
LENGTH = 118

generate_sequence(LENGTH, startPosition)

outstr = ''
for i in rndstr:
    outstr = outstr + i

print(outstr)
    
from collections import Counter

def MIN_PRIORITY_QUEUE(S):
    return sorted(S.items(), key=lambda x: x[1], reverse=True)

def EXTRACT_MIN(Q):
    return Q.pop()

def INSERT(Q, z):
    return Q.append(z)

def HUFFMAN(S, a):
    n = len(S)
    Q = MIN_PRIORITY_QUEUE(S)
    print(n)
    print(Q)
    for i in range(n - 1):
        print(Q)
        left = EXTRACT_MIN(Q)
        right = EXTRACT_MIN(Q)
        #print(left)
        #print(right)
        freq = left[1] + right[1]
        z = (left[0] + right[0], freq)
        INSERT(Q, z)
        #print("left:")
        #print(left)
        #print("right:")
        #print(right)
        a.append([left, "0", left[0] + right[0]])
        a.append([right, "1", left[0] + right[0]])
        Q = dict(zip([i[0] for i in Q], [i[1] for i in Q]))
        Q = MIN_PRIORITY_QUEUE(Q)
    a.append([EXTRACT_MIN(Q), "", "top"])
    return a

def PrintReslut(b):
    for i in range(len(a)):
        now = a[i][0][0]
        num = a[i][1]
        j = 0
        while a[j][2] != 'top':
            if a[i][2] == a[j][0][0]:
                num = a[j][1] + num
                i = j
                flag = 0
                for k in range(len(a)):
                    if a[k][0][0] == 'top' or a[j][2] == a[k][0][0]:
                        flag = 1
                        break
            else:
                j += 1
        if now in s:
            b.append([now, num])
    return b

def DivideS(S):
    S = list(S)
    S = Counter(S)
    S = dict(S)
    return S

print("-----")

str=outstr

s = DivideS(str)
a = HUFFMAN(s, [])
for b in sorted(PrintReslut([])):
    print(b[0] + ": " + b[1])
            
