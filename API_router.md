# **Router**

---
### GET **/public** 
list all public APIs

**Sample Request**  
GET {ServerPath}/public

**Sample Success Response**
```
create_course
POST,OPTIONS
/public/course

create_instance
POST,OPTIONS
/public/instance/[instanceType]/[shard_number]

create_instance
POST,OPTIONS
/public/instance/[instanceType]

create_new_column_for_course_schema
POST,OPTIONS
/public/course/schema
...
```

**Possible Error Response**  
* 500 Unexpected internal error



---

### POST **/public/instance/[instanceType]/[shardNumber]**  
API for starting new microservice instance: 

 - student (need to specify shardNumber)
 - course
 - registration

**Sample Request 1**  
POST {ServerPath}/public/instance/course
###### *HTTP Body* 
empty

**Sample Request 2**  
POST {ServerPath}/public/instance/student/1
###### *HTTP Body* 
empty

**Sample Success Response**
```
200
```

**Possible Error Response**
* 500 Failed to connect to mongodb
* 500 Illegal shard number
* 500 Shard has already been started
* 500 reach the max of shards
* 500 Unexpected internal error

---

### DELETE **/public/instance/[iid]**  
API for stopping microservice instance: 

 - student
 - course
 - registration

**Sample Request**  
DELETE {ServerPath}/public/instance/6000
###### *HTTP Body* 
empty

**Sample Success Response**
```
200
```

**Possible Error Response**
* 500 Failed to connect to mongodb
* 500 Unexpected internal error