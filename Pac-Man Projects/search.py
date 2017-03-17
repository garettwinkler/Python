# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())

    "*** YOUR CODE HERE ***"

    from util import Stack
    edgeNodes = Stack()   #stack because it's DFS
    nodesExpanded = []       #keep a nodes visited/expanded list b/c graph search
    rootNode = problem.getStartState()
    #tuple with node and a lists (directions taken (which is returned)) So each state will have the coordinates of the node and the directions from the start state it took to get there
    edgeNodes.push ((rootNode, []))
    
    
    while (not edgeNodes.isEmpty()):                        #cycle through edges
        node, directions = edgeNodes.pop()                  #pop next node
        if problem.isGoalState(node):                       #check if it's a goal, if it is we're done
            return directions
        if (not node in nodesExpanded):                     #make sure it hasn't already been expanded
            nodesExpanded.append(node)                      #add it to expanded list
            successors = problem.getSuccessors(node)            #getSuccessors returns coordinate, direction, and cost (cost doesn't matter here)
            for nodeCoordinates, direction, cost in successors: #go through all successors
                edgeNodes.push((nodeCoordinates, directions + [direction]))   #pushing successors to stack with directions             
                
    return []     
    
    
    """" util.raiseNotDefined() """

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
   
    from util import Queue
    edgeNodes = Queue()      #using queue now because BFS, otherwise pretty much same as DFS
    nodesExpanded = []           
    rootNode = problem.getStartState()
    #same thing here, tuple with node and list for directions
    edgeNodes.push((rootNode, []))
    

    while (not edgeNodes.isEmpty()):
        node, directions = edgeNodes.pop()
        if problem.isGoalState(node):
            return directions
        if not (node in nodesExpanded):
            nodesExpanded.append(node)
            successors = problem.getSuccessors(node)
            for nodeCoordinates, direction, cost in successors:
                edgeNodes.push((nodeCoordinates, directions + [direction] ))
                
    return [] 
    
    
    """ util.raiseNotDefined() """

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    from util import PriorityQueue      #priority queue because no longer uniform cost.  g value introduced
    edgeNodes = PriorityQueue()
    nodesExpanded = []
    rootNode = problem.getStartState()
    edgeNodes.push((rootNode, []), 0)   #same except now have priority value as part of it
    

    while (not edgeNodes.isEmpty()):
        node, directions = edgeNodes.pop()
        if problem.isGoalState(node):
            return directions
        if (not node in nodesExpanded):
            nodesExpanded.append(node)
            for nodeCoordinates, direction, cost in problem.getSuccessors(node):    #maybe cost should be used here somewhere?  Could be pushed with the node and then wouldn't have to use getCostOfAction? but then why is it there? it's working...
            #only thing different, pushing to priority queue the node coord, adding direction, and with a priority value
                edgeNodes.push((nodeCoordinates, directions + [direction]), problem.getCostOfActions(directions + [direction]))

    return []    
    
    """util.raiseNotDefined() """

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    from util import PriorityQueue
    edgeNodes = PriorityQueue()
    nodesExpanded = []
    rootNode = problem.getStartState()
    edgeNodes.push((rootNode, []), heuristic(rootNode, problem))  #so now here we also push the heuristic

    while (not edgeNodes.isEmpty()):
        node, directions = edgeNodes.pop()
        if (not node in nodesExpanded):
            if problem.isGoalState(node):
                return directions
            nodesExpanded.append(node)
            for nodeCoordinates, direction, cost in problem.getSuccessors(node):
                hvalue = heuristic(nodeCoordinates, problem)
                if hvalue is None:
                    hvalue = 0
                fValue = problem.getCostOfActions(directions + [direction]) + hvalue  #and here we get the f-value by adding the gvalue (getCostOfAction) and the h-value (heuristic)
                edgeNodes.push((nodeCoordinates, directions + [direction]), fValue)   #then pass the f-value in as the value for the priority queue

    return []    
    
    """ util.raiseNotDefined() """


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
