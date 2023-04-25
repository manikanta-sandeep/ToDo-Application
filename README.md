# ToDo-Application
To Do Application (Backend) Software Developer (Backend)

## How to run the application:

1. Download the Source code
2. Navigate to root folder
3. Run the setup.sh file [ in case if you can't run the .sh file you can directly run main file if your system met all the requirements.]

## Browsing through the application [Front End]:

1. You can directly access the web application by clicking on the specified url by the python script output.
2. After entering the application you can see login.
3. You can create a user and login to the application successfully.

## Using APIs :

All the API's are listed below:

```

1. Api Name : LoginAPI
   path     : /api/login
   methods  : [POST]
   parameter : [username, password]
   response : 404 ,200
   
   
2. Api Name : CreateUserAPI
   path     : /api/create_user
   methods  : [POST]
   parameter : [username, email, dob, password, date_joined]
   response : 404 ,200
   
   
3. Api Name : DeleteUserAPI
   path     : /api/delete_user
   methods  : [POST]
   parameter : [user_id]
   response : 404 ,200
   
   
4. Api Name : UpdateUserAPI
   path     : /api/update_user
   methods  : [POST]
   parameter : [username, email, dob, password, date_joined]
   response : 404 ,200
   
   
5. Api Name : UserDetailsAPI
   path     : /api/user_details
   methods  : [POST]
   parameter : [user_id]
   response : 404 ,200
   
   
6. Api Name : GetTodoAPI
   path     : /api/get_todo
   methods  : [GET]
   parameter : [todo_id, user_id]
   response : 404 ,200
   
 
7. Api Name : TodoAPI
   path     : /api/get_todo
   methods  : [GET]
     parameter : [user_id]
     response : 404 ,200

   methods  : [POST]
     parameter : [user_id,todo_id,title,status,description,last_updated,deadline]
     response : 404 ,200

   methods  : [PUT]
     parameter : [user_id,title,status,description,last_updated,deadline,date_created]
     response : 404 ,200

   methods  : [DELETE]
     parameter : [user_id,todo_id]
     response : 404 ,200

 

```


## Entity Relationship Diagram:

![TODO](https://user-images.githubusercontent.com/89150264/234098722-0022f089-78e7-45c0-b1ca-05e3ab44e698.svg)
