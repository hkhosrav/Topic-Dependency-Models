import numpy as np
import csv

FOLDERNAME = "uploads"
SQAFILE ="SQA.CSV"
QTFILE = "QT.CSV"


def loadSQA():
    SQAfile = FOLDERNAME + "/" + SQAFILE
    csv_file = csv.reader(open(SQAfile, "rU"), delimiter=",")
    SQA= []
    for row in csv_file:
        SQA.append([row[0], row[1], row[2]])
    return SQA

def loadQT():
    SQAfile = FOLDERNAME + "/" + QTFILE
    csv_file = csv.reader(open(SQAfile, "rU"), delimiter=",")
    QT = []
    for row in csv_file:
        QT.append([row[0], row[1]])
    return QT    
