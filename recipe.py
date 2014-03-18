from flask import Flask, render_template
from bs4 import BeautifulSoup
import urllib2
from random import choice,randint

app = Flask(__name__, static_url_path='')

class Recipe():
  """docstring for Recipe"""
  def __init__(self, name, description, image, link):
    self.name = name
    self.description = description
    self.image = image
    self.link = link


@app.route('/')
def recipe(name=None):

  '''url = 'http://foodgawker.com/page/1/?s_exclude=drinks&cats_inc%5B0%5D=No+Desserts'
  request = urllib2.Request(url, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'})
  site = urllib2.urlopen(request)
  html = site.read()

  parsed_html = BeautifulSoup(html)
  maxpage = int(parsed_html.body.find('div', attrs={'class' : 'post-section'}).attrs['data-maxpage'])
  '''
  new_page = str(randint(1, 7300))

  url = 'http://foodgawker.com/page/' + new_page + '/?s_exclude=drinks&cats_inc%5B0%5D=No+Desserts'
  request = urllib2.Request(url, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'})
  site = urllib2.urlopen(request)
  html = site.read()

  parsed_html = BeautifulSoup(html)

  dishes = parsed_html.body.find_all('div', attrs={'class' : 'flipwrapper'})

  chosen = choice(dishes)

  name = chosen.attrs['data-sharetitle']
  description = chosen.find('section', attrs={'class' : 'description'}).text
  img = chosen.find('a', attrs={'class' : 'picture-link'})
  link = img.attrs['href']
  image = img.find('img').attrs['src']
  recipe_info = Recipe(name, description, image, link)

  return render_template('result.html', recipe_data=recipe_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)