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
### GET **/student/\<uni\>**

Retrieve student by uni.

**Sample Request**

GET {ServerPath}/public/student/uni/ys2816

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

```json
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>
```



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
### PUR **/student/\<uni\>**

Update student info

**Sample Request**

PUT {ServerPath}/v1/users

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
### DELETE **/student/\<uni\>**

Delete student by uni.


**Sample Request**

DELETE {ServerPath}/student/<uni>

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




