import logging
from google.cloud import storage
from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
#import pickle as p
import json
import joblib
import io
app = Flask(__name__)


def read_file():
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('diabetes-bucket')
    blob = bucket.blob('diabetes_pickled.joblib')
    blob.download_to_filename('diabetes_pickled.joblib')
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

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    # modelfile = read_file()
    # model = p.load(open(modelfile, 'rb'))
    # I am hardwiring the file, IS THAT OKAY??? #teraform: look it up
    # When testing web app locally, use different cloud shell
    
    #model = joblib.load(read_file())
    #print(model)
    app.run(host='127.0.0.1', port=8080, debug=True)


    #Questions:
    # Why isn't my predict URL working? Why isn't request.py working?
    # Is it okay to hardwire the file as long as it's saved in the same directory?
    # Should I rename app.yml as app.yaml?
    # How would I call this project on my resume? 
