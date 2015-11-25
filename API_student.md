**Student**
----------

### GET **/student**


List all students.


**Sample Request**

GET {ServerPath}/public/student

**Sample Success Response**

```json
{
    "_items": [
        {
            "_updated": "Sun, 15 Nov 2015 03:58:15 GMT",
            "major": "computer science",
            "firstname": "qiuyang",
            "lastname": "shen",
            "_links": {
                "self": {
                    "href": "student10/564802d774dc81c873f2a998",
                    "title": "Student10"
                }
            },
            "uni": "qs2147",
            "_created": "Sun, 15 Nov 2015 03:58:15 GMT",
            "_id": "564802d774dc81c873f2a998",
            "_etag": "05f74eb4c9bc7655ac3f771cff56fb46d2dab7d7"
        },
        {
            "_updated": "Sun, 15 Nov 2015 04:09:36 GMT",
            "major": "computer science",
            "firstname": "yun",
            "lastname": "sun",
            "_links": {
                "self": {
                    "href": "student10/5648058074dc81d0c23db232",
                    "title": "Student10"
                }
            },
            "uni": "ys2816",
            "_created": "Sun, 15 Nov 2015 04:09:36 GMT",
            "_id": "5648058074dc81d0c23db232",
            "_etag": "378a95fb2f6e12c88106ef069157394340fa3c60"
        }
    ],
    "_links": {
        "self": {
            "href": "student10",
            "title": "student10"
        },
        "parent": {
            "href": "/",
            "title": "home"
        }
    },
    "_meta": {
        "max_results": 25,
        "total": 2,
        "page": 1
    }
}
```

**Possible Error Response**  
* 404 Resource not found  
* 500 Failed to connect to mongodb
* 500 Failed to read configuration of student service from mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error

---
### GET **/student/\<uni\>**

Retrieve student by uni.

**Sample Request**

GET {ServerPath}/public/student/qs2147

**Sample Success Response**

```json
{
    "_updated": "Sun, 15 Nov 2015 03:58:15 GMT",
    "major": "computer science",
    "firstname": "qiuyang",
    "lastname": "shen",
    "_links": {
        "self": {
            "href": "student10/564802d774dc81c873f2a998",
            "title": "Student10"
        },
        "collection": {
            "href": "student10",
            "title": "student10"
        },
        "parent": {
            "href": "/",
            "title": "home"
        }
    },
    "uni": "qs2147",
    "_created": "Sun, 15 Nov 2015 03:58:15 GMT",
    "_id": "564802d774dc81c873f2a998",
    "_etag": "05f74eb4c9bc7655ac3f771cff56fb46d2dab7d7"
}
```

**Possible Error Response**  
* 500 Failed to connect to mongodb
* 500 Failed to read configuration of student service from mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error


---
### POST **/student**

Create new student.

**Sample Request**

POST {ServerPath}/public/student

*HTTP Body*
```json
{
    "firstname":"qiuyang", 
    "lastname":"shen", 
    "uni":"qs2147", 
    "major":"computer science"
}
```

**Sample Success Response**

*HTTP Body*
```json
{
    "status": 201
}
```

**Possible Error Response**  
* 404 Resource not found  
* 500 Failed to connect to mongodb
* 500 Failed to read configuration of student service from mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error


---
### PUT **/student/\<uni\>**

Update student info

**Sample Request**

PUT {ServerPath}/public/student/qs2147

*HTTP Body*
```json
{
    "firstname":"qiuyang", 
    "lastname":"shen", 
    "uni":"qs2147", 
    "major":"computer engineering"
}
```

**Sample Success Response**

```json
{
    "_updated": "Wed, 25 Nov 2015 05:34:06 GMT",
    "_links": {
        "self": {
            "href": "student10/564802d774dc81c873f2a998",
            "title": "Student10"
        }
    },
    "_created": "Sun, 15 Nov 2015 03:58:15 GMT",
    "_status": "OK",
    "_id": "564802d774dc81c873f2a998",
    "_etag": "4932aec28442feacbc83363d671857cb0a7cece0"
}
```

**Possible Error Response**
* 404 Resource not found
* 412 Client and server etags don't match
* 500 Failed to connect to mongodb
* 500 Failed to read configuration of student service from mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error
* 504 Failed to connect to registration service
* 502 Failed to delete related registration information

---
### DELETE **/student/\<uni\>**

Delete student by uni.


**Sample Request**

DELETE {ServerPath}/public/student/qs2147

**Sample Success Response**

```json
{
    "status": 200
}
```

**Possible Error Response**
* 404 Resource not found
* 412 Client and server etags don't match
* 500 Failed to connect to mongodb
* 500 Failed to read configuration of student service from mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error
* 504 Failed to connect to registration service
* 502 Failed to delete related registration information

---
### GET **/student/schema** 
View the schema of student service.

**Sample Request**  
GET {ServerPath}/public/student/schema

**Sample Success Response**
```json
{
    "firstname": {
        "empty": false,
        "type": "string"
    },
    "lastname": {
        "empty": false,
        "type": "string"
    },
    "major": {
        "type": "string"
    },
    "uni": {
        "empty": false,
        "type": "string",
        "unique": true
    }
}
```

**Possible Error Response**  
* 500 Failed to connect to mongodb
* 500 Failed to read configuration of student service from mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error



---
### POST **/student/schema**  
Add new columns/attributes to student schema. If a column/attribute in submitted data already exists in schema, it will be ignored and the rest will be added.

**Sample Request**  
POST {ServerPath}/public/student/schema
###### *HTTP Body* 
```json
{
    "test_attr1": {
        "type": "string"
    },
    "test_attr2": {
        "type": "integer"
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
* 500 Failed to read configuration of student service from mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error



---
### PUT **/student/schema**  
Update existing columns/attributes in student schema. If a column/attribute in submitted data does not already exist in schema, it will be ignored and the rest will be updated.

**Sample Request**  
POST {ServerPath}/public/student/schema
###### *HTTP Body* 
```json
{
    "test_attr1": {
        "type": "integer"
    },
    "test_attr3": {
        "type": "integer"
    }
}
```

**Sample Success Response**
```json
{
  "_status": "SUCCESS",
  "_success": {
    "message": "1 column(s) updated",
    "code": 200
  }
}
```

**Possible Error Response**
* 500 Failed to connect to mongodb
* 500 Failed to read configuration of student service from mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error



---
### DELETE **/student/schema**  
Delete student with specified uni.

**Sample Request**  
DELETE {ServerPath}/public/student/schema
###### *HTTP Body* 
```json
["test_attr1", "test_attr2", "test_attr3"]
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
* 500 Failed to read configuration of student service from mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error





