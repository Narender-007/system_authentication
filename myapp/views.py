import datetime

from django.db import connections
from django.shortcuts import render
import io
from myapp.retriveimage import retimage, retimageWITHnames
import PIL.Image
import cv2
import numpy
from myapp.deduplicate import is_duplicate
import glob
import os
import random


# Create your views here.
def home(request):
    return render(request, 'index.html')


def reg(request):
    return render(request, 'home.html')


def log(request):
    return render(request, 'login.html')


def logout(request):
    return render(request, 'index.html')


def uhome(request):
    uid = request.session['uid']
    return render(request, 'uhome.html', {'uid': uid})


def upload(request):
    return render(request, 'upload.html')


def req(request):
    uid = request.session['uid']
    fid = request.POST['fid']
    sta = 'pending'
    print(fid)
    d = datetime.datetime.now()
    val = (uid, fid, sta, d)
    con = connections['mysql']
    mycursor = con.cursor()
    mycursor.execute('insert into freq values(%s,%s,%s,%s)', val)
    return render(request, 'search.html')


def search(request):
    return render(request, 'search.html')


def approve(request):
    uid = request.session['uid']
    fid = request.POST['fid']
    con = connections['mysql']
    print(fid)
    mycursor = con.cursor()
    mycursor.execute("update freq set status1='Approve' where fid='" + uid + "' and date1='" + fid + "'")
    return render(request, 'uhome.html')


def reject(request):
    uid = request.session['uid']
    fid = request.POST['fid']
    con = connections['mysql']
    mycursor = con.cursor()
    mycursor.execute("update freq set status1='Reject' where fid='" + uid + "' and date1='" + fid + "'")
    return render(request, 'uhome.html')


def sea(request):
    con = connections['mysql']
    mycursor = con.cursor()
    uid = request.session['uid']
    frnd = request.POST['frnd']
    mycursor.execute(
        "select name,mobile,location,email from user where name like '%" + frnd + "%' and email!='" + uid + "'")
    result = mycursor.fetchall()
    return render(request, 'view.html', {'result': result})


def frnd(request):
    con = connections['mysql']
    mycursor = con.cursor()
    uid = request.session['uid']
    p = 'pending'
    val = (uid, p)
    mycursor.execute('select * from freq where fid=%s and status1=%s', val)
    result = mycursor.fetchall()
    return render(request, 'frnd.html', {'result': result})


def msg(request):
    con = connections['mysql']
    mycursor = con.cursor()
    uid = request.session['uid']
    mycursor.execute("select * from msg where fid='" + uid + "'")
    result = mycursor.fetchall()
    return render(request, 'msg.html', {"result": result})


def msgs(request):
    con = connections['mysql']
    mycursor = con.cursor()
    fid = request.session['uid']
    name = request.POST['fname']
    uname = request.POST['msg']
    d = datetime.datetime.today()
    val = (fid, name, uname, d)
    mycursor.execute("insert into msg values(%s,%s,%s,%s)", val)
    myresult = mycursor.execute
    con.commit()
    return render(request, 'upload.html')


def login(request):
    con = connections['mysql']
    mycursor = con.cursor()
    uname = request.POST['uid']
    pwd = request.POST['pwd']
    val = (uname, pwd)
    mycursor.execute("select * from user where email='" + uname + "' and password='" + pwd + "' and status1='Approved'")
    myresult = mycursor.fetchall()
    i = 0
    for x in myresult:
        i += 1
    if i > 0:
        request.session['uid'] = uname
        images, label = retimageWITHnames(con, request.session['uid'])
        print("label:", label)
        files = glob.glob('media/dump/*.jpg')
        for f in files:
            print(f)
            os.remove(f)
        paths = []
        dicti = {}
        j = 0
        for image in images:
            cv2.imwrite(f"media/dump/temp{j}.jpg", numpy.array(image))
            dicti[f"/media/dump/temp{j}.jpg"] = label[j]
            j += 1
        if j <= 3:
            return render(request, 'uhome.html', {"uid": uname})
        else:
            rn = random.randint(0, j - 1)
            k = 0
            for key in dicti:
                if rn == k:
                    paths.append(key)
                    val = (uname, key, dicti[key], 1)
                    mycursor.execute("insert into login values(%s,%s,%s,%s)", val)
                    res = mycursor.execute
                    con.commit
                k += 1
            print(paths)
            s = []
            for key in dicti:
                s.append(dicti[key])
            l = set(s)
            return render(request, 'ulog.html', {"paths": paths, "rs": l, "att": 1})
    else:
        return render(request, 'login.html')


