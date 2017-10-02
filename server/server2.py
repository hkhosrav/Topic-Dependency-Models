from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qsl
import json
import time
import cgi, cgitb
import os

from topicDependency import generateTDM
from topicDependency import generateUserTDM
from topicDependency import generateIndividualTDM
from topicDependency import getUserList
from dataGenerator import createDataset
from dataParser import loadSQA
from dataParser import loadQT
from upload import saveData

hostName = "localhost"
hostPort = 9000

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        
        parsedURL = urlparse(self.path)
        inputParams = dict(parse_qsl(parsedURL.query))


        # inputParams.studentNumber <int>
        # inputParams.studentDiversity <int>
        # inputParams.questionDifficulty <int>
        # inputParams.competencyValue <int>
        # inputParams.modelClass <"dynamic" | "static">

        # SQA has sid, qid, score
        # QT has qid and list of associated topics

        if int(inputParams['load']) == 0:
            indivdualComp = float(inputParams['competencyValue'])
            SQA, QT =  createDataset(inputParams)
            individualData = {
                "name": "Random Indivual's Data",
                "data":  generateIndividualTDM(SQA, QT, indivdualComp)
            }
            compareAgainstData = {
                "name": "Class Average",
                "data":  generateTDM(SQA, QT)
            }
            self.wfile.write(str(json.dumps([individualData, compareAgainstData])))

        if int(inputParams['load']) == 1:
            
            SQA = loadSQA()
            userList = getUserList(SQA)
            self.wfile.write(str(json.dumps(userList)))

        if int(inputParams['load']) == 2:
            SQA = loadSQA()
            QT = loadQT()
            User = inputParams['User']
            individualData = {
                "name": inputParams['User'],
                "data": generateUserTDM(SQA, QT,User)
            }
            compareAgainstData = {
                "name": "Class Average",
                "data":  generateTDM(SQA, QT)
            }
            self.wfile.write(str(json.dumps([individualData, compareAgainstData])))


    def do_POST(self):

        self.send_response(200)
        self.send_header("Content-type", "multipart/form-data")
        self.end_headers()

        ctype, pdict = cgi.parse_header(self.headers['content-type'])

        postvars = cgi.parse_multipart(self.rfile, pdict)
        filename = postvars.keys()[0]

        data = postvars.values()[0][0]
        print filename
        saveData(filename, data)



if __name__ == "__main__":
    myServer = HTTPServer((hostName, hostPort), MyServer)
    print((time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort)))

    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        myServer.server_close()

    print((time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort)))
