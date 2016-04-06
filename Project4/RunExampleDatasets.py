from DataInterface import getDummyDataset2,getDummyDataset1,getConnect4Dataset, getCarDataset
from DecisionTree import makeTree, setEntropy,infoGain
import random
import Testing

def run():
    Testing.testDummySet1()
    Testing.testDummySet2()
    Testing.testConnect4()
    Testing.testCar()

run()
