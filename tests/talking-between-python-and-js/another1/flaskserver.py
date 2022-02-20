# https://stackoverflow.com/questions/21942320/calling-a-local-python-script-from-javascript
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    xml = "hello"
    # make fancy operations if you want
    return xml

if __name__ == "__main__":
    app.run() 
