from flask import Blueprint, jsonify, request, make_response


bp = Blueprint('auth', __name__)


@bp.route('/', methods=['GET'])
def auth_root():
    return make_response(jsonify({'message': 'test route'}), 200)


@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200


def register_routes(app):
    app.register_blueprint(bp)
