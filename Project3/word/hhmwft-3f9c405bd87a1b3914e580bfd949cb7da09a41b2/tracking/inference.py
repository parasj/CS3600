import util
import random
import busters
import game

class InferenceModule:
  def __init__(self, ghostAgent):
    self.ghostAgent = ghostAgent
    self.index = ghostAgent.index

  def getJailPosition(self):
     return (2 * self.ghostAgent.index - 1, 1)
    
  def getPositionDistribution(self, gameState):
    ghostPosition = gameState.getGhostPosition(self.index)
    actionDist = self.ghostAgent.getDistribution(gameState)
    dist = util.Counter()
    for action, prob in actionDist.items():
      successorPosition = game.Actions.getSuccessor(ghostPosition, action)
      dist[successorPosition] = prob
    return dist
  
  def setGhostPosition(self, gameState, ghostPosition):
    conf = game.Configuration(ghostPosition, game.Directions.STOP)
    gameState.data.agentStates[self.index] = game.AgentState(conf, False)
    return gameState
  
  def observeState(self, gameState):
    distances = gameState.getNoisyGhostDistances()
    if len(distances) >= self.index:
      obs = distances[self.index - 1]
      self.observe(obs, gameState)
      
  def initialize(self, gameState):
    self.legalPositions = [p for p in gameState.getWalls().asList(False) if p[1] > 1]   
    self.initializeUniformly(gameState)
  
  def initializeUniformly(self, gameState):
    pass
  
  def observe(self, observation, gameState):
    pass
  
  def elapseTime(self, gameState):
    pass
    
  def getBeliefDistribution(self):
    pass

class ExactInference(InferenceModule):
  def initializeUniformly(self, gameState):
    self.beliefs = util.Counter()
    for p in self.legalPositions: self.beliefs[p] = 1.0
    self.beliefs.normalize()
  
  def observe(self, observation, gameState):
    noisyDistance = observation
    emissionModel = busters.getObservationDistribution(noisyDistance)
    pacmanPosition = gameState.getPacmanPosition()
    
    allPossible = util.Counter()
    for p in self.legalPositions:
      if noisyDistance == None:
          if p == self.getJailPosition():
              allPossible[p] = 1.0
          else:
              allPossible[p] = 0.0
      else:
          trueDistance = util.manhattanDistance(p, pacmanPosition)
          allPossible[p] = emissionModel[trueDistance] * self.beliefs[p]
    allPossible.normalize()
    
    self.beliefs = allPossible
    
  def elapseTime(self, gameState):
    newBeliefs = util.Counter()
    for p in self.legalPositions:
      newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, p))
      for newPos, prob in newPosDist.items():
        newBeliefs[newPos] += prob * self.beliefs[p]
    
    self.beliefs = newBeliefs

  def getBeliefDistribution(self):
    return self.beliefs

class ParticleFilter(InferenceModule):
  def __init__(self, ghostAgent, numParticles=300):
     InferenceModule.__init__(self, ghostAgent);
     self.setNumParticles(numParticles)
  
  def setNumParticles(self, numParticles):
    self.numParticles = numParticles
  
  def initializeUniformly(self, gameState):
    self.particles = [random.choice(self.legalPositions) for i in range(self.numParticles)]
  
  def observe(self, observation, gameState):
    noisyDistance = observation
    emissionModel = busters.getObservationDistribution(noisyDistance)
    pacmanPosition = gameState.getPacmanPosition()
    
    beliefs = util.Counter()
    if noisyDistance == None:
      self.particles = [self.getJailPosition() for i in range(self.numParticles)]
    else:
      for particle in self.particles:
        beliefs[particle] += emissionModel[util.manhattanDistance(particle, pacmanPosition)]
      if beliefs.totalCount() != 0:
        self.particles = [util.sample(beliefs) for i in range(self.numParticles)]
      else:
        self.initializeUniformly(gameState)

  def elapseTime(self, gameState):
    self.particles = [util.sample(self.getPositionDistribution(self.setGhostPosition(gameState, particle))) for particle in self.particles]

  def getBeliefDistribution(self):
    dist = util.Counter()
    for part in self.particles:
      dist[part] += 1
    dist.normalize()
    return dist

