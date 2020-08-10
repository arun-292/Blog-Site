from flask import Flask, render_template,redirect,request,url_for,session,jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client['Login_Database']

@app.route('/')
def home():
    return redirect(url_for('signin'))

@app.route('/homepage')
def homepage():
    dbs=db.users.find_one({'Email':session['Email']})
    return render_template('homepage.html',data=dbs)


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        if request.form['fullname'] and request.form['Email'] and request.form['password']:
            users=db.users
            existing_user = users.find_one({'Email':request.form['Email']})
            if existing_user is None:
                users.insert({'fullname' : request.form['fullname'], 'Email':request.form['Email'], 'password': request.form['password'], 'posts':[] })
                return redirect(url_for('signin'))
            else:
                return 'that email already exist!'
        else:
            return 'enter valid details'
    else:
        return render_template('signup.html')

@app.route('/signin',methods=['POST','GET'])
def signin():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'Email':request.form['Email']})
        if existing_user is None:
            return redirect(url_for('signup'))
        else:
            if request.form['password'] == existing_user['password']:
                session['Email'] = existing_user['Email']
                return redirect(url_for('homepage'))
            else:
                return 'invalid details...'
    else:
        return render_template('signin.html')

@app.route('/handlesession')
def handlesession():
    session.clear()
    return redirect(url_for('signin'))

@app.route('/posts/<string:_id>',methods=['GET','POST'])
def posts(_id):
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['description']
        dbs=db.users.find_one({"Email" : session['Email']})
        post_array=[]
        for i in dbs['posts']:
            post_array.append(i)
        post_array.append({'title' : request.form['title'], 'description':request.form['description']})
        result={
            '_id' : dbs['_id'],
            'fullname': dbs['fullname'],
            'Email': dbs['Email'],
            'password' : dbs['password'],
            'posts' : post_array
        }
        db.users.remove({'Email': session['Email']})
        db.users.insert(result)
        return redirect(url_for('homepage'))

        #dbs.update({'$push': {'title' : request.form['title'], 'description':request.form['description']}})
    else:
        return redirect(url_for('homepage'))

@app.route('/posts/delete/<string:title>/<string:description>')
def delete(title,description):
    dbs = db.users.find_one({'Email': session['Email']})
    post_array=[]
    for i in dbs['posts']:
        if i['title'] == title:
            if i['description'] == description:
                continue
            else:
                post_array.append(i)
        else:
            post_array.append(i)
    result={
            '_id' : dbs['_id'],
            'fullname': dbs['fullname'],
            'Email': dbs['Email'],
            'password' : dbs['password'],
            'posts' : post_array
        }
    db.users.remove({'Email': session['Email']})
    db.users.insert(result)
    return redirect(url_for('homepage'))

@app.route('/posts/update/<string:title>/<string:description>',methods=['GET','POST'])
def update(title,description):
    if request.method == 'POST':
        dbs = db.users.find_one({'Email': session['Email']})
        post_array=[]
        for i in dbs['posts']:
            if i['title'] == title:
                if i['description'] == description:
                    continue
                else:
                    post_array.append(i)
            else:
                post_array.append(i)
        result={
            '_id' : dbs['_id'],
            'fullname': dbs['fullname'],
            'Email': dbs['Email'],
            'password' : dbs['password'],
            'posts' : post_array
        }
        db.users.remove({'Email': session['Email']})
        db.users.insert(result)

        dbs=db.users.find_one({"Email" : session['Email']})
        post_array=[]
        for i in dbs['posts']:
            post_array.append(i)
        post_array.append({'title' : request.form['title'], 'description':request.form['description']})
        result={
            '_id' : dbs['_id'],
            'fullname': dbs['fullname'],
            'Email': dbs['Email'],
            'password' : dbs['password'],
            'posts' : post_array
        }
        db.users.remove({'Email': session['Email']})
        db.users.insert(result)
        return redirect(url_for('homepage'))

    else:
        dbs=db.users.find_one({'Email':session['Email']})
        return render_template('update.html',title=title,description=description)

if __name__ == "__main__":
    app.secret_key='arun'
    app.run(debug=True)