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
        scores = [self.evaluationFunction(gameState, action) for action in
                  legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if
                       scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        newScaredTimes = [ghostState.scaredTimer for ghostState in
                          newGhostStates]

        "*** YOUR CODE HERE ***"
        score = float("-inf")

        curFood = currentGameState.getFood().asList()

        if action == 'Stop':
            return score

        for state in newGhostStates:
            if state.getPosition() == newPos and (state.scaredTimer == 0):
                return score

        for i in curFood:
            negDis = -(manhattanDistance(newPos, i))
            if (negDis > score):
                score = negDis

        return score

        # return successorGameState.getScore()


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

        def minimax(state, depth, agent):

            if state.isWin() or state.isLose() or depth == self.depth or state.getLegalActions(
                    agent) == 0:
                return (self.evaluationFunction(state), None)

            if agent is 0:
                val = float("-inf")
                move = None
                for action in state.getLegalActions(agent):
                    (nextVal, nextMove) = minimax(
                        state.generateSuccessor(agent, action), depth,
                        (agent + 1) % state.getNumAgents())
                    if nextVal > val:
                        val = nextVal
                        move = action
                if val is not float("-inf"):
                    return val, move

            if agent is not 0:
                val = float("inf")
                move = None
                for action in state.getLegalActions(agent):
                    if ((agent + 1) % state.getNumAgents()) is not 0:
                        (nextVal, nextMove) = minimax(
                            state.generateSuccessor(agent, action), depth,
                            (agent + 1) % state.getNumAgents())
                    else:
                        (nextVal, nextMove) = minimax(
                            state.generateSuccessor(agent, action), (depth + 1),
                            (agent + 1) % state.getNumAgents())
                    if nextVal < val:
                        val = nextVal
                        move = action
                if val is not float("inf"):
                    return val, move

        return minimax(gameState, 0, 0)[1]

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
        def alphaBetaMinimax(state, depth, agent, alpha, beta):

            if state.isWin() or state.isLose() or depth == self.depth or state.getLegalActions(
                    agent) == 0:
                return (self.evaluationFunction(state), None)

            if agent is 0:
                val = float("-inf")
                move = None
                for action in state.getLegalActions(agent):
                    (nextVal, nextMove) = alphaBetaMinimax(
                        state.generateSuccessor(agent, action), depth,
                        (agent + 1) % state.getNumAgents(), alpha, beta)
                    if nextVal > val:
                        val = nextVal
                        move = action
                    if val >= beta:
                        return val, move
                    alpha = max(alpha, val)
                if val is not float("-inf"):
                    return val, move

            if agent is not 0:
                val = float("inf")
                move = None
                for action in state.getLegalActions(agent):
                    if ((agent + 1) % state.getNumAgents()) is not 0:
                        (nextVal, nextMove) = alphaBetaMinimax(
                            state.generateSuccessor(agent, action), depth,
                            (agent + 1) % state.getNumAgents(), alpha, beta)
                    else:
                        (nextVal, nextMove) = alphaBetaMinimax(
                            state.generateSuccessor(agent, action), (depth + 1),
                            (agent + 1) % state.getNumAgents(), alpha, beta)
                    if nextVal < val:
                        val = nextVal
                        move = action
                    if val <= alpha:
                        return val, move
                    beta = min(beta, val)
                if val is not float("inf"):
                    return val, move

        return alphaBetaMinimax(gameState, 0, 0, float("-inf"), float("inf"))[1]
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
        def Expectimax(state, depth, agent):

            if state.isWin() or state.isLose() or depth == self.depth or state.getLegalActions(
                    agent) == 0:
                return (self.evaluationFunction(state), None)

            if agent is 0:
                val = float("-inf")
                move = None
                for action in state.getLegalActions(agent):
                    (nextVal, nextMove) = Expectimax(
                        state.generateSuccessor(agent, action), depth,
                        (agent + 1) % state.getNumAgents())
                    if nextVal > val:
                        val = nextVal
                        move = action
                if val is not float("-inf"):
                    return val, move

            if agent is not 0:
                val = float("inf")
                sum = 0.0
                move = None
                div = len(state.getLegalActions(agent))
                for action in state.getLegalActions(agent):
                    if ((agent + 1) % state.getNumAgents()) is not 0:
                        (nextVal, nextMove) = Expectimax(
                            state.generateSuccessor(agent, action), depth,
                            (agent + 1) % state.getNumAgents())
                    else:
                        (nextVal, nextMove) = Expectimax(
                            state.generateSuccessor(agent, action), (depth + 1),
                            (agent + 1) % state.getNumAgents())
                    sum += nextVal
                # if val is not float("inf"):
                return sum/div, move

        return Expectimax(gameState, 0, 0)[1]

        # util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    score = currentGameState.getScore()
    ghostStates = currentGameState.getGhostStates()

    for g in ghostStates:
        if pos != g.getPosition():
            dis = manhattanDistance(pos, g.getPosition())
            if g.scaredTimer != 0:
                score += 60/dis
            else:
                if dis <= 6:
                    score -= 30/dis
        else:
            score -= 1000

    foodList = []

    for f in foods:
        foodList.append(manhattanDistance(f, pos))

    if len(foodList)>0:
        score -= min(foodList)

    return score

    # util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
