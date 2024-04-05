import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np
from PIL import ImageEnhance, Image as im
import random as rd

p = 43  # nombre de classes

def readTrafficSigns(rootpath):
    '''Reads traffic sign data for German Traffic Sign Recognition Benchmark.'''
    images = []  # images
    labels = []  # corresponding labels
    for c in range(0, p):
        prefix = rootpath + '/' + format(c, '05d') + '/'  # subdirectory for class
        gtFile = open(prefix + 'GT-' + format(c, '05d') + '.csv')  # annotations file
        gtReader = csv.reader(gtFile, delimiter=';')  # csv parser for annotations file
        next(gtReader)  # skip header
        for row in gtReader:
            images.append(plt.imread(prefix + row[0]))  # the 1th column is the filename
            labels.append(row[7])  # the 8th column is the label
            plt.imshow(plt.imread(prefix + row[0]))
            plt.show()
        gtFile.close()
    return images, labels

data = readTrafficSigns("F:/R&D/BDDs/GTSRB_random_0.3/Final_Training/Images")
