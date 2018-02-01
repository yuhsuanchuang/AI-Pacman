# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        

        # for _ in range(0,self.iterations):
        i = 0
        while(i < self.iterations):
            i = i + 1
            ValuesForStates = util.Counter()
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state):
                        ValuesForStates[state] = 0
                else:
                    # maxvalue = float("-inf")
                    myValuesForActions = util.Counter()
                    for action in self.mdp.getPossibleActions(state):
                        # total = 0
                    #     for nextState, prob in self.mdp.getTransitionStatesAndProbs(state,action):
                    #             total += prob * (self.mdp.getReward(state,action,nextState) + (self.discount*self.values[nextState]))
                        myValuesForActions[action] = self.getQValue(state, action)
                        # maxvalue = max(total, maxvalue)
                        ValuesForStates[state] = myValuesForActions[myValuesForActions.argMax()]
                        # ValuesForStates[state] = maxvalue
            self.values = ValuesForStates





        # myValues = util.Counter()
        # time = 0
        # while(time < self.iterations):

   #      for _ in range(0,self.iterations):
   #        time += 1
   #        # if time >= self.iterations:
   #        #   break
   #        tmpValues = util.Counter()
      #       for state in self.mdp.getStates():
                
      #         if self.mdp.isTerminal(state):
      #             self.values[state] = 0
      #         else:
            #       maxvalue = float("-inf")
            #       for action in self.mdp.getPossibleActions(state):
            #           total = 0
            #           for nextState, prob in self.mdp.getTransitionStatesAndProbs(state,action):
            #               total += prob * (self.mdp.getReward(state,action,nextState) + (self.discount*self.values[nextState]))
            #           maxvalue = max(total, maxvalue)
            #           tmpValues[state] = maxvalue
            # self.values = tmpValues

        

        # for state in mdp.getStates():
        # self.computeActionFromValues(self.mdp.getStartState())

        # return None
        # self.mydict = {}
    
        # time = 0
        # while(time < iterations) {

            # time = time + 1
            # for state in mdp.getStates():
                
                # state = self.values
                # for action in mdp.getPossibleActions(state):
                    # getValue(mdp.getTransitionStatesAndProbs())
                    # action = mdp.getPossibleActions(state)
                    # qValue = self.computeQValueFromValues(state, action)

                    # state[action] = self.getValue(mdp.getTransitionStatesAndProbs(state, action)[0])
                # bestAction = state.argMax()
                # nextState = mdp.getTransitionStatesAndProbs(state, bestAction)[0]
                # nextProb = mdp.getTransitionStatesAndProbs(state, bestAction)[1]
                # bestValue = nextProb*(mdp.getReward(state, bestAction, nextState) + self.getValue(nextState))
                # mydict[time][state] = bestValue
        # }
        # for state in mdp.getStates():
            # bestAction = self.computeActionFromValues(state)
            # return bestAction 



    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # self.values[action] = 
        # nextState = self.mdp.getTransitionStatesAndProbs(state, action)[0]
        # nextProb = self.mdp.getTransitionStatesAndProbs(state, action)[1]
        myDict = util.Counter()
        for stateAndProb in self.mdp.getTransitionStatesAndProbs(state, action):
            myDict[stateAndProb[0]] = stateAndProb[1]*(self.mdp.getReward(state, action, stateAndProb[0]) + self.discount*self.getValue(stateAndProb[0]))
        return myDict.totalCount()


        # value = self.getValue(nextState)
        # reward = self.mdp.getReward(state, action, nextState)
        # qValue = nextProb*(reward + self.discount*value)
        # return qValue
        
        

        



    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # self.getValue(state)

        # Terminal State Case
        if self.mdp.isTerminal(state):
            return None

        mydict = util.Counter()
        for action in self.mdp.getPossibleActions(state):
            mydict[action] = self.computeQValueFromValues(state, action)
        return mydict.argMax()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
