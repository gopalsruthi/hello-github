import logging
from google.cloud import storage
from flask import Flask, request, jsonify
import numpy as np
import joblib
import io

app = Flask(__name__)

def read_file():
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('diabetes-bucket')
    blob = bucket.blob('diabetes_pickled.joblib')
    #blob.download_to_filename('diabetes_pickled.joblib') #This downloads directly into directory
    x = io.BytesIO(blob.download_as_string())
    return x

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/newroute/<name>')
def newroute(name):
    """parameter"""
    return "this was passed in: %s" % name

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

@app.route('/predict', methods=['POST'])
def pred():
    model = joblib.load(read_file())
    print(model)
    data = request.get_json()
    prediction = np.array2string(model.predict(data))
    print('This is the data:', data)
    print('This is the prediction', prediction)
    return jsonify(prediction)

@app.route('/loaderio-bd9c583078780187f53afe60d102f2a7.txt')
def test():
    return 'loaderio-bd9c583078780187f53afe60d102f2a7'

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
