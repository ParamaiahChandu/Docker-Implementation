from flask import Flask, json, request, render_template
from flask_restful import Resource, Api
import csv

app = Flask(__name__)
api = Api(app)

#Open CSV file
csvFile = open('daily.csv','r')

#Reading CSV file
csvReader=csv.DictReader(csvFile)

#Converting CSV to JSON
jsonOutput = json.dumps([row for row in csvReader])

#Loading JSON data
jsonData = json.loads(jsonOutput)

#WebPage.html calling logic
@app.route('/web/')
def Page():
   return render_template('WebPage.html')

hist=[]
class Historical(Resource):
    def get(self):
        for i in range(0,len(jsonData)):
            hist.append({"DATE":jsonData[i]['DATE']})
        return hist,200

class Histdate(Resource):
    def get(self,date_id):
        for i in range(0,len(jsonData)):
            if jsonData[i]['DATE'] == date_id:
                return jsonData[i]
        return {'Not': 'Found'},404

class postdate(Resource):
    def post(self):
        jsonData.append(request.get_json(force=True))
        return {"DATE" : request.get_json(force=True)["DATE"]}, 201


class deldate(Resource):
    def delete(self,datedel_id):
        for j in range(0,len(jsonData)):
            if jsonData[j]['DATE'] == datedel_id:
                del jsonData[j]
                return '',204

#Forecasting logic
class Forecast(Resource):
   def get(self, userDate):
        outputObject = []
        tmax = []
        tmin = []
        date = []

        for year in range(2013, 2018):
                for i in range(0, len(jsonData)):
                  if jsonData[i]['DATE'] == str(year) + str(userDate)[4:]:
                    userYear = str(userDate)[:4]

                    for j in range(0, 5):
                     if year == 2013:
                      date.append(userYear + jsonData[i + j]['DATE'][4:])
                      tmax.append(float(jsonData[i + j]['TMAX']))
                      tmin.append(float(jsonData[i + j]['TMIN']))
                     else:
                      tmax[j] += float(jsonData[i + j]['TMAX'])
                      tmin[j] += float(jsonData[i + j]['TMIN'])

        tmax[:] = [x/5 for x in tmax]
        tmin[:] = [y/5 for y in tmin]

        for i in range(0, 5):
         outputObject.append({"DATE":date[i], "TMAX":str(tmax[i]), "TMIN":str(tmin[i])})

        return outputObject

api.add_resource(Historical, '/historical/')

api.add_resource(Histdate,'/historical/<string:date_id>')

api.add_resource(postdate,'/historical/')

api.add_resource(deldate,'/historical/<string:datedel_id>')

api.add_resource(Forecast,'/forecast/<string:userDate>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
