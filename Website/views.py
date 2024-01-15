from flask import Blueprint, render_template, Flask

#This is a Blueprint of our application
views = Blueprint('views', __name__)

@views.route('/')
def home():         #Whenever we go to URL we will run home (Views is called a decorator)
    return render_template("home.html")
   