# API Documentation Version 1.0
# All routes in this version of the api have the prefix: '/api/v1.0/'

## Get All Users
#### URL
    /users/
#### METHOD
    GET
#### URL Params
#### Data Params
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    users : [
    {
        uri : [string],
        id : [integer],
        name : [string],
        email : [string],
        role : [string],
        confirmed : [boolean],
        lattes : [string],
    },
    ]
}
```
#### Error Response
##### If the user does not send the authorization token

Status Code: 401

##### If the user does send the authorization token but do not have administer permissions

Status Code: 403
Content:
{
    error : forbidden,
    message : 'Insufficient permissions'
}
#### Sample Call
#### Notes
The user must be logged in and be a administrator

## Get User By Id
#### URL
    /users/<int:id>
#### METHOD
    GET
#### URL Params
    [integer] id
#### Data Params
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    {
        uri : [string],
        id : [integer],
        name : [string],
        email : [string],
        role : [string],
        confirmed : [boolean],
        lattes : [string]
    }
}
```
#### Error Response
##### If the requested id doesn't match any user in the database
Status Code: 404

Content:
```
{
    "error": "Not Found",
    "message": "Resource Not Found"
}
```

#### Sample Call
#### Notes

## Create User
#### URL
    /users/
#### METHOD
    POST
#### URL Params
#### Data Params
```
{
    name : [string],     (Minimum length 3)
    email : [string],
    password : [string], (Minimum length 8)
    lattes : [string],   (Optional)
}
```
#### Success Response
##### Header
Status Code: 201
Location: /users/id/ -- id of the created user

Content:
```
{
    uri : [string],
    id : [integer],
    name : [string],
    email : [string],
    role : [string],
    confirmed : [boolean],
    lattes : [string]
}
```
#### Error Response
##### If there are missing parameters(or parameters with invalid input) in the json payload.

Status Code: 400

Content:
```
{
    error : bad request,
    message : Invalid parameters
}
```

##### If the email is already registered in another account

Status Code: 400
Content:
```
{
    error : bad request,
    message : User already registered.
}
```
##### If the email is not institutional

Status Code: 400
Content:
```
{
    error : bad request,
    message : Email address is not institutional
}
```

#### Sample Call
#### Notes

## Update User
#### URL
    /users/<int:id>
#### METHOD
    PUT
#### URL Params
    [integer] id
#### Data Params
##### Note: All parameters (key-value pair) are optional.
```
{
    name : [string],      (Minimum length 3)
    password : [string],  (Minimum length 8)
    lattes : [string],
    confirm : [integer],
    role_id : [integer],  (Only Admin Users)
    confirmed : [integer] (Only Admin Users)
}
```
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    uri : [string],
    id : [integer],
    name : [string],
    email : [string],
    role : [string],
    confirmed : [boolean],
    lattes : [string]
}
```
#### Error Response

##### If the user try to update the information of another user without being an administrator

Status Code: 403

Content:
```
{
    error : forbidden,
    message : Insufficient credentials
}
```

##### If there are parameters with invalid input in the json payload.

Status Code: 400

Content:
```
{
    error : bad request,
    message : Invalid parameters
}
```

##### If the authentication and authorization are correct and the requested id doesn't match any user in the database

Status Code: 404

Content:
```
{
    "error": "Not Found",
    "message": "Resource Not Found"
}
```

#### Sample Call
#### Notes

## Get Current User
#### URL
    /currentuser/
#### METHOD
    GET
#### URL Params
#### Data Params
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    uri : [string],
    id : [integer],
    name : [string],
    email : [string],
    role : [string],
    confirmed : [boolean],
    lattes : [string]
}
```

#### Error Response

##### If the user does not send the authorization token

Status Code: 401

#### Sample Call
#### Notes
##### The user must have to send the authentication token in the Authorization header

## Generate Confirmation Token
#### URL
    /confirm
#### METHOD
    GET
