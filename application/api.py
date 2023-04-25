from flask_restful import Resource
from application.models import user,todo
from application.database import db
from flask import request


class LoginAPI(Resource):
    def post(self):
        args=request.args
        username = args.get("username", None)
        email = args.get("email", None)
        user_id = args.get("username", None)

        password = args.get("password", None)
        user1 = db.session.query(user).filter(user.email == email).first()
        if user1 is None:
            return "Email Not Found",404
        user1 = db.session.query(user).filter((user.email == email),user.password==password).first()
        if user1 is None:
            return "Invalid Credentials",404
        return {'user_id':user1.user_id,'username':user1.username,'email':user1.email,"dob":user1.dob,'password':user1.password,'date_joined':user1.date_joined,"message":"User Successfully Logged IN"},200


class CreateUserAPI(Resource):
    def post(self):
        args=request.args
        username = args.get("username", None)
        email = args.get("email", None)
        dob = args.get("dob", None)
        password = args.get("password", None)
        date_joined = args.get("date_joined", None)
        if username is None:
            return {"error_message":"username is required"},404

        if email is None:
            return {"error_message":"email is required"},404

        if "@" in email:
            pass
        else:
            return {"error_message":"Invalid email"},404

        user1 = db.session.query(user).filter((user.username == username) | (user.email == email)).first()
        if user1:
            return {"error_message":"Duplicate user"},404        

        new_user = user(username=username, email=email, dob=dob, password=password, date_joined=date_joined)
        db.session.add(new_user)
        db.session.commit()
        return {'user_id':new_user.user_id,'username':new_user.username,'email':new_user.email,"dob":new_user.dob,'password':new_user.password,'date_joined':new_user.date_joined,'message':"User Created Successfully"},200


class UpdateUserAPI(Resource):
    def post(self):
        args=request.args
        username = args.get("username", None)
        email = args.get("email", None)
        user_id = args.get("user_id", None)
        dob = args.get("dob", None)
        password = args.get("password", None)
        date_joined = args.get("date_joined", None)
        user1 = db.session.query(user).filter((user.email == email) | (user.user_id == user_id) ).first()
        if username is None:
            user1.username=user1.username
        else:
            user1.username=username
        if dob is None:
            user1.dob=user1.dob
        else:
            user1.dob=dob
        if password is None:
            user1.password=user1.password
        else:
            user1.password=password

        db.session.commit()
        new_user= db.session.query(user).filter(user.email == email).first()
        
        return {'user_id':new_user.user_id,'username':new_user.username,'email':new_user.email,"dob":new_user.dob,'password':new_user.password,'date_joined':new_user.date_joined},200


class DeleteUserAPI(Resource):    
    def post(self):
        args=request.args
        email = args.get("email", None)
        user_id = args.get("user_id", None)
        user1 = db.session.query(user).filter((user.email == email) | (user.user_id==user_id)).first()
        if user1 is None:
            return "Not Found",404
        db.session.delete(user1)
        db.session.commit()
        return {'message':'Deleted Successfully','user_id':  user1.user_id,'username':    user1.username,'email':    user1.email},200



class UserDetailsAPI(Resource):
    def post(self):
        args=request.args
        user_id = args.get("user_id", None)
        user1 = db.session.query(user).filter((user.user_id == user_id)).first()
        
        if user1 is None:
            return {'message':"User Not Found"},404
        return {'user_id':user1.user_id,'username':user1.username,'email':user1.email,"dob":user1.dob,'password':user1.password,'date_joined':user1.date_joined}

class GetTodoAPI(Resource):
    def get(self):
        args=request.args
        todo_id= args.get("todo_id", None)
        user_id= args.get("user_id", None)
        user1 = db.session.query(user).filter(user.user_id == user_id).first()
        if user1 is None:
            return {"message":"User Not Found"},404

        #Todo ID None
        todo1 = db.session.query(todo).filter(todo.todo_id == todo_id).first()
        if todo1 is None:
            return {"message":"Task Not Found"},404

        #Invalid Access
        todo_c=db.session.query(todo).filter(todo.todo_id==todo_id, todo.creator_id==user_id).first()
        if todo_c is None:
            return {"message":"Access Invalid"},404
        
        todo1=db.session.query(todo).filter(todo.todo_id == todo_id).first()
        
        return {"creator_id":todo1.creator_id, "todo_id":todo1.todo_id ,"title":todo1.title,"description":todo1.description,"status":todo1.status,"date_created":todo1.date_created,"deadline":todo1.deadline,"last_updated":todo1.last_updated},200
    




