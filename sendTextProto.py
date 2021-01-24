def pushInStockAlert(body):
  print(body)
  server = smtplib.SMTP( "smtp.gmail.com", 587 )
  server.starttls()
  server.login( 'GET FROM CONFIG', 'GET FROM CONFIG' )
  from_mail = 'GET FROM CONFIG'
  to = 'GET FROM CONFIG'
  subject = "Stock Alert"
  message = ("From: %s\r\n" % from_mail
             + "To: %s\r\n" % to
             + "Subject: %s\r\n" % subject
             + "\r\n"
             + body)
  server.sendmail(from_mail, to, message)

print(inStockIndeces)
if len(inStockIndeces) > 0:
  for index in inStockIndeces:
    print(products[index].get("url"))
    sendText("%s " % products[index].get("name")
             + "is in stock at %s:\r\n" % products[index].get("store")
             + "%s" % shortenUrl(products[index].get("url")))

             
def shortenUrl(url):
  api_key= "GET FROM CONFIG"
  api_url = f"https://cutt.ly/api/api.php?key={api_key}&short={url}"
  data = requests.get(api_url).json()["url"]
  if data["status"] == 7:
      shortened_url = data["shortLink"]
      return shortened_url
  else:
      print("[!] Error Shortening URL:", data)
      return "Error Shortening URL"