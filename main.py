from flask import Flask
from Website import create_app

app= create_app()

if __name__ == '__main__':              # Runs the web server if I run this doc directly.
    app.run(debug=True)                 # Everytime a change is made in the code this will rerun the webserver. Turn it FALSE when running on production
    #192.168.50.171


#If it an error pop up and says "No module named flask", the python interpreter is wrong.
# To change it: CTRL + SHIFT + P then type "python select interpreter" then choose "python 3.8.3 64-bit (conda)"