from flask import Flask, jsonify
from flask_swagger import swagger

app = Flask(__name__)

@app.route("/spec")
def spec():
    return jsonify(swagger(app))

@app.route("/")
def index():
    """
        Flask Index Page
        ---
        responses:
          200:
            description: OK
        """
    return 'Hello World'


if __name__ == "__main__":
    Flask.run(app)