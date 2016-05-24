from app.mod_base.errors import error_response


def configure_access(app):
    set_cors(app)
    set_errors(app)


def set_cors(app):

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE')
        return response


def set_errors(app):

    @app.errorhandler(403)
    def forbidden(e):
        return error_response(403)

    @app.errorhandler(404)
    def not_found(e):
        return error_response(404)

    @app.errorhandler(405)
    def not_allowed(e):
        return error_response(405)
