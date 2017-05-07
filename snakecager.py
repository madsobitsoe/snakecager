import rowop
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["DEBUG"] = True
comments = []
m = 3
n = 3
matrix = [[rowop.F(1) for i in range(m)] for j in range(n)]
def updateMatrix(form):
    for key in sorted(form.keys()):
        if (key[0] == "a"):
            val = form[key]
            matrix[int(key[1])-1][int(key[2])-1] = rowop.F(val)

def toMatrix(form):
    updateMatrix(form)
    s = ""
    for row in matrix:
        s += "[ "
        for col in row:
            s += "%s " % col
        s += "]\n"
    return s


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", comments=comments, matrix=matrix)
    updateMatrix(request.form)
    #comments.append(toMatrix(request.form))
    #for key in sorted(request.form):
        #comments.append("Key: %s, value: %s" % (key, request.form[key]))
    try:
        global matrix
        #comments.append(rowop.fracToLatexMatrix(matrix))

        #comments.append(rowop.fracToLatexMatrix(matrix))
        row1 = int(request.form["row1"])
        row2 = int(request.form["row2"])
        mul = request.form["multiplier"]
        op = request.form["op"]
        comments.append("Here is your latex:")
        comments.append(rowop.printRowOp(matrix, row1, row2, rowop.F(mul), op))
    except:
        pass

    try:
        global m
        m = int(request.form["M"])
        global n
        n = int(request.form["N"])
        global matrix
        matrix = rowop.stringToFracMatrix([["1" for i in range(m)] for j in range(n)])
    except:
        pass

    return redirect(url_for('index'))
