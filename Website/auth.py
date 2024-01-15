from flask import Blueprint, render_template, flash, jsonify
from flask import Flask,url_for, redirect

from . import db    
from .models import Values 
from . import create_app

import json
import requests

from urllib.request import urlopen
from time import time


# ==================== This is a Blueprint of our application ====================
auth = Blueprint('auth', __name__)


# ==================== Requests for ThingSpeak API ====================

# r = requests.get('https://api.thingspeak.com/channels/2351521/fields/1.json?results=10')        #Används för att få data från en specifik channel
r = requests.get('https://api.thingspeak.com/channels/2351521/feeds.json?results=20')
thingdatatest = json.loads(r.text)
   
    
url_all= "https://api.thingspeak.com/channels/2351521/feeds.json?"                                  # Visar alla värde för alla fields i the channel
with urlopen(url_all) as response:
    dat= response.read()
all_dat = json.loads(dat)


# send = "https://api.thingspeak.com/update?api_key=DZZRAATBY9W7FKH8&field1=0" + str(100)  #Används för att adda information till thingspeak


extract = []
field_1=[]
field_2=[]
field_3=[]
# Test on how to extract data from ThingSpeak
for key, value in all_dat.items():
    if isinstance(value, dict):
        field1_value = value.get('field1', None)
        field2_value = value.get('field2', None)
        field3_value = value.get('field3', None)
        if field1_value is not None:
            extract.append(('field1', field1_value))
            extract.append(('field2', field2_value))
            extract.append(('field3', field3_value))
    elif isinstance(value, list):
        for i in value:
            for inner_key, inner_value in i.items():
                extract.append((inner_key, inner_value))
                if inner_key == 'field1':
                    field_1.append(inner_value)
                elif inner_key == 'field2':
                    field_2.append(inner_value)
                elif inner_key == 'field3':
                    field_3.append(inner_value)
                
                        

# ==================== How to define different Routes ====================


# -------------------- Routes for the different parameters --------------------
    #The methods makes it possible to get and post request from this route
    #You can use if sats to differenciate between post and get by using if request.method == 'POST'

# -------------------- Code to constantly update the information from Thingspeak --------------------
@auth.route('/all_data')
def all_data():
    print("Getting all data")
    url_all= "https://api.thingspeak.com/channels/2351521/feeds.json?results=25"                  # Visar alla värde för alla fields i the channel
    link = requests.get(url_all)
    all_dat = json.loads(link.text)

    for x in all_dat['feeds']:
        if x['created_at']:
            response= {
                'created_at' : x['created_at'],
                "field1": x['field1'],
                'field2': x['field2'],
                "field3": x['field3'],
                'field4': x['field4'],
                "field5": x['field5'],
                'field6': x['field6'],
                "field7": x['field7'],
                'field8': x['field8']
                } 
            
    save_data= [
        response['created_at'],
        response['field1'],
        response['field2'],
        response['field3'],
        response['field4'],
        response['field5'],
        response['field6'],
        response['field7'],
        response['field8']
        ]
    # Store the information on the Database
    app= create_app()
    with app.app_context():
        db.create_all()
    entry2= Values(
        date=save_data[0], 
        field1=save_data[1], 
        field2=save_data[2], 
        field3=save_data[3], 
        field4=save_data[4], 
        field5=save_data[5], 
        field6=save_data[6], 
        field7=save_data[7], 
        field8=save_data[8]
        ) 
    with app.app_context():
            db.session.add(entry2)        
            db.session.commit()  

    # Build our response to send back to the Javascript
    print(f'Sending {response}')
    return jsonify(response)


# -------------------- Definition for the different OBD2 Parameters --------------------

@auth.route("AllValues")
def index():
    entries= Values.query.all()
    return render_template("AllValues.html", 
                           title     = 'AllValues', 
                           entries   = entries, 
                           thingdata = thingdatatest
                           )

@auth.route('/Vehicle-Speed', methods= ['GET', 'POST'])         
def Vspeed():
    entries= Values.query.all()
    return render_template("VehicleSpeed.html", 
                           entries   = entries, 
                           thingdata = thingdatatest
                        )

@auth.route("Motor-Temp")
def MotorTempSide():
    entries= Values.query.all()
    return render_template("MotorTemp.html", 
                           title     = 'Motor-Temp', 
                           entries   = entries, 
                           thingdata = thingdatatest
                           )

@auth.route("Battery")
def BatterySide():
    entries= Values.query.all()
    return render_template("Battery.html", 
                           title     = 'Battery', 
                           entries   = entries,
                           thingdata = thingdatatest
                           )

@auth.route("CarTemp")
def CarTempSide():
    entries= Values.query.all()
    return render_template("CarTemp.html", 
                           title     = 'Temperature in the Vehicle', 
                           entries   = entries, 
                           thingdata = thingdatatest
                           )

@auth.route("FluidLevel")
def FluidLevelSide():
    entries= Values.query.all()
    return render_template("FluidLevel.html", 
                           title     = 'Washer Fluid Level', 
                           entries   = entries, 
                           thingdata = thingdatatest
                           )

@auth.route("Fuel-Tank-Level")
def FuelTankLvlSide():
    entries= Values.query.all()
    return render_template("FuelTank.html", 
                           title     = 'Fuel-Tank-Level', 
                           entries   = entries, 
                           thingdata = thingdatatest
                           )

@auth.route("RPM")
def RPMSide():
    entries= Values.query.all()
    return render_template("RPM.html", 
                           title     = 'RPM_Values', 
                           entries   = entries, 
                           thingdata = thingdatatest
                           )

@auth.route("GPS")
def GPSSide():
    entries= Values.query.all()
    return render_template("GPS.html", 
                           title     = 'GPS Location ', 
                           entries   = entries, 
                           thingdata = thingdatatest
                           )


# -------------------- Other Routes --------------------

@auth.route('/About')
def About():
    return render_template("About.html")


@auth.route('/delete-post/<int:entry_id>')
def delete(entry_id):
    entry = Values.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("The data has been deleted", "succes")
    return redirect(url_for("auth.index"))


