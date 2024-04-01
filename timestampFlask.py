import os
import pandas as pd
import datetime
from datetime import datetime as dt
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)

@app.route("/date", methods=['POST'])
def getDate():
    data = request.get_json()   
    print(data)
    DateTime = data['datetime_data']
    DateTimeInteger = int(DateTime)
    deltaTime = datetime.timedelta(minutes = DateTimeInteger)
    FileName = data['filename_data']
    dataHora = pd.read_csv(FileName, sep=',', low_memory=False).drop([0, 1])
    currentTime = datetime.datetime.strptime(dataHora.TIMESTAMP[2], "%Y-%m-%d %H:%M:%S")
    newData = []
    nanRow = [None]*(len(dataHora.columns) + 1)             
    for row in dataHora.itertuples():
        rowTime = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
        while currentTime < rowTime:
            aux = nanRow.copy()
            aux[1] = currentTime
            newData.append(aux)
            currentTime += deltaTime
        newData.append(row)
        currentTime += deltaTime   
    dataHora = pd.DataFrame (newData)
    dataHora.to_csv(FileName+'_Ajustado', sep=',', index=False)
    return 'ta dando certo!'   
       
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if (__name__ == "__main__"):
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 5555)))
    CORS(app)