#### URL Params
#### Data Params
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    message : [string]
}
```
##### An email will be sent to the user with the confirmation token.
#### Error Response

##### If the user does not send the authorization token

Status Code: 401

##### If the user tries to get a confirmation token for an already confirmed account

Status Code: 400

Content:
```
{
    error : bad request,
    message : User already confirmed this account.
}
```
#### Sample Call
#### Notes

## Get Image
#### URL
    /images/<int:id>/
#### METHOD
    GET
#### URL Params
    [integer] id
#### Data Params
#### Success Response
##### Header
Status Code: 200
Content-Type: image/[file-format]
#### Error Response

##### If the requested id doesn't match any image in the database

Status Code: 404

Content:
```
{
    "error": "Not Found",
    "message": "Resource Not Found"
}
```

#### Sample Call
#### Notes


## Create Image
#### URL
    /images/
#### METHOD
    POST
#### URL Params
#### Data Params
```
{
    filename : [string],
    image_string : [string, base64 enconded image],
    alternate : [string]
}
```
#### Success Response
##### Header
Status Code: 201
Location: /images/id -- id of the created image

Content:
```
{
    id : [integer],
    uri : [string],
    filename : [string],
    uploaded_by : [string],
    alternate : [string],
    last_modified : [string],
    creation_date : [string]
}
```
#### Error Response
##### If there are missing parameters(or parameters with invalid input) in the json payload.

Status Code: 400

Content:
```
{
    error : bad request,
    message : Invalid parameters
}
```

##### If the user does not send the authentication token

Status Code: 401

#### Sample Call
#### Notes

## Get Image Metadata
#### URL
    /images/<int:id>/metadata/
#### METHOD
    GET
#### URL Params
    [integer] id
#### Data Params
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    id : [integer],
    uri : [string],
    filename : [string],
    uploaded_by : [string],
    alternate : [string],
    last_modified : [string],
    creation_date : [string]
}
```

#### Error Response

##### If the requested id doesn't match any image in the database

Status Code: 404

Content:
```
{
    "error": "Not Found",
    "message": "Resource Not Found"
}
```

#### Sample Call
#### Notes

## Update Image
#### URL
    /images/<int:id>
#### METHOD
    PUT
#### URL Params
    [integer] id
#### Data Params
##### Note: All parameters (key-value pair) are optional.
```
{
    filename : [string],
    image_string : [string, base64 encoded image]
    alternate : [string],
}
```
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    id : [integer],
    uri : [string],
    filename : [string],
    uploaded_by : [string],
    alternate : [string],
    last_modified : [string],
    creation_date : [string]
}
```

#### Error Response

##### If the user try to update an image that he didn't uploaded without being an administrator

Status Code: 403

Content:
```
{
    error : forbidden,
    message : Insufficient credentials
}
```

##### If there are parameters with invalid input in the json payload.

Status Code: 400

Content:
```
{
    error : bad request,
    message : Invalid parameters
}
```

##### If the authentication and authorization are correct and the requested id doesn't match any image in the database

Status Code: 404

Content:
```
{
    "error": "Not Found",
    "message": "Resource Not Found"
}
```

#### Sample Call
#### Notes

## Get Message By Id
#### URL
    /messages/<int:id>/
#### METHOD
    GET
#### URL Params
    [integer] id
#### Data Params
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    {
        id : [integer],
        uri : [string],
        name : [string],
        last_name : [string],
        email : [string],
        body : [string]
    }
}
```
#### Error Response
##### If the authentication and authorization are correct and the requested id doesn't match any message in the database
Status Code: 404

Content:
```
{
    "error": "Not Found",
    "message": "Resource Not Found"
}
```

##### If the user does not send the authentication token

Status Code: 401

##### If the user try to access the message without being an administrator

Status Code: 403
Content:
```
{
    error : forbidden,
    message : 'Insufficient permissions'
}
```
#### Sample Call
#### Notes

The user must be logged in and be a administrator

## Create A Message
#### URL
    /messages/
#### METHOD
    POST
#### URL Params
#### Data Params
```
{
    name : [string],
    last_name : [string],
    email : [string],
    body : [string]
}
```
#### Success Response
##### Header
Status Code: 201
Location: /messages/id -- id of the created message

Content:
```
{
    message : [string] "The message was sent to the course staff."
}
```

#### Error Response

##### If the email in the json payload is not a valid email

Status Code: 400
Content:
```
{
    error : bad request,
    message : Invalid email.
}
```

##### If there are missing parameters(or parameters with invalid input) in the json payload.

Status Code: 400

Content:
```
{
    error : bad request,
    message : Invalid parameters
}
```

#### Sample Call
#### Notes

## Delete Message
#### URL
    /messages/<int:id>
#### METHOD
    DELETE
#### URL Params
    [integer] id
