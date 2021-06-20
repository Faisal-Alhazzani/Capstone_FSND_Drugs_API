# FSND Capstone API Backend

### Having troubles finding your medications? Here's Drugs API, that helps you find your nearst drug's provider.

## Getting Started

### Installing Dependencies

#### Python 3.9.5


Follow instructions to install the version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

It's good practise to work within a virtual environment whenever using Python. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

```
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we use to handle cross origin requests from the frontend server. 

## Database Setup

Create a new database in Postgress:
```
createdb drugsApp
```
## Running the server locally

From within the home directory first ensure you are working using your created virtual environment.

To run the server, execute:
```
FLASK_APP=app.py FLASK_ENV=development python3.9 -m flask run
```

## Live server can be found in

> Base URL `https://capstone-drugs-app.herokuapp.com/`


# API Endpoints

> Base URL `https://capstone-drugs-app.herokuapp.com/`

URI|Method|Action|Curl example|return example
---|---|---|---|---
/|GET|test the application is running|`curl https://capstone-drugs-app.herokuapp.com/`| `[{ "Welcome To DrugsApp!": "App is Running"}, {"Endpoints": ["/login", "/drugs", "/drugs/<int:drug_id>", "/drug/create", "/pharmacies", "/pharmacies/<int:pharmacy_id>", "/pharmacy/create", "/pharmacy/<int:pharmacy_id>/edit", "/pharmacy/<int:pharmacy_id>/delete" ]}]`
/login|GET|get auth0 URL to login gain a token|`curl https://capstone-drugs-app.herokuapp.com/login`|`{"LoginURL": "https://dev-faisal.us.auth0.com/authorize?audience=drugs&response_type=token&client_id=ISIDDGjOprw72TuzTcLp9bACvnbo7dDX&redirect_uri=https://capstone-drugs-app.herokuapp.com/"}`|
/pharmacies|GET|Fetches all pharmacies as a List|`curl https://capstone-drugs-app.herokuapp.com/pharmacies -H"Authorization: Bearer <Token>"`|`{"data": [{"id": 1,"name": "Alnahdi pharmacy"},{"id": 2, "name": "Pharmacy 2"},{"id": 3, "name": "Pharmacy 3"}],"success": true}`|
/drugs|GET|Fetches all drugs as a List|`curl https://capstone-drugs-app.herokuapp.com/drugs -H"Authorization: Bearer <Token>"`|`{"data": [{"id": 1,"name": "Brofin","price": "13"},{"id": 2,"name": "Panadol","price": "13" }],"success": true}`|
/pharmacies/<id>/edit|PATCH|Modifies the content of a stored pharmacy. Returns a new updated pharmacies list|`curl https://capstone-drugs-app.herokuapp.com/pharmacy/3/edit -X PATCH -H"Authorization: Bearer <Token>" -H"Content-Type: application/json" -d'{"name": "edit test"}`|`{"pharmacies": [{"city": "Riyadh","id": 1,"image_link": "https://image.com", "location_link": "https://location.com","name": "Alnahdi pharmacy","phone": "0555546135"},{"city": "Riyadh","id": 2,"image_link": "https://image.com","location_link": "https://location.com","name": "edit test","phone": "0555546135"},{"city": "Riyadh","id": 3,"image_link": "https://image.com","location_link": "https://location.com","name": "Pharmacy 3","phone": "0555546135"}],"success": true}`|
/pharmacy/<id>/delete|DELETE|Deletes the selected pharmacy by specified id|`curl https://capstone-drugs-app.herokuapp.com/pharmacy/3/delete -X DELETE -H"Authorization: Bearer <Token>"`|`{"data": [{"city": "Riyadh","id": 1,"image_link": "https://image.com","location_link": "https://location.com","name": "Alnahdi pharmacy", "phone": "0555546135"},{"city": "Riyadh","id": 2,"image_link": "https://image.com","location_link": "https://location.com","name": "edit test","phone": "0555546135"}],"success": true}`|
/pharmacy/create|POST|Adds a new pharmacy to the database. Returns a new updated drugs list|`curl https://capstone-drugs-app.herokuapp.com/pharmacy/create -X POST -H"Authorization: Bearer <Token>" -H"Content-Type: application/json" -d'{"name":"test add","city":"Riyadh", "phone":"0555546135","location_link":"https://location.com","image_link":"https://image.com"}'`|`{"data": [{"city": "Riyadh", "id": 1,"image_link": "https://image.com", "location_link": "https://location.com", "name": "Alnahdi pharmacy","phone": "0555546135"},{"city": "Riyadh","id": 2, "image_link": "https://image.com", "location_link": "https://location.com", "name": "edit test", "phone": "0555546135"},{"city": "Riyadh","id": 4,"image_link": "https://image.com","location_link": "https://location.com", "name": "test add","phone": "0555546135"}],"success": true}`|
/drug/create|POST|Adds a new drug to the database. Returns a new updated drugs list.|`curl -X POST https://capstone-drugs-app.herokuapp.com/drug/create  -H"Authorization: Bearer <Token>" -H"Content-Type: application/json" -d '{"name": "add test","description": "drug description","side_effects":"Headache","price":"13","image_link":"https://image.com"}'`|`{"data": [{"description": "drug_description","id": 1,"image_link": "https://image.com","name": "Brofin","price": "13","side_effects": "Headache"},{"description": "drug_description","id": 2,"image_link": "https://image.com","name": "Panadol","price": "13","side_effects": "Headache"},{"description": "drug description","id": 3,"image_link": "https://image.com","name": "add test","price": "13","side_effects": "Headache"}],"success": true}`|


