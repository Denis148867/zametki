from flask import Flask,render_template,request,url_for,redirect
import json

app = Flask(__name__)

@app.route('/')
def my_notes():
    with open("notes.json", "r", encoding="utf-8") as f:
        notes = json.load(f)
    return render_template("index.html",notes=notes)

@app.route('/add', methods=["POST","GET"])
def addnotest():
    error = ""
    if request.method == "POST":
        with open("notes.json", "r", encoding="utf-8") as f:
            notes = json.load(f)
        title = request.form["title"]
        text = request.form['text']
        if title not in notes.keys():
            notes[title] = text
            with open(f"notes.json", "w", encoding="utf-8") as f:
                json.dump(notes,  f, indent=4, ensure_ascii=False)
            return redirect(url_for("my_notes"))
        else:
            error = "такая заметка уже существует"
            return render_template("add.html", error=error)
    return render_template("add.html",error=error)


@app.route('/deltete/<key>', methods=["POST"])
def delnotes(key):
    with open("notes.json", "r", encoding="utf-8") as f:
        notes = json.load(f)
    del notes[key]
    with open(f"notes.json","w",encoding="utf-8") as f:
        json.dump(notes,f,indent=4,ensure_ascii=False)
    return redirect(url_for("my_notes"))

@app.route('/detail/<key>')
def detail(key):
    with open("notes.json", "r", encoding = "utf-8") as f:
        notes = json.load(f)
    file = notes[key]
    return render_template("detail.html", file = file,key = key)


@app.route('/edit/<key>', methods=['POST','GET'])
def edit(key):
    with open(f"notes.json", "r" ,encoding = "utf-8") as f:
        notes = json.load(f)
    file = notes[key]
    if request.method == "POST":
        new_file = request.form["text"]
        notes[key]=new_file
        with open(f"notes.json","w",encoding="utf-8") as f:
            json.dump(notes,f,indent=4,ensure_ascii=False)
        return redirect(url_for("my_notes"))
    return render_template("edit.html", file = file,key = key)





if __name__ == '__main__':
    app.run(debug=True)
