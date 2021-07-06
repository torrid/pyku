from flask import Flask
from subprocess import Popen
from psutil import cpu_percent,getloadavg
from os import environ,getenv
from time import time 

app = Flask(__name__)

STRESSTIME=60
host=getenv('HOSTNAME')

def cpustress(seconds):
    assert type(seconds) == type(1) and seconds < 120
    start=time()
    while True:
        a=1
        while a < 1000:
            x=a*a
            x=1.3333*x/(a+3.333)
            a+=1

        if (time() - start) > seconds:
            break

@app.route("/")
def hello():
    return "Hello from Python!"

@app.route("/stress")
def stress():
    # out=Popen(["/usr/bin/stress", "--cpu", "1", "--timeout", "%s"%STRESSTIME])
	cpustress(STRESSTIME)
	return "Host: %s %ss stress.\n" % (host, STRESSTIME)

@app.route("/cpu")
def cpu():
    # out=cpu_percent(interval=0.2)
    out=getloadavg()[0]
    return "Host: %s, CPU load: %s\n" %(host, out)

@app.route("/insight")
def insight():
	return "\n%s\n" % str(environ)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
