import cPickle
from math import pow, sqrt
from NeuralNetUtil import buildExamplesFromCarData, buildExamplesFromPenData
from NeuralNet import buildNeuralNet
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

def average(argList):
    return sum(argList) / float(len(argList))


def stDeviation(argList):
    mean = average(argList)
    diffSq = [pow((val - mean), 2) for val in argList]
    return sqrt(sum(diffSq) / len(argList))


penData = buildExamplesFromPenData()
def testPenData(hiddenLayers=[24]):
    return buildNeuralNet(penData, maxItr=200, hiddenLayerList=hiddenLayers)

carData = buildExamplesFromCarData()
def testCarData(hiddenLayers=[16]):
    return buildNeuralNet(carData, maxItr=200, hiddenLayerList=hiddenLayers)


def car(a):
	return testCarData()[1]

def pen(a):
	return testPenData()[1]

def runQuestionFive():
	pool = Pool(5)
	carResults = pool.map(car, range(5))
	pool.close()
	pool.join()

	print carResults
	print 'Car test average: %.3f, standard deviation %.3f\n' % (average(carResults), stDeviation(carResults))

	pool = Pool(5)
	penResults = pool.map(pen, range(5))
	pool.close()
	pool.join()

	print penResults
	print 'Pen test average: %.3f, standard deviation %.3f\n' % (average(penResults), stDeviation(penResults))

trials = [1, 2]

def carTrialRunner(a):
	return [testCarData(hiddenLayers=[trial])[1] for trial in trials]

def carRunner():
	pool = Pool(5)
	carResults = pool.map(carTrialRunner, range(2))
	pool.close()
	pool.join()
	
	# carResults = [[0.7002617801047121, 0.8075916230366492, 0.8520942408376964, 0.8304973821989529, 0.8291884816753927, 0.8553664921465969, 0.8291884816753927, 0.8213350785340314, 0.8141361256544503], [0.7002617801047121, 0.8632198952879581, 0.8462041884816754, 0.8318062827225131, 0.8383507853403142, 0.8370418848167539, 0.837696335078534, 0.8049738219895288, 0.8455497382198953], [0.7002617801047121, 0.8488219895287958, 0.850130890052356, 0.8520942408376964, 0.8540575916230366, 0.8337696335078534, 0.856675392670157, 0.8416230366492147, 0.831151832460733], [0.7002617801047121, 0.8540575916230366, 0.8599476439790575, 0.8442408376963351, 0.8586387434554974, 0.8285340314136126, 0.81217277486911, 0.8416230366492147, 0.8390052356020943], [0.7002617801047121, 0.8704188481675392, 0.875, 0.850130890052356, 0.8468586387434555, 0.8435863874345549, 0.850130890052356, 0.8239528795811518, 0.8357329842931938]]

	print carResults
	for i in range(len(trials)):
		trialResult = [result[i] for result in carResults]
		print '%d\t%.3f\t%.3f' % (trials[i], average(trialResult), stDeviation(trialResult))

	return carResults

def penTrialRunner(a):
	return [testPenData(hiddenLayers=[trial])[1] for trial in trials]

def penRunner():
	pool = Pool(5)
	penResults = pool.map(penTrialRunner, range(2))
	pool.close()
	pool.join()
	
	# penResults = [[0.7002617801047121, 0.8075916230366492, 0.8520942408376964, 0.8304973821989529, 0.8291884816753927, 0.8553664921465969, 0.8291884816753927, 0.8213350785340314, 0.8141361256544503], [0.7002617801047121, 0.8632198952879581, 0.8462041884816754, 0.8318062827225131, 0.8383507853403142, 0.8370418848167539, 0.837696335078534, 0.8049738219895288, 0.8455497382198953], [0.7002617801047121, 0.8488219895287958, 0.850130890052356, 0.8520942408376964, 0.8540575916230366, 0.8337696335078534, 0.856675392670157, 0.8416230366492147, 0.831151832460733], [0.7002617801047121, 0.8540575916230366, 0.8599476439790575, 0.8442408376963351, 0.8586387434554974, 0.8285340314136126, 0.81217277486911, 0.8416230366492147, 0.8390052356020943], [0.7002617801047121, 0.8704188481675392, 0.875, 0.850130890052356, 0.8468586387434555, 0.8435863874345549, 0.850130890052356, 0.8239528795811518, 0.8357329842931938]]

	print penResults
	for i in range(len(trials)):
		trialResult = [result[i] for result in penResults]
		print '%d\t%.3f\t%.3f' % (trials[i], average(trialResult), stDeviation(trialResult))

	return penResults

def runQuestionSix():
	# carResults = carRunner()
	penResults = penRunner()
	


runQuestionSix()