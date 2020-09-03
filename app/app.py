from flask import Flask, render_template, request, redirect
import pandas as pd
import requests

app = Flask(__name__)

API_KEY = 'JZ83OOJHHC5428Z3'
symbol='IBM'
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY\
&outputsize=full&symbol={}&apikey={}'.format(symbol, API_KEY)

r = requests.get(url)

df = pd.DataFrame(r.json()['Time Series (Daily)'], dtype=float)
df = df.T # transpose so dates are in the rows

@app.route('/')
def index():
  return render_template('index.html', data=df)

if __name__ == '__main__':
  app.run(port=33507)
