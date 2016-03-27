# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  def __init__(self, mdp, discount=0.9, iterations=100):
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0
    for i in range(iterations):
      currentValues = self.values.copy()
      for state in mdp.getStates():
        if not self.mdp.isTerminal(state):
          currentValues[state] = max([self.getQValue(state, action) for action in mdp.getPossibleActions(state)])
      self.values = currentValues
    
  def getValue(self, state):
    return self.values[state]

  def getQValue(self, state, action):
    return sum([prob * (self.mdp.getReward(state, action, nextState) + (self.discount * self.getValue(nextState))) for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action)])

  def getPolicy(self, state):
    actions = self.mdp.getPossibleActions(state)
    policy = None
    tempValues = util.Counter()
    for action in actions:
      tempValues[action] = self.getQValue(state, action)
    policy = tempValues.argMax()
    return policy

  def getAction(self, state):
    return self.getPolicy(state)
  
