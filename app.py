import asyncio
import pathlib
import api.routes
from api.middlewares import auth_middleware
from aiohttp import web
from aiohttp_apispec import validation_middleware, setup_aiohttp_apispec
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PROJ_ROOT = pathlib.Path(__file__).parent.parent
Base = declarative_base()
engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/main")
Base.metadata.create_all(bind=engine)
session = Session(bind=engine)
DBSession = sessionmaker(bind=engine)
globals().update({"session": session})

async def init(loop):
    app = web.Application()
    for route in api.routes.routes:
        app.router.add_route(*route)
   
    middlewares = [
       # db, 
      #validation_middleware, 
        auth_middleware
        ]
    app.middlewares.extend(middlewares)

    # Setup api_spec
    setup_aiohttp_apispec(
        app=app,
        title="API documentation",
        version='v1',
        url="/api/v1/docs/swagger.json",
        swagger_path="/api/v1/docs/")
    host = "0.0.0.0"
    port = 80
    return app, host, port
def main():
    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init(loop))
    web.run_app(app, host=host, port=port)


# Run app
if __name__ == '__main__':
    main()