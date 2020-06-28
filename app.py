import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
DBS_NAME = "ademre"
COLLECTION_NAME = "words"

mongo = PyMongo(app)
WORDS = mongo.db.words.find()
WORDS_LIST = list(WORDS)
CATEGORY = mongo.db.category.find()
CAT_LIST = list(CATEGORY)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/all_words')
def all_words():
    words = mongo.db.words.find()
    return render_template("all_words.html", words=words)


@app.route('/add_word')
def add_word():
    return render_template("add_word.html", words=WORDS)


@app.route('/insert_word', methods=['POST'])
def insert_word():
    words = mongo.db.words
    words.insert_one(request.form.to_dict())
    return redirect(url_for('all_words'))


@app.route('/edit_word/<word_id>')
def edit_word(word_id):
    the_word = mongo.db.words.find_one({'_id': ObjectId(word_id)})    
    return render_template("edit_word.html", word=the_word)


@app.route('/update_word/<word_id>', methods=['POST'])
def update_word(word_id):
    words = mongo.db.words
    words.update({'_id': ObjectId(word_id)}, 
    {
        'eng': request.form.get('eng'),     
        'gesture': request.form.get('gesture'),
        'name': request.form.get('name'),
        'more_info': request.form.get('more_info')
    })
        
    return redirect(url_for('all_words'))


@app.route('/delete_word/<word_id>')
def delete_word(word_id):
    the_word = mongo.db.words.find_one({'_id': ObjectId(word_id)})  
    return render_template("delete_word.html", word=the_word)


@app.route('/remove_word/<word_id>', methods=['POST', 'GET'])
def remove_word(word_id):
    mongo.db.words.remove({'_id': ObjectId(word_id)})
    return redirect(url_for('all_words'))


@app.route('/contact')
def contact():
    return render_template("contact.html")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
