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
import copy
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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    
    solution = []
    previousstack = []

    successorsNODE = util.Stack()
    successorsDIRECTION = util.Stack()
    successorsNODE_record = util.Stack()
    successorsDIRECTION_record = util.Stack()
    
    StartState = problem.getStartState()
    current_node = StartState
    previousstack.append(StartState)
    
    from game import Directions
    w = Directions.WEST
    e = Directions.EAST 
    s = Directions.SOUTH
    n = Directions.NORTH
   
    for node, direction, distance in problem.getSuccessors(current_node):
	if node not in previousstack:
		successorsNODE.push(node)
		successorsDIRECTION.push(direction)
		successorsNODE_record.push(node)
		successorsDIRECTION_record.push(direction)

    
    while problem.isGoalState(current_node) == False:	
        forward = False
	if successorsNODE.isEmpty() != True:
    		direction = successorsDIRECTION.pop()
		current_node = successorsNODE.pop()
		previousstack.append(current_node)
		solution.append(direction)
		
		if problem.isGoalState(current_node) == True:
			return solution
		for NODE, DIRECTION, DISTANCE in problem.getSuccessors(current_node):
			if NODE not in previousstack:
				successorsNODE.push(NODE)
				successorsDIRECTION.push(DIRECTION)
				successorsNODE_record.push(NODE)
				successorsDIRECTION_record.push(DIRECTION)
				forward = True

		if forward == False:
			direction = successorsDIRECTION.pop()
			current_node = successorsNODE.pop()
			
			wrong_node = successorsNODE_record.pop()
			wrong_direction = successorsDIRECTION_record.pop()
			while current_node != wrong_node:
				if len(solution) != 0:
					solution.pop()
				wrong_node = successorsNODE_record.pop()
				wrong_direction = successorsDIRECTION_record.pop()


			previousstack.append(current_node)
			successorsNODE_record.push(current_node)
			successorsDIRECTION_record.push(direction)
			solution.append(direction)

			for NODE, DIRECTION, DISTANCE in problem.getSuccessors(current_node):
				if NODE not in previousstack:
					successorsNODE.push(NODE)
					successorsDIRECTION.push(DIRECTION)
					successorsNODE_record.push(NODE)
					successorsDIRECTION_record.push(DIRECTION)	

		
    return solution



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    queue = util.Queue()
    visited = []
    route = []
    dictionary = {}
    count = 0
    gotSuccessor = []
    start = (problem.getStartState(), '', 1)
    goal = ((0, 0), 'None', 0)
    startState = problem.getStartState()

    
    queue.push((problem.getStartState(), []))
    while queue.isEmpty() == False:
        count = count + 1
        #print "count: ", count
        node, action = queue.pop()
        #print "Node popped:", node

        if problem.isGoalState(node):
            #print "Action:", action
            #print "len(Action):", len(action)
            return action

        # print "problem.getStartState()", problem.getStartState()
        # print "startState", startState

        if not node in visited:
            visited.append(node)
            #print "Append:", node
        
            for coordinate, direction, cost in problem.getSuccessors(node):
                queue.push((coordinate, action + [direction]))
                #print "Push:", coordinate
                # dictionary[successor2] = u
                
    return []

    # util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    pqueue = util.PriorityQueue()
    visited = []
    route = []
    dictionary = {}
    count = 0
    gotSuccessor = []
    start = (problem.getStartState(), 'None', 0)
    goal = ((0, 0), '', 0)

    
    pqueue.push(start, start[2])
    while pqueue.isEmpty() == False:
        count = count + 1
        #print "count: ", count
        u = pqueue.pop()
        # print "u:", u
        if problem.isGoalState(u[0]):
            goal = u
            #print "Goal:", goal
            break
        if not u[0] in visited:
            visited.append(u[0])
            if not problem.isGoalState(u[0]):
                    for successor2 in problem.getSuccessors(u[0]):
                        if not successor2[0] in visited:
                            dictionary[successor2] = u
                            now = successor2
                            tmp = 0
                            ct = 0
                            while now[0] != problem.getStartState():
                                ct = ct + 1
                                #print "ct:", ct
                                tmp = now[2] + tmp
                                #print "tmp:", tmp
                                now = dictionary[now]
                                #print "now:", now
                                
                            pqueue.update(successor2, tmp)
                            #print "Update:", successor2, tmp
                            
    current = goal
    while current[0] != problem.getStartState():
        try:
            route.append(current[1])
            current = dictionary[current]
        except KeyError:
            break
    
    return route[::-1]


def nullHeuristic(state, problem=None):

    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):

    """Search the node that has the lowest combined cost and heuristic first."""
    
    from game import Directions
    w = Directions.WEST
    e = Directions.EAST 
    s = Directions.SOUTH
    n = Directions.NORTH

    NODE = util.PriorityQueue()
    #NODE_info = []
    
    previousstack = []
    PATHH = []
    StartState = problem.getStartState()
    current_node = StartState
    previousstack.append(StartState)

    for sucessor in problem.getSuccessors(current_node):
	if sucessor[0] not in previousstack:
		PATH = []
		cost = sucessor[2]
         	PATH.append(sucessor[1])
		f = cost + heuristic(sucessor[0], problem)
		NODE.push((sucessor, PATH, cost), f)


    while NODE.isEmpty() != True:
	directionPATH = []
	CURRENTNODE = NODE.pop()
	NODEINFO = CURRENTNODE[0]
	directionPATH = CURRENTNODE[1]
	PARENTcost = CURRENTNODE[2]

	current_node = NODEINFO[0]
	
	if problem.isGoalState(current_node):
		return directionPATH

	if current_node not in previousstack:
		previousstack.append(current_node)
		for SUCESSORS in problem.getSuccessors(current_node):
				if SUCESSORS[0] not in previousstack:
					f = 0
					PPATH = []
					ccost = SUCESSORS[2]
					PPATH = copy.deepcopy(directionPATH)
       				 	PPATH.append(SUCESSORS[1])
					g = PARENTcost + ccost
					f = g + heuristic(SUCESSORS[0], problem)
					#print "!!h:", heuristic(SUCESSORS[0], problem)
					NODE.push((SUCESSORS, PPATH, g), f)

					

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