class MarginalInference(InferenceModule):
  def initializeUniformly(self, gameState):
    if self.index == 1: jointInference.initialize(gameState, self.legalPositions)
    jointInference.addGhostAgent(self.ghostAgent)
    
  def observeState(self, gameState):
    if self.index == 1: jointInference.observeState(gameState)
    
  def elapseTime(self, gameState):
    if self.index == 1: jointInference.elapseTime(gameState)
    
  def getBeliefDistribution(self):
    jointDistribution = jointInference.getBeliefDistribution()
    dist = util.Counter()
    for t, prob in jointDistribution.items():
      dist[t[self.index - 1]] += prob
    return dist
  
class JointParticleFilter:
  def __init__(self, numParticles=600):
     self.setNumParticles(numParticles)
  
  def setNumParticles(self, numParticles):
    self.numParticles = numParticles
  
  def initialize(self, gameState, legalPositions):
    self.numGhosts = gameState.getNumAgents() - 1
    self.ghostAgents = []
    self.legalPositions = legalPositions
    self.initializeParticles()
    
  def initializeParticles(self):
    self.particles = [tuple(random.choice(self.legalPositions) for ghost in range(self.numGhosts)) for part in range(self.numParticles)]

  def addGhostAgent(self, agent):
    self.ghostAgents.append(agent)
    
  def elapseTime(self, gameState):
    newParticles = []
    for oldParticle in self.particles:
      newParticle = list(oldParticle)
      for i in range(self.numGhosts):
        newParticle[i] = util.sample(getPositionDistributionForGhost(setGhostPositions(gameState, list(oldParticle)), i, self.ghostAgents[i]))
      newParticles.append(tuple(newParticle))
    self.particles = newParticles

  def getJailPosition(self, i):
    return (2 * i + 1, 1);
  
  def observeState(self, gameState):
    pacmanPosition = gameState.getPacmanPosition()
    noisyDistances = gameState.getNoisyGhostDistances()
    if len(noisyDistances) < self.numGhosts: return
    emissionModels = [busters.getObservationDistribution(dist) for dist in noisyDistances]
    
    beliefs = util.Counter()
    for ghost in range(self.numGhosts):
      if not noisyDistances[ghost]:
        for particle in range(self.numParticles):
          listParticle = list(self.particles[particle])
          listParticle[ghost] = self.getJailPosition(ghost)
          self.particles[particle] = tuple(listParticle)
    for particle in self.particles:
      beliefs[particle] += reduce(lambda x, y: x * y, [emissionModels[ghost][util.manhattanDistance(particle[ghost], pacmanPosition)] for ghost in range(self.numGhosts) if noisyDistances[ghost] != None])
    if beliefs.totalCount() != 0:
      self.particles = [util.sample(beliefs) for k in range(self.numParticles)]
    else:
      self.initializeParticles()

  
  def getBeliefDistribution(self):
    dist = util.Counter()
    for part in self.particles: dist[part] += 1
    dist.normalize()
    return dist
jointInference = JointParticleFilter()

def getPositionDistributionForGhost(gameState, ghostIndex, agent):
  ghostPosition = gameState.getGhostPosition(ghostIndex + 1) 
  actionDist = agent.getDistribution(gameState)
  dist = util.Counter()
  for action, prob in actionDist.items():
    successorPosition = game.Actions.getSuccessor(ghostPosition, action)
    dist[successorPosition] = prob
  return dist
  
def setGhostPositions(gameState, ghostPositions):
  for index, pos in enumerate(ghostPositions):
    conf = game.Configuration(pos, game.Directions.STOP)
    gameState.data.agentStates[index + 1] = game.AgentState(conf, False)
  return gameState  

