from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_restful import Resource,Api

app=None
api=None 
def create_app():
    app=Flask(__name__,template_folder="templates",static_folder="static")
    api=Api(app)
    print("Starting Manikanta's Local Development")
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    
    app.app_context().push()
    app.secret_key="BAD_SECRET_KEY"
    return app,api 

app,api=create_app()


#Import all controllers
from application.controllers import *


#Add all restful controllers
from application.api import *
api.add_resource(LoginAPI,"/api/login")
#api.add_resource(LoginAPI,"/api/login")
api.add_resource(CreateUserAPI,"/api/create_user")
api.add_resource(DeleteUserAPI,"/api/delete_user")
api.add_resource(UpdateUserAPI,"/api/update_user")

api.add_resource(ToDoAPI,"/api/todo")


api.add_resource(UserDetailsAPI,"/api/user_details")


api.add_resource(GetTodoAPI,'/api/get_todo')

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8085)
