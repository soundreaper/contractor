from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from random import randint

client = MongoClient()
db = client.Starterpack

starterpacks = db.starterpacks
starterpacks.drop
client_cart = db.client_cart
client_cart.drop

db.starterpacks.insert_many([
    {"name": "VSCO Girl Starter Pack", "description": "A VSCO girl's starter pack", "price": 200.00, "image": "./static/"},
    {"name": "College Student Starter Pack", "description": "A College Student's starter pack", "price": "A Lifetime of Debt", "image": "./static/"},
    {"name": "CS Student Starter Pack", "description": "A CS Student's Starter Pack", "price": "Your Sanity", "image": "./static/"},
    {"name": "'Pro' Gamer Starter Pack", "description": "A 'Pro' Gamer's Starter Pack", "price": "The Ability to Leave Home", "image": "./static/"}
    ])

app = Flask(__name__)

@app.route('/')
def starterpacks_index():
    """Show all Starterpacks."""
    # This will display all the starterpacks by looping through the DB
    return render_template('starterpacks_index.html', playlists=starterpacks.find())

if __name__ == '__main__':
  app.run(debug=True)