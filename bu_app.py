#! /usr/bin/python3
from flask import Flask, render_template, request, redirect
from common.config import config
from bu_api import bu_api_blueprint
from common.utils import get_logger


log = get_logger(__name__)
log.info('Starting Application')


app = Flask(__name__)
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'


app.register_blueprint(bu_api_blueprint)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html',
                           company=config['company'],
                           api_url=request.url + '/api/v1')


@app.errorhandler(404)
def not_found(error):
    _ = error
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
