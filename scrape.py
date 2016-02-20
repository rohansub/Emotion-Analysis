from bs4 import BeautifulSoup
import urllib
import requests

# Starts the session
session = requests.Session()
# Opens the Facebook login page in the session
homepage_response = session.get('https://www.messenger.com/').text
# Loads the login page into a BeautifulSoup soup object
soup = BeautifulSoup(homepage_response,  "html.parser")
# Extracts the LSD token from Facebook login page, required for login post request
lsd = str(soup.find_all('input', attrs={"name": "lsd"})[0]['value'])

#print(soup.prettify())

username = raw_input('Enter your username: ')
password = raw_input('Enter your password: ')

login_data = {
    'lsd': lsd,
}
login_data['email'] = username
login_data['pass'] = password
login_data['login'] = 'Log In'
# URL for the login POST request
login_url = 'https://www.messenger.com/login.php?login_attempt=1'
# Logs in and stores the response page (our Facebook home feed)
content = session.post(login_url, data=login_data, verify=False).content
soup2 = BeautifulSoup(content,  "html.parser")

print soup2.prettify()
