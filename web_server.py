# Add to this file for the sample app lab
from flask import Flask
from flask import request
from flask import render_template


webApp = Flask(__name__)

@webApp.route("/")
def main():
    return render_template("index.html")
    
if __name__ == "__main__":
    webApp.run(host="127.0.0.1", port=8080)
