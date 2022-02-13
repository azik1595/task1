#Task:
#nput:
HTTP Rest API with several endpoints based on Python 3.9 Aiohttp async web framework.
Every user of this application can book COUPON for a single EVENT. One COUPON = one EVENT.
Models:
PERSON:
name
surname
token
EVENT:
remain
title
description
price
date
COUPON:
event
user
hash
Comments:
Please, use:
Access-Token for route safety
JWT or similar token-based user authentication
Pydantic for schema validation
Access-Token middleware
Docker Compose (all containers must be healthy)
MySQL
Python Black
PEP8
SQL Alchemy
Alembic Migrations
Integration Tests (Pytest)
 Create report endpoints
Person list which participated at least in 3 events (persons name, surname, event name,
Event list which filters by persons count and accepted coupons by persons (event name and date, coupon hash, person name
Write all environment variables in a docker-compose.yml file. 
Add Github Actions for Black linting and for tests part.
Upload your source code to private Github repository and add postman collection file for testing.
## For start app run `docker-compose up` in app-root folder.
Tests with run at starts docker container.
Application will be aviable at localhost:8000. 
### Docs
Swagger docs are aviable at /api/v1/docs/.
