from flask import Flask, render_template, request, redirect
import pandas as pd
import datetime
import requests

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

app = Flask(__name__)

API_KEY = 'JZ83OOJHHC5428Z3'
symbol='IBM'
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY\
&outputsize=full&symbol={}&apikey={}'.format(symbol, API_KEY)

@app.route('/')
def index():

    r = requests.get(url)

    df = pd.DataFrame(r.json()['Time Series (Daily)'], dtype=float)
    df = df.T # transpose so dates are in the rows

    return render_template('index.html', data=df)

@app.route('/plot')
def plot():
    '''
    Display a Bokeh plot, following
    https://github.com/realpython/flask-bokeh-example
    '''

    r = requests.get(url)

    df = pd.DataFrame(r.json()['Time Series (Daily)'], dtype=float)
    df = df.T  # transpose so data for each date are in the rows
    df.index = pd.to_datetime(df.index)  # convert to datetime object

    now = datetime.datetime.now()
    one_month_ago = now - pd.DateOffset(months=1)
    df_month = df[df.index > one_month_ago]

    fig = figure(plot_width=600, plot_height=600)
    fig.line(x=df_month.index, y=df_month['4. close'])

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(fig)
    html = render_template('plot.html', plot_script=script, plot_div=div,
        js_resources=js_resources, css_resources=css_resources)
    return encode_utf8(html)


if __name__ == '__main__':
  app.run(port=33507)
