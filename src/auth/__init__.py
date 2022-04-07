from app.jwt import jwt
from auth.jwt_handlers import user_identity_lookup, user_lookup_callback


def init_package(*args, **kwargs):
    jwt.user_identity_loader(user_identity_lookup)
    jwt.user_lookup_loader(user_lookup_callback)
