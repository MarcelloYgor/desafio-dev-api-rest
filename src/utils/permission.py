
from functools import wraps

from werkzeug.exceptions import Forbidden

from model.usuario import Usuario

def admin_only():
    def admin_only_decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token_info = kwargs.get('token_info')

            usuario = Usuario.query.filter_by(id=token_info.get('id')).first()

            if not usuario.admin:
                raise Forbidden

            return f(*args, **kwargs)

        return decorated
    return admin_only_decorator
