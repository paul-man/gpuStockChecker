import configparser
import json
import logging
import mechanicalsoup
import re
import sys
from pushbullet import Pushbullet
from os.path import dirname, abspath

# Setting up file paths helps when running cron
path = dirname(abspath(__file__))
configPath   = f'{path}/config.ini'
loggingPath  = f'{path}/app.log'
productsPath = f'{path}/products.json'
storesPath   = f'{path}/stores.json'

# Log INFO level messages
logging.basicConfig(filename=loggingPath,
  format='%(asctime)s - %(message)s',
  level=logging.INFO)
# sys.exit()

# Get PushBullet API_KEY from config
config = configparser.ConfigParser()
config.read(configPath)
pb = Pushbullet(config['pushbullet']['API_KEY'])

# Load products
with open(productsPath) as f:
  products = json.load(f)

# Load stores
with open(storesPath) as f:
  stores = json.load(f)

def main():
  # TODO: Track the indeces and log names/stores OR # at each store
  itemsFound = 0
  try:
      # logging.info('___________ Begin stock check ___________')
      browser = mechanicalsoup.StatefulBrowser(user_agent='Mozilla/5.0')
      browser.open("https://bestbuy.com/")
      for product in products:
        browser.open(product['url'])
        pageSource = str(browser.page.encode("utf-8"))
        soldOutPhrase = stores[product["store"]]["soldOutPhrase"]
        soldOut = re.search(soldOutPhrase, pageSource)
        if soldOut == None:
          pushInStockAlert(product)
          itemsFound = itemsFound + 1
          # logging.info(f'Found GPU in stock: {product["store"]}->{product["name"]}')
        # else:
        #   logging.info(f'No GPU found: {product["store"]}->{product["name"]}')
  finally:
      try:
          if itemsFound == 0 :
            logging.info('__ No items found')
          else:
            logging.info(f'{itemsFound} GPUs found, check PushBullet notifications.')
          # logging.info('___________ End stock check ___________')
          browser.quit()
      except:
          pass

      
def pushInStockAlert(product):
  subject = f'{product["name"]} is in stock at {product["store"]}'
  pb.push_link(subject, product['url'])

if __name__ == "__main__":
  main()