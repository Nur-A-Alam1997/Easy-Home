import gc
import os

from EasyHome import app
from flask import render_template, request, flash, session, redirect, url_for, send_from_directory, jsonify
from wtforms import form
from functools import wraps
import sqlite3
from EasyHome.register import RegisterForm
from EasyHome import db


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('logintransparent'))
    return wrap


@app.route('/', methods=['GET'])
def home():
    data = db.engine.execute(
        "SELECT address,housetype,rentfee,id from post_ad_table").fetchall()
    db.session.commit()
    print(data)
    x = len(data)
    if x > 6:
        l = x - 6
    else:
        l = 0
    print(l)
    if x > 6:
        li = range(x-6, x)
        li = [*li]
        li.reverse()
    else:
        li = range(0, x)
        li = [*li]
        li.reverse()

    img = []

    print(li)
    for d in li:
        b = str(data[d][3]) + ".jpg"
        img.append(b)

    img = [*img]
    img.reverse()
    print(img)
    return render_template("index.html", data=data, li=li, img=img, l=l)


@app.route('/profile', methods=['GET'])
def profile():
    data = db.engine.execute(
        "SELECT name,username,email,Mobile_no,Address from registration_table  WHERE username = ?", [session['username']]).fetchall()
    db.session.commit()
    data_n = db.engine.execute(
        "SELECT address,housetype,rentfee,id from post_ad_table WHERE username=?", [session['username']]).fetchall()
    db.session.commit()

    x = len(data_n)
    print(x)

    img = []

    if x > 6:
        li = range(x-6, x)
        li = [*li]
        li.reverse()
    else:
        li = range(0, x)
        li = [*li]
        li.reverse()

    for d in li:
        print(d)
        print(data_n[d][3])
        img.append(str(data_n[d][3])+".jpg")

    if x > 6:
        l = x - 6
    else:
        l = 0
    img = [*img]
    img.reverse()

    usr_image = session['username']+'.jpg'
    return render_template("profile.html", data=data, data_n=data_n, li=li, img=img, l=l, usr_image=usr_image)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'logged_in' not in session:
        return redirect(url_for("home"))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobileno = request.form['mobileno']
        address = request.form['address']

        db.engine.execute("UPDATE registration_table SET name=?, email =?, Mobile_no = ?, Address=? WHERE username= ?",
                          (name, email, mobileno, address, [session['username']]))

        db.session.commit()

        return redirect(url_for('profile'))
    return render_template('edit_profile.html')


@app.route('/description/<string:id>', methods=['GET'])
def description(id):
    homeId = id
    id_n = homeId.split()
    g_data = db.engine.execute(
        "SELECT username,address,housetype,contactinformation,id from post_ad_table WHERE id=?", id).fetchone()

    if session.get("username"):
        fab_id = db.engine.execute(
            "SELECT id from fav_tab WHERE id=? AND username=?", (int(id), session['username'])).fetchone()
    else:
        fab_id = None
    des_data = db.engine.execute(
        "SELECT description from post_ad_table WHERE id=?", id).fetchall()

    img = id+'.jpg'
    return render_template("description.html", g_data=g_data, des_data=des_data, filename=img, fab_id=fab_id)


@app.route('/update', methods=['GET'])
def update():
    if not session.get('logged_in'):
        data = {"error": "please,log in"}
        res = jsonify(data)
        # responseText
        return "please,log in", 403
    homeId = request.args.get('query')
    id_n = homeId.split()
    fab_id = db.engine.execute(
        "SELECT id from fav_tab WHERE id=? AND username=?", (int(id_n[2]), session['username'])).fetchone()

    print("favourite", fab_id, "USername", session['username'], sep="---")
    if fab_id:
        db.engine.execute("DELETE FROM fav_tab WHERE id=? AND username=?", (int(
            id_n[2]), session['username']))
    else:
        db.engine.execute(
            "INSERT INTO fav_tab(id ,username) VALUES(?, ?)",
            ((int(id_n[2]), session['username'])))
    db.session.commit()

    return 'success',201



@app.route('/favourite', methods=['GET', 'POST'])
def favourite():
    if not session.get("username"):
        return 'Sorry Sir, log in first'
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    db.engine.execute(
        "SELECT address,housetype,rentfee,id FROM fav_tab")
    data = cursor.fetchall()

    x = len(data)
    print(x)

    img = []
    if x > 6:
        li = range(x - 6, x)
        li = [*li]
        li.reverse()
    else:
        li = range(0, x)
        li = [*li]
        li.reverse()

    for d in li:
        print(d)
        print(data[d][3])
        img.append(str(data[d][3]) + ".jpg")

    if x > 6:
        l = x - 6
    else:
        l = 0
    img = [*img]
    img.reverse()

    return render_template("favourite.html", data=data, li=li, img=img, l=l)



@app.route('/search/<string:division>', methods=['GET', 'POST'])
def search_dhaka(division):
    if request.method == 'POST' and session.get("username"):
        division = division.upper()
        area = request.form.get('area')
        housetype = request.form.get('housetype')

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        db.engine.execute(
            "SELECT address,housetype,rentfee,id FROM post_ad_table where (housetype,division, area)=( ?, ?, ?)",
            (housetype, division, area))
        data = cursor.fetchall()

        x = len(data)
        print(x)

        img = []
        if x > 6:
            li = range(x - 6, x)
            li = [*li]
            li.reverse()
        else:
            li = range(0, x)
            li = [*li]
            li.reverse()

        for d in li:
            print(d)
            print(data[d][3])
            img.append(str(data[d][3]) + ".jpg")

        if x > 6:
            l = x - 6
        else:
            l = 0
        img = [*img]
        img.reverse()

        return render_template("search_dhaka.html", data=data, li=li, img=img, l=l)
    return render_template("search_"+division+".html")



