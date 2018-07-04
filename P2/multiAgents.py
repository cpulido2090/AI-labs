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

#############################################
#   CARLLOS PULIDO MARQUEZ    NIA: 163842   #
#   ALBERT BOVE CASTELLVI     NIA: 163729   #
#############################################

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

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        #obtener el food actual y lo convertimos en lista para despues usarlo
        food = currentGameState.getFood()
        foodList = food.asList()

        newGhostPosition = successorGameState.getGhostPositions() #nuevas posiciones de los ghost
        distFood = set() #creamos una lista para luego guardar la distancia a los food
        score = 0 #inicializamos la puntuacion a 0

        #distancia entre posicion del pacman y cada food
        for food in foodList:
          distFood.add(manhattanDistance(food, newPos))

        #Miramos la distancia entre cada uno de los ghost
        for ghost in newGhostPosition:
          if manhattanDistance(newPos, ghost) < 2 :#Si la distancia hacia el ghost es inferior a 2, penalizamos con -50 puntos
            return score-50

        #Si vemos que el pacman esta parado, penalizamos con -50 puntos
        if currentGameState.getPacmanPosition() is Directions.STOP:
          return score-50

        #Comprobamos si queda comida y si queda, miramos la distancia minima
        if len(foodList)>0:
          score = min(distFood)

        return -score
        #retornamos un score negativo ya que sino cuando tengamos distancia 2, que estemos cerca del food, nuestro pacman no comera ya que el getAction se queda con el maximo
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
        #Evaluar
        def evaluate(depth, state, agentIndex):
          #Si es el ultimo agente, bajamos la profundidad
          #y empezamos otra vez
          if agentIndex is state.getNumAgents():
            depth-= 1
            agentIndex = 0
              
          #Turno pacman
          if agentIndex is 0:
            #Evaluamos state,indice,profundidad
            if depth is 0 or state.isLose() or state.isWin():
              return self.evaluationFunction(state)

            value = float("-inf")
            for action in state.getLegalActions(agentIndex):
              nextState = state.generateSuccessor(agentIndex, action)
              value = max( value, evaluate(depth, nextState, agentIndex+1))
            return value

          #turno ghost
          else:
            #comprobar si es un terminal o profundidad limite
            if depth is 0 or state.isLose() or state.isWin():
              return self.evaluationFunction(state)

            value = float("inf")
            for action in state.getLegalActions(agentIndex):
              nextState = state.generateSuccessor(agentIndex, action)
              value = min(value, evaluate(depth, nextState, agentIndex+1))
            return value

        #Main
        score = float("-inf")
        bestAction = Directions.STOP

        #Recorremos acciones legales de pacman
        for action in gameState.getLegalActions(self.index):
          fill = gameState.generateSuccessor(self.index, action)
          newScore = evaluate(self.depth, fill, self.index+1)

          #Actualizamos el score y nos quedamos con el mayor
          if newScore > score:
            score = newScore
            bestAction = action
        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #Evaluar
        def evaluate(depth, state, agentIndex, alpha, beta):
          #Si es el ultimo agente, bajamos laprofundidad
          #y empezamos otra vez
          if agentIndex is state.getNumAgents():
            depth-= 1
            agentIndex = 0
              
          #Turno pacman
          if agentIndex is 0:
            #Evaluamos state,indice,profundidad
            if depth is 0 or state.isLose() or state.isWin():
              return self.evaluationFunction(state)
            value = float("-inf")

            for action in state.getLegalActions(agentIndex):
              nextState = state.generateSuccessor(agentIndex, action)
              value = max( value, evaluate(depth, nextState, agentIndex+1, alpha, beta))
              if value > beta: return value
              alpha = max(value, alpha)
            return value

          #turno ghost
          else:
            #comprobar si es un terminal o profundidad limite
            if depth is 0 or state.isLose() or state.isWin():
              return self.evaluationFunction(state)

            value = float("inf")
            for action in state.getLegalActions(agentIndex):
              nextState = state.generateSuccessor(agentIndex, action)
              value = min(value, evaluate(depth, nextState, agentIndex+1, alpha, beta))
              if value < alpha: return value
              beta = min(value, beta)
            return value

        #Main
        score = alpha =  float("-inf")
        bestAction = Directions.STOP
        beta = float('inf')

        #Recorremos acciones legales de pacman
        for action in gameState.getLegalActions(self.index):
          fill = gameState.generateSuccessor(self.index, action)
          newScore = evaluate(self.depth, fill, self.index+1, alpha, beta)
          alpha = max(newScore, alpha)

          #Actualizamos el score y nos quedamos con el mayor
          if newScore > score:
            score = newScore
            bestAction = action
        return bestAction

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
        util.raiseNotDefined()

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

