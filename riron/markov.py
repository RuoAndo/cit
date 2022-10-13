import numpy as np
import random as rm

# The statespace
states = ["Sleep","Icecream","Run"]

# Possible sequences of events
transitionName = [["SS","SR","SI"],["RS","RR","RI"],["IS","IR","II"]]

# Probabilities matrix (transition matrix)
transitionMatrix = [[0.2,0.6,0.2],[0.1,0.6,0.3],[0.2,0.7,0.1]]

if sum(transitionMatrix[0])+sum(transitionMatrix[1])+sum(transitionMatrix[1]) != 3:
    print("Somewhere, something went wrong. Transition matrix, perhaps?")
else: print("All is gonna be okay, you should move on!! ;)")


# To save every activityList
list_activity = []
count = 0

for iterations in range(1,100):
        list_activity.append(activity_forecast(2))

for i in list_activity:
    print(i)
        
# `Range` starts from the first count up until but excluding the last count
#for iterations in range(1,10000):
#        list_activity.append(activity_forecast(2))

        # Check out all the `activityList` we collected    
#print(list_activity)

# Iterate through the list to get a count of all activities ending in state:'Run'
#for smaller_list in list_activity:
#    if(smaller_list[2] == "Run"):
#        count += 1

# Calculate the probability of starting from state:'Sleep' and ending at state:'Run'
#percentage = (count/10000) * 100
#print("The probability of starting at state:'Sleep' and ending at state:'Run'= " + str(percentage) + "%")

