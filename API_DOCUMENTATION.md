# API Documentation Version 1.0

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
    message : 'Insufficient permissions'
}
#### Sample Call
#### Notes
The user must be logged in and be a administrator

## Get User By Id
#### URL
    /users/<int:id>/
#### METHOD
    GET
#### URL Params
    Integer id
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
##### If the authentication and authorization are correct and the requested id doesn't match any user in the database
Status Code: 404

##### If the user does not send the authentication token

Status Code: 401

##### If the user try to access the information of another user without being an administrator

Status Code: 403
Content:
```
{
    message : 'Insufficient credentials'
}
```
#### Sample Call
#### Notes
The user must be logged in and be a administrator or
the user he is trying to access
