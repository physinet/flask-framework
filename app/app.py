from flask import Flask, render_template, request, redirect
import pandas as pd
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

r = requests.get(url)

df = pd.DataFrame(r.json()['Time Series (Daily)'], dtype=float)
df = df.T # transpose so dates are in the rows

@app.route('/')
def index():
  return render_template('index.html', data=df)

@app.route('/plot')
def plot():
    '''
    Following https://github.com/realpython/flask-bokeh-example
    '''
    fig = figure(plot_width=600, plot_height=600)
    fig.line(x=[1,2,3], y=[4,5,6])

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(fig)
    html = render_template('plot.html', plot_script=script, plot_div=div,
        js_resources=js_resources, css_resources=css_resources)
    return encode_utf8(html)


if __name__ == '__main__':
  app.run(port=33507)
