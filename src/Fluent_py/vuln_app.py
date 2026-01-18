from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/run")
def run():
    cmd = request.args.get("cmd")
    os.system(cmd)   # 🚨 Command Injection
    return "done"

if __name__ == "__main__":
    app.run()
