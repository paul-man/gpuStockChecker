# GPUStockChecker
Simple tool to check GPU stock availability

This program is ran via a crontab, will grab the page source from the URLs in `products.json`, and check the results against the criteria in `stores.json`.

If the criteria **IS** met the product is sold out and the results are logged and the program will exit.

If the criteria **IS NOT** met this potentially means the product is available and PushBullet is used to send the URL to my phone where I can follow the link to the product page.

This tool is for alerting purposes only -- it does not log me in, add items to my cart, or purchase any merchandise.
