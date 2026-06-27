"""
API LEARNING FILE

This file covers:

1. API basics
2. REST API explanation
3. requests library    = call APIs
4. FastAPI             = build APIs
5. BaseModel           = define JSON body structure
6. Path   parameters
7. Query  parameters
8. Status codes
9. Error handling
10. One Product API example
11. One Book API example
12. requests examples to test APIs

Run this file:

pip install fastapi uvicorn requests

uvicorn main:app --reload

Open:

http://127.0.0.1:8000/docs
"""

# ============================================================
# API BASICS
# ============================================================

"""
API:
    Rules that let software communicate.

Endpoint:
    URL/path where API is available.
    Example:
        /products/1
        /books/2

Request:
    Message sent to an API.

Response:
    Message returned by an API.

JSON:
    Common API data format.
    Example:
        {"name": "Book", "price": 10.5}

HTTP METHODS:
    GET     = read data
    POST    = create/send data
    PATCH   = update part of data
    DELETE  = remove data

STATUS CODES:
    200 = success
    201 = created
    204 = success, no body
    
    400 = bad request
    401 = not authenticated
    403 = no permission
    404 = not found
    422 = validation error
    429 = too many requests
    
    500 = server error
"""

# ============================================================
# REST API EXPLANATION
# ============================================================

"""
REST API:

REST API is not a new library.
REST API is a style/design for building APIs.

API:
    General idea: software talks to software.

REST API:
    A common API style that uses:

    1. URLs for resources/things
    2. HTTP methods for actions
    3. JSON for sending/receiving data
    4. Status codes for results

Resource:
    A thing/data in your app.

Examples of resources:
    products
    books
    users
    orders

In REST, each resource usually has a URL.

Examples:

    /products
    /products/1
    /books
    /books/2

HTTP method decides the action:

    GET /products
        Read all products.

    GET /products/1
        Read one product.

    POST /products
        Create a new product.

    PATCH /products/1
        Update part of product 1.

    DELETE /products/1
        Delete product 1.

So this:

    @app.get("/books/{book_id}")

is a REST-style endpoint because:

    /books/{book_id}
        is the resource URL.

    GET
        is the action: read data.

Important idea:

    REST API = API that follows this URL + HTTP method style.

"""

# ============================================================
# REQUESTS GENERAL STRUCTURE
# ============================================================

"""
requests is a Python library used to CALL APIs.

General structure:

import requests

response = requests.get   (url,  params=params, headers=headers, timeout=10)
response = requests.post  (url,  json=data,     headers=headers, timeout=10)
response = requests.patch (url,  json=data,     headers=headers, timeout=10)
response = requests.delete(url,                 headers=headers, timeout=10)

params:
    Query/filter options for GET requests.

json:
    Data sent in the request body for POST/PATCH.

headers:
    Extra request information, like API token.

timeout:
    Maximum waiting time.
"""

import requests


def call_external_api_example():
    """
    Example of calling someone else's API.
    This is CLIENT SIDE code.
    """

    url = "https://jsonplaceholder.typicode.com/posts"

    params = {
        "userId": 1
    }

    response = requests.get(url, params=params, timeout=10)

    print(response.status_code)

    data = response.json()
    print(data)


# ============================================================
# FASTAPI IMPORTS
# ============================================================

# FastAPI:
#     Creates the API app.
#
# HTTPException:
#     Lets us return errors like 404.
#
# status:
#     Gives readable status code names like HTTP_201_CREATED.
from fastapi import FastAPI, HTTPException, status

# BaseModel:
#     Lets us define the required shape of JSON request bodies.
#
# Example:
#     class Product(BaseModel):
#         name: str
#         price: float
from pydantic import BaseModel

# Optional:
#     Means a field is allowed to be missing.
#
# Used for PATCH because PATCH updates only part of data.
from typing import Optional


# ============================================================
# FASTAPI GENERAL STRUCTURE
# ============================================================

"""
FastAPI is a Python library used to BUILD APIs.

General structure:

app = FastAPI()

@app.METHOD("PATH")
def function_name(parameters):
    return JSON

Meaning:

app = FastAPI()
    Create the API app.

@app.get("/path")
    Create a GET endpoint.

def function_name():
    Function that runs when the endpoint is called.

return {...}
    JSON response sent back to the client.
"""

