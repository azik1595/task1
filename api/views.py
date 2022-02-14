from datetime import datetime, timedelta

import aiohttp
from api.utils import pretty_json, login_required
from aiohttp_apispec import docs, request_schema, response_schema
from api.models import Persons,Event,Coupon
from aiohttp import web, ClientSession
import jwt
from api.schemas import (
     EventCouponSchema, UserRegistrationRequestSchema,UserRegistrationResponseSchema,
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


@docs(tags=["Event Coupon"],
      summary=".",
      description=".")
@request_schema(EventCouponSchema)
@login_required
async def events_new(request):
    db_session = DBSession()
    jwt_token = request.headers.get('Authorization', None)
    payload = jwt.decode(
                jwt_token, config["DEFAULT"]['JWT_SECRET'], algorithms= [config["DEFAULT"]['JWT_ALGORITHM']])
    data =  await request.json()
    event_id = data["event_id"]
    user_id =  payload['user_id']
    hash =  jwt_token    
    new_coupon = Coupon(event_id = event_id,user_id = user_id,hash = hash)
    async with aiohttp.ClientSession():
            db_session.add(new_coupon)
            db_session.commit()

    return web.json_response(new_coupon, dumps=pretty_json)



