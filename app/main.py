"""
Author: Aviad Barel
Reviewer: gili
"""

from flask import Flask, render_template, request
from app.API_functions import get_weather

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def search():
    # check if the request is get to return output without a data
    if request.method == 'GET':
        return render_template('mainpage.html', method='get')
    # check if the request is post to return an output with data
    if request.method == 'POST':
        city = request.form['city']
        return render_template('mainpage.html', **get_weather(city), method='post')


if __name__ == "__main__":
    app.run()