# Create the FastAPI app.
app = FastAPI()


# ============================================================
# PYDANTIC MODELS / REQUEST BODY STRUCTURE
# ============================================================

"""
BaseModel explanation:

class Product(BaseModel):
    name: str
    price: float

This means Product is a JSON body template.

The client must send JSON like:

{
    "name": "Book",
    "price": 10.5
}

Fields:

name: str
    Required field.
    Must be text.

price: float
    Required field.
    Must be a number.

If the client sends wrong data, FastAPI returns 422 validation error.
"""


class Product(BaseModel):
    name: str
    price: float


"""
ProductUpdate is for PATCH.

PATCH means update only part of existing data.

So fields are Optional.

Valid JSON examples:

{
    "name": "New Book"
}

{
    "price": 15.0
}

{
    "name": "New Book",
    "price": 15.0
}
"""


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None


# ============================================================
# FAKE DATABASES
# ============================================================

"""
These are fake databases.

In real projects, you use a real database like PostgreSQL.
Here we use dictionaries to keep it simple.
"""

products = {}
next_id = 1

books = {
    1: {"title":  "Python Basics",   "author": "Ali",    "year": 2020},
    2: {"title":  "FastAPI Guide",   "author": "Hari",   "year": 2023},
    3: {"title":    "API Mastery",   "author": "John",   "year": 2024},
}


# ============================================================
# HOME ENDPOINT
# ============================================================

# GET /
# This is the home endpoint.
@app.get("/")
def home():
    return {"message": "Welcome to API Learning File by Hari!"}


# ============================================================
# PRODUCT API EXAMPLE
# ============================================================

# POST /products
#
# Create a new product.
#
# product: Product
#     The client must send JSON matching the Product model.
#
# status_code=201
#     Means created successfully.
@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    global next_id

    products[next_id] = product

    result = {
        "id": next_id,
        "name": product.name,
        "price": product.price
    }

    next_id += 1

    return result


# GET /products
#
# Read all products.
#
# limit: int = 10
#     Query parameter.
#
# Example:
#     /products?limit=5
@app.get("/products")
def list_products(limit: int = 10):
    result = []

    for product_id, product in list(products.items())[:limit]:
        result.append({
            "id": product_id,
            "name": product.name,
            "price": product.price
        })

    return {
        "limit": limit,
        "products": result
    }


# GET /products/{product_id}
#
# Read one product by ID.
#
# product_id: int
#     Path parameter.
#
# Example:
#     /products/1
@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product = products[product_id]

    return {
        "id": product_id,
        "name": product.name,
        "price": product.price
    }


# PATCH /products/{product_id}
#
# Update part of a product.
#
# product_update: ProductUpdate
#     Client can send name, price, or both.
@app.patch("/products/{product_id}")
def update_product(product_id: int, product_update: ProductUpdate):
    if product_id not in products:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    old_product = products[product_id]

    new_name = product_update.name if product_update.name is not None else old_product.name
    new_price = product_update.price if product_update.price is not None else old_product.price

    updated_product = Product(
        name=new_name,
        price=new_price
    )

    products[product_id] = updated_product

    return {
        "id": product_id,
        "name": updated_product.name,
        "price": updated_product.price
    }


# DELETE /products/{product_id}
#
# Delete one product by ID.
#
# status_code=204
#     Success, but no response body.
@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    if product_id not in products:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    del products[product_id]

    return None


# ============================================================
# BOOK API EXAMPLE
# ============================================================

