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
	nowPos = currentGameState.getPacmanPosition()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
	ghostposition = successorGameState.getGhostPositions()
        "*** YOUR CODE HERE ***"
	uneaten_food_node = newFood.asList()
	score = 0
	if (newPos[0] == ghostposition[0][0] and newPos[1] == ghostposition[0][1]) or (newPos[0] == ghostposition[0][0]+1 and newPos[1] == ghostposition[0][1]) or (newPos[0] == ghostposition[0][0]-1 and newPos[1] == ghostposition[0][1]) or (newPos[0] == ghostposition[0][0] and newPos[1] == ghostposition[0][1]+1) or (newPos[0] == ghostposition[0][0] and newPos[1] == ghostposition[0][1]-1):
		score = -10000

	count = 0
	mindistance = 1000
	for food_node in uneaten_food_node:
		distance = abs(newPos[0] - food_node[0]) + abs(newPos[1] - food_node[1])
		
		if count == 0:
			mindistance = distance
			mininode = food_node
			count = 1
		else:
			if distance < mindistance:
				mindistance = distance
				mininode = food_node
	
        return successorGameState.getScore() + score + 1.0/mindistance

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
	finalaction = self.maxvalue(gameState, 0)
	return finalaction[1]

    def maxvalue(self, STATE, LAYER):
   	NumAgents = STATE.getNumAgents()
	totalaction = STATE.getLegalActions(0)
	if len(totalaction) == 0:
		return (self.evaluationFunction(STATE), None)
	max_value = -100000
	max_action = None
	for action in totalaction:
		SUCCESSORS = STATE.generateSuccessor(0, action)
		if SUCCESSORS.isWin() or SUCCESSORS.isLose() or ((LAYER+1)/NumAgents == self.depth):
			tempvalue = (self.evaluationFunction(SUCCESSORS), None)
		elif (LAYER+1) % NumAgents == 0:
			tempvalue = self.maxvalue(SUCCESSORS, LAYER+1)
		else:
			tempvalue = self.minvalue(SUCCESSORS, LAYER+1)
		if tempvalue[0] > max_value:
			max_value = tempvalue[0]
			max_action = action
	return (max_value, max_action)
		
    def minvalue(self, STATE, LAYER):
	NumAgents = STATE.getNumAgents()
	GHOSTNUM = LAYER % NumAgents
	totalaction = STATE.getLegalActions(GHOSTNUM)
	if len(totalaction) == 0:
		return (self.evaluationFunction(STATE), None)

	min_value = 100000
	min_action = None
	for action in totalaction:
		SUCCESSORS = STATE.generateSuccessor(GHOSTNUM, action)
		if SUCCESSORS.isWin() or SUCCESSORS.isLose() or ((LAYER+1)/NumAgents == self.depth):
			tempvalue = (self.evaluationFunction(SUCCESSORS), None)
		elif (LAYER+1) % NumAgents == 0:
			tempvalue = self.maxvalue(SUCCESSORS, LAYER+1)
		else:
			tempvalue = self.minvalue(SUCCESSORS, LAYER+1)
		if tempvalue[0] < min_value:
			min_value = tempvalue[0]
			min_action = action
	return (min_value, min_action)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
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
	finalaction = self.maxvalue(gameState, 0, -100000, 100000)
	return finalaction[1]

    def maxvalue(self, STATE, LAYER, alpha, beta):
   	NumAgents = STATE.getNumAgents()
	totalaction = STATE.getLegalActions(0)
	if len(totalaction) == 0:
		return (self.evaluationFunction(STATE), None)
	max_value = -100000
	max_action = None
	for action in totalaction:
		SUCCESSORS = STATE.generateSuccessor(0, action)
		if SUCCESSORS.isWin() or SUCCESSORS.isLose() or ((LAYER+1)/NumAgents == self.depth):
			tempvalue = (self.evaluationFunction(SUCCESSORS), None)
		elif (LAYER+1) % NumAgents == 0:
			tempvalue = self.maxvalue(SUCCESSORS, LAYER+1, alpha, beta)
		else:
			tempvalue = self.minvalue(SUCCESSORS, LAYER+1, alpha, beta)
		if tempvalue[0] > max_value:
			max_value = tempvalue[0]
			max_action = action
		if max_value > beta:
			return (max_value, max_action)
		alpha = max(alpha, max_value)
	return (max_value, max_action)
		
    def minvalue(self, STATE, LAYER, alpha, beta):
	NumAgents = STATE.getNumAgents()
	GHOSTNUM = LAYER % NumAgents
	totalaction = STATE.getLegalActions(GHOSTNUM)
	if len(totalaction) == 0:
		return (self.evaluationFunction(STATE), None)

	min_value = 100000
	min_action = None
	for action in totalaction:
		SUCCESSORS = STATE.generateSuccessor(GHOSTNUM, action)
		if SUCCESSORS.isWin() or SUCCESSORS.isLose() or ((LAYER+1)/NumAgents == self.depth):
			tempvalue = (self.evaluationFunction(SUCCESSORS), None)
		elif (LAYER+1) % NumAgents == 0:
			tempvalue = self.maxvalue(SUCCESSORS, LAYER+1, alpha, beta)
		else:
			tempvalue = self.minvalue(SUCCESSORS, LAYER+1, alpha, beta)
		if tempvalue[0] < min_value:
			min_value = tempvalue[0]
			min_action = action
		if min_value < alpha:
			return (min_value, min_action)
		beta = min(beta, min_value)
	return (min_value, min_action)

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
        finalaction = self.maxvalue(gameState, 0)
	return finalaction[1]

    def maxvalue(self, STATE, LAYER):
   	NumAgents = STATE.getNumAgents()
	totalaction = STATE.getLegalActions(0)
	if len(totalaction) == 0:
		return (self.evaluationFunction(STATE), None)
	max_value = -100000
	max_action = None
	for action in totalaction:
		SUCCESSORS = STATE.generateSuccessor(0, action)
		if SUCCESSORS.isWin() or SUCCESSORS.isLose() or ((LAYER+1)/NumAgents == self.depth):
			tempvalue = (self.evaluationFunction(SUCCESSORS), None)
		elif (LAYER+1) % NumAgents == 0:
			tempvalue = self.maxvalue(SUCCESSORS, LAYER+1)
		else:
			tempvalue = self.expetivalue(SUCCESSORS, LAYER+1)
		if tempvalue[0] > max_value:
			max_value = tempvalue[0]
			max_action = action
	return (max_value, max_action)
		
    def expetivalue(self, STATE, LAYER):
	NumAgents = STATE.getNumAgents()
	GHOSTNUM = LAYER % NumAgents
	totalaction = STATE.getLegalActions(GHOSTNUM)
	if len(totalaction) == 0:
		return (self.evaluationFunction(STATE), None)

	expeti_value = 0.
	for action in totalaction:
		SUCCESSORS = STATE.generateSuccessor(GHOSTNUM, action)
		if SUCCESSORS.isWin() or SUCCESSORS.isLose() or ((LAYER+1)/NumAgents == self.depth):
			tempvalue = (self.evaluationFunction(SUCCESSORS), None)
		elif (LAYER+1) % NumAgents == 0:
			tempvalue = self.maxvalue(SUCCESSORS, LAYER+1)
		else:
			tempvalue = self.expetivalue(SUCCESSORS, LAYER+1)
		
		expeti_value = expeti_value + tempvalue[0]/len(totalaction)

	return (expeti_value, None)
	
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    nowPos = currentGameState.getPacmanPosition()
    GhostStates = currentGameState.getGhostStates()
    ghostposition = currentGameState.getGhostPositions()
    Food = currentGameState.getFood()
    uneaten_food_node = Food.asList()
    
    score = 0
    if (nowPos[0] == ghostposition[0][0] and nowPos[1] == ghostposition[0][1]):
    	score = -10000
    ghostdistance = abs(nowPos[0] - ghostposition[0][0]) + abs(nowPos[1] - ghostposition[0][1])
    foodcount = len(uneaten_food_node)
    fooddone = 0
    if foodcount == 0:
    	fooddone = 1000
    count = 0
    minfooddistance = 1000
    for food_node in uneaten_food_node:
	fooddistance = abs(nowPos[0] - food_node[0]) + abs(nowPos[1] - food_node[1])
	if count == 0:
		minfooddistance = fooddistance
		minifoodnode = food_node
		count = 1
	else:
		if fooddistance < minfooddistance:
			minfooddistance = fooddistance
			minifoodnode = food_node
    return currentGameState.getScore() + score + 10.0/minfooddistance + fooddone - foodcount

# Abbreviation
better = betterEvaluationFunction

