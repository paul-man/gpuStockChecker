import configparser
import json
import re
from pushbullet import Pushbullet
from os.path import dirname, abspath
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# import sys
# sys.exit()

# Setup PushBullet
path = dirname(abspath(__file__))
config_path = path + '/config.ini'
config = configparser.ConfigParser()
config.read(config_path)

pb_config = config['pushbullet']
pb = Pushbullet(pb_config['API_KEY'])

def pushInStockAlert(product):
  subject = f'{product["name"]} is in stock at {product["store"]}'
  pb.push_link(subject, product['url'])

# Load products
with open('./products.json') as f:
  products = json.load(f)

try:
    opts = Options()
    opts.headless = True
    brower = webdriver.Firefox(options=opts)

    for i in range(len(products)):
      brower.get(products[i].get("url"))
      pageSource = str(brower.page_source.encode("utf-8"))
      soldOut = re.search(">Sold Out<", pageSource)
      if soldOut != None:
        pushInStockAlert(products[i])
finally:
    try:
        brower.close()
    except:
        pass
