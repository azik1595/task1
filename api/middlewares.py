
import jwt
from aiohttp import web
from api.models import Persons
import configparser
import app
from api import utils 
config = configparser.ConfigParser()
config.read('config.ini')


@web.middleware
async def auth_middleware(request, handler):
    request.user = None
    jwt_token = request.headers.get('Authorization', None)

    if jwt_token:
        if jwt_token.startswith('Bearer '):
            jwt_token = jwt_token[7:]
        try:
            payload = jwt.decode(
                jwt_token, config["DEFAULT"]['JWT_SECRET'], algorithms= [config["DEFAULT"]['JWT_ALGORITHM']])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            await utils.service_log(request)
            return web.json_response(
                {'message': 'Token is invalid'}, status=400)
        db_session = app.DBSession()
        request.user = db_session.query(Persons).filter(Persons.id == payload['user_id']).first()  
        # Create log with user.id.
        await utils.service_log(request)
    return await handler(request)
