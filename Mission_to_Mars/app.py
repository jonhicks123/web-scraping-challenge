# Copy over template from craigslist activity and rename respective files/data.
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    main_dict = mongo.db.main_dict.find_one()
    return render_template("index.html", mars=main_dict)


@app.route("/scrape")
def scrape():
    main_dict = mongo.db.main_dict
    mars_data = scrape_mars.scraper()
    main_dict.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
