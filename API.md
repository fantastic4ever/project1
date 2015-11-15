**Registration**
----------

### GET **/registration**


List all registrations.


**Sample Request**

GET {ServerPath}/public/registration

**Sample Success Response**

```json
{
    "_items": [
        {
            "_updated": "Sun, 18 Oct 2015 09:11:07 GMT",
            "_links": {
                "self": {
                    "href": "registration/5623622b3f5c880baff62d03",
                    "title": "Registration"
                }
            },
            "UNI": "ys2816",
            "Course_ID": "COMSW4771",
            "_created": "Sun, 18 Oct 2015 09:11:07 GMT",
            "_id": "5623622b3f5c880baff62d03",
            "_etag": "54534ad0f7ab994d19880c23106bef15ecd0af2f"
        },
        {
            "_updated": "Fri, 13 Nov 2015 21:05:42 GMT",
            "_links": {
                "self": {
                    "href": "registration/564650a63fc0e7317c0e2d42",
                    "title": "Registration"
                }
            },
            "UNI": "ys2816",
            "Course_ID": "12345",
            "_created": "Fri, 13 Nov 2015 21:05:42 GMT",
            "_id": "564650a63fc0e7317c0e2d42",
            "_etag": "39bccb3d5da1f7e9b4c844b6568297ab92304dc8"
        },
        {
            "_updated": "Fri, 13 Nov 2015 22:14:30 GMT",
            "_links": {
                "self": {
                    "href": "registration/564660c63fc0e72d147280c0",
                    "title": "Registration"
                }
            },
            "UNI": "ys2816",
            "Course_ID": "12345",
            "_created": "Fri, 13 Nov 2015 22:14:30 GMT",
            "_id": "564660c63fc0e72d147280c0",
            "_etag": "e1e138f458fb4960f22c5291132ddb32a0e056c6"
        }
    ],
    "_links": {
        "self": {
            "href": "registration",
            "title": "registration"
        },
        "parent": {
            "href": "/",
            "title": "home"
        }
    },
    "_meta": {
        "max_results": 25,
        "total": 3,
        "page": 1
    }
}
```

**Possible Error Response**


---
### GET **/registraion/courseid/\<cid\>**

Retrieve registrations by course id.

**Sample Request**

GET {ServerPath}/public/registraion/cid/COMSW4771

**Sample Success Response**

```json
{
    "_items": [
        {
            "_updated": "Sun, 18 Oct 2015 09:11:07 GMT",
            "_links": {
                "self": {
                    "href": "registration/5623622b3f5c880baff62d03",
                    "title": "Registration"
                }
            },
            "UNI": "ys2816",
            "Course_ID": "COMSW4771",
            "_created": "Sun, 18 Oct 2015 09:11:07 GMT",
            "_id": "5623622b3f5c880baff62d03",
            "_etag": "54534ad0f7ab994d19880c23106bef15ecd0af2f"
        }
    ],
    "_links": {
        "self": {
            "href": "registration?where=Course_ID==COMSW4771",
            "title": "registration"
        },
        "parent": {
            "href": "/",
            "title": "home"
        }
    },
    "_meta": {
        "max_results": 25,
        "total": 1,
        "page": 1
    }
}
```

**Possible Error Response**

```json
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>
```

---
### GET **/registraion/uni/\<uni\>**

Retrieve registrations by uni.

**Sample Request**

GET {ServerPath}/public/registraion/uni/ys2816

**Sample Success Response**

```json
{
    "_items": [
        {
            "_updated": "Sun, 18 Oct 2015 09:11:07 GMT",
            "_links": {
                "self": {
                    "href": "registration/5623622b3f5c880baff62d03",
                    "title": "Registration"
                }
            },
            "UNI": "ys2816",
            "Course_ID": "COMSW4771",
            "_created": "Sun, 18 Oct 2015 09:11:07 GMT",
            "_id": "5623622b3f5c880baff62d03",
            "_etag": "54534ad0f7ab994d19880c23106bef15ecd0af2f"
        },
        {
            "_updated": "Fri, 13 Nov 2015 21:05:42 GMT",
            "_links": {
                "self": {
                    "href": "registration/564650a63fc0e7317c0e2d42",
                    "title": "Registration"
                }
            },
            "UNI": "ys2816",
            "Course_ID": "12345",
            "_created": "Fri, 13 Nov 2015 21:05:42 GMT",
            "_id": "564650a63fc0e7317c0e2d42",
            "_etag": "39bccb3d5da1f7e9b4c844b6568297ab92304dc8"
        },
        {
            "_updated": "Fri, 13 Nov 2015 22:14:30 GMT",
            "_links": {
                "self": {
                    "href": "registration/564660c63fc0e72d147280c0",
                    "title": "Registration"
                }
            },
            "UNI": "ys2816",
            "Course_ID": "12345",
            "_created": "Fri, 13 Nov 2015 22:14:30 GMT",
            "_id": "564660c63fc0e72d147280c0",
            "_etag": "e1e138f458fb4960f22c5291132ddb32a0e056c6"
        }
    ],
    "_links": {
        "self": {
            "href": "registration?where=UNI==ys2816",
            "title": "registration"
        },
        "parent": {
            "href": "/",
            "title": "home"
        }
    },
    "_meta": {
        "max_results": 25,
        "total": 3,
        "page": 1
    }
}
```

**Possible Error Response**

```json
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>
```



---
### POST **/registration**

Create new registrations.

**Sample Request**

POST {ServerPath}/public/registraion

