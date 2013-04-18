Developer Challenge
===================

Installation
------------

    git clone git@github.com:TwigWorld/DeveloperChallenge.git
    cd DeveloperChallenge
    mkvirtualenv env
    pip install -r requirements.txt

Run locally
-----------

    # view in browser at 127.0.0.1:5000
    python route.py

Run on Heroku
-------------

    heroku create
    git push heroku master
    heroku ps:scale web=1