from flask import Flask

app = Flask(__name__)

@app.route("/")
def health_check():
    return "ok"