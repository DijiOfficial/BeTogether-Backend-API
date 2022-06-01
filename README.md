# BeTogether-Backend-API

## Overview
  - BeTogether will be part of the BeApps tool set for coaches and learners to use.
  - In this BeTogether App the learners will be able to upload descriptions of projects they want to work on.
  - They will then be able to sort through all the propositions and rearrange them in their preferred order.
  - The app will then create groups based on learners preferences

## User Stories
  1. As a Coach, I can initiate a new group Project.
  2. As A learner I can Upload my project description.
  3. When all the projects have been uploaded,
  4. As a learner I can reorder the projects to vote for my favorites ones.
  5. When all the votes have been finalized,
  6. As a learner I can consult the final list of projects and how the app made the groups

## Database Schema
![db schma](https://user-images.githubusercontent.com/33450259/171354720-e3421ad5-e069-4f30-affd-a754eed47fc0.PNG)

## API Routes
To 'GET' Users => https://be-together.herokuapp.com/user or https://be-together.herokuapp.com/user/pk where you replace "pk" by the project id e.g: https://be-together.herokuapp.com/user/3 to "GET" the User with 3

To add a User "POST" => https://be-together.herokuapp.com/user with a format:
```Json
{
    "password": "password",
    "email": "any@email.com",
    "username": "username",
    "first_name": "user's name",
    "last_name": "user's last name"
}
```

To change a User 'PUT' => https://be-together.herokuapp.com/user with a format:
```JSON
{
    "id": 3,
    "password": "newPassword",
    "email": "new@email.com",
    "first_name": "NewName",
    "last_name": "NewLastName"
}
```

To delete a User 'DELETE' => https://be-together.herokuapp.com/user/pk

When a user is created you receive a JsonResponse in this format: 
```JSON
{
    "response": "Successfully Added To DB",
    "email": "test@test.test",
    "username": "test",
    "token": "4be879541ccb87d90c5cee55ce0537589f9066f8"
}
```

The token is used to identify the user for further requests 
If you want to login => https://be-together.herokuapp.com/login with "POST" in Json format: 
```JSON
{
    "password": "heroku",
    "username": "heroku@test.test"
}
```
and JsonResponse in this format:
```JSON
{
    "token": "d6835743fc33a23bdeb4fdd7e0a6a90cfa21b9df"
}
```
=> yes the email has to be sent as username. Just django things..

To 'GET' the projects => https://be-together.herokuapp.com/project ou https://be-together.herokuapp.com/project/pk where you replace "pk" by the project id e.g: https://be-together.herokuapp.com/project/3 to"GET" the project with id 3

To add a project "POST" => https://be-together.herokuapp.com/project like this:
Variables name for posting projects are:
```JSON
{
  name: "",
  description: "",
  database_schema_picture: "",
  mockup_picture: "",
  groupProject: ""
} 
```
make sure user is authenticated with the token

To "GET" pictures from a project =>  https://be-together.herokuapp.com/ (link Of Image See Below Project JsonResponse Link)
e.g:  https://be-together.herokuapp.com/images/images/9a501_orig_Fy00pSr.jpg to get the image
```JSON
{
        "id": 3,
        "user": {
            "id": 5,
            "password": "pbkdf2_sha256$260000$POSszL8EgLxLn4cWIbETrd$Q02Xw0U9G5ub25WZvkEvNu76NYsXUuyMiFQRWXzSH6U=",
            "email": "whet@faee.zto",
            "username": "usterr45",
            "first_name": "TestingOtherMethods",
            "last_name": "johnson",
            "date_joined": "2022-05-24T11:23:00.487000Z",
            "last_login": "2022-05-24T11:23:00.487000Z",
            "is_admin": false,
            "is_active": true,
            "is_staff": false,
            "is_superuser": false
        },
        "name": "test",
        "description": "hugh jackman's nipples",
        "database_schema_picture": "/images/images/9a501_orig_Fy00pSr.jpg",
        "mockup_picture": "/images/images/croco.JPG"
    }
 ```
The last routes are unfinished, as there was no frontend to follow I lost motivation to create routes that will never be used.
See below the algorithm that sorts the groups (uses fake data and doesn't put anything inside the databse)
The algorithm is based on "The hospital-resident assignment problem" but adapted to the project as projects don't have learner preference.

The python file of The [algorithm](https://github.com/DijiOfficial/BeTogether-Backend-API/blob/master/betogether/algo.py)
