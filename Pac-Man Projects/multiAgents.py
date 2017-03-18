# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action) #ascii board
        newPos = successorGameState.getPacmanPosition()                       #position coordinates
        newFood = successorGameState.getFood()                                # T or F for all moves around?  and one for current position?
        newGhostStates = successorGameState.getGhostStates()                  #where the ghosts are
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]    # number of moves for scared ghost

        "*** YOUR CODE HERE ***"
        #print successorGameState     
        #print successorGameState.getScore()
        #print newPos
        #print newFood
        #print newGhostStates
        #print newScaredTimes
        
        distOfFood = []
        distOfGhosts = []
        
        worryAboutGhosts = False
        
        #we're not going to worry about scared ghosts with more than 3 moves
        if ghostState.scaredTimer <= 3:
          worryAboutGhosts = True 
        
        for ghostState in newGhostStates:
          if worryAboutGhosts: 
            distOfGhosts.append(manhattanDistance(newPos, ghostState.getPosition()))    #otherwise we add the ghosts distance

        for food in newFood.asList():
          distOfFood.append(manhattanDistance(newPos, food))  #add the distance to food

        #sort both lists so the closest ghost and food are at index 0
        distOfGhosts.sort()
        distOfFood.sort()

        if len(distOfFood) > 0:
          closestFood = distOfFood[0]
        else:
          closestFood = 0

        foodLeft = successorGameState.getNumFood()    #number of food left
        #print foodLeft

        ghostFunction = 0
        if len(distOfGhosts) > 0:
          ghostFunction += distOfGhosts[0]  #first add distance of closest ghost  

        foodFunction = 0                       
        for dist in distOfFood:
          foodFunction += dist
        
        #print "ghostFunction: %d" % ghostFunction
        #print "foodLeft: %d" % foodLeft
        #print "closestFood: %d\n" % closestFood

        #reciprocals weren't working, didn't use
        foodRecip = 1 / (foodFunction + 1)
        ghostRecip = 1 / (ghostFunction + 1)
        closestFoodRecip = 1 / (closestFood + 1)
        foodLeftRecip = 1 / (foodLeft + 1)

        evaluation = ghostFunction - closestFood - 7*foodLeft  #closest ghost distance (we want high) - closest food (we want low) - number of food left (we want low) with a factor of 7 which came from tial and error
        #print "ghostFunction: %d" % ghostFunction
        #print "foodFunction: %d" % foodFunction
        #print evaluation
        return evaluation
        
        
        
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        bestScore,bestMove=self.maximum(gameState,self.depth)
        return bestMove

    def minimum(self,gameState,agent, depth):  
        if depth == 0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "holdStill"    #no where to go
        actions = gameState.getLegalActions(agent)    #returns list of legal actions for an agent
        if(agent != gameState.getNumAgents() - 1):
          scoreList = [self.minimum(gameState.generateSuccessor(agent,action),agent+1,depth) for action in actions]   #list with score and direction/action
        else:
          scoreList = [self.maximum(gameState.generateSuccessor(agent,action),(depth-1))[0] for action in actions]
        #print scoreList
        minScore = min(scoreList)
        #print minScore
        minIndexes = []
        for index in range(len(scoreList)):
          if scoreList[index] == minScore:
            minIndexes.append(index)
        
        Index = minIndexes[0]
        return minScore, actions[Index]    

    def maximum(self,gameState,depth):
        if depth == 0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "holdStill"    
        actions = gameState.getLegalActions() 
        scoreList = [self.minimum(gameState.generateSuccessor(self.index,action),1, depth) for action in actions]  
        #print scoreList 
        topScore = max(scoreList)
        #print topScore
        maxIndexes = []
        for index in range(len(scoreList)):
          if scoreList[index] == topScore:
            maxIndexes.append(index)
        #print maxIndexes
        Index = maxIndexes[0]
        return topScore,actions[Index]
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        
        maximizer = self.alphaPrune(gameState, 1, 0, float("-inf"), float("inf"))
        return maximizer        

    def alphaPrune(self, gameState, depth, agentIndex, alpha, beta):
      maxPossible= float("-inf")    # -infinity in python
      if gameState.isWin() or gameState.isLose(): #then this is a leaf/edge node, return the evaluation value of it.
        return self.evaluationFunction(gameState)

      for action in gameState.getLegalActions(0):   #cycle through every successor
        successor = gameState.generateSuccessor(0, action)
        valueToCheck = self.betaPrune(successor, depth, 1, alpha, beta)   #run betaPrune on it
        #print valueToCheck
        if valueToCheck > beta:
          return valueToCheck
        if valueToCheck > maxPossible:
          maxPossible = valueToCheck    #new maxPossible
          maxAction = action
        #print alpha  
        alpha = max(alpha, maxPossible) #setting alpha

      if depth != 1:
        return maxPossible
      else:
        return maxAction

    def betaPrune(self, gameState, depth, agentIndex, alpha, beta):
      minPossible= float("inf")
      numAgents = gameState.getNumAgents()          #number of agents - 1 (us, pacman) =  number of ghosts
      if gameState.isWin() or gameState.isLose():   #edge node
        return self.evaluationFunction(gameState)

      for action in gameState.getLegalActions(agentIndex):
        successor = gameState.generateSuccessor(agentIndex, action)
        if agentIndex == numAgents - 1:   #remember agentIndex > 0 is ghosts so this is last ghost
          #print depth
          if depth == self.depth:
            valueToCheck = self.evaluationFunction(successor)
          else:
            valueToCheck = self.alphaPrune(successor, depth+1, 0, alpha, beta) #run alphaPrune on it
        else:
          valueToCheck = self.betaPrune(successor, depth, agentIndex+1, alpha, beta)  #otherwise run betaPrune on agentIndex+1 (next ghost)
        #print valueToCheck
        if valueToCheck < alpha:
          return valueToCheck
        if valueToCheck < minPossible:
          minPossible = valueToCheck    #new minPossible
        #print beta
        beta = min(beta, minPossible)   #set beta
      return minPossible

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"  #temporarily putting minimax here in place of expectimax in order to attempt the extra credit Q5
        #util.raiseNotDefined()
        bestScore,bestMove=self.maximum(gameState,self.depth)
        return bestMove
            
    def minimum(self,gameState,agent, depth):  
        if depth == 0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "holdStill"
        actions = gameState.getLegalActions(agent)
        if(agent != gameState.getNumAgents() - 1):
          scoreList = [self.minimum(gameState.generateSuccessor(agent,action),agent+1,depth) for action in actions]
        else:
          scoreList = [self.maximum(gameState.generateSuccessor(agent,action),(depth-1))[0] for action in actions]
        minScore = min(scoreList)
        minIndexes = []
        for index in range(len(scoreList)):
          if scoreList[index] == minScore:
            minIndexes.append(index)
        Index = minIndexes[0]
        return minScore, actions[Index]    

    def maximum(self,gameState,depth):
        if depth == 0 or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState), "holdStill"    #no where to go
        actions = gameState.getLegalActions() #returns list of legal actions for an agent
        scoreList = [self.minimum(gameState.generateSuccessor(self.index,action),1, depth) for action in actions]  #list with score and direction/action
        #print scoreList 
        topScore = max(scoreList)
        #print topScore
        maxIndexes = []
        for index in range(len(scoreList)):
          if scoreList[index] == topScore:
            maxIndexes.append(index)
        #print maxIndexes
        Index = maxIndexes[0]
        return topScore,actions[Index]                

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

