from NeuralNet import buildNeuralNet

truthTable = [([0, 0], [0]),
			  ([1, 0], [1]),
			  ([0, 1], [1]),
			  ([1, 1], [0])]

def buildNet(hiddenLayer=[]):
	accuracies = []
	for i in range(5):
		nnet, accuracy = buildNeuralNet(examples=(truthTable, truthTable), hiddenLayerList=hiddenLayer, maxItr=5000)
		accuracies.append(accuracy)
	return float(sum(accuracies)) / float(len(accuracies))


results=[]

results.append(buildNet([]))
for i in range(1, 30):
	results.append(buildNet([i]))

for i in range(len(results)):
	print "%d\t%f"%(i, results[i])