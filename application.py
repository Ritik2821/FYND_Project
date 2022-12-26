from flask import *
import sqlite3
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_student")
def add_student():
    return render_template("add_student.html")

@app.route("/saverecord",methods = ["POST","GET"])
def saveRecord():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            gender = request.form["gender"]
            contact = request.form["contact"]
            dob = request.form["dob"]
            address = request.form["address"]
            with sqlite3.connect("student_detials.db") as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT into Student_Info (name, email, gender, contact, dob, address) values (?,?,?,?,?,?)",(name, email, gender, contact, dob, address))
                connection.commit()
                msg = "Student detials successfully Added"
        except:
            connection.rollback()
            msg = "We can not add Student detials to the database"
        finally:
            return render_template("success_record.html",msg = msg)
            connection.close()


@app.route("/delete_student")
def delete_student():
    return render_template("delete_student.html")



@app.route("/student_info")
def student_info():
    connection = sqlite3.connect("student_detials.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("select * from Student_Info")
    rows = cursor.fetchall()
    return render_template("student_info.html",rows = rows)



@app.route("/update_info")
def update_student_info():
    return render_template("update.html")


@app.route("/updaterecord",methods =["POST"])
def updaterecord():
    id = request.form["id"]
    u1 = request.form["u1"]
    u2 = request.form["u2"]
    updatedFields=(u1,u2,id)
    with sqlite3.connect("student_detials.db") as connection:

        cursor = connection.cursor()
        cursor.execute("select * from Student_Info where id=?", (id,))
        rows = cursor.fetchall()
        if not rows == []:
           # cursor.execute('UPDATE "{}" SET ? =? WHERE id=?'.format(Student_Info.replace('"', '""')),
           #             (times_before + 1, food))
           if u1 == "Address":
               cursor.execute("Update Student_Info set Address=? where id=?",(u2,id,))
              # msg = "Student details Updated  successfully"
              # return render_template("update_student.html", msg=msg)
           elif u1=="Contact":
               cursor.execute("Update Student_Info set Contact=? where id=?", (u2, id,))
           elif u1=="Email":
               cursor.execute("Update Student_Info set Email=? where id=?", (u2, id,))
           msg = "Student details Updated  successfully"
           return render_template("update_student.html", msg=msg)


        else:
            msg = "can't be updated"
            return render_template("update_student.html", msg=msg)



# @app.route("/delete_student")
# def delete_student():
#     return render_template("delete_student.html")


@app.route("/deleterecord",methods = ["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("student_detials.db") as connection:

        cursor = connection.cursor()
        cursor.execute("select * from Student_Info where id=?", (id,))
        rows = cursor.fetchall()
        if not rows == []:

            cursor.execute("delete from Student_Info where id = ?",(id,))
            msg = "Student detail successfully deleted"
            return render_template("delete_record.html", msg=msg)

        else:
            msg = "can't be deleted"
            return render_template("delete_record.html", msg=msg)

        
        
if __name__ == "__main__":
    app.run(debug = True , port = 5001)