*HTTP Body*
```json
{
	"username": "RahXephone",
	"password": "dolem",
	"name": {
		"first": "Olin",
		"last": "Staccato"
	},
	"gender": 2,
	"contactInfo": {
		"email": "os@gmail.com"
	}
}
```

**Sample Success Response**

*HTTP Header*
```
Location:{ServerPath}/v1/users/9999
```
*HTTP Body*
```json
{
	"status": 201
}
```

**Possible Error Response**

```json
{
	"status": 400,
    "data": "Invalid request: Bad data."
}
```
```json
{
	"status": 500,
	"data": "Internal server error."
}
```



---
### PUT **/v1/users**

Update user info in batch with complete info.


**Request Body**

| Attribute | Validate   | Type   | Value | Default | Note |
|:---------:|:------:|:--------:|:-----:|:-----:|:-----:|
|userId	|required	|string	|	|	|Rule to be designed.  |
|password	|required	|string	|	|	|Rule to be designed.  |
|name	|required	|JSONObject	|	|	|	|
|name.first	|required	|string	|	|	|   |
|name.middle	|required	|string	|	|	|  |
|name.last	|required	|string	|	|	|   |
|gender	|required	|int	|0/1/2	|	|Filter users by gender. Value 0 for unspecified; 1 for male; 2 for female.|
|contact	|required	|JSONObject	|	|	|  |
|contact.email	|required	|string	|	|	|  |
|contact.phone	|required	|string	|	|	|  |

**Sample Request**

PUT {ServerPath}/v1/users

*HTTP Body*
```json
{
	"userId": "9999",
	"password": "dolem",
	"name": {
		"first": "Olin",
		"last": "Staccato"
	},
	"gender": 2,
	"contactInfo": {
		"email": "os@gmail.com",
		"phone": "",
	}
}
```

**Sample Success Response**

```json
{
	"status": 200
}
```

**Possible Error Response**

```json
{
	"status": 400,
	"data": "Invalid request: Bad data."
}
```
```json
{
	"status": 500,
	"data": "Internal server error."
}
```


---
### DELETE **/v1/users**

Delete all users.


**Sample Request**

DELETE {ServerPath}/v1/users

**Sample Success Response**

```json
{
	"status": 200
}
```

**Error Response**

```json
{
	"status": 500,
	"data": "Internal server error."
}
```


---
### POST **/v1/users/:id**

Invalid request. <br>
* If adding new users, see "POST /v1/users".


**Error Response**
```json
{
	"status": 400,
	"data": "Invalid request: Method not allowed."
}
```



---
### PUT **/v1/users/:id**

Update a user given id with complete info. Same effect as PUT /v1/users with id in request body.


**Request Body**

| Attribute | Validate   | Type   | Value | Default | Note |
|:---------:|:------:|:--------:|:-----:|:-----:|:-----:|
|password	|required	|string	|	|	|Rule to be designed.  |
|name	|required	|JSONObject	|	|	|	|
|name.first	|required	|string	|	|	|  |
|name.middle	|required	|string	|	|	|  |
|name.last	|required	|string	|	|	|  |
|gender	|required	|int	|0/1/2	|	|Filter users by gender. Value 0 for unspecified; 1 for male; 2 for female.|
|contact	|required	|JSONObject	|	|	|	|
|contact.email	|required	|string	|	|	|  |
|contact.phone	|required	|string	|	|	|  |

**Sample Request**

PUT {ServerPath}/v1/users/9999

*HTTP Body*
```json
{
	"password": "dolemmelod",
	"name": {
		"first": "Olin",
		"middle": "",
		"last": "Spaghetti"
	},
	"gender": 1,
	"contactInfo": {
		"email": "os@gmail.com",
		"phone": "",
	}
}
```

**Sample Success Response**

```json
{
	"status": 200
}
```

**Possible Error Response**

```json
{
	"status": 400,
	"data": "Error Message"
}
```
```json
{
	"status": 500,
	"data": "Error Message"
}
```



---
### PATCH **/v1/users/:id**

Update a user given id with partial info. Same effect as PATCH /v1/users with id in request body.


**Request Body**

| Attribute | Validate   | Type   | Value | Default | Note |
|:---------:|:------:|:--------:|:-----:|:-----:|:-----:|
|password	|optional	|string	|	|	|Rule to be designed.  |
|name	|optional	|JSONObject	|	|	|	|
|name.first	|optional	|string	|	|	|  |
|name.middle	|optional	|string	|	|	|  |
|name.last	|optional	|string	|	|	|  |
|gender	|optional	|int	|0/1/2	|	|Filter users by gender. Value 0 for unspecified; 1 for male; 2 for female.|
|contact	|optional	|JSONObject	|	|	|	|
|contact.email	|optional	|string	|	|	|  |
|contact.phone	|optional	|string	|	|	|  |

**Sample Request**

PATCH {ServerPath}/v1/users/9999

*HTTP Body*
```json
{
	"password": "dolemmelod",
	"name": {
		"last": "Spaghetti"
	}
}
```

**Sample Success Response**

```json
{
	"status": 201
}
```

**Possible Error Response**

```json
{
	"status": 400,
	"data": "Error Message"
}
```
```json
{
	"status": 500,
	"data": "Error Message"
}
```



---
### DELETE **/v1/users/:id**

Delete a user given id.


**Sample Request**

DELETE {ServerPath}/v1/users/3999

**Sample Success Response**

```json
{
	"status": 200
}
```

**Error Response**

```json
{
	"status": 500,
	"data": "Internal server error."
}
```

