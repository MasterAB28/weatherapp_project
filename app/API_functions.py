"""
Author: Aviad Barel
Reviewer: gili
"""

import requests
import boto3
import datetime

from flask import Response


def gecode(city):
    """this function get a city name and return a dictionary with city name and latitude and longitude and country"""
    try:
        response = (requests.get(
            "https://geocoding-api.open-meteo.com/v1/search?name=" + city + "&count=1&language=en&format=json")
                    .json())["results"][0]  # get the results from the api
        return {"city": response["name"], "latitude": response["latitude"],
                "longitude": response["longitude"],
                "country": response["country"]}  # return the dictionary
    except KeyError:
        return None  # catch keyError that mean there is no result and return None


def convert_date_to_day(date_str):
    """this function convert date string to day"""
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date().strftime("%A")


def convert_full_date_to_format(date_str):
    """this function convert date string to formatted date %d/%m"""
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m")


def get_weather(city):
    """this function get city name and return a dictionary with city name and country and weather data: current weather
    data(temp, is day or night and humidity), and a data for 7 days forward(min and max temp, humidity, days and dates
    of the days)"""
    data = gecode(city)  # take the data from the gecode function
    if data is None:
        # check if the data is None if yes return a dictionary with key not found with value true
        return {"not_found": "True"}
    # request from the weather api to get the weather data
    response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=" + str(data["latitude"]) +
                            "&longitude=" + str(data["longitude"])
                            + "&current=temperature_2m,relative_humidity_2m,"
                            + "is_day,weather_code&hourly=relative_humidity_2m&daily="
                            + "weather_code,temperature_2m_max,temperature_2m_min,"
                            + "relative_humidity_2m_mean&timezone=Africa%2FCairo").json()
    # return the dictionary
    return {"city": data["city"], "country": data["country"],
            "current_humidity": response["current"]["relative_humidity_2m"],
            "current_temperature": response["current"]["temperature_2m"],
            "days": [convert_date_to_day(day) for day in response["daily"]["time"]],
            "daily_time": [convert_full_date_to_format(day) for day in response["daily"]["time"]],
            "daily_max_temperature": response["daily"]["temperature_2m_max"],
            "daily_min_temperature": response["daily"]["temperature_2m_min"],
            "humidity": response["daily"]["relative_humidity_2m_mean"],
            "weather_code": response["daily"]["weather_code"],
            "is_day": response["current"]["is_day"],
            "current_weather_code": response["current"]["weather_code"],
            "not_found": "False"}


def download_image():
    s3_client = boto3.client('s3')
    obj = s3_client.get_object(Bucket="aviad.website", Key="sky.jpg")
    return Response(obj["Body"].read(), mimetype='Content-Type',
                    headers={'Content-Disposition': 'attachment; filename=sky.jpg'})
