import cPickle
from math import pow, sqrt
from NeuralNetUtil import buildExamplesFromExtraData
from NeuralNet import buildNeuralNet
from multiprocessing import Pool

def average(argList):
    return sum(argList) / float(len(argList))

def stDeviation(argList):
    mean = average(argList)
    diffSq = [pow((val - mean), 2) for val in argList]
    return sqrt(sum(diffSq) / len(argList))


extraData = buildExamplesFromExtraData()
def testExtraData(hiddenLayers=[4]):
    return buildNeuralNet(extraData, maxItr=200, hiddenLayerList=hiddenLayers)

def extra(a):
	return testExtraData()[1]

def runQuestionFiveExtra():
	pool = Pool(5)
	carResults = pool.map(extra, range(5))
	pool.close()
	pool.join()

	print carResults
	print 'Extra credit test average: %.3f, standard deviation %.3f\n' % (average(carResults), stDeviation(carResults))

runQuestionFiveExtra()