@app.route('/post_ad', methods=['GET', 'POST'])
def post_ad():
    if request.method == 'POST' and session.get("username"):
        address = request.form['address']
        housetype = request.form.get('housetype')
        description = request.form['description']
        rentfee = request.form['rentfee']
        contactinformation = request.form['contactinformation']
        division = request.form.get('division')
        district = request.form.get('district')
        area = request.form.get('area')
        username = [session['username']]

        print(type(address), housetype, description, rentfee,
              contactinformation, division, district, area, username[0])

        db.engine.execute(
            "INSERT INTO post_ad_table( address, housetype, description, rentfee, contactinformation, division, district, area, username) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (address, housetype, description, rentfee, contactinformation, division, district, area, username[0]))

        db.engine.execute(
            "SELECT id FROM post_ad_table where ( address, housetype, description, rentfee, contactinformation, division, district, area, username)=(?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (address, housetype, description, rentfee, contactinformation, division, district, area, username[0]))
        data = cursor.fetchall()
        print("MY DATA", data)
        Id = str(data[0][0])+".jpg"
        print(Id)

        target = os.path.join(app.root_path, 'images/')
        # target = os.path.join(APP_ROOT, 'static/')
        print(target)
        if not os.path.isdir(target):
            os.mkdir(target)
        else:
            print("Couldn't create upload directory: {}".format(target))
        print(request.files.getlist("file"))
        for upload in request.files.getlist("file"):
            print(upload)
            print("{} is the file name".format(upload.filename))
            filename = upload.filename

            # Id = request.form['Id']
            # Id = Id + ".jpg"
            destination = "/".join([target, Id])
            print("Accept incoming file:", filename)
            print("Save it to:", destination)
            upload.save(destination)

        # Commit to DB
        db.session.commit()

        # Close connection

        return redirect("http://127.0.0.1:5000/")
    return render_template("post_ad.html")


@app.route('/profile/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/upload/<filename>')
def send_image1(filename):
    return send_from_directory("images", filename)


@app.route('/<filename>')
def send_image2(filename):
    return send_from_directory("images", filename)

# User loginmain


@app.route('/loginmain', methods=['GET', 'POST'])
def loginmain():
    if session.get("username"):
        return redirect(url_for("home"))
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        with conn:
            result = db.engine.execute(
                "SELECT * FROM registration_table WHERE username = ?", [username])
            if result > 0:
                data = cur.fetchone()
                password = data[3]

                if sha256_crypt.verify(password_candidate, password):
                    # Passed
                    session['logged_in'] = True
                    session['username'] = username

                    flash('You are now logged in', 'success')
                    return render_template('index.html')
                else:
                    error = 'Invalid login'
                    return render_template('loginmain.html', error=error)
                # Close connection
                cur.close()
            else:
                error = 'Username not found'
                return render_template('index.html', error=error)

    return render_template('loginmain.html')

# Check if user logged in
# def is_logged_in(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return f(*args, **kwargs)
#         else:
#             flash('Unauthorized, Please login', 'danger')
#             return redirect(url_for('logintransparent'))
#     return wrap

# Logout


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect("http://127.0.0.1:5000/")


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template("dashboard.html")


@app.route('/registertrans', methods=['GET', 'POST'])
def registertrans():
    if 'logged_in' in session:
        return redirect("/")
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        # password = sha256_crypt.encrypt(str(form.password.data))
        password = str(form.password.data)
        mobileno = form.mobileno.data
        address = form.address.data

        # Create cursor
        # cur = mysql.connection.cursor()
        # conn=sqlite3.connect("database.db")
        # cursor=conn.cursor()
        # Execute query
        db.engine.execute("INSERT INTO registration_table( name, username, email, password, Mobile_no, address) VALUES(?, ?, ?, ?, ?, ?)",
                          (name,  username, email, password, mobileno, address))

        db.engine.execute(
            "SELECT username FROM registration_table where (username)=(?)", [username]).fetchall()

        print(data[0][0])
        Id = str(data[0][0]) + ".jpg"
        print(Id)
        target = os.path.join(app.root_path, 'images/')
        # target = os.path.join(APP_ROOT, 'static/')
        print(target)
        if not os.path.isdir(target):
            os.mkdir(target)
        else:
            print("Couldn't create upload directory: {}".format(target))
        print(request.files.getlist("file"))
        for upload in request.files.getlist("file"):
            print(upload)
            print("{} is the file name".format(upload.filename))
            filename = upload.filename
            destination = "/".join([target, Id])
            print("Accept incoming file:", filename)
            print("Save it to:", destination)
            upload.save(destination)
        db.session.commit()
        flash('You are now registered and can log in', 'success')
        return redirect("http://127.0.0.1:5000/")
    return render_template('registertrans.html', form=form)


# User loginmain
@app.route('/logintransparent', methods=['GET', 'POST'])
def logintransparent():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        result = db.engine.execute(
            "SELECT * FROM registration_table WHERE username = ?", [username]).fetchone()
        print("my result:", result)
        if result:
            data = cursor.fetchone()
            password = result[3]
            if password_candidate == password:
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect("http://127.0.0.1:5000/")
            else:
                error = 'Invalid login'
                return render_template('logintransparent.html', error=error)
        else:
            error = 'Username not found'
            return render_template('logintransparent.html', error=error)

    return render_template('logintransparent.html')
