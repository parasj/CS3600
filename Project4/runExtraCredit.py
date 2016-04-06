from DataInterface import getDummyDataset2,getDummyDataset1,getConnect4Dataset, getCarDataset, getMushroomDataset
from DecisionTree import makeTree, setEntropy,infoGain
import random
from Testing import *

def testMushroom(setFunc = setEntropy, infoFunc = infoGain):
    """Correct classification averate rate is about 0.95"""
    examples,attrValues,labelName,labelValues = getMushroomDataset()
    print 'Testing Mushroom dataset. Number of examples %d.'%len(examples)
    tree = makeTree(examples, attrValues, labelName, setFunc, infoFunc)
    f = open('mushrooms.out','w')
    f.write(str(tree))
    f.close()
    print 'Tree size: %d.\n'%tree.count()
    print 'Entire tree written out to mushrooms.out in local directory\n'
    evaluation = getAverageClassificaionRate((examples,attrValues,labelName,labelValues))
    print 'Results for training set:\n%s\n'%str(evaluation)
    printDemarcation()
    return (tree,evaluation)

testMushroom()