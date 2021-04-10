import base64
import PIL.Image
import io


def retimage(db_conn, user):
    img_set = []
    mycursor = db_conn.cursor()
    html = "SELECT image FROM  post where uid ='"+user+"'"

    val = user
    print(html, val)
    mycursor.execute(html)
    images = mycursor.fetchall()
    for image in images:
        print("data2", len(image[0]))
        file_like = io.BytesIO(image[0])
        img = PIL.Image.open(file_like)
        img_set.append(img)
        # img.show()
    return img_set


def retimageWITHnames(db_conn, user):
    img_set = []
    name_set = []
    fid_det = []
    mycursor = db_conn.cursor()
    html = "SELECT UserId FROM  freq where fid ='" + user + "'"
    val = user
    print(html, val)
    mycursor.execute(html)
    fids = mycursor.fetchall()
    for fid in fids:
        fid_det.append(fid[0])
    fid_det.append(user)
    print(fid_det)
    for fid in set(fid_det):
        html = "SELECT image,tags FROM  post where uid ='" + user + "'"
        val = user
        print(html, val)
        mycursor.execute(html)
        images = mycursor.fetchall()
        for image in images:
            print("data2", len(image[0]))
            file_like = io.BytesIO(image[0])
            img = PIL.Image.open(file_like)
            img_set.append(img)
            name_set.append(image[1])
            # img.show()
    return img_set, name_set
