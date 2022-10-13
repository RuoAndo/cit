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

#print("TV:" + str((alist.count('TV')/LENGTH)*100)+"%")
#print("Chabudai:" + str((alist.count('Chabudai')/LENGTH)*100)+"%")
#print("Husuma:" + str((alist.count('Husuma')/LENGTH)*100)+"%")

outstr = ''
for i in rndstr:
    outstr = outstr + i

print(outstr)
    
#for i in alist:
#    rstring = rstring + i[0]
#print(rstring)
            
