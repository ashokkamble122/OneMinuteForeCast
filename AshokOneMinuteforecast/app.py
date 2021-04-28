
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import flasgger
from flasgger import Swagger

from flask_marshmallow import Marshmallow

from flask_sqlalchemy import SQLAlchemy

import pyodbc

import sqlalchemy

from ForeCastUtilities import ForeCastDataHandling

openweathermap=ForeCastDataHandling()

from LatLaninfo import mycitydict

app = Flask(__name__)
Swagger(app)


#app.config['SQLALCHEMY_DATABASE_URI']='mssql+pyodbc://localhost\SQLEXPRESS01/TFS?driver=Sql+Server'
app.config['SQLALCHEMY_DATABASE_URI']='mssql+pyodbc://localhost\SQLEXPRESS01/General?driver=SQL+Server+Native+Client+11.0?Trusted_Connection=yes'

app.config['SQLALCHEMY_TRACK_MODIFIACTIONS']=True

# init db

db=SQLAlchemy(app)

# init marshmallow

ma=Marshmallow(app)




# craete model/class

class OneMinuteForecast(db.Model):
    
    id=db.Column(db.Integer,primary_key=True)
    location=db.Column(db.String(200))
    lat=db.Column(db.String(200))
    lon=db.Column(db.String(200))
    dt=db.Column(db.String(200))
    precipitation=db.Column(db.String(200))
    def __init__(self,location,lat,lon,dt,precipitation):

        self.location = location
        self.lat = lat
        self.lon = lon
        self.dt = dt
        self.precipitation = precipitation

# create schemas 

class OneMinuteForecastSchema(ma.Schema):

    class Meta:

        fields=('id','location','lat','lon','dt','precipitation')

# init schema

forcast_Schema=OneMinuteForecastSchema()

forcasts_Schema=OneMinuteForecastSchema(many=True)

#db.create_all()

forcastclass=OneMinuteForecast

@app.route('/getforecastdata')
def getdata():
    '''
    lets get a user data
    ---
    responses:
        200:
            description: Ok
    ''' 
    all_data = forcastclass.query.all()

    result=forcasts_Schema.dump(all_data)

    return jsonify({'Mydbdata':result}),200 
    

@app.route('/updateforecast',methods=['GET'])
def updatedata():
    '''
    lets get a user data
    ---
    responses:
        200:
            description: Ok
    ''' 
    
    msg=None
    try:
        duplicate=0
        for i in mycitydict:
            print(i)
            print(mycitydict[i])
            lat=mycitydict[i][0]
            lon= mycitydict[i][1]
            forecastdat=openweathermap.getoneminutedata(lat,lon)
            for elm in forecastdat:
                try:
                    isduplicate = forcastclass.query.filter_by(lat=lat,lon=lon,dt=str(elm['dt'])).first()
                    #print(isduplicate)                                               
                    if  isduplicate is None:
                        new_record= OneMinuteForecast(str(i),str(lat),str(lon),str(elm['dt']),str(elm['precipitation']))
                        db.session.add(new_record)
                        db.session.commit()
                    else:
                        duplicate=duplicate+1
                except:
                       pass
                       
        msg="records uodated successfully"
    except:
        msg="somthing wen wrong please connect to admin"
        
    return jsonify({"message":msg})
        
        
    
    


if __name__ == "__main__":
    app.run(debug=False)
    
    
