import requests

url = "http://geo.brdtest.com/mygeo.json"

victor =  {'http': 'http://brd-customer-hl_4907aa65-zone-web_unlocker1:lqp000jrvn3m@brd.superproxy.io:22225',
            'https': 'http://brd-customer-hl_4907aa65-zone-web_unlocker1:lqp000jrvn3m@brd.superproxy.io:22225'}

response = requests.get(url, proxies=victor)

json_response = response.json()
country = json_response['country']
city = json_response['geo']['city']

print(f"Votre adresse es êtes localisé en {country} à {city}")