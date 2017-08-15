from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
import json
import time

from dataGenerator import MakeData

hostName = "localhost"
hostPort = 9000

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        
        parsedURL = urlparse(self.path)
        inputParams = parse_qs(parsedURL.query)

        # inputParams.studentNumber <int>
        # inputParams.studentDiversity <int>
        # inputParams.questionDifficulty <int>
        # inputParams.competencyValue <int>
        # inputParams.modelClass <"dynamic" | "static">
        
        individualData = {
            "name": "Individual Data",
            "data": MakeData()
        }
        compareAgainstData = {
            "name": "Class Average",
            "data": MakeData()
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