#### Data Params
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    message : [string] "The message was deleted."
}
```
#### Error Response

##### If the authentication and authorization are correct(The user is an administrator) and the requested id doesn't match any message in the database

Status Code: 404

Content:
```
{
    "error": "Not Found",
    "message": "Resource Not Found"
}
```

#### Sample Call
#### Notes

## Get Virtual Learning Environments
#### URL
    /vles/
#### METHOD
    GET
#### URL Params
#### Data Params
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    {
        vles : [
            {
                id : [integer],
                uri : [string],
                name : [string],
                link : [string],
                author : [string] link to the author,
                last_modified: [string],
                creation_date: [string]
            },
        ]
    }
}
```
#### Error Response
#### Sample Call
#### Notes

## Get Virtual Learning Environment By Id
#### URL
    /vles/<int:id>
#### METHOD
    GET
#### URL Params
    [integer] id
#### Data Params
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    {
        id : [integer],
        uri : [string],
        name : [string],
        link : [string],
        author : [string] link to the author,
        last_modified: [string],
        creation_date: [string]
    }
}
```
#### Error Response
##### If the requested id doesn't match any virtual learning environments in the database
Status Code: 404

Content:
```
{
    "error": "Not Found",
    "message": "Resource Not Found"
}
```

#### Sample Call
#### Notes

## Create A Virtual Learning Environment
#### URL
    /vles/
#### METHOD
    POST
#### URL Params
#### Data Params
```
{
    name : [string],
    link : [string]
}
```
#### Success Response
##### Header
Status Code: 201
Location: /vles/id -- id of the created vle

Content:
```
{
    id : [integer],
    uri : [string],
    name : [string],
    link : [string],
    author : [string] link to the author,
    last_modified: [string],
    creation_date: [string]
}
```

#### Error Response

##### If there are missing parameters(or parameters with invalid input) in the json payload.

Status Code: 400

Content:
```
{
    error : bad request,
    message : Invalid parameters
}
```

#### Sample Call
#### Notes

## Delete Message
#### URL
    /vles/<int:id>
#### METHOD
    DELETE
#### URL Params
    [integer] id
#### Data Params
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    message : [string] "The virtual learning environment was deleted."
}
```
#### Error Response

##### If the authentication and authorization are correct(The user is an administrator) and the requested id doesn't match any vle in the database

Status Code: 404

Content:
```
{
    "error": "Not Found",
    "message": "Resource Not Found"
}
```


#### Sample Call
#### Notes

##### The user must have to be an administrator


## Get Campuses
#### URL
    /campuses/
#### METHOD
    GET
#### URL Params
#### Data Params
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    campuses : [
        {
            uri : [string],
            id : [integer],
            name : [string],
            localization : [string],
            contacts : [string] url
        },
    ]
}
```
#### Error Response
#### Sample Call
#### Notes

## Get Campus
#### URL
    /campuses/<int:id>
#### METHOD
    GET
#### URL Params
    [integer] id
#### Data Params
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    uri : [string],
    id : [integer],
    name : [string],
    localization : [string],
    contacts : [string] url
}
```
#### Error Response
##### If the requested id doesn't match any campus in the database
Status Code: 404

Content:
```
{
    "error": "Not Found",
    "message": "Resource Not Found"
}
```

#### Sample Call
#### Notes

## Create Campus
#### URL
    /campuses/
#### METHOD
    POST
#### URL Params
#### Data Params
```
{
    name : [string],
    localization : [string]
}
```
#### Success Response
##### Header
Status Code: 201

Content:
```
{
    uri : [string],
    id : [integer],
    name : [string],
    localization : [string],
    contacts : [string] url
}
```
#### Error Response
##### If the user does not send the authorization token

Status Code: 401

##### If the user does send the authorization token but do not have administer permissions

Status Code: 403
Content:
{
    error : forbidden,
    message : 'Insufficient permissions'
}

#### Sample Call
#### Notes
The user must be logged in and be a administrator

## Update Campus
#### URL
    /campuses/<int:id>
#### METHOD
    PUT
#### URL Params
#### Data Params
```
{
    name : [string],
    localization : [string]
}
```
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    uri : [string],
    id : [integer],
    name : [string],
    localization : [string],
    contacts : [string] url
}
```
#### Error Response
##### If the user does not send the authorization token

Status Code: 401

##### If the user does send the authorization token but do not have administer permissions

Status Code: 403
Content:
{
    error : forbidden,
    message : 'Insufficient permissions'
}

#### Sample Call
#### Notes
The user must be logged in and be a administrator

## Delete Campus
#### URL
    /campuses/<int:id>
#### METHOD
    DELETE
#### URL Params
#### Data Params
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    message : [string] "The campus was deleted."
}
```
#### Error Response
##### If the user does not send the authorization token

