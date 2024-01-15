# ==================== In this file we create the Database models ==================== 

#The dot means "current package". So import db from this current package
from . import db 


# -------------------- Database Model --------------------
class Values(db.Model):
    id = db.Column(db.Integer, primary_key= True)                   # ID for each data row

    field1 = db.Column(db.Integer, nullable = False)                # Data received from ThingSpeak
    field2 = db.Column(db.Integer, nullable = False)
    field3 = db.Column(db.Integer, nullable = False)
    field4 = db.Column(db.Integer, nullable = False)
    field5 = db.Column(db.Integer, nullable = False)
    field6 = db.Column(db.Integer, nullable = False)
    field7 = db.Column(db.Integer, nullable = False)
    field8 = db.Column(db.Integer, nullable = False)

    date = db.Column(db.Integer, nullable = False)                  # Creation date
    
    def __str__(self):
        return self.id

    