## Test tokens:

#### Admin

`eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhGeTNsSkVIa3dKWXNITEZ6am5CZCJ9.eyJpc3MiOiJodHRwczovL2Rldi1mYWlzYWwudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwOTI1ZDhiYzgxODY1MDA2YTYzZDZjNCIsImF1ZCI6ImRydWdzIiwiaWF0IjoxNjI0MjI1NzExLCJleHAiOjE2MjQzMTIxMTEsImF6cCI6IklTSURER2pPcHJ3NzJUdXpUY0xwOWJBQ3ZuYm83ZERYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJ1Z3MiLCJkZWxldGU6cGhhcm1hY2llcyIsImVkaXQ6cGhhcm1hY2llcyIsImdldDpkcnVncyIsImdldDpwaGFybWFjaWVzIiwicG9zdDpkcnVncyIsInBvc3Q6cGhhcm1hY2llcyJdfQ.M1jXYTvX1iIl4KBx6Aiyh72VCuZDC6RmXdAfNHPgdvzlDghqxMj6W0QA5AkKPAzj9H2py2_CT08HF_sLTbiplxYSbmRUp7bZSsK3HXZrORZMhsdUuKGqPjyXeIAsGc1IkjQ8OL0N_tXJVJpioJnUi1AISSMPdFa-5g2I11rBHWX0tmcj_7-0ixCEzg3JHaeUNQnkn8r1wLznfjL_mcmNu5Iiqg59A9ly356I5jGvYVxXvhz27dWxCP-2eAgwX8OCAtr_WdHVBcNF4YMlWYY23M4FfRjz2-lorfGcu6h6En7DzFjXogwxpCfIUg9i22CemBsedC8JtQQ9dZaPo8inBQ`

#### Visitor

`eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InhGeTNsSkVIa3dKWXNITEZ6am5CZCJ9.eyJpc3MiOiJodHRwczovL2Rldi1mYWlzYWwudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwOGM1NjAwY2QwMzFjMDA2OTRjNjM1MCIsImF1ZCI6ImRydWdzIiwiaWF0IjoxNjI0MjI1Nzg5LCJleHAiOjE2MjQzMTIxODksImF6cCI6IklTSURER2pPcHJ3NzJUdXpUY0xwOWJBQ3ZuYm83ZERYIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6ZHJ1Z3MiLCJnZXQ6cGhhcm1hY2llcyJdfQ.rctF4yTosIc93qza6UIzYINBf5ufpYf0ee9FFkx4Wyjc8ClMklb1SL31PGfPPWF-AWlhs-PNFI4ZotrYlOo7MNGcZrj6PNNZCEhSr0ElX5Ie4EJVvrw4DWAbAawmWfUchDcNYL-XXWsDZTh8Yi82Yj3xIFEvom7qQdQlpj7DMIhf5LP9O3gE_qskoJy3FLzu3MF-91NWYEGYEFOxEMJOyzm1UG4FD516x-cUfivfXH-anqcIlWoNyYAb1CnE2oXMcOwl_n2OryTsi5UP5fdskldYPcBEnur-y94oTmBJKQYhI5koauAdnMzS3bxu45l2rhVU3zNgadPghcwEkysi2w`



## Permissions

Permissions|Details
---|---
get:drugs|Can retieve all drugs
get:pharmacies|Can retieve all pharmacies
post:drugs|Can add drugs to the DB
post:pharmacies|Can add pharmacies to the DB
delete:pharmacies|Can delete pharmacy from the DB
edit:pharmacies|Can modify pharmacy from the DB

## Roles

Role|Permissions
---|---
Admin| get:drugs get:pharmacies post:drugs post:pharmacies delete:pharmacies edit:pharmacies
Visitor| get:drugs get:pharmacies 
