from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import urllib2
import random
import os
from flask.ext.pymongo import PyMongo
import time

app = Flask(__name__, static_url_path='')

app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'recipeasy'
app.config['MONGO_USERNAME'] = 'recip'
app.config['MONGO_PASSWORD'] = 'sleazy'

mongo = PyMongo(app, config_prefix='MONGO')

class Recipe():
  """docstring for Recipe"""
  def __init__(self, name, description, image, link):
    self.name = name
    self.description = description
    self.image = image
    self.link = link


@app.route('/')
def recipe(name=None):

  '''filter_params = request.args.get('filter', '')
  print 'filter =', filter_params

  maxpage = 17000

  if filter_params != '':
    url = 'http://foodgawker.com/page/' + '1' + '/?cats_inc%5B0%5D='+filter_params
    print url
    rq = urllib2.Request(url, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'})
    site = urllib2.urlopen(rq)
    html = site.read()

    parsed_html = BeautifulSoup(html)
    maxpage = int(parsed_html.body.find('div', attrs={'class' : 'post-section'}).attrs['data-maxpage'])

  new_page = str(randint(1, maxpage))
  url = 'http://foodgawker.com/page/' + new_page + '/?cats_inc%5B0%5D='+filter_params
  print url

  rq = urllib2.Request(url, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'})
  site = urllib2.urlopen(rq)
  html = site.read()

  parsed_html = BeautifulSoup(html)

  dishes = parsed_html.body.find_all('div', attrs={'class' : 'flipwrapper'})

  chosen = choice(dishes)

  name = chosen.attrs['data-sharetitle']
  description = chosen.find('section', attrs={'class' : 'description'}).text
  img = chosen.find('a', attrs={'class' : 'picture-link'})
  link = img.attrs['href']
  image = img.find('img').attrs['src']'''

  collection = mongo.db.recipes
  numRecipes = collection.count()

  random.seed(time.time())
  randRecipe = random.randint(1, numRecipes)
  
  recipe = collection.find().limit(-1).skip(randRecipe).next()

  recipe_info = Recipe(recipe['title'], recipe['description'], recipe['image'], recipe['link'])

  return render_template('result.html', recipe_data=recipe_info)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=True, port=port)
