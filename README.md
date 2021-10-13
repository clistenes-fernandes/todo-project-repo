# To Do Project

The project consists of creating a REST service that allows you to create and store tasks (To Dos), edit and remove them. In this service, each To Do is associated with a user that will also be created, stored, edited and removed.

### What it must do

The tasks that this service must perform are described below:

- Allow only access for logged in users (use djangos user framework) 
- Endpoints for:
  - Insert/update a Todo 
  - get a single Todo by id 
  - get all Todos   
  - get all Todos filtered by name 
  - get all Todos filtered by a flag 
- On insert a Todo:
  - Add a create date and edit date 
  - get the logged in user from Django framework and add it to the todo 
 - Update the user in the associated TO DO task if it is changed in the Django backend 
 - Check the reminder and due value when the TO DO is returned (In this item a reminder message is returned if the task is within the remaining time until the end date) 


### Technologies

The technologies used in this project were the following:

- [Docker](https://www.docker.com/)
- Local [Kubernetes Cluster (MiniKube)](https://kubernetes.io/)
- Automated services deployment ([Google Skaffold](https://skaffold.dev/))
- [MongoDB](https://www.mongodb.com/)
- TodoService - Python REST Service ([Django Framework](https://www.djangoproject.com/))
- [Postman] (https://www.postman.com/) to test it.

### Database Structure
The structure that the API should return is below:
- Id (autogenerate from MongoDB)
- Name -> String
- Description -> String
- User -> Object
  - user id (from django)
  - firstname
  - lastname
  - email
- status -> String (NONE, ACTIVE, DONE)
- created -> Datetime
- edited -> Datetime
- due -> Datetime
- reminder -> Int (value < 0 -> no reminder, value >= 0 send reminder)
(reminder mail should be send x (value of reminder) minutes before
the due date)
- flags -> List of Strings (max 5 flags(5 Strings))

For the creation of the user we used the predefined [Django User structure](https://docs.djangoproject.com/en/3.2/ref/contrib/auth/) and manipulated it according to the needs of the project. The user was passed as a foreign key in the TODO collection in database, so changes to the user information were kept only in the user's collection.

### Endpoints:

Excluding the login and user creation endpoints, the rest of the operations were done using the JWT token returned from the login endpoint.

#### USER

**POST:** /user – para criar um usuário	
{
    "username": "j_smith",
    "password": "john1234!",
    "email": "johnsmith@email.com",
    "first_name":"John",
    "last_name":"Smith"
}

**POST:** /user/login – User login (returns an access and refresh token)

```
{
    "username": "j_smith",
    "password": "john1234!"
}
```

**PUT:** /user

```
{
    "last_name": "Walker",
    "email": "johnwalker@email.com"
}
```

**DELETE:** /user – Remove the current user

**GET:** /user – Get the current user information

#### TODO:

**GET:**

	- /todo – returns all To Dos from the current user;
	- /todo/{todo_id} – returns a specific To Do based on its id;
	- /todo?flags=flag name – get a To Do based on its flag name
  - /todo?name= name of TODO – get a To Do based on its name

**POST:**	/todo – create a new todo for the current user. The due date and time must be greater than the moment of insertion. The flags number must not exceed 5 items.

```
{
    "name":"Soccer",
    "description": "Play soccer with friends",
    "status": "A",
    "due": "2021-10-13 00:10",
    "reminder":30,
    "flags": ["soccer", "freinds", "week"]
}
```

**PUT:** /todo/{todo_id} – Update a To Do based on its id

```
  {
    "reminder":25,
    "due": "2021-10-12 23:50"
}
```

**DELETE:** /todo/{todo_id} – delete a To Do based on its id 

### Build and Deployment:

An image of the project was created using Docker, and the Dockerfile is among the project files. After the image was created, it was uploaded to dockerhub and used in the settings to create the container in Kubernetes. A ready-made MongoDB image was also used.

For the Kubernetes configurations three files were created:

**todo-secret.yaml** – Configuração de algumas variáveis de ambiente;

**todo-deploy.yaml** – Configuração do deployment;

**todo-service.yaml** – Configuração do service;


To facilitate the deployment of this project we used Google Skaffold, whose configuration was created in the file below.


**skaffold.yaml**


### Run:

To deploy and run the project, the command "skaffold run" was used and all builds and deploys were done automatically by skaffold.

