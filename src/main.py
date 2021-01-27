import configparser
import json
import logging
import mechanicalsoup
import re
import sys
from pushbullet  import Pushbullet
from os.path     import dirname, abspath
from proxyScrape import getProxies
from itertools   import cycle

# Setting up file paths helps when running cron
path = dirname(abspath(__file__))
configPath   = f'{path}/config.ini'
loggingPath  = f'{path}/app.log'
errorPath    = f'{path}/error.log'
productsPath = f'{path}/products.json'
storesPath   = f'{path}/stores.json'
agentsPath   = f'{path}/agents.json'

# Load products
with open(productsPath) as f:
  products = json.load(f)
# Load stores
with open(storesPath) as f:
  stores = json.load(f)
# Load user agents
with open(agentsPath) as f:
  userAgents = json.load(f)
# Scrape proxies
proxies = getProxies()

# Create cycle for rotation
agentPool = cycle(userAgents)
proxyPool = cycle(proxies)

# sys.exit()

# Get PushBullet API_KEY from config
config = configparser.ConfigParser()
config.read(configPath)
pb = Pushbullet(config['pushbullet']['API_KEY'])

def main():
  # TODO: Track the indeces and log names/stores OR # at each store
  itemsFound = 0
  rateLimitedStores = []
  try:
    # logging.info('___________ Begin stock check ___________')
    browser = mechanicalsoup.StatefulBrowser()
    for product in products:
      proxy     = next(proxyPool)
      userAgent = next(agentPool)
      try:
        browser.open(product['url'],
          proxies={"http": f'http://{proxy}', "https": f'https://{proxy}'},
          headers={'User-Agent': userAgent})
      except:
        logging.error("Connecton Error")
        logging.error(sys.exc_info()[0])
        logging.error("_______________")
        sys.exit()

      pageSource = str(browser.page.encode("utf-8"))
      soldOutPhrase = stores[product["store"]]["soldOutPhrase"]
      soldOut = re.search(soldOutPhrase, pageSource)
      rateLimited = re.search(">Access to this page has been denied.<", pageSource)
      if soldOut == None and rateLimited == None:
        pushInStockAlert(product)
        itemsFound = itemsFound + 1
      if rateLimited != None:
        if product["store"] not in rateLimitedStores:
          pushRateLimitWarning(product["store"])
          logging.info(f'{product["store"]} is rate limiting')
          rateLimitedStores.append(product["store"])
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

def pushRateLimitWarning(store):
  body = f'{store} is rate limiting instock requests'
  push = pb.push_note("Rate Limiting", body)



# Log INFO level messages
logging.basicConfig(filename=loggingPath,
  format='%(asctime)s - %(message)s',
  level=logging.INFO)
# Log ERROR
logging.basicConfig(filename=errorPath,
  format='%(asctime)s - %(message)s',
  level=logging.ERROR)

if __name__ == "__main__":
  main()
