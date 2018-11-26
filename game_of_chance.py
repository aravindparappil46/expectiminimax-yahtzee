#!/usr/bin/env python3
import itertools
import sys

#------ Declaring constants here ----------- #

initial_dice = [int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])]
sum_so_far = 0
max_score = -1

#------- End of constants ------------------ #


#----------------------------------------------------
# Class which has data, children and score attributes
# Data: Value of that particular node
# Score: Score calculated for each leaf nodes by multiplying with probabilites
#----------------------------------------------------
class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []
        self.score = 0

    def add_child(self, obj):
        self.children.append(obj)


# In case of 2 die roll decisions, this function
# returns the indices of those dice to roll
# Helps in setting the other die as static

def find_which_indices_to_roll(dice_to_roll):
    indices = []
    for i in dice_to_roll:
        indices.append(initial_dice.index(i))

    return indices[0], indices[1]

# Calculates and returns the score for current combo
# Returns 25, in case of three of a kind
# Otherwise, returns the sum of digits of dice combo passed

def calculate_score(a, b, c):
    if a == b == c:
        return 25
    else:
        return sum((a,b,c))


# Creating the initial 7 combinations possible (No roll combo done last!)
roll_only_these = []
[roll_only_these.append([i]) for i in initial_dice]
[roll_only_these.append(list(i)) for i in list(itertools.combinations(initial_dice,2))]
[roll_only_these.append(list(i)) for i in list(itertools.combinations(initial_dice,3))]


# Setting the root node as given configuration of dice
root = Node(initial_dice)

# Creating 7 children for the root based on the combos made earlier
# These are the chance nodes

for i in roll_only_these:
    child = Node(i)
    root.add_child(child)

# ----------------------------------------------
# Below chunk of code calculates expected values
# for each chance node
#
# If only 1 die is to be rolled:
#   There are 3 loops which changes the position
#   of the iterator based on which die we choose
#   to roll. Other indices are left as original
#   dice
#   Probability : 1/6
#
# If 2 dice are to be rolled:
#   We find out the indices of dice to be rolled
#   and keep the other index as static
#   Probability: 1/36
#
# If all 3 dice are to be rolled:
#   Three iterators at each position are checked
#   and corresponding sum is found. No die index
#   is left static
#   Probability: 1/216
# ----------------------------------------------

for child in root.children:
    if len(child.data) == 1:
        if initial_dice.index(child.data[0]) == 0:
            for i in range(1,7):
                sum_so_far += ((1/6)*calculate_score(i,initial_dice[1],initial_dice[2]))  
            child.score = sum_so_far
            sum_so_far = 0
            
        elif initial_dice.index(child.data[0]) == 1:
            for i in range(1,7):
                sum_so_far += ((1/6)*calculate_score(initial_dice[0],i,initial_dice[2]))
            child.score = sum_so_far
            sum_so_far = 0

        else:
            for i in range(1,7):
                sum_so_far += ((1/6)*calculate_score(initial_dice[0],initial_dice[1],i))
            child.score = sum_so_far
            sum_so_far = 0

    elif len(child.data) == 2:
        index_1, index_2 = find_which_indices_to_roll(child.data)
        
        if index_1 == 0 and index_2 == 1:
            for i in range(1,7):
                for j in range(1,7):
                    sum_so_far += ((1/36)*calculate_score(i,j,initial_dice[2]))
            child.score = sum_so_far
            sum_so_far = 0

        elif index_1 == 0 and index_2 == 2:
            for i in range(1,7):
                for j in range(1,7):
                    sum_so_far += ((1/36)*calculate_score(i,initial_dice[1],j))
            child.score = sum_so_far
            sum_so_far = 0

        else:
            for i in range(1,7):
                for j in range(1,7):
                    sum_so_far += ((1/36)*calculate_score(initial_dice[0],i,j))
            child.score = sum_so_far
            sum_so_far = 0

    else:
        for i in range(1,7):
            for j in range(1,7):
                for k in range(1,7):
                    sum_so_far += ((1/216)*calculate_score(i,j,k))
        child.score = sum_so_far
        sum_so_far = 0


# Creating a node that tells the user to not roll any die
# The score of this node will either be sum of digits of initial dice
# or 25, in case of three of a kind combo (no probability multiplier)
no_roll_node = Node('no_roll')
root.add_child(no_roll_node)
root.children[7].score = calculate_score(initial_dice[0],initial_dice[1],initial_dice[2])


print("\n -----------------------------------")
print("| Chance Nodes || Expected value")
print(" -----------------------------------")
for i in range(0,len(root.children)):
    print('|',root.children[i].data,' ==> ',root.children[i].score)
print(" ----------------------------------\n")

# Amongst all the expected values, finds the max
# and returns the value of that chance node
# User should choose to roll that dice/die next!

for child in root.children:
    if child.score > max_score:
        max_score = child.score
        dice_to_roll = child

print("You had rolled", initial_dice)

if dice_to_roll.data == 'no_roll':
	print("It's best if you don't roll anything now!") 
else:
	print("You should next roll the die/dice whose face value was: ",dice_to_roll.data)