def reg1(request):
    con = connections['mysql']
    mycursor = con.cursor()
    name = request.POST['name']
    uname = request.POST['uname']
    pwd = request.POST['password']
    mob = request.POST['mob']
    loc = request.POST['loc']
    gen = request.POST['gen']
    val = (name, uname, pwd, mob, gen, loc, 'Approved')
    mycursor.execute("insert into user values(%s,%s,%s,%s,%s,%s,%s)", val)
    myresult = mycursor.execute
    con.commit()
    return render(request, 'login.html')


def post1(request):
    return render(request, 'post.html')


def pview(request):
    db = connections['mysql']
    images, label = retimageWITHnames(db, request.session['uid'])
    files = glob.glob('media/dump/*.jpg')
    for f in files:
        print(f)
        os.remove(f)
    paths = []
    dicti = {}
    i = 0
    for image in images:
        cv2.imwrite(f"media/dump/temp{i}.jpg", numpy.array(image))
        dicti[f"/media/dump/temp{i}.jpg"] = label[i]
        i += 1
    return render(request, 'pview.html', {"paths": dicti})


def upload1(request):
    db_conn = connections['mysql']
    images = retimage(db_conn, request.session['uid'])
    mycursor = db_conn.cursor()
    name = request.POST["name"]
    picture = request.FILES["picture"].read()
    file_like = io.BytesIO(picture)
    img = PIL.Image.open(file_like)
    uid = request.session['uid']
    image = is_duplicate(img, images)
    cv2.imwrite("media/temp.jpg", image)
    image = PIL.Image.fromarray(image.astype('uint8'), 'RGB')
    # image.show()
    # images = image.objects.all()
    # Hotels = Image.objects.all()
    d = datetime.datetime.now()
    sql = "INSERT INTO post VALUES (%s, %s, %s, %s)"
    val = (uid, picture, name, d)
    mycursor.execute(sql, val)
    db_conn.commit()
    return render(request, "post.html")


def verify(request):
    uid = request.session['uid']
    ps = request.POST['ps']
    print(ps)
    con = connections['mysql']
    mycursor = con.cursor()
    mycursor.execute("select * from login where uid='" + uid + "' and tags ='" + ps + "'")
    myresult = mycursor.fetchall()
    i = 0
    for x in myresult:
        i += 1
    mycursor.execute("select att from login where uid='" + uid + "'")
    rs = mycursor.fetchall()
    att = 0
    for a in rs:
        for o in a:
            att = o

    if i == 1 and att <= 3:
        mycursor.execute("delete from login where uid='" + uid + "'")
        mycursor.execute
        con.commit()
        return render(request, 'uhome.html', {"uid": uid})
    else:
        att += 1
        if att == 4:
            mycursor.execute("update user set status1='Blocked' where email='" + uid + "'")
            mycursor.execute
            con.commit()
            mycursor.execute("delete from login where uid='" + uid + "'")
            mycursor.execute
            con.commit()
            return render(request, 'block.html')
        else:
            images, label = retimageWITHnames(con, request.session['uid'])
            files = glob.glob('media/dump/*.jpg')
            for f in files:
                os.remove(f)
            paths = []
            dicti = {}
            j = 0
            for image in images:
                cv2.imwrite(f"media/dump/temp{j}.jpg", numpy.array(image))
                dicti[f"/media/dump/temp{j}.jpg"] = label[j]
                j += 1
            rn = random.randint(0, j - 1)
            k = 0

            for key in dicti:
                if rn == k:
                    paths.append(key)
                    val = (key, dicti[key], att, uid)
                    mycursor.execute("update login set img=%s, tags=%s, att=%s where uid=%s", val)
                    res = mycursor.execute
                    con.commit
                k += 1
            s = []
            for key in dicti:
                s.append(dicti[key])
            l = set(s)
            return render(request, 'ulog.html', {"paths": paths, "rs": l, "att": att})
