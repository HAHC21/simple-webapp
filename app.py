# Import libraries
from flask import Flask, jsonify, redirect, render_template, request, session
from flask.json.tag import TaggedJSONSerializer
import requests, json, pandas
from bs4 import BeautifulSoup as soup
from cs50 import SQL
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

# Define app
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# API Information
api_key = ''
secret_api = ''
api_reviews_url = 'https://api.nytimes.com/svc/books/v3/reviews.json'
api_bestseller_url = 'https://api.nytimes.com/svc/books/v3/lists.json'

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Main route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Obtains information from form
        author = request.form.get('author')
        title = request.form.get('title')
        isbn = request.form.get('ISBN')

        # Checks to see which fields are not empty
        if title == '':
            title_check = ''
        else:
            title_check = f'&title={title}'

        if author == '':
            author_check = ''
        else:
            author_check = f'&author={author}'

        if isbn == '':
            isbn_check = ''
        else:
            isbn_check = f'&isbn={isbn}'
        
        
        # Obtain query from API
        nytimes_response = requests.get(f'{api_reviews_url}?api-key={api_key}{title_check}{author_check}{isbn_check}')

        # Load JSON data into a dictionary
        nytimes_data = json.loads(nytimes_response.content)

        # Stores the results inner data structure
        nytimes_results = nytimes_data['results']

        # Renders the results teplate with relevant information
        return render_template('search.html', nytimes_results=nytimes_results, results_analysis=len(nytimes_results), search_data=f'{title}+{author}+{isbn}')


    # Renders main template
    if request.method == "GET":

        # Get data for Hardcover Fiction best seller list
        nytimes_bestseller_hardcover_fiction = requests.get(f'{api_bestseller_url}?list=hardcover-fiction&api-key={api_key}')
        nytimes_bestseller_hf_data = json.loads(nytimes_bestseller_hardcover_fiction.content)
        nytimes_bestseller_hf_results = nytimes_bestseller_hf_data['results']

        # Get data for Hardcover Nonfiction best seller list
        nytimes_bestseller_hardcover_nonfiction = requests.get(f'{api_bestseller_url}?list=hardcover-nonfiction&api-key={api_key}')
        nytimes_bestseller_hnf_data = json.loads(nytimes_bestseller_hardcover_nonfiction.content)
        nytimes_bestseller_hnf_results = nytimes_bestseller_hnf_data['results']
        
        return render_template('index.html', bestsellers_f=nytimes_bestseller_hf_results, bestsellers_nf=nytimes_bestseller_hnf_results)