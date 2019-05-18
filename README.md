# Transfers RESTful API

This repository contains a Django RESTful API for a simple wallet transfer app

## TECHNOLOGY STACK

 - Python
 - Django
 - Django Rest Framework
 - Django Rest Framework Simple JWT
 - PyCharm (IDE)
 - Travis (CI)
 - Docker (**WIP**)


## ENDPOINTS

| URL | METHOD | DATA | INFO | RETURNS |
|--|--|--|--|--|
| /api/token | GET | {Email, Password} ||Token authenticator
| /api/users | POST | {Email, Password, Username, First name, Last name, Initial wallet balance} |It creates a new user, initial custom balance is allowed, this is not production ready.|Created user info
|/api/users/<int:id>|GET||Only allowed to GET info of same user that made the request|Details of user
|/api/users/<int:id>/transfer|POST|{To user (id), Amount}|Creates a transfer and updates wallets. This is only allowed if <int:id> is your own id.| Returns the transfer details.
