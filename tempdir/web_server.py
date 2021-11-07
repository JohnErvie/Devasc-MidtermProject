# Add to this file for the sample app lab
from flask import Flask, url_for, redirect
from flask import request
from flask import render_template


webApp = Flask(__name__)

@webApp.route("/")
def main():
    return render_template("index.html")

@webApp.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('main'))

    # show the form, it wasn't submitted
    return render_template('test.html')

@webApp.route('/aboutus', methods=['GET', 'POST'])
def aboutus():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('main'))

    # show the form, it wasn't submitted
    return render_template('aboutus.html')
    
if __name__ == "__main__":
    webApp.run(host="0.0.0.0", port=8080)
