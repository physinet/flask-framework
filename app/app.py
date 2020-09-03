from flask import Flask, render_template, request, redirect

app = Flask(__name__)


data = {'test': [1,2,3], 'testagain': [3,4,5]}

@app.route('/')
def index():
  return render_template('index.html', data=data)

if __name__ == '__main__':
  app.run(port=33507)
