import traceback
import rowop
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for, session

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
    return render_template("index.html", comments=session["comments"].split(";"), matrix=[[rowop.F(1) for i in range(3)] for j in range(3)])

@app.route("/", methods=["GET", "POST"])
def index():
    if "comments" not in session:
        session["comments"] = ""

    if request.method == "GET":
        return render_template("index.html", comments=session["comments"].split(";"), matrix=[[rowop.F(1) for i in range(3)] for j in range(3)])

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

    try:
        m = int(request.form["M"])
        n = int(request.form["N"])
        matrix = rowop.stringToFracMatrix([["1" for i in range(m)] for j in range(n)])
        return render_template("index.html", comments=comments, matrix=matrix)

    except:
        pass

    return redirect(url_for('index'))
