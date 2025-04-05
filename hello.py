from flask import Flask
import logging
app = Flask(__name__)
logging.basicConfig(filename='pythonflasksensor.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@app.route("/")
def hello_world():

    app.logger.info('Info level log')
    app.logger.warning('Warning level log')

    return "<p>Hello, World2!</p>"