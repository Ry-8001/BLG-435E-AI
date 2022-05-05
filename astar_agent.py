import time
import random
from copy import deepcopy
from agent import Agent

#  use whichever data structure you like, or create a custom one
import queue
import heapq
from collections import deque

"""
  you may use the following Node class
  modify it if needed, or create your own
"""


class Node():

    def __init__(self, parent_node, level_matrix, player_row, player_column, depth, chosen_dir, h_value,givenCost):
        self.parent_node = parent_node
        self.level_matrix = level_matrix
        self.player_row = player_row
        self.player_col = player_column
        self.depth = depth
        self.chosen_dir = chosen_dir
        self.h = h_value + self.depth

        self.givenCost = givenCost
        
    def __lt__(self, other):
        return self.depth + self.h < other.depth + other.h

        """
            There are different strategies you can choose for
        tie breaking, that is, which node to choose when two
        nodes have equal f (g+h) values. Some of these are:

        1- Choose the node with lower h value, implying that you
        trust your heuristic more than g.

        2- Choose the node with lower g value, implying that you
        do not trust your heuristic function that much.

        3- Choose the node which is put into the
        queue earlier/later

        4- Use a secondary heuristic function to compare two 
        nodes when they have equal f value

        5- Select one of the nodes randomly. Not good for this
        assignment, but if you are making a game this also has
        an effect that makes your agent follow different routes
        each time it runs (if there are more than 1 shortest path
        to goal)

        ...
        ...
        ... 
        """


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

    def count(self):
        return len(self.elements)

class AStarAgent(Agent):

    def __init__(self):
        super().__init__()
        self.openList = PriorityQueue()

    def solve(self, level_matrix, goal, player_row, player_column):
        super().solve(level_matrix, goal, player_row, player_column)
        move_sequence = [] #frontier
        self.extendedLevels = [] #explored state
        self.costMatrix = [] #and corrseponding cost

        """
            YOUR CODE STARTS HERE
            fill move_sequence list with directions chars
        """


        level_matrix_ = [list(row) for row in level_matrix] #deepcopy(level_matrix)
        finalCost= super().real_distance(player_row,player_column,goal[0],goal[1])#distance_to_closest_apple(applePositions, player_row, player_column)  #  fill this value with your heuristic function
        row_ = len(level_matrix_)
        col_ = len(level_matrix_[0])


        s0 = Node(None, level_matrix_, player_row, player_column, 0, "-", finalCost, 0)
        self.openList.put( s0, finalCost)
        maxSize = 0

        while not self.openList.empty():
            curr_state = self.openList.get()
            self.expanded_node_count += 1
            #if not in the explored set then add
            
            self.extendedLevels.append(deepcopy(curr_state.level_matrix))
            self.costMatrix.append(curr_state.givenCost)
                
                
            if goal == [curr_state.player_row,curr_state.player_col]:
                getpath(curr_state,move_sequence)
                break

            curr_state.level_matrix[curr_state.player_row][curr_state.player_col] = 'F'

            if curr_state.player_row > 0 and not curr_state.level_matrix[curr_state.player_row-1][curr_state.player_col]=='W':
                    
                temp_level_matrix = deepcopy(curr_state.level_matrix)
                    

                temp_level_matrix[curr_state.player_row-1][curr_state.player_col] = 'P'
                #if not in the explored set 
                if temp_level_matrix not in self.extendedLevels:
                    heur_val = super().real_distance(curr_state.player_row-1, curr_state.player_col,goal[0],goal[1])
                    
                    tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row-1, curr_state.player_col, curr_state.depth+1, 'U',heur_val, curr_state.givenCost +1)
                    self.generated_node_count +=1
                    self.openList.put(tempNode, heur_val + tempNode.givenCost)
                else:
                    index_ =self.extendedLevels.index(temp_level_matrix)
                        #if it is already visited then look for the better one
                    if self.costMatrix[index_]>curr_state.givenCost:
                        self.costMatrix.pop(index_)
                        self.extendedLevels.pop(index_)
                        


            if curr_state.player_row < row_-1 and not curr_state.level_matrix[curr_state.player_row+1][curr_state.player_col] == 'W':
                    
                    temp_level_matrix = deepcopy(curr_state.level_matrix)
                    
                    temp_level_matrix[curr_state.player_row+1][curr_state.player_col] = 'P'
                    if temp_level_matrix not in self.extendedLevels:
                       
                        heur_val =super().real_distance(curr_state.player_row+1, curr_state.player_col,goal[0],goal[1])
                     
                        tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row+1, curr_state.player_col, curr_state.depth+1, 'D', heur_val, curr_state.givenCost +1)
                        self.generated_node_count += 1
                        self.openList.put(tempNode, heur_val+tempNode.givenCost)
                    else:
                         #if it is already visited then look for the better one
                        index_ =self.extendedLevels.index(temp_level_matrix)
                        if self.costMatrix[index_]>curr_state.givenCost:
                            self.costMatrix.pop(index_)
                            self.extendedLevels.pop(index_)
                           
            if curr_state.player_col > 0 and not curr_state.level_matrix[curr_state.player_row][curr_state.player_col-1] == 'W':
                   
                    temp_level_matrix = deepcopy(curr_state.level_matrix)
                   
                    temp_level_matrix[curr_state.player_row][curr_state.player_col-1] = 'P'
                    if temp_level_matrix not in self.extendedLevels:
                       
                        heur_val = super().real_distance(curr_state.player_row, curr_state.player_col-1,goal[0],goal[1])
                       
                        tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row, curr_state.player_col-1, curr_state.depth+1, 'L',heur_val,curr_state.givenCost +1)
                        self.generated_node_count += 1
                        self.openList.put(tempNode, heur_val+tempNode.givenCost)
                    else:
                        index_ =self.extendedLevels.index(temp_level_matrix)
                        if self.costMatrix[index_]>curr_state.givenCost:
                            self.costMatrix.pop(index_)
                            self.extendedLevels.pop(index_)
                            


            if curr_state.player_col < col_-1 and not curr_state.level_matrix[curr_state.player_row][curr_state.player_col+1] == 'W':
                    appleCount = 0
                    temp_level_matrix = deepcopy(curr_state.level_matrix)
                    
                    temp_level_matrix[curr_state.player_row][curr_state.player_col+1] = 'P'
                    if temp_level_matrix not in self.extendedLevels:
                       
                        heur_val = super().real_distance (curr_state.player_row, curr_state.player_col+1,goal[0],goal[1])
                       
                        tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row, curr_state.player_col+1, curr_state.depth+1, 'R',heur_val,curr_state.givenCost +1)
                        self.generated_node_count += 1
                        self.openList.put(tempNode,heur_val+tempNode.givenCost)
                    else:
                        index_ =self.extendedLevels.index(temp_level_matrix)
                        if self.costMatrix[index_]>curr_state.givenCost:
                            self.costMatrix.pop(index_)
                            self.extendedLevels.pop(index_)
                            

            if self.openList.count() > maxSize:
                maxSize = self.openList.count()


        #if break was taken -> make solved state true, get sequence by getting curr_state.seq
        self.maximum_node_in_memory_count = maxSize

                



        """
            YOUR CODE ENDS HERE
            return move_sequence
        """
        return move_sequence

def getpath(node,sq):
    
    while  node.parent_node:
        
        sq.append(node.chosen_dir)
        node=node.parent_node
    sq=sq.reverse()