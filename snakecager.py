#!/bin/env/python
import traceback
import rowop
from flask import Flask, redirect, render_template, request, url_for, session, flash

app = Flask(__name__)
app.config["SECRET_KEY"] = "development key"

def createMatrix(form):
    # Find the matrix entries
    keys = sorted(filter(lambda x: x[0] == "a", form.keys()))
    m = int(keys[-1][1])
    n = int(keys[-1][2])
    matrix = [[rowop.F(0) for xi in range(n)] for x in range(m)]
    for key in keys:
            val = form[key]
            matrix[int(key[1])-1][int(key[2])-1] = rowop.F(val)
    return matrix

@app.route("/reset", methods=["GET"])
def reset():
    session["comments"] = ""
    #session["matrix"] =  ""
    return render_template("index.html", comments=session["comments"].split(";"), matrix=[[rowop.F(1) if (i==j) else rowop.F(0) for i in range(int(session["n"]))] for j in range(int(session["m"]))])


@app.route("/resize", methods=["POST"])
def resize():
    try:
        session["m"] = request.form["M"]
        session["n"] = request.form["N"]
        matrix = [[rowop.F(1) if (i==j) else rowop.F(0) for i in range(int(session["n"]))] for j in range(int(session["m"]))]
        return render_template("index.html", comments=[], matrix=matrix)
    except:
        pass

    return redirect(url_for('index'))
    

@app.route("/", methods=["GET", "POST"])
def index():
    if "comments" not in session:
        session["comments"] = ""
    if "m" not in session:
        session["m"] = "3"
    if "n" not in session:
        session["n"] = "3"
    if request.method == "GET":
        return render_template("index.html",
                                   comments=session["comments"].split(";"),
                                   matrix=[[rowop.F(1) if (i==j) else rowop.F(0) for i in range(int(session["n"]))] for j in range(int(session["m"]))])

    # if request is not GET, we know it's post
    try:
        comments = session["comments"].split(";")
        row1 = int(request.form["row1"])
        row2 = int(request.form["row2"])
        mul = request.form["multiplier"]
        op = request.form["op"]

        tmpmatrix = createMatrix(request.form)
        newMat = rowop.printRowOp(tmpmatrix, row1, row2, rowop.F(mul), op)
        comments.insert(0, "Here is your latex:")
        comments.insert(1, str(newMat[1]))
        session["comments"] += ";".join(comments)
        return render_template("index.html", comments=comments, matrix=newMat[0])
    except:
        comments.append("Exception thrown")
        comments.append(traceback.format_exc())


    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
