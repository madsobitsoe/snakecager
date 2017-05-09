#!/bin/env/python
import traceback
import rowop
from flask import Flask, redirect, render_template, request, url_for, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "development key"

def create_matrix(form):
    """Creates a matrix from form input"""
    # Find the matrix entries
    keys = sorted(filter(lambda x: x[0] == "a", form.keys()))
    m_rows = int(keys[-1][1])
    n_cols = int(keys[-1][2])
    matrix = [[rowop.F(0) for xi in range(n_cols)] for x in range(m_rows)]
    for key in keys:
        val = form[key]
        matrix[int(key[1])-1][int(key[2])-1] = rowop.F(val)
    return matrix

@app.route("/reset", methods=["GET"])
def reset():
    session["comments"] = ""
    #session["matrix"] =  ""
    return render_template("index.html",
                           comments=session["comments"].split(";"),
                           matrix=[[rowop.F(1) if (i == j) else rowop.F(0)
                                    for i in range(int(session["n"]))]
                                   for j in range(int(session["m"]))])


@app.route("/resize", methods=["POST"])
def resize():
    try:
        session["m"] = request.form["M"]
        session["n"] = request.form["N"]
        matrix = [[rowop.F(1) if (i == j) else rowop.F(0) for i in range(int(session["n"]))]
                  for j in range(int(session["m"]))]
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
                               matrix=[[rowop.F(1) if (i == j)
                                        else rowop.F(0) for i in range(int(session["n"]))]
                                       for j in range(int(session["m"]))])

    # if request is not GET, we know it's post
    try:
        comments = session["comments"].split(";")
        row1 = int(request.form["row1"])
        row2 = int(request.form["row2"])
        multiplier = rowop.F(request.form["multiplier"])
        operation = request.form["op"]

        tmpmatrix = create_matrix(request.form)
        new_mat = rowop.print_row_op(tmpmatrix, row1, row2, rowop.F(multiplier), operation)
        comments.insert(0, "Here is your latex:")
        comments.insert(1, str(new_mat[1]))
        session["comments"] += ";".join(comments)
        return render_template("index.html", comments=comments, matrix=new_mat[0])
    except:
        comments.append("Exception thrown")
        comments.append(traceback.format_exc())


    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