class ToDoAPI(Resource):
    def get(self):
        args=request.args
        user_id = args.get("user_id", None)
        

        user1 = db.session.query(user).filter(user.user_id == user_id).first()
        print(user1)
        if user1 is None:
            return "User Not Found",404
        

        todo1 = db.session.query(todo).filter(todo.creator_id == user_id).all()
        print(todo1)
        if todo1 is None or len(todo1)==0:
            return "No tasks Yet",200
        d,count={},1
        for i in todo1:
            d['task '+str(count)]={"creator_id":i.creator_id,"title":i.title,"description":i.description,"status":i.status,"date_created":i.date_created,"deadline":i.deadline,"last_updated":i.last_updated}
            count+=1
        return d,200
    
    def put(self):
        args=request.args
        user_id = args.get("user_id", None)
        title = args.get("title", None)
        status= args.get("status", None)
        description = args.get("description", None)
        date_created = args.get("date_created", None)
        deadline = args.get("deadline", None)
        last_updated = args.get("last_updated", None)
        
        if title is None:
            return "Title is Required",404
        if status is None:
            return "Current status is Required",404
        if user_id is None:
            return "User not logged in",404
        todo1=todo(creator_id=user_id,title=title,description=description,status=status,date_created=date_created,deadline=deadline,last_updated=last_updated)
        db.session.add(todo1)
        db.session.commit()
        
        return {"creator_id":user_id,"title":title,"description":description,"status":status,"date_created":date_created,"deadline":deadline,"last_updated":last_updated, "message":"Task Created Successfully"},200
    

    
    def post(self):
        args=request.args
        user_id = args.get("user_id", None)
        todo_id=args.get("todo_id",None)
        title = args.get("title", None)
        status= args.get("status", None)
        description = args.get("description", None)
        date_created = args.get("date_created", None)
        deadline = args.get("deadline", None)
        last_updated = args.get("last_updated", None)
        
        
        if todo_id is None:
            return "ToDo ID Required",404
        if user_id is None:
            return "User not logged in",404

        #Username None
        user1 = db.session.query(user).filter(user.user_id == user_id).first()
        if user1 is None:
            return "User Not Found",404

        #Todo ID None
        todo1 = db.session.query(todo).filter(todo.todo_id == todo_id).first()
        if todo1 is None:
            return "Task Not Found",404

        #Invalid Access
        todo_c=db.session.query(todo).filter(todo.todo_id==todo_id, todo.creator_id==user_id).first()
        if todo_c is None:
            return "Access Invalid",404

        #Modify
        if title is None:
            todo_c.title=todo_c.title
        else:
            todo_c.title=title

        if status is None:
            todo_c.status=todo_c.status
        else:
            todo_c.status=status

        if description is None:
            todo_c.description=todo_c.description
        else:
            todo_c.description=description

        if last_updated is None:
            todo_c.last_updated=todo_c.last_updated
        else:
            todo_c.last_updated=last_updated

        if deadline is None:
            todo_c.deadline=todo_c.deadline
        else:
            todo_c.deadline=deadline


        db.session.commit()
        
        todo1=db.session.query(todo).filter(todo.todo_id==todo_id,todo.creator_id==user_id).first()
        

        return {"creator_id":todo1.creator_id,"title":todo1.title,"description":todo1.description,"status":todo1.status,"date_created":todo1.date_created,"deadline":todo1.deadline,"last_updated":todo1.last_updated, "message":"Task Updated Successfully"},200
    
    
    def delete(self):
        args=request.args
        user_id = args.get("user_id", None)
        todo_id=args.get("todo_id",None)
      
        if todo_id is None:
            return "ToDo ID Required",404
        if user_id is None:
            return "User not logged in",404

        #Username None
        user1 = db.session.query(user).filter(user.user_id == user_id).first()
        if user1 is None:
            return "User Not Found",404

        #Todo ID None
        todo1 = db.session.query(todo).filter(todo.todo_id == todo_id).first()
        if todo1 is None:
            return "Task Not Found",404

        #Invalid Access
        todo_c=db.session.query(todo).filter(todo.todo_id==todo_id, todo.creator_id==user_id).first()
        if todo_c is None:
            return "Access Invalid",404
        
        todo1=db.session.query(todo).filter(todo.todo_id==todo_id, todo.creator_id==user_id).first()
        db.session.delete(todo1)
        db.session.commit()

        return {"creator_id":todo1.creator_id,"title":todo1.title,"description":todo1.description,"status":todo1.status,"date_created":todo1.date_created,"deadline":todo1.deadline,"last_updated":todo1.last_updated, "message":"Task Deleted Successfully"},200
    

