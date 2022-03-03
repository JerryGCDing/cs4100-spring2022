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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        foodPos = currentGameState.getFood().asList()
        newGhostPos = [_.getPosition() for _ in newGhostStates]
        value = 0

        if newPos in foodPos:
            # avoid being way too passive
            value += 1

        if newPos in newGhostPos and newScaredTimes[newGhostPos.index(newPos)] != 0:
            return -100

        # food distance
        foodDistance = []
        for food in foodPos:
            foodDistance.append(manhattanDistance(newPos, food))
        for capsule in currentGameState.getCapsules():
            foodDistance.append(manhattanDistance(newPos, capsule) / 1.5)

        # ghost distance
        ghostDistance = []
        for ghostIndex in range(len(newGhostPos)):
            if newScaredTimes[ghostIndex] <= 2:
                ghostDistance.append(manhattanDistance(newPos, newGhostPos[ghostIndex]))
            else:
                foodDistance.append(manhattanDistance(newPos, newGhostPos[ghostIndex]) / 4)

        # avoid NaN
        if min(newScaredTimes) <= 1:
            # higher ghost weight as close
            value += 2 / (min(foodDistance) + 1) - 1.5 / (min(ghostDistance) + 1)
        else:
            value += 2 / (min(foodDistance) + 1)

        return value
        # return successorGameState.getScore() + max(fourDirection)

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        agentNumber = gameState.getNumAgents()

        def minimizer(gameState, depth, agentIndex):
            if end(gameState, depth):
                return self.evaluationFunction(gameState), None

            minVal = 999999
            action = None
            for _ in gameState.getLegalActions(agentIndex):
                # recursive call
                # update minimum boundary
                if agentIndex == agentNumber - 1:
                    # pacman turn update depth after a full turn
                    result = maximizer(gameState.generateSuccessor(agentIndex, _), depth + 1, 0)[0]
                else:
                    result = minimizer(gameState.generateSuccessor(agentIndex, _), depth, agentIndex + 1)[0]

                if result < minVal:
                    minVal = result
                    action = _

            return minVal, action

        def maximizer(gameState, depth, agentIndex):
            if end(gameState, depth):
                return self.evaluationFunction(gameState), None

            maxVal = -999999
            action = None
            for _ in gameState.getLegalActions(agentIndex):
                # update maximum boundary
                result = minimizer(gameState.generateSuccessor(agentIndex, _), depth, agentIndex + 1)[0]
                if result > maxVal:
                    maxVal = result
                    action = _

            return maxVal, action

        def end(gameState, depth):
            return gameState.isWin() or gameState.isLose() or depth >= self.depth

        return maximizer(gameState, 0, 0)[1]
        # util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        agentNumber = gameState.getNumAgents()

        def minimizer(gameState, depth, agentIndex, alpha, beta):
            if end(gameState, depth):
                return self.evaluationFunction(gameState)

            minVal = 999999
            for _ in gameState.getLegalActions(agentIndex):
                # recursive call
                # update minimum boundary
                if agentIndex == agentNumber - 1:
                    # pacman turn update depth after a full turn
                    result = maximizer(gameState.generateSuccessor(agentIndex, _), depth + 1, 0, alpha, beta)[0]
                else:
                    result = minimizer(gameState.generateSuccessor(agentIndex, _), depth, agentIndex + 1, alpha, beta)

                # prune
                if result < minVal:
                    minVal = result
                if result < alpha:
                    return result
                # update beta
                beta = min(beta, minVal)

            return minVal

        def maximizer(gameState, depth, agentIndex, alpha, beta):
            if end(gameState, depth):
                return self.evaluationFunction(gameState), None

            maxVal = -999999
            action = None
            for _ in gameState.getLegalActions(agentIndex):
                # update maximum boundary
                minimizer_result = minimizer(gameState.generateSuccessor(agentIndex, _), depth, agentIndex + 1, alpha, beta)

                if minimizer_result > maxVal:
                    maxVal = minimizer_result
                    action = _

                # prune
                if minimizer_result > beta:
                    return minimizer_result, action
                alpha = max(alpha, maxVal)

            return maxVal, action

        def end(gameState, depth):
            return gameState.isWin() or gameState.isLose() or depth >= self.depth

        # root maximizer node
        alpha = -999999
        beta = 999999

        return maximizer(gameState, 0, 0, alpha, beta)[1]
        # util.raiseNotDefined()

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
        agentNumber = gameState.getNumAgents()

        def maximizer(gameState, depth, agentIndex):
            if end(gameState, depth):
                return self.evaluationFunction(gameState), None

            maxVal = -999999
            action = None
            for _ in gameState.getLegalActions(agentIndex):
                # update maximum boundary
                result = expectVal(gameState.generateSuccessor(agentIndex, _), depth, agentIndex + 1)
                if result > maxVal:
                    maxVal = result
                    action = _

            return maxVal, action

        def expectVal(gameState, depth, agentIndex):
            if end(gameState, depth):
                return self.evaluationFunction(gameState)

            value = 0
            weight = 1 / len(gameState.getLegalActions(agentIndex))
            for _ in gameState.getLegalActions(agentIndex):
                # recursive call
                # update minimum boundary
                if agentIndex == agentNumber - 1:
                    # pacman turn update depth after a full turn
                    value += weight * maximizer(gameState.generateSuccessor(agentIndex, _), depth + 1, 0)[0]
                else:
                    value += weight * expectVal(gameState.generateSuccessor(agentIndex, _), depth, agentIndex + 1)

            return value

        def end(gameState, depth):
            return gameState.isWin() or gameState.isLose() or depth >= self.depth

        return maximizer(gameState, 0, 0)[1]
        # util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    calculate the manhattan distance from current pos to food (weight 2), to ghost (weight -1) and scared ghost
    (weight 4) for score bonus. The evaluation value basis is the current score to avoid pacman playing passive also
    indicates the current position has food. And if the ghosts are scared, basically can neglect its influence on
    current state evaluation.
    """
    "*** YOUR CODE HERE ***"
    currentPos = currentGameState.getPacmanPosition()
    currentGhostStates = currentGameState.getGhostStates()
    currentScaredTimes = [ghostState.scaredTimer for ghostState in currentGhostStates]

    foodPos = currentGameState.getCapsules()
    newGhostPos = [_.getPosition() for _ in currentGhostStates]
    value = currentGameState.getScore()

    # food distance
    foodDistance = [999999]  # fail safe
    for food in foodPos:
        foodDistance.append(manhattanDistance(currentPos, food))

    # ghost distance
    ghostDistance = [999999]  # fail safe
    for ghostIndex in range(len(newGhostPos)):
        if currentScaredTimes[ghostIndex] <= 2:
            ghostDistance.append(manhattanDistance(currentPos, newGhostPos[ghostIndex]))
        else:
            foodDistance.append(manhattanDistance(currentPos, newGhostPos[ghostIndex]) / 2)

    # avoid NaN
    value += 2 / (min(foodDistance) + 1) - 1 / (min(ghostDistance) + 1)

    return value

# Abbreviation
better = betterEvaluationFunction
