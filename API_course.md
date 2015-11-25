# **Course**

---
### GET **/course** 
List all courses.

**Sample Request**  
GET {ServerPath}/public/registration

**Sample Success Response**
```json
{
  "_items": [
    {
      "_updated": "Sun, 18 Oct 2015 22:47:12 GMT",
      "call_number": "54321",
      "title": "Test Course",
      "_links": {
        "self": {
          "href": "course/54321",
          "title": "Course"
        }
      },
      "_created": "Sun, 18 Oct 2015 22:47:12 GMT",
      "_id": "562421703fc0e70b78ab62a0",
      "_etag": "de50409ca0a5f732078e9e6659e63538fa2dafb9"
    },
    {
      "_updated": "Tue, 17 Nov 2015 00:19:21 GMT",
      "call_number": "12345",
      "title": "Test Course 1",
      "_links": {
        "self": {
          "href": "course/12345",
          "title": "Course"
        }
      },
      "_created": "Tue, 17 Nov 2015 00:19:21 GMT",
      "_id": "564a72893fc0e71410b15fe5",
      "_etag": "8dc86c88fcaa416b40771c9e729eacf08d091166"
    }
  ],
  "_links": {
    "self": {
      "href": "course",
      "title": "course"
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
* 500 Failed to connect to mongodb
* 500 Failed to read configuration of course service from mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error



---
### GET **/course/<call_number>  
Retrieve a specific course by its call_name, where call_name should be exactly five digits.

**Sample Request**  
GET {ServerPath}/public/course/12345

**Sample Success Response**
```json
{
  "_updated": "Tue, 17 Nov 2015 00:19:21 GMT",
  "call_number": "12345",
  "title": "Test Course 1",
  "_links": {
    "self": {
      "href": "course/12345",
      "title": "Course"
    },
    "collection": {
      "href": "course",
      "title": "course"
    },
    "parent": {
      "href": "/",
      "title": "home"
    }
  },
  "_created": "Tue, 17 Nov 2015 00:19:21 GMT",
  "_id": "564a72893fc0e71410b15fe5",
  "_etag": "8dc86c88fcaa416b40771c9e729eacf08d091166"
}
```

**Possible Error Response**  
* 404 Resource not found  
* 500 Failed to connect to mongodb
* 500 Failed to read configuration of course service from mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error



---
### POST **/course**  
Create new courses.

**Sample Request**  
POST {ServerPath}/public/course
###### *HTTP Body* 
```json
[
    {
        "call_number": "22345",
        "title": "Test Course 2"
    },
    {
        "call_number": "32345",
        "title": "Test Course 3"
    }
]
```

**Sample Success Response**
```json
{
  "_status": "OK",
  "_items": [
    {
      "_updated": "Tue, 17 Nov 2015 17:31:18 GMT",
      "call_number": "22345",
      "_links": {
        "self": {
          "href": "course/22345",
          "title": "Course"
        }
      },
      "_created": "Tue, 17 Nov 2015 17:31:18 GMT",
      "_status": "OK",
      "_etag": "9e6b4ca71d4eee3de16e8690b78c5f1d46e98fab"
    },
    {
      "_updated": "Tue, 17 Nov 2015 17:31:18 GMT",
      "call_number": "32345",
      "_links": {
        "self": {
          "href": "course/32345",
          "title": "Course"
        }
      },
      "_created": "Tue, 17 Nov 2015 17:31:18 GMT",
      "_status": "OK",
      "_etag": "f8db2941176639eac9cb85167a2257e54de803db"
    }
  ]
}
```

**Possible Error Response**
* 422 call_number not unique
* 422 invalid call_number format
* 500 Failed to connect to mongodb
* 500 Failed to read configuration of course service from mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error



---
### DELETE **/course/<call_number>**  
Delete course with specified call_number.

**Sample Request**  
DELETE {ServerPath}/public/course/22345
###### *HTTP Head* 
```
If-Match = 9e6b4ca71d4eee3de16e8690b78c5f1d46e98fab
```

**Sample Success Response**
```json
Status 204 NO CONTENT
No response received
```

**Possible Error Response**
* 404 Resource not found
* 412 Client and server etags don't match
* 500 Failed to connect to mongodb
* 500 Failed to read configuration of course service from mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error
* 504 Failed to connect to registration service
* 502 Failed to delete related registration information



---
### GET **/course/schema** 
View the schema of course service.

**Sample Request**  
GET {ServerPath}/public/course/schema

**Sample Success Response**
```json
{
  "day_time": {
    "type": "string"
  },
  "call_number": {
    "unique": true,
    "type": "string",
    "required": true
  },
  "enrollment_current": {
    "type": "integer"
  },
  "title": {
    "type": "string"
  },
  "section_number": {
    "type": "string"
  },
  "enrollment_cap": {
    "type": "integer"
  },
  "credit": {
    "type": "integer"
  },
  "semester": {
    "type": "string"
  },
  "texbook": {
    "type": "string"
  },
  "course_number": {
    "type": "string"
  },
  "location": {
    "type": "string"
  },
  "department": {
    "type": "string"
  },
  "instructor": {
    "type": "string"
  },
  "subject": {
    "type": "string"
  }
}
```

**Possible Error Response**  
* 500 Failed to connect to mongodb
* 500 Failed to read configuration of course service from mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error



---
### POST **/course/schema**  
Add new columns/attributes to course schema. If a column/attribute in submitted data already exists in schema, it will be ignored and the rest will be added.

**Sample Request**  
POST {ServerPath}/public/course/schema
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
* 500 Failed to read configuration of course service from mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error



---
### PUT **/course/schema**  
Update existing columns/attributes in course schema. If a column/attribute in submitted data does not already exist in schema, it will be ignored and the rest will be updated.

**Sample Request**  
POST {ServerPath}/public/course/schema
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
* 500 Failed to read configuration of course service from mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error



---
### DELETE **/course/schema**  
Delete course with specified call_number.

**Sample Request**  
DELETE {ServerPath}/public/course/schema
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
* 500 Failed to read configuration of course service from mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error
