# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from __future__ import division
from util import manhattanDistance
from game import Directions
import random, util
import operator

from game import Agent

def inf():
    return float('inf')

def neginf():
    return float('inf') * -1

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
        #print"scores:", scores
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        #print"Action,Score:", (legalMoves[chosenIndex], bestScore)
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        capsuleScore = 0.0
        ghostScore = 0.0
        scareScore = 0.0
        closestFoodScore = 0.0
        finalScore = successorGameState.getScore()
       
        if len(newFood) != 0:  
            newFoodDist = [util.manhattanDistance(newPos, food) for food in newFood]
            closestFoodScore = 1.0/(min(newFoodDist))
         
        newGhostPos = successorGameState.getGhostPositions()
        newGhostDist = [util.manhattanDistance(newPos, ghost) for ghost in newGhostPos]
        closestGhostDist = min(newGhostDist)
        ghostIndex = 0 
        ghostThreshold = 10
        
        if closestGhostDist < ghostThreshold:
            for index in range(len(newGhostDist)): 
                if newGhostDist[index] == closestGhostDist:
                    ghostIndex = index
            if newScaredTimes[ghostIndex] > closestGhostDist:
                scareScore += newScaredTimes[ghostIndex]
            if closestGhostDist != 0:
                ghostScore += (1.0/closestGhostDist)
             
        finalScore += (1*capsuleScore) + (-1*ghostScore) + (10*scareScore)  + (1*closestFoodScore)
         
        return finalScore

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
        def maxMove(gameState, counter, last_move):
            if gameState.isWin() or gameState.isLose() or counter == 0:
                return (self.evaluationFunction(gameState), last_move)
            else:
                best_score = neginf()
                best_move = last_move
                moves = gameState.getLegalActions(self.index) 
                for move in moves: 
                    move_score = (minMove(gameState.generateSuccessor(self.index, move), counter, move, gameState.getNumAgents()-1))[0]
                    if move_score > best_score:
                        best_move = move
                        best_score = move_score
                return (best_score, best_move)
    
        def minMove(gameState, counter, last_move, num_ghosts):
            if gameState.isLose() or gameState.isWin() or counter == 0:
                return (self.evaluationFunction(gameState), last_move)
            else:     
                best_score = inf()
                best_move = last_move
                num_agents = gameState.getNumAgents()
                moves = gameState.getLegalActions(num_agents - num_ghosts)
                for move in moves:
                    if num_ghosts == 1:
                        move_score = (maxMove(gameState.generateSuccessor(num_agents - num_ghosts, move), counter-1, move))[0]
                    else:
                        move_score = (minMove(gameState.generateSuccessor(num_agents - num_ghosts, move), counter, move, num_ghosts-1))[0]
                    if move_score < best_score:
                        best_move = move
                        best_score = move_score
                return (best_score, best_move)
            
        if self.index == 0:
            toRet = (maxMove(gameState, self.depth, ""))[1]
        else:
            toRet = (minMove(gameState, self.depth, ""))[1]
        return toRet


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxMove(gameState, counter, last_move, alpha, beta):
            if gameState.isWin() or gameState.isLose() or counter == 0:
                return (self.evaluationFunction(gameState), last_move)
            else:
                best_score = neginf()
                best_move = last_move
                moves = gameState.getLegalActions(0) 
                for move in moves: 
                    move_score = (minMove(gameState.generateSuccessor(self.index, move), counter, move, gameState.getNumAgents()-1, alpha, beta))[0]
                    if move_score > best_score:
                        best_move = move
                        best_score = move_score
                    if best_score > beta:
                        break
                    alpha = max(alpha, best_score)
                return (best_score, best_move)
    
        def minMove(gameState, counter, last_move, num_ghosts, alpha, beta):
            if gameState.isLose() or gameState.isWin() or counter == 0:
                return (self.evaluationFunction(gameState), last_move)
            else:     
                best_score = inf()
                best_move = last_move
                num_agents = gameState.getNumAgents()
                moves = gameState.getLegalActions(num_agents - num_ghosts)
                for move in moves:
                    if num_ghosts == 1:
                        move_score = (maxMove(gameState.generateSuccessor(num_agents - num_ghosts, move), counter-1, move, alpha, beta))[0]
                    else:
                        move_score = (minMove(gameState.generateSuccessor(num_agents - num_ghosts, move), counter, move, num_ghosts-1, alpha, beta))[0]
                    if move_score < best_score:
                        best_move = move
                        best_score = move_score
                    if best_score < alpha:
                        break
                    beta = min(beta, best_score)
                return (best_score, best_move)
            
        if self.index == 0:
            toRet = (maxMove(gameState, self.depth, "", -1 * float('inf'), float('inf')))[1]
        else:
            toRet = (minMove(gameState, self.depth, "", gameState.getNumAgents(), neginf(), inf()))[1]
        return toRet

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
        "*** YOUR CODE HERE ***"
        def maxMove(gameState, counter, last_move):
            if gameState.isWin() or gameState.isLose() or counter == 0:
                return (self.evaluationFunction(gameState), last_move)
            else:
                best_score = neginf()
                best_move = last_move
                moves = gameState.getLegalActions(self.index) 
                for move in moves: 
                    move_score = (expMove(gameState.generateSuccessor(self.index, move), counter, move, gameState.getNumAgents()-1))[0]
                    if move_score > best_score:
                        best_move = move
                        best_score = move_score
                return (best_score, best_move)
        
        def expMove(gameState, counter, last_move, num_ghosts):
            if gameState.isLose() or gameState.isWin() or counter == 0:
                return (self.evaluationFunction(gameState), last_move)
            else:     
                best_score = 0
                num_agents = gameState.getNumAgents()
                moves = gameState.getLegalActions(num_agents - num_ghosts)
                randMove = random.sample(moves, 1)[0] 
                for move in moves:
                    prob = 1.0/len(moves)
                    if num_ghosts == 1:
                        move_score = (maxMove(gameState.generateSuccessor(num_agents - num_ghosts, move), counter-1, move))[0]
                    else:
                        move_score = (expMove(gameState.generateSuccessor(num_agents - num_ghosts, move), counter, move, num_ghosts-1))[0]
                    best_score += prob * move_score     
                return (best_score, randMove)   
        
        if self.index == 0:
            toRet = (maxMove(gameState, self.depth, ""))[1]
        else:
            toRet = (expMove(gameState, self.depth, ""))[1]
        return toRet



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
    
      DESCRIPTION: 
        -Naive Implementation
        -Always go after the closest food
        -If near a ghost, enter run_mode    
        -If in run_mode, go after the pellet
        -If you have eaten the pellet
        -Attack at the ghosts

      Let's Get Creative!    
      (1) The ghosts are likely to clump later in the game so save power pellets for the later part of the game
          -> You want to eat the ghosts when they are clumped together :) [DOUBLE KILL!]
          -> But make sure they are close to you when you do eat it
          -> You can do this by luring them! Do this by toggling back and forth 
    
      (2) Avoid danger zone, in other words, the bottom row because its easy to get trapped there
          -> And when you travel that straight line, the ghosts can team up and surround you
      
      (3) In the beginning of the game you know that the ghost is in his house. Therefore go after food with higher priority
          in the beginning of the game
    
    """
    #Positions/List of Positions
    pac_pos = currentGameState.getPacmanPosition() #Just the position
    ghost_list = currentGameState.getGhostPositions() #List of Ghost positions
    food_list = currentGameState.getFood().asList() #List of food positions

    #Ghost Info
    newGhostStates = currentGameState.getGhostStates() #DON"T USE! Only for newScaredTimes
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] #ghostScaredStates
    "*** YOUR CODE HERE ***"   
    capsuleScore = 0.0
    ghostScore = 0.0
    scareScore = 0.0
    closestFoodScore = 0.0
    final_score = currentGameState.getScore()
        
    if len(food_list) != 0:  
        newFoodDist = [util.manhattanDistance(pac_pos, food) for food in food_list]
        closestFoodScore = 1.0/(min(newFoodDist))
     
    newGhostPos = ghost_list
    newGhostDist = [util.manhattanDistance(pac_pos, ghost) for ghost in newGhostPos]
    closestGhostDist = min(newGhostDist)
    ghostIndex = 0 
    ghostThreshold = 10
    
    if closestGhostDist < ghostThreshold:
        for index in range(len(newGhostDist)): 
            if newGhostDist[index] == closestGhostDist:
                ghostIndex = index
        if newScaredTimes[ghostIndex] > closestGhostDist:
            scareScore += newScaredTimes[ghostIndex]
        if closestGhostDist != 0:
            ghostScore += (1.0/closestGhostDist)
         
    final_score += (1*capsuleScore) + (-1*ghostScore) + (10*scareScore)  + (1*closestFoodScore)
     
    return final_score

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