# GET /books/{book_id}
#
# This example shows both:
#
# 1. Path parameter:
#       book_id
#
# 2. Query parameter:
#       show_author
#
# Example URLs:
#
#     /books/1
#     /books/1?show_author=false
#     /books/2?show_author=true
#
# book_id: int
#     Comes from the URL path.
#     Example:
#         /books/1
#
# show_author: bool = True
#     Comes from the query string.
#     Example:
#         ?show_author=false
#
# If show_author is true:
#     Return title, author, and year.
#
# If show_author is false:
#     Return only title and year.
@app.get("/books/{book_id}")
def get_book(book_id: int, show_author: bool = True):
    book = books.get(book_id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    if show_author == False:
        return {
            "title": book["title"],
            "year": book["year"]
        }

    return book


# ============================================================
# BOOK URL EXAMPLES AND OUTPUTS
# ============================================================

"""
Try these in your browser after running:

uvicorn main:app --reload


URL 1:

http://127.0.0.1:8000/books/1

Output:

{
    "title": "Python Basics",
    "author": "Ali",
    "year": 2020
}


URL 2:

http://127.0.0.1:8000/books/2

Output:

{
    "title": "FastAPI Guide",
    "author": "Sara",
    "year": 2023
}


URL 3:

http://127.0.0.1:8000/books/1?show_author=false

Output:

{
    "title": "Python Basics",
    "year": 2020
}


URL 4:

http://127.0.0.1:8000/books/3?show_author=true

Output:

{
    "title": "API Mastery",
    "author": "John",
    "year": 2024
}


URL 5:

http://127.0.0.1:8000/books/99

Output:

{
    "detail": "Book not found"
}


Key idea:

/books/1
    1 is a path parameter.

?show_author=false
    show_author is a query parameter.
"""


# ============================================================
# HOW TO RUN THIS API
# ============================================================

"""
Save this file as:

main.py

Install libraries:

pip install fastapi uvicorn requests

Run server:

uvicorn main:app --reload

Open API:

http://127.0.0.1:8000

Open automatic docs:

http://127.0.0.1:8000/docs
"""


# ============================================================
# CLIENT EXAMPLES USING REQUESTS
# ============================================================

"""
These examples show how a client calls your FastAPI API.

Use them in another file, for example:

client.py

Run them only after your FastAPI server is running.
"""


def test_my_fastapi_api():
    base_url = "http://127.0.0.1:8000"

    # GET /
    response = requests.get(base_url + "/", timeout=10)
    print(response.status_code)
    print(response.json())

    # POST /products
    data = {
        "name": "Book",
        "price": 10.5
    }

    response = requests.post(
        base_url + "/products",
        json=data,
        timeout=10
    )

    print(response.status_code)
    print(response.json())

    # GET /products/1
    response = requests.get(
        base_url + "/products/1",
        timeout=10
    )

    print(response.status_code)
    print(response.json())

    # GET /products?limit=5
    params = {
        "limit": 5
    }

    response = requests.get(
        base_url + "/products",
        params=params,
        timeout=10
    )

    print(response.status_code)
    print(response.json())

    # PATCH /products/1
    data = {
        "price": 15.0
    }

    response = requests.patch(
        base_url + "/products/1",
        json=data,
        timeout=10
    )

    print(response.status_code)
    print(response.json())

    # DELETE /products/1
    response = requests.delete(
        base_url + "/products/1",
        timeout=10
    )

    print(response.status_code)

    # GET /books/1
    response = requests.get(
        base_url + "/books/1",
        timeout=10
    )

    print(response.status_code)
    print(response.json())

    # GET /books/1?show_author=false
    params = {
        "show_author": False
    }

    response = requests.get(
        base_url + "/books/1",
        params=params,
        timeout=10
    )

    print(response.status_code)
    print(response.json())


"""
FINAL MEMORY STRUCTURE

CLIENT SIDE with requests:

response = requests.get    (url, params=params, headers=headers, timeout=10)
response = requests.post   (url, json=data,     headers=headers, timeout=10)
response = requests.patch  (url, json=data,     headers=headers, timeout=10)
response = requests.delete (url,                headers=headers, timeout=10)


SERVER SIDE with FastAPI:

@app.get("/path")
def function():
    return {"key": "value"}

@app.post("/path")
def function(data: Model):
    return data


PATH PARAMETER:

@app.get("/books/{book_id}")
def get_book(book_id: int):
    return ...


QUERY PARAMETER:

@app.get("/books/{book_id}")
def get_book(book_id: int, show_author: bool = True):
    return ...


REQUEST BODY:

class Product(BaseModel):
    name: str
    price: float

@app.post("/products")
def create_product(product: Product):
    return product


REST API:

REST API means building APIs using this style:

URL          = resource
HTTP method  = action
JSON         = data format
status code  = result

Examples:

GET /products
    Read all products.

GET /products/1
    Read product 1.

POST /products
    Create product.

PATCH /products/1
    Update product 1.

DELETE /products/1
    Delete product 1.


MOST IMPORTANT FASTAPI FORMULA:

@app.METHOD("PATH")
def function_name(parameters):
    return JSON
"""
