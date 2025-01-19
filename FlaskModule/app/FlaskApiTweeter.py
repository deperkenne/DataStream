from flask import Blueprint, jsonify, request
from KafkaTest.tweeter_consumer import *

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return jsonify({"message": "Welcome to the Flask API!"})


# get all record in topic events
@main.route("/records", methods=["GET"])
def get_records():
    list_sentiment = sentiments_analyse()
    return list_sentiment


