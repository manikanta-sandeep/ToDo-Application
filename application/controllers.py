from flask import current_app as app,flash
from flask import render_template, redirect,g, request, session
from .functions import *





@app.route('/',methods=['GET','POST'])
def root():
    return render_template('index.html')


@app.route('/login',methods=['GET'])
def login():
    return render_template('login.html',title='Login into your account')


@app.route('/logout',methods=['GET'])
def logout():
    session.clear()
    return redirect('/login')


@app.route('/login',methods=['POST'])
def login_verify():
    email = request.form["email"]
    password = request.form["password"]
    a=Login().login_account(email,password)
    if a['code']==0 or a['code']==1:
        flash(a['message'], category='warning')
        alarm = True
        return render_template('login.html',title=a['title'],alarm=alarm)
    elif a['code']==2:
        session['email']=a['email']
        session['username']=a['username']
        session['user_id']=a['user_id']
        return redirect('/home')

@app.route('/create_account',methods=['GET'])
def create_account():
    return render_template('create_user.html',title='Create account')

@app.route('/create_account',methods=['POST'])
def created_account():
    username,email,dob,password,cnf_password=request.form['username'],request.form['email'],request.form['dob'],request.form['password'],request.form['cnf_password']
    if cnf_password!=password:
        flash('Password not matched', category='warning')
        alarm = True
        return render_template('create_user.html',title='Create account',alarm=alarm)

    a=CreateUser().create(username,email,dob,password)
    print(a)
    if a['code']==0:
        flash(a['message'], category='warning')
        alarm = True  
        return render_template('create_user.html',title=a['title'],alarm=alarm)
    elif a['code']==1:
        flash('Account Created Successfully', category='warning')
        alarm = False
        return render_template('login.html',title='Login into your account',alarm=alarm)


@app.route('/home',methods=['GET','POST'])
def home():
    user_id=session['user_id']
    a=ToDo().get_all_tasks(user_id)
    if a['code']==0:
        flash(a['message'], category='warning')
        alarm = True  
        return render_template('message.html',title=a['title'],alarm=alarm,home=True)
    elif a['code']==1:
        flash(a['message'], category='warning')
        alarm = False
        return render_template('message.html',title=a['title'],alarm=alarm,home=True)
    elif a['code']==2:
        return render_template('home.html',title=a['title'],data=a['tasks'],home=True)
    

@app.route('/create_task', methods=['GET'])
def create_task():
    return render_template('create_task.html',title='Create a Task')

@app.route('/create_task', methods=['POST'])
def created_task():
    title,description,deadline,status,user_id=request.form["title"],request.form["description"],request.form["deadline"],request.form["status"],session["user_id"]
    a=ToDo().create_task(user_id,title,status,description,deadline)
    flash(a['message'], category='warning')
    
    if a['code']==3:
        alarm = False
    elif a['code']==0 or a['code']==1 or a['code']==2: 
        alarm=True
    return render_template('message.html',title=a['title'],alarm=alarm,data=a,c=1)
    

@app.route('/update_task/<id>',methods=['GET','POST'])
def update_task(id):
    user_id=session['user_id']
    task_id=int(id)
    a=GetTask().get_task(task_id,user_id)
    if a['code']==4:
        return render_template('update_task.html',title=a['title'],data=a)
    
@app.route('/updated/<id>',methods=['POST'])
def updated_task(id):
    title,description,deadline,status,user_id=request.form["title"],request.form["description"],request.form["deadline"],request.form["status"],session["user_id"]
    a=ToDo().update_task(user_id,int(id),title,status,description,deadline)
    flash(a['message'], category='warning')
    if a['code']==5:
        alarm=False
    elif a['code'] in [0,1,2,3,4]:
        alarm=True 
    return render_template('message.html',title=a['title'],alarm=alarm,data=a,c=2)


@app.route('/delete_task/<id>',methods=['POST'])
def delete_task(id):
    todo_id,user_id=int(id),session["user_id"]
    a=ToDo().delete_task(todo_id,user_id)
    flash(a['message'], category='warning')
    if a['code']==5:
        alarm=False
    elif a['code'] in [0,1,2,3,4]:
        alarm=True 
    return render_template('message.html',title=a['title'],alarm=alarm)



@app.route('/profile',methods=['GET'])
def profile():
    a=UserDetails().get_details(session['user_id'])
    if a['code']==0:
        flash(a['message'], category='warning')
        alarm=True 
        return render_template('message.html',title=a['title'],alarm=alarm)
    return render_template('profile.html',profile=1,title=a['title'],data=a)

@app.route('/update_profile',methods=['GET','POST'])
def update_profile():
    a=UserDetails().get_details(session['user_id'])
    if a['code']==0:
        flash(a['message'], category='warning')
        alarm=True 
        return render_template('message.html',title=a['title'],alarm=alarm)
    return render_template('update_profile.html',profile=1,title='Update Profiel',data=a)



@app.route('/profile',methods=['POST'])
def updated_profile():
    user_id,username,email,dob,password,cnf_password=session['user_id'],session['username'],session['email'],request.form['dob'],request.form['password'],request.form['cnf_password']
    if password!=cnf_password:
        flash('Password not matched', category='warning')
        alarm = True
        return render_template('update_profile.html',title='Create account',alarm=alarm)
    
    b=UpdateUser().update(user_id,dob,password)
    a=UserDetails().get_details(session['user_id'])
    if a['code']==0:
        flash(a['message'], category='warning')
        alarm=True 
        return render_template('message.html',title=a['title'],alarm=alarm)
    flash(b['message'], category='warning')
    alarm=False
    return render_template('profile.html',title=b['title'],alarm=alarm,data=a)

@app.route('/api/docs',methods=['GET','POST'])
def documentation():
    return render_template('docs.html',title='Documentation',api=True)
    