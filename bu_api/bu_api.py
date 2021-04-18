from flask import request, jsonify
from flask import Blueprint, make_response
from flask_restx import Resource, Api
from re import search
from common.config import config
from common.utils import get_logger, get_file_contents
from common.utils import make_file_name, write_json
from .utils.utils import get_models_parsers
from .utils.utils import auth_required, get_example_certs


# initialize logging:
log = get_logger(__name__)


response_codes = {
    200: 'OK',
    400: 'Bad Request',
    401: 'Unauthorized'
}


# API configuration
bu_api_blueprint = Blueprint('bu_api', __name__, url_prefix='/api/v1')
api = Api(bu_api_blueprint, doc='/', version='1.0', title='API V1')

api.namespaces = []
ns = api.namespace('', description='Resources [env: %s]:' % config['env'])


get_file_parser, post_file_model = get_models_parsers(api)


@ns.route('/get-file-store')
@api.route('/get-file-store')
@api.doc(responses=response_codes)
@api.doc(parser=get_file_parser)
class GetFileStore(Resource):

    @auth_required
    def get(self):
        try:
            file_name = request.headers['FileName']
            if not file_name:
                raise Exception('Invalid file name provided')
            if search(r'[\s\W]', file_name) is not None:
                raise Exception('Invalid characters entered')
            content = get_file_contents(file_name)
        except Exception as err:
            log.error(err)
            return make_response(jsonify({'Error': str(err)}), 400)
        return jsonify({file_name: content})


@ns.route('/post-file-store')
@api.route('/post-file-store')
@api.doc(responses=response_codes)
class PostFileStore(Resource):

    @auth_required
    @api.expect(post_file_model)
    def post(self):
        resp = {'Created': False, 'FileName': 'N/A'}

        try:
            incoming_data = request.json['FileData']
        except Exception as err:
            log.error(err)
            return make_response(jsonify(resp), 400)

        file_name = make_file_name()
        try:
            write_json(file_name, incoming_data)
        except Exception as err:
            log.error('FAILED write')
            log.error(err)
            return make_response(jsonify(resp), 400)

        resp['Created'], resp['FileName'] = True, file_name
        return jsonify(resp)


@ns.route('/get-example-certificates')
@api.route('/get-example-certificates')
@api.doc(responses=response_codes)
class GetExampleCertificates(Resource):

    @auth_required
    def get(self):
        return jsonify(get_example_certs())
