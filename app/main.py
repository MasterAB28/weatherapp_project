"""
Author: Aviad Barel
Reviewer: gili
"""
import os

from flask import Flask, render_template, request, redirect, send_file
from API_functions import get_weather, download_image, dynamodb_send_item, save_history
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
bg_color = os.environ.get('BG_COLOR')


@app.route("/", methods=['GET', 'POST'])
def search():
    # ch    eck if the request is get to return output without a data
    if request.method == 'GET':
        return render_template('mainpage.html', method='get')
    # check if the request is post to return an output with data
    if request.method == 'POST':
        try:
            city = request.form['city']
            weather = get_weather(city)
            save_history(weather)
            return render_template('mainpage.html', **weather, method='post', bg_color=bg_color)
        except KeyError:
            return render_template('mainpage.html', **weather, method='post', bg_color=bg_color)

@app.route("/download")
def download():
    return download_image()


@app.route("/dynamodb", methods=['POST'])
def dynamodb():
    city = request.form['city']
    dynamodb_send_item(get_weather(city))
    return redirect('/')


@app.route('/download_history')
def download_history():
    directory_path = os.path.join(os.path.abspath(os.getcwd()), "history")
    files = [file for file in os.listdir(directory_path) if file.endswith('.json')]
    files.sort()
    return render_template('download_history.html', files=files)


@app.route('/download_history/<path:filename>')
def download_file(filename):
    file_path = os.path.join(os.path.abspath(os.getcwd()), f"history/{filename}")
    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run()
