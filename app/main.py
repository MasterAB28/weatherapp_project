"""
Author: Aviad Barel
Reviewer: gili
"""

from flask import Flask, render_template, request, redirect
from API_functions import get_weather, download_image, dynamodb_send_item
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route("/", methods=['GET', 'POST'])
def search():
    # ch    eck if the request is get to return output without a data
    if request.method == 'GET':
        return render_template('mainpage.html', method='get')
    # check if the request is post to return an output with data
    if request.method == 'POST':
        city = request.form['city']
        weather = get_weather(city)
        return render_template('mainpage.html', **weather, method='post')


@app.route("/download")
def download():
    return download_image()


@app.route("/dynamodb", methods=['POST'])
def dynamodb():
    city = request.form['city']
    dynamodb_send_item(get_weather(city))
    return redirect('/')


if __name__ == "__main__":
    app.run()
