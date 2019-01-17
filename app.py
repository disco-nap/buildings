from flask import Flask, render_template, jsonify, redirect
import sys
from flask_pymongo import PyMongo
#import scrape

#create instance of the flask app
sys.setrecursionlimit(2000)
app = Flask(__name__)

#create mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/eiaDB"
mongo = PyMongo(app)

@app.route("/")
def home():
   # mars_list = [{"news_title": "I", "news_p" : "You"}]
    usage_list = list(mongo.db.usage.find())
    print("HEEEEEELLLLLLO")
#    print(mars_list)
#    return render_template('index.html', mars_list=mars_list)
    return jsonify(usage_list)

#@app.route("/scrape")
#def data_scrape():
#    db.collection.remove({})
#    mars_list = scrape.scrape()
#    db.collection.insert_one(mars_list)
#    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
