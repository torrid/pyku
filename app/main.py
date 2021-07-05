from flask import Flask
app = Flask(__name__)

STRESSTIME=60

@app.route("/")
def hello():
    return "Hello from Python!"

@app.route("/stress")
def stress():
    os.system("/usr/bin/stress --cpu 2 --timeout 2")
    out=subprocess.Popen("/usr/bin/stress --cpu 1 --timeout %s" \
        %(STRESSTIME).split())
    return "60 Seconds CPU stress.\n\rResult: " + out

if __name__ == "__main__":
    app.run(host='0.0.0.0')
