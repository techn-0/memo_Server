from bson import ObjectId
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)


client = MongoClient('mongodb://test:test@localhost',27017)
db = client.dbjungle

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/memo', methods=['POST'])
def post_article():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    
    time_id = datetime.now().strftime("%Y%m%d%H%M%S")

    article = {
        'title': title_receive,
        'content': content_receive,
        'likes': 0,
        'time_id': time_id
    }

    db.memos.insert_one(article)
    return jsonify({'result': 'success'})

@app.route('/memo', methods=['GET'])
def read_articles():
    articles = list(db.memos.find({}, {'_id': 0}))  # _id 필드 제외
    return jsonify({'result': 'success', 'articles': articles})

@app.route('/memo/update', methods=['PUT'])
def update_article():
    time_id_receive = request.form['time_id']
    new_title = request.form['title']
    new_text = request.form['content']

    db.memos.update_one({'time_id': time_id_receive}, {'$set': {'title': new_title}})
    db.memos.update_one({'time_id': time_id_receive}, {'$set': {'content': new_text}})
    return jsonify({'result': 'success'})



@app.route('/memo', methods=['DELETE'])
def delete_article():
    time_id_receive = request.form['time_id']

    db.memos.delete_many({'time_id': time_id_receive})
    return jsonify({'result': 'success'})



@app.route('/memo/like', methods=['PUT'])
def like_article():
    time_id_receive = request.form['time_id']

    db.memos.update_one({'time_id': time_id_receive}, {'$inc': {'likes': 1}})
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)