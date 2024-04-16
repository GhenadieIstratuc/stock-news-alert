import requests
from datetime import date, timedelta
from twilio.rest import Client

# Alphavantage API
ALPHAVANTAGE_ENDPOINT = "https://www.alphavantage.co/query"
STOCK = "TSLA"
ALPHA_VANTAGE_KEY = "YOUR KEY"

alphavantage_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_VANTAGE_KEY
    }

# News API
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
COMPANY_NAME = "Tesla Inc"
NEWS_KEY = "YOUR KEY"
yesterday = date.today() - timedelta(days=1)
formatted_yesterday = yesterday.strftime("%Y-%m-%d")
DATE = formatted_yesterday
LANGUAGE = "en"
SORTING = "publishedAt"

news_parameters = {
    "q": COMPANY_NAME,
    "from": DATE,
    "language": LANGUAGE,
    "sortBy": SORTING,
    "apiKey": NEWS_KEY,
}

# Twilio API
TWILIO_SID = "YOUR SID"
TWILIO_AUTH_TOKEN = "YOUR TOKEN"

# Gathering data from stocks API
response = requests.get(url=ALPHAVANTAGE_ENDPOINT, params=alphavantage_parameters)
response.raise_for_status()
data = response.json()
daily_data = data["Time Series (Daily)"]
daily_data_list = []
for day in daily_data:
    daily_data_list.append(daily_data[day])

yesterday_closing_price = float(daily_data_list[0]["4. close"])
day_before_closing_price = float(daily_data_list[1]["4. close"])

diff = yesterday_closing_price - day_before_closing_price

if yesterday_closing_price >= day_before_closing_price:
    # Price increased
    percent = round(abs(diff * 100 / yesterday_closing_price))
else:
    # Price decreased
    percent = round(abs(diff * 100 / day_before_closing_price))

# Gathering data from news API
resp = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
resp.raise_for_status()
news_data = resp.json()
articles = news_data["articles"][:3]

# Sending SMS
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
UP = "🔺"
DOWN = "🔻"
if percent > 2:
    first_articles = [f'Headline: {article["title"]} \n Brief: {article["description"]}' for article in articles]
    for article in first_articles:
        if diff >= 0:
            message = client.messages.create(
                body=f"{STOCK}: {UP}{percent}%\n{article}",
                from_='+12*********',
                to='+373********'
            )
        else:
            message = client.messages.create(
                body=f"TSLA: {DOWN}{percent}%\n{article}",
                from_='+12*********',
                to='+373******'
            )
