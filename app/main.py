from flask import Flask
from subprocess import Popen
from psutil import cpu_percent,getloadavg
from os import environ

app = Flask(__name__)

STRESSTIME=60
pod="main"

@app.route("/")
def hello():
    return "Hello from Python!"

@app.route("/stress")
def stress():
    out=Popen(["/usr/bin/stress", "--cpu", "1", "--timeout", "%s"%STRESSTIME])
    return "60 Seconds CPU stress."

@app.route("/cpu")
def cpu():
    # out=cpu_percent(interval=0.2)
    out=getloadavg()[0]
    return "CPU load: %s" %(out)

@app.route("/insight")
def insight():
env=environ()
	return env



if __name__ == "__main__":
    app.run(host='0.0.0.0')
