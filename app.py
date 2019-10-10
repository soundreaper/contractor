from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Starterpack')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()

starterpacks = db.starterpacks
bags = db.bag

starterpacks.drop()
bags.drop()

db.starterpacks.insert_many([
    {"name": "VSCO Girl", "description": "Overpriced Waterbottle", "price": "$200.00", "image": "./static/vsco.png"},
    {"name": "College Student", "description": "We broke out here", "price": "A Lifetime of Debt", "image": "./static/college.png"},
    {"name": "CS Student", "description": "I have 200+ side projects", "price": "Your Sanity", "image": "./static/cs.png"},
    {"name": "'Pro' Gamer", "description": "What is a social life", "price": "The Ability to Leave Home", "image": "./static/game.png"}
    ])

app = Flask(__name__)

@app.route('/')
def starterpacks_index():
    return render_template('starterpacks_index.html', starterpacks=starterpacks.find())

@app.route('/bag')
def show_bag():
    bag = bags.find()

    num = list(bags.find({}))
    if len(num) > 0:
        quant = num[0]['quantity']
    else:
        quant = 0
        
    return render_template('bag.html', bags=bag, num=len(num), quant=quant)

@app.route('/starterpacks/<starterpack_id>/add', methods=['POST'])
def starterpack_create(starterpack_id):
    if bags.find_one({'_id': ObjectId(starterpack_id)}):
        bags.update_one(
            {'_id': ObjectId(starterpack_id)},
            {'$inc': {'quantity': int(1)}}
        )
    else:
        bags.insert_one(starterpacks.find_one({'_id': ObjectId(starterpack_id)}))
        bags.update(starterpacks.find_one({'_id': ObjectId(starterpack_id)}), {'$set': {'quantity': 1}})

    return redirect(url_for('show_bag'))

@app.route('/bags/<bag_id>/delete', methods=['POST'])
def bag_delete(bag_id):
    bag_item  = bags.find_one({'_id': ObjectId(bag_id)})

    bags.update_one(
        {'_id': ObjectId(bag_id)},
        {'$inc': {'quantity': -int(1)}}
    )

    if bag_item['quantity'] == 1:
        bags.remove({'_id': ObjectId(bag_id)})

    return redirect(url_for('show_bag'))

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))