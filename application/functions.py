from application.models import user,todo
from application.database import db
from flask import request
from application.local_time import time_calc


class Login():
    def login_account(self,email,password):
        user1 = db.session.query(user).filter(user.email == email).first()
        if user1 is None:
            return {'code':0,'title':'Email Not Found','message':"Email Not Found"}
        user1 = db.session.query(user).filter((user.email == email),user.password==password).first()
        if user1 is None:
            return {'code':1,'title':"Invalid Credentials",'message':"Invalid Credentials"}
        return {'code':2,'user_id':user1.user_id,'username':user1.username,'email':user1.email,"dob":user1.dob,'password':user1.password,'date_joined':user1.date_joined,"message":"User Successfully Logged IN"}


class CreateUser():
    def create(self,username,email,dob,password):
        date_joined = time_calc().time()
        
        user1 = db.session.query(user).filter((user.username == username) | (user.email == email)).first()
        if user1:
            return {'code':0,'title':'Duplicate user',"message":"User already exists with either same email or same username."}        

        new_user = user(username=username, email=email, dob=dob, password=password, date_joined=date_joined)
        db.session.add(new_user)
        db.session.commit()
        return {'code':1,'user_id':new_user.user_id,'username':new_user.username,'email':new_user.email,"dob":new_user.dob,'password':new_user.password,'date_joined':new_user.date_joined,'message':"User Created Successfully"}


class UpdateUser():
    def update(self,user_id,dob,password):
        
        user1 = db.session.query(user).filter((user.user_id == user_id)).first()
        
        if dob is None or dob=='':
            user1.dob=user1.dob
        else:
            user1.dob=dob
        if password is None or password=='':
            user1.password=user1.password
        else:
            user1.password=password

        db.session.commit()
        new_user= db.session.query(user).filter(user.user_id == user_id).first()
        
        return {'code':0,'title':"Updated",'user_id':new_user.user_id,'username':new_user.username,'email':new_user.email,"dob":new_user.dob,'password':new_user.password,'date_joined':new_user.date_joined,'message':'User profile updated Successfully'}


class DeleteUser():    
    def delete(self,user_id):
        user1 = db.session.query(user).filter(user.user_id == user_id).first()
        if user1 is None:
            return "Not Found"
        db.session.delete(user1)
        db.session.commit()
        return {'code':0,'title':'','message':'Deleted Successfully','user_id':  user1.user_id,'username':    user1.username,'email':    user1.email}


class UserDetails():
    def get_details(self,user_id):
        user1 = db.session.query(user).filter((user.user_id == user_id)).first()
        
        if user1 is None:
            return {'code':0,'title':'User Not Found','message':"User Not Found"}
        return {'code':1,'title':'User Profile','user_id':user1.user_id,'username':user1.username,'email':user1.email,"dob":user1.dob,'password':user1.password,'date_joined':user1.date_joined,"message":"User Details"}



class GetTask():
    def get_task(self,todo_id,user_id):
        
        user1 = db.session.query(user).filter(user.user_id == user_id).first()
        if user1 is None:
            return {'code':1,'title':'Task Not Found',"message":"User Not Found"}

        #Todo ID None
        todo1 = db.session.query(todo).filter(todo.todo_id == todo_id).first()
        if todo1 is None:
            return {'code':2,'title':'Task Not Found',"message":"Task Not Found"}

        #Invalid Access
        todo_c=db.session.query(todo).filter(todo.todo_id==todo_id, todo.creator_id==user_id).first()
        if todo_c is None:
            return {'code':3,'title':'Invalid Access',"message":"Access Invalid"}
        
        todo1=db.session.query(todo).filter(todo.todo_id == todo_id).first()
        
        return {'code':4,'title':'Task',"message":"Task","creator_id":todo1.creator_id, "todo_id":todo1.todo_id ,"title":todo1.title,"description":todo1.description,"status":todo1.status,"date_created":todo1.date_created,"deadline":todo1.deadline,"last_updated":todo1.last_updated}
    


        
