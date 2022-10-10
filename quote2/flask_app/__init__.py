from flask import Flask

app = Flask(__name__)
app.secret_key = "password123"

DATABASE = "quotes_schema"