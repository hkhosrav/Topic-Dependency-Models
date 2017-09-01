from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qsl
import json
import time

from topicDependency import generateTDM
from topicDependency import createGraph
from dataGenerator import createDataset

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
        print inputParams
        indivdualComp = float(inputParams['competencyValue'])

        # inputParams.studentNumber <int>
        # inputParams.studentDiversity <int>
        # inputParams.questionDifficulty <int>
        # inputParams.competencyValue <int>
        # inputParams.modelClass <"dynamic" | "static">

        # SQA has sid, qid, score
        # QT has qid and list of associated topics
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


if __name__ == "__main__":
    myServer = HTTPServer((hostName, hostPort), MyServer)
    print((time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort)))

    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        myServer.server_close()

    print((time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort)))