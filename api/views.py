from datetime import datetime, timedelta

import aiohttp
from api.utils import pretty_json, login_required
from aiohttp_apispec import docs, request_schema, response_schema
from api.models import Persons,Event,Coupon
from aiohttp import web, ClientSession
import jwt
from api.schemas import (
     UserRegistrationRequestSchema,UserRegistrationResponseSchema,
    UserLoginRequestSchema, UserLoginResponseSchema)
from api.validator import AuthRequestSchema
from app import DBSession

import configparser

config = configparser.ConfigParser()
config.read('config.ini')




@docs(tags=["Authorization"],
      summary="Return JWT token for authentication user.",
      description=(
          "Accept POST request and return token if credentials is valid."))
@request_schema(UserLoginRequestSchema)
@response_schema(UserLoginResponseSchema, 200)
async def login(request):
    data =  await request.json()
    username = data['username']
    raw_password = data['password']
    validated_user  =AuthRequestSchema(username=username,password=raw_password).dict()
    db_session = DBSession()
    user = db_session.query(Persons).filter(Persons.username == validated_user['username'] and Persons.verify_password( validated_user['password'])).first()
    if user is None :
        return web.json_response({'Error': 'Wrong credentials'}, status=400)

    payload = {
        'user_id': user.id,
        'exp': datetime.now() + timedelta(seconds=int(config["DEFAULT"]['JWT_EXP_DELTA_SECONDS']))}
    jwt_token = jwt.encode(payload, config["DEFAULT"]['JWT_SECRET'], config["DEFAULT"]['JWT_ALGORITHM'])
    user.token = jwt_token
    async with aiohttp.ClientSession():        
            db_session.commit()
    return web.json_response(
        {'token': jwt_token}, dumps=pretty_json)


@docs(tags=["Authorization"],
      summary="Registration for new user.",
      description=(
          "Accept POST request and return new user's id. "
          "After you can authorization with username and password on /login."))

@request_schema(UserRegistrationRequestSchema)
@response_schema(UserRegistrationResponseSchema, 201)
async def registration(request):
    data =  await request.json()
    username = data['username']
    surname = data['surname']
    raw_password = data['password']
    stored_password = Persons.hash_password(raw_password)


    db_session = DBSession()
    new_user = Persons(username=username, password=stored_password,surname = surname)
    async with aiohttp.ClientSession():
            db_session.add(new_user)
            db_session.commit()


    return web.json_response(
        {'id': new_user.id, 'username': username}, dumps=pretty_json, status=201)


@docs(tags=["Events"],
      summary="Return all user's Events.",
      description="Accept GET request and return Events.")
@login_required
async def events_list(request):
    db_session = DBSession()
    events = db_session.query(Event).all()
    return web.json_response({'events': events}, dumps=pretty_json)







# @docs(tags=["Jokes"],
#       summary="Update joke by ID.",
#       description="Accept PATCH request for joke and update joke's text.")
# @request_schema(JokeRequestSchema(strict=True))
# @response_schema(JokeResponseSchema(), 200)
# @login_required
# async def joke_update(request):
#     joke_id = int(request.match_info['id'])
#     data = request["data"]
#     new_text = data["text"]

#     joke = await Joke.get(joke_id)

#     if joke is None:
#         raise web.HTTPNotFound()
#     if not joke.is_joke_owner(request.user):
#         return web.json_response(
#             {"Error": "This is not your joke."}, dumps=pretty_json, status=403)

#     await joke.update(text=new_text).apply()

#     joke_schema = JokeResponseSchema()
#     joke_json, errors = joke_schema.dump(joke)

#     return web.json_response(joke_json, dumps=pretty_json)


# @docs(tags=['Jokes'],
#       summary='Delete joke by ID.',
#       description='Accept DELETE request for joke and delete it.')
# @response_schema(DeleteJokeResponseSchema(), code=204)
# @login_required
# async def joke_delete(request):
#     """
#     I dont know why, but this endpoint return nothing, if everything ok.
#     Its raise exception Response <type of response> not prepared.
#     Also other web.json_responses responses correctly.
#     I've tried other aiohttp versions, without result.
#     I think its aiohttp bug.
#     ¯\_(ツ)_/¯
#     """
#     joke_id = int(request.match_info['id'])
#     joke = await Joke.get(joke_id)
#     if joke is None:
#         raise web.HTTPNotFound()
#     if not joke.is_joke_owner(request.user):
#         return web.json_response(
#             {'Error': 'This is not your joke.'}, dumps=pretty_json, status=403)

#     await joke.delete()

#     return web.json_response(
#         {'Message': 'Successfuly deleted'}, dumps=pretty_json, status=204)
