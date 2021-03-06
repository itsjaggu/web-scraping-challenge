from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/webscrapedb"
mongo = PyMongo(app)

@app.route("/")
def index():
    # This function loads the data from Mongo DB and pass it to HTML Template
    mars_coll = mongo.db.MarsCollection.find_one()
    return render_template("index.html", mars_data=mars_coll)


@app.route("/scrape")
def scraper():
    # This function is called to scrape the data from website, done in scrape_mars.py script
    mars_coll = mongo.db.MarsCollection
    mars_data = scrape_mars.scrape()
    mars_coll.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)