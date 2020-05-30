import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# os.environ.get('MONGO_URI')
app.config["MONGO_URI"] = "mongodb+srv://root:r00tUser@myfirstcluster-vdori.mongodb.net/ademre?retryWrites=true&w=majority"
MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = "ademre"
COLLECTION_NAME = "words"

mongo = PyMongo(app)

words = mongo.db.words.find()
words_list = [word for word in words]

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/admin.html')
def admin():
    return render_template("admin.html")

@app.route('/all_words.html')
def all_words():
    words = mongo.db.words.find()
    return render_template("all_words.html", words=words)


@app.route('/add_word.html')
def add_word():
    return render_template("add_word.html", words=words)


@app.route('/insert_word', methods=['POST'])
def insert_word():
    words = mongo.db.words
    words.insert_one(request.form.to_dict())
    return redirect(url_for('all_words'))


@app.route('/edit_word.html/<word_id>')
def edit_word(word_id):
    the_word = mongo.db.words.find_one({'_id': ObjectId(word_id)})    
    return render_template("edit_word.html", word=the_word, categories=words_list)


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


@app.route('/delete_word.html/<word_id>')
def delete_word(word_id):
    the_word = mongo.db.words.find_one({'_id': ObjectId(word_id)})  
    return render_template("delete_word.html", word=the_word)


@app.route('/remove_word/<word_id>', methods=['POST', 'GET'])
def remove_word(word_id):
    mongo.db.words.remove({'_id': ObjectId(word_id)})
    return redirect(url_for('all_words'))


@app.route('/contact.html')
def contact():
    return render_template("contact.html")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
