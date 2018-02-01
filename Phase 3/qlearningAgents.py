# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"

        self.qValues = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # myDict = util.Counter()
        # for stateAndProb in self.mdp.getTransitionStatesAndProbs(state, action):
        #     myDict[stateAndProb[0]] = stateAndProb[1]*(self.mdp.getReward(state, action, stateAndProb[0]) + self.discount*self.getValue(stateAndProb[0]))
        # return myDict.totalCount()

        if (state, action) not in self.qValues:
          self.qValues[(state, action)] = 0.0
          return self.qValues[(state, action)]
        else:
          return self.qValues[(state, action)]



    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # if self.getLegalActions(state) == []:
        if len(self.getLegalActions(state)) == 0:
          # print "no action"
          return 0.0
        else:
          values = util.Counter()
          for action in self.getLegalActions(state):
            values[action] = (self.getQValue(state, action))
          return values[values.argMax()]


    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # if self.getLegalActions(state) == []:
        if len(self.getLegalActions(state)) == 0:
          return None
        else:
          values = util.Counter()
          for action in self.getLegalActions(state):
            values[action] = (self.getQValue(state, action))
          return values.argMax()


    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        if util.flipCoin(self.epsilon) != 0:
          action = random.choice(legalActions)
        else:
          action = self.computeActionFromQValues(state)


        # print legalActions

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # self.qValues[(state, action)] = (1 - self.alpha)*self.getQValue(state, action) + self.alpha*(reward + self.discount*self.getQValue(state, action))
        self.qValues[(state, action)] = (1 - self.alpha)*self.getQValue(state, action) + self.alpha*(reward + self.discount*self.computeValueFromQValues(nextState))

        # return self.qValues[(state, action)]

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # return self.qValues((state, action)) = self.getWeights()*self.featureExtractors.getFeatures(state, action)

        qValue = 0
        for feature in self.featExtractor.getFeatures(state, action):
          qValue += self.featExtractor.getFeatures(state, action)[feature]*self.getWeights()[feature]
        return qValue

        # feats = self.featExtractor.getFeatures(state, action)
        # qval = 0
        # for f in feats:
        #   qval += feats[f] * self.getWeights()[f]
        # return qval

        # features= self.featExtractor.getFeatures(state,action)
        # return self.weights*features

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # self.weights = self.getWeights() + qlearningAgents.self.alpha*((reward + self.epsilon*qlearningAgents.self.qValues[qlearningAgents.self.qValues.argMax()]) - qlearningAgents.self.qValues[(nextState, action)])*featureExtractors.getFeatures(state, action)

        # Zack: Why can't I put "difference" into the equation?
        difference = (reward + self.discount*self.computeValueFromQValues(nextState)) - self.getQValue(state, action)
        for feature in self.featExtractor.getFeatures(state, action):
          self.weights[feature] = self.getWeights()[feature] + self.alpha*(difference)*self.featExtractor.getFeatures(state, action)[feature]

        # dictionary = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
        # for key in dictionary:
        #   print "key:", key

        # feats = self.featExtractor.getFeatures(state, action)
        # for f in feats: 
        #   self.weights[f] = self.weights[f] + self.alpha * feats[f]*((reward + self.discount * self.computeValueFromQValues(nextState)) - self.getQValue(state, action))

        # difference = (reward+self.discount*self.computeValueFromQValues(nextState))-self.getQValue(state,action)
        # features = self.featExtractor.getFeatures(state,action)
        # for f in features.keys():
        #   # print("feature:"+str(features[f]))
        #   # print(self.weights)
        #   # print("diff: "+str(difference)+"\talpha: "+str(self.alpha)+"\tfeat: "+ str(features[f]))
        #   self.weights[f] = self.getWeights()[f]+(self.alpha*difference*features[f])



    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