Status Code: 401

##### If the user does send the authorization token but do not have administer permissions

Status Code: 403
Content:
{
    error : forbidden,
    message : 'Insufficient permissions'
}

#### Sample Call
#### Notes
The user must be logged in and be a administrator

## Get All Contacts 
#### URL
    /contacts/
#### METHOD
    GET
#### URL Params
#### Data Params
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    "contacts": [
        {
            id : [integer],
            uri : [string],
            description : [string],
            telephone_number : [string],
            email : [string],
            campus : [string] url,
        },
    ]
}
```
#### Error Response

##### If the requested id doesn't match any contact in the database
Status Code: 404

Content:
```
{
    "error": "Not Found",
    "message": "Resource Not Found"
}
```

#### Sample Call
#### Notes

## Get Contact
#### URL
    /contacts/<int:id>
#### METHOD
    GET
#### URL Params
    [integer] id
#### Data Params
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    id : [integer],
    uri : [string],
    description : [string],
    telephone_number : [string],
    email : [string],
    campus : [string] url,
}
```
#### Error Response

##### If the requested id doesn't match any contact in the database
Status Code: 404

Content:
```
{
    "error": "Not Found",
    "message": "Resource Not Found"
}
```

#### Sample Call
#### Notes

## Update Contact
#### URL
    /contacts/<int:id>
#### METHOD
    PUT
#### URL Params
    [integer] id
#### Data Params
```
{
    description : [string],
    telephone_number : [string],
    email : [string]
}
```
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    id : [integer],
    uri : [string],
    description : [string],
    telephone_number : [string],
    email : [string],
    campus : [string] url,
}
```
#### Error Response

##### If the requested id doesn't match any contact in the database
Status Code: 404

Content:
```
{
    "error": "Not Found",
    "message": "Resource Not Found"
}
```

#### Sample Call
#### Notes

## Delete Contact
#### URL
    /contacts/<int:id>
#### METHOD
    DELETE
#### URL Params
    [integer] id
#### Data Params
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    message : [string] "The contact was deleted."
}
```

#### Error Response

##### If the requested id doesn't match any contact in the database
Status Code: 404

Content:
```
{
    "error": "Not Found",
    "message": "Resource Not Found"
}
```

##### If the user does not send the authorization token

Status Code: 401

##### If the user does send the authorization token but do not have administer permissions

Status Code: 403
Content:
{
    error : forbidden,
    message : 'Insufficient permissions'
}

#### Sample Call
#### Notes

## Create Campus Contact
#### URL
    /campuses/<int:id>/contacts/
#### METHOD
    POST
#### URL Params
    [integer] id -- campus id
#### Data Params
#### Success Response
##### Header
Status Code: 201
Location: /contacts/id/ -- id of the created contact

Content:
```
{
    id : [integer],
    uri : [string],
    description : [string],
    telephone_number : [string],
    email : [string],
    campus : [string] url,
}
```

#### Error Response

##### If the requested id doesn't match any campus in the database
Status Code: 404

Content:
```
{
    "error": "Not Found",
    "message": "Resource Not Found"
}
```

##### If the user does not send the authorization token

Status Code: 401

##### If the user does send the authorization token but do not have administer permissions

Status Code: 403
Content:
{
    error : forbidden,
    message : 'Insufficient permissions'
}

#### Sample Call
#### Notes
The user must be logged in and be a administrator

## Get Campus Contacts
#### URL
    /campuses/<int:id>/contacts/
#### METHOD
    GET
#### URL Params
    [integer] id -- campus id
#### Data Params
#### Success Response
##### Header
Status Code: 200

Content:
```
{
    "contacts": [
        {
            id : [integer],
            uri : [string],
            description : [string],
            telephone_number : [string],
            email : [string],
            campus : [string] url,
        },
    ]
}
```

#### Error Response

##### If the requested id doesn't match any campus in the database
Status Code: 404

Content:
```
{
    "error": "Not Found",
    "message": "Resource Not Found"
}
```

#### Sample Call
#### Notes
