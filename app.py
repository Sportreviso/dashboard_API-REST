
from flask import Flask, render_template, jsonify
import requests, json, os
app = Flask(__name__)
CHANNEL_ID='3272763'
API_KEY='5IIMKO2XDCJ9GT67'
FIELD_UMIDADE='field1'
URL=f'https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={API_KEY}&results=200'
@app.route('/')
def index(): return render_template('dashboard.html')
@app.route('/data')
def data():
 r=requests.get(URL).json().get('feeds',[]);x=[];y=[]
 for f in r:
  if f.get(FIELD_UMIDADE): x.append(f['created_at']);y.append(float(f[FIELD_UMIDADE]))
g = {
    'data': [{
        'x': x,
        'y': y,
        'type': 'scatter',
        'mode': 'lines+markers',
        'name': 'Umidade do Solo'
    }],
    'layout': {
        'title': 'Umidade do Solo (%)',
        'xaxis': {
            'title': 'Tempo'
        },
        'yaxis': {
            'title': 'Umidade (%)',
            'range': [0, 100]
        }
    }
}
if __name__=='__main__':
 port=int(os.environ.get('PORT',5000));app.run(host='0.0.0.0',port=port)
