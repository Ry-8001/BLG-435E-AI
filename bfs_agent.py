import time
import random
from copy import deepcopy
from typing import Sequence
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
    def __init__(self, parent_node, level_matrix, player_row, player_column, depth, chosen_dir):
        self.parent_node = parent_node
        self.level_matrix = level_matrix
        self.player_row = player_row
        self.player_col = player_column
        self.depth = depth
        self.chosen_dir = chosen_dir
        


class BFSAgent(Agent):

    def __init__(self):
        super().__init__()
        self.openList = queue.Queue() #frontier is queue
        self.closedList = [] #for the graph search method

    def solve(self, level_matrix, goal, player_row, player_column):
        super().solve(level_matrix, goal, player_row, player_column)
        move_sequence = []

        """
            YOUR CODE STARTS HERE
            fill move_sequence list with directions chars
        """

        level_matrix_ = [list(row) for row in level_matrix] #deepcopy(level_matrix)
        row_ = len(level_matrix_)
        col_ = len(level_matrix_[0])
        

         
        s0 = Node(None, level_matrix_, player_row, player_column, 0, "-")
        self.openList.put(s0)
        maxSize = 0
        
        while not self.openList.empty():

            curr_state = self.openList.get()
            self.generated_node_count += 1
           
            #for the Graph search method
            #while runnig tree method comment out 
            
          
            self.closedList.append(deepcopy(curr_state.level_matrix))
            
            
            
                
            #if it is goal state retun path
            if goal == [curr_state.player_row,curr_state.player_col]:
                getpath(curr_state,move_sequence)
                break
            #mark the current state as floor
            curr_state.level_matrix[curr_state.player_row][curr_state.player_col] = 'F'
            #if succesor is valid then add it to the frontiter
            if curr_state.player_row > 0 and not curr_state.level_matrix[curr_state.player_row-1][curr_state.player_col]=='W':
                    
                temp_level_matrix = deepcopy(curr_state.level_matrix)
                temp_level_matrix[curr_state.player_row-1][curr_state.player_col] = 'P'
                #for the Graph method
                #if not explored
                if temp_level_matrix not in self.closedList:
                    tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row-1, curr_state.player_col, curr_state.depth+1, 'U')
                    self.expanded_node_count +=1
                    self.openList.put(tempNode)
            
                #for the tree Search method
                '''
                
                tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row-1, curr_state.player_col, curr_state.depth+1, 'U')
                self.expanded_node_count +=1
                self.openList.put(tempNode)
                
                '''
                
                 #if succesor is valid then add it to the frontiter
                
            if curr_state.player_row < row_-1 and not curr_state.level_matrix[curr_state.player_row+1][curr_state.player_col] == 'W':
                   
                temp_level_matrix = deepcopy(curr_state.level_matrix)
                temp_level_matrix[curr_state.player_row+1][curr_state.player_col] = 'P'
                #for the Graph method
                 #if not explored
                
                if   temp_level_matrix not in self.closedList:
                    tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row+1, curr_state.player_col, curr_state.depth+1, 'D')
                    self.expanded_node_count += 1
                    self.openList.put(tempNode)

                
                #for the tree Search method
                '''
                tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row+1, curr_state.player_col, curr_state.depth+1, 'D')
                self.expanded_node_count += 1
                self.openList.put(tempNode)

                '''
                  #if succesor is valid then add it to the frontiter
            if curr_state.player_col > 0 and not curr_state.level_matrix[curr_state.player_row][curr_state.player_col-1] == 'W':
                    
                temp_level_matrix = deepcopy(curr_state.level_matrix)
                temp_level_matrix[curr_state.player_row][curr_state.player_col-1] = 'P'
                #for the Graph method
                 #if not explored
                if   temp_level_matrix not in self.closedList:   
                    tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row, curr_state.player_col-1, curr_state.depth+1, 'L')
                    self.expanded_node_count += 1
                    self.openList.put(tempNode)
                #for the tree Search method
                '''
                
                tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row, curr_state.player_col-1, curr_state.depth+1, 'L')
                self.expanded_node_count += 1
                self.openList.put(tempNode)
              '''
                #if succesor is valid then add it to the frontiter
            if curr_state.player_col < col_-1 and not curr_state.level_matrix[curr_state.player_row][curr_state.player_col+1] == 'W':
                    
                temp_level_matrix = deepcopy(curr_state.level_matrix)
                temp_level_matrix[curr_state.player_row][curr_state.player_col+1] = 'P'
                #for the Graph method
                 #if not explored
                if  temp_level_matrix not in self.closedList:
                    tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row, curr_state.player_col+1, curr_state.depth+1, 'R')
                    self.expanded_node_count += 1
                    self.openList.put(tempNode)
                #for the tree Search method
                '''
                
                tempNode = Node(curr_state, temp_level_matrix, curr_state.player_row, curr_state.player_col+1, curr_state.depth+1, 'R')
                self.expanded_node_count += 1
                self.openList.put(tempNode)
                '''

            if self.openList.qsize() > maxSize:
                    maxSize = self.openList.qsize()


        self.maximum_node_in_memory_count = maxSize




        """
            YOUR CODE ENDS HERE
            return move_sequence
        """
        return move_sequence
        #get path via using parent
def getpath(node,sq):
    
    while  node.parent_node:
        
        sq.append(node.chosen_dir)
        node=node.parent_node
    sq=sq.reverse()
    
                


