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
* 500 Failed to connect to mongodb  
* 500 Failed to connect to eve service  
* 500 Unexpected internal error

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
* 404 Resource not found  
* 500 Failed to connect to mongodb  
* 500 Failed to connect to eve service  
* 500 Unexpected internal error  

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
* 404 Resource not found  
* 500 Failed to connect to mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error



---
### POST **/registration**

Create new registrations.

**Sample Request**

POST {ServerPath}/public/registraion

*HTTP Body*
```json
{
  "UNI": "ck5945",
  "Course_ID": "COMSW4444"
}
```

**Sample Success Response**
```json
{
    "_updated": "Wed, 25 Nov 2015 06:27:24 GMT",
    "_links": {
        "self": {
            "href": "registration/565554cc3f5c880c1ca9d506",
            "title": "Registration"
        }
    },
    "_created": "Wed, 25 Nov 2015 06:27:24 GMT",
    "_status": "OK",
    "_id": "565554cc3f5c880c1ca9d506",
    "_etag": "82e3596a187204874c5f1268d30a0bf5260eb1b1"
}
```

**Possible Error Response**
* 500 Failed to connect to mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error


---
### DELETE **/registration**

Delete all registration info.

**Sample Request**

DELETE {ServerPath}/public/registration

**Sample Success Response**
```json
{
    "_status": "SUCCESS",
    "_success": {
        "message": "delete succesfully",
        "code": 200
    }
}
```

**Possible Error Response**
* 500 Failed to connect to mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error


---
### DELETE **/registration/uni/\<uni\>**

Delete the registration info of the student with the correspoinding uni.

**Sample Request**

DELETE {ServerPath}/public/registration/uni/ck5945

**Sample Success Response**
```json
{
    "_status": "SUCCESS",
    "_success": {
        "message": "delete succesfully",
        "code": 200
    }
}
```

**Possible Error Response**
* 500 Failed to connect to mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error


---
### DELETE **/registration/courseid/\<cid\>**

Delete the registration info of the course with the correspoinding course id.

**Sample Request**

DELETE {ServerPath}/public/registration/courseid/COMSW4444

**Sample Success Response**
```json
{
    "_status": "SUCCESS",
    "_success": {
        "message": "delete succesfully",
        "code": 200
    }
}
```

**Possible Error Response**
* 500 Failed to connect to mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error

---
### DELETE **/registration/uni/\<uni\>/courseid/\<cid\>**

Delete the registration info of the student with the corresponding uni and the course with the corresponding course id.

**Sample Request**

DELETE {ServerPath}/public/registration/uni/ck5945/courseid/COMSW4444

**Sample Success Response**
```json
{
    "_status": "SUCCESS",
    "_success": {
        "message": "delete succesfully",
        "code": 200
    }
}
```

**Possible Error Response**
* 500 Failed to connect to mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error


---
### PUT **/registration/uni/\<uni\>/courseid/\<cid\>**

Update the registration info of the student with the corresponding uni and the course with the corresponding course id.

**Sample Request**

PUT {ServerPath}/public/registration/uni/ys2816/courseid/COMSW4771

**Sample Success Response**
```json
{
    "_updated": "Wed, 25 Nov 2015 06:51:59 GMT",
    "_links": {
        "self": {
            "href": "registration/5623622b3f5c880baff62d03",
            "title": "Registration"
        }
    },
    "_created": "Sun, 18 Oct 2015 09:11:07 GMT",
    "_status": "OK",
    "_id": "5623622b3f5c880baff62d03",
    "_etag": "6c7aac19e416e4e1c9e92e23bada26a5d8da8d07"
}
```

**Possible Error Response**
* 404 Not Found
* 500 Failed to connect to mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error


@app.route("/private/registration/schema", methods = ['PUT'])
@app.route("/private/registration/schema", methods = ['DELETE'])

---
### GET **/registration/schema**

View the schema of registration service.

**Sample Request**

GET {ServerPath}/public/registration/schema

**Sample Success Response**
```json
{
    "Course_ID": {
        "type": "string"
    },
    "Lecturer": {
        "type": "dict"
    },
    "UNI": {
        "type": "string"
    }
}
```

**Possible Error Response**
* 500 Failed to connect to mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error

---
### POST **/registration/schema**  
Add new columns/attributes to registration schema. If a column/attribute in submitted data already exists in schema, it will be ignored and the rest will be added.

**Sample Request**  
POST {ServerPath}/public/registration/schema
###### *HTTP Body* 
```json
{
    "Grade": {
        "type": "string"
    },
    "Title": {
        "type": "string"
    }
}
```

**Sample Success Response**
```json
{
    "_status": "SUCCESS",
    "_success": {
        "message": "2 column(s) added",
        "code": 200
    }
}
```

**Possible Error Response**
* 500 Failed to connect to mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error

---
### PUT **/registration/schema**  
Update existing columns/attributes in registration schema. If a column/attribute in submitted data does not already exist in schema, it will be ignored and the rest will be updated.

**Sample Request**  
PUT {ServerPath}/public/registration/schema
###### *HTTP Body* 
```json
{
  "Grade": {
  "type": "Interger"
  },
  "Title": {
  "type": "Integer"
  }
}
```

**Sample Success Response**
```json
{
    "_status": "SUCCESS",
    "_success": {
        "message": "2 column(s) updated",
        "code": 200
    }
}
```

**Possible Error Response**
* 500 Failed to connect to mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error


---
### DELETE **/registration/schema**   
Delete existing columns/attributes in registration schema. If a column/attribute in submitted data does not already exist in schema, it will be ignored and the rest will be deleted.

**Sample Request**  
DELETE {ServerPath}/public/registration/schema
###### *HTTP Body* 
```json
["Grade", "Lecturer"]
```

**Sample Success Response**
```json
{
    "_status": "SUCCESS",
    "_success": {
        "message": "2 column(s) deleted",
        "code": 200
    }
}
```

**Possible Error Response**
* 500 Failed to connect to mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error
