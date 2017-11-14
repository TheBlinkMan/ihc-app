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

##### If the user does send the authorization token but
##### do not have administer permissions

Status Code: 403
Content:
{
    message : 'Insufficient permissions'
}
#### Sample Call
#### Notes
The user must be logged in and be a administrator
