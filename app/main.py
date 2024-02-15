"""
Author: Aviad Barel
Reviewer: gili
"""

from flask import Flask, render_template, request
from API_functions import get_weather, download_image

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


@app.route("/download")
def download():
    return download_image()


if __name__ == "__main__":
    app.run()
