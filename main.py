"""
- Projet : Hello World en flask
- Auteur : Iago Dolfini
- Date : 05.10.2026
"""


import os
from flask import Flask
from markupsafe import escape


# Crée une application flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    message = os.environ.get("MESSAGE", " ... ")# <----- Modifier ici !
    return f"Hello, World!<br>{escape(message)}"

if __name__ == "__main__":
    try:
        # Run the Flask development server
        # debug=True enables auto-reload and better error messages
        app.run(host="0.0.0.0", port=5000, debug=True)
    except Exception as e:
        print(f"Erreur lors du démmarage du serveur Flask: {e}")