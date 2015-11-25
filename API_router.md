# **Router**

---
### GET **/[url]/_<[resource]_>** 
[explanation]

**Sample Request**  
GET {ServerPath}/public/[url]

**Sample Success Response**
```json
{
  [response]
}
```

**Possible Error Response**  
* 500 Failed to connect to mongodb
* 500 Failed to read configuration of course service from mongodb
* 500 Failed to connect to eve service
* 500 Unexpected internal error



---
### POST **/[url]**  
[explanation]

**Sample Request**  
POST {ServerPath}/public/[url]
###### *HTTP Body* 
```json
{
  [request body]
}
```

**Sample Success Response**
```json
{
  [response]
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