class ToDo():
    def get_all_tasks(self,user_id):
        
        user1 = db.session.query(user).filter(user.user_id == user_id).first()
        print(user1)
        if user1 is None:
            return {'code':0,'title':'User Not Found',"message":"User Not Found"}
        

        todo1 = db.session.query(todo).filter(todo.creator_id == user_id).order_by(todo.todo_id.desc()).all()
        print(todo1)
        if todo1 is None or len(todo1)==0:
            return {'code':1,'title':'My Tasks',"message":"No tasks Yet"}
        d,count={'code':2,'title':'My Tasks','tasks':{}},1
        for i in todo1:
            d['tasks']['task '+str(count)]={"creator_id":i.creator_id,'task_id':i.todo_id,"title":i.title,"description":i.description,"status":i.status,"date_created":i.date_created,"deadline":i.deadline,"last_updated":i.last_updated}
            count+=1
        return d
    
    def create_task(self,user_id,title,status,description,deadline):
        
        date_created = time_calc().time()
        last_updated = time_calc().time()
        
        if title is None:
            return {'code':0,'title':'My Tasks',"message":"Title is Required"}
        if status is None:
            return {'code':1,'title':'My Tasks',"message":"Current status is Required"}
        if user_id is None:
            return {'code':2,'title':'My Tasks',"message":"User not logged in"}
        todo1=todo(creator_id=user_id,title=title,description=description,status=status,date_created=date_created,deadline=deadline,last_updated=last_updated)
        db.session.add(todo1)
        db.session.commit()
        
        return {'code':3,'title':'My Tasks',"message":"Task created Successfully","creator_id":user_id,"title":title,"description":description,"status":status,"date_created":date_created,"deadline":deadline,"last_updated":last_updated, "message":"Task Created Successfully"}
    

    
    def update_task(self,user_id,todo_id,title,status,description,deadline):
        
        last_updated = time_calc().time()
        
        if todo_id is None:
            return {'code':0,'title':'Updation Failed',"message":"ToDo ID Required"}
        if user_id is None:
            return {'code':1,'title':'Required Login',"message":"User not logged in"}

        #Username None
        user1 = db.session.query(user).filter(user.user_id == user_id).first()
        if user1 is None:
            return {'code':2,'title':'User Not Found',"message":"User Not Found"}

        #Todo ID None
        todo1 = db.session.query(todo).filter(todo.todo_id == todo_id).first()
        if todo1 is None:
            return {'code':3,'title':'Task Not Found',"message":"Task Not Found"}

        #Invalid Access
        todo_c=db.session.query(todo).filter(todo.todo_id==todo_id, todo.creator_id==user_id).first()
        if todo_c is None:
            return {'code':4,'title':'Invalid Access',"message":"Access Invalid"}

        #Modify
        if title is None or title=='':
            todo_c.title=todo_c.title
        else:
            todo_c.title=title

        if status is None or status=='':
            todo_c.status=todo_c.status
        else:
            todo_c.status=status

        if description is None or description=='':
            todo_c.description=todo_c.description
        else:
            todo_c.description=description

        if last_updated is None:
            todo_c.last_updated=todo_c.last_updated
        else:
            todo_c.last_updated=last_updated

        if deadline is None or deadline=='':
            todo_c.deadline=todo_c.deadline
        else:
            todo_c.deadline=deadline


        db.session.commit()
        
        todo1=db.session.query(todo).filter(todo.todo_id==todo_id,todo.creator_id==user_id).first()
        

        return {'code':5,'title':'Updated Scuccessfully',"message":"Updation Successful","creator_id":todo1.creator_id,"title":todo1.title,"description":todo1.description,"status":todo1.status,"date_created":todo1.date_created,"deadline":todo1.deadline,"last_updated":todo1.last_updated, "message":"Task Updated Successfully"}
    
    
    def delete_task(self,todo_id,user_id):
        if todo_id is None:
            return {'code':0,'title':'ToDo ID Required',"message":"ToDo ID Required"}
        if user_id is None:
            return {'code':1,'title':'User not logged in',"message":"User not logged in"}

        #Username None
        user1 = db.session.query(user).filter(user.user_id == user_id).first()
        if user1 is None:
            return {'code':2,'title':'User Not Found',"message":"User Not Found"}

        #Todo ID None
        todo1 = db.session.query(todo).filter(todo.todo_id == todo_id).first()
        if todo1 is None:
            return {'code':3,'title':'Task Not Found',"message":"Task Not Found"}

        #Invalid Access
        todo_c=db.session.query(todo).filter(todo.todo_id==todo_id, todo.creator_id==user_id).first()
        if todo_c is None:
            return {'code':4,'title':'Invalid Access',"message":"Access Invalid"}
        
        todo1=db.session.query(todo).filter(todo.todo_id==todo_id, todo.creator_id==user_id).first()
        db.session.delete(todo1)
        db.session.commit()

        return {'code':5,'title':'Deleted Successfully',"message":"Deleted Successfully","creator_id":todo1.creator_id,"title":todo1.title,"description":todo1.description,"status":todo1.status,"date_created":todo1.date_created,"deadline":todo1.deadline,"last_updated":todo1.last_updated, "message":"Task Deleted Successfully"}
    

