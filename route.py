
from flask import Flask, render_template
from scraper import Scraper


app = Flask(__name__)

@app.route('/')
def show_route():

    #runs scraper and will pull back 3 pages of data for mean and median statistics
    scraper = Scraper(3)

    return render_template('route.html', tag_results=scraper.tag_categories, top_results=scraper.type_categories,
                           stats=scraper.stat_categories)
if __name__ == '__main__':
    app.run(debug=True)



