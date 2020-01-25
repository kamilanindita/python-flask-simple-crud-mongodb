from flask import Flask,render_template, request, url_for, redirect
from pymongo import MongoClient
from bson import ObjectId # For ObjectId to work  
 


app = Flask(__name__)
#mongodb
client = MongoClient('mongodb://localhost:27017/') #uri
db = client.mywebsite_crud  #database name
mongo = db.buku #collection



@app.route("/")
def index():
    title="Index"
    return render_template("index.html",title=title)
    
@app.route("/buku")
def buku():
    title="Buku"

    Buku=[]
    data = mongo.find()
    for buku in data :
        Buku.append(buku)

    return render_template("buku.html",data=Buku, title=title)

@app.route("/buku/add")
def add():
    title="Tambah"
    return render_template("tambah.html",title=title)
   
@app.route("/buku/tambah/save",methods=["POST"])
def save():
    penulis=request.form["penulis"]
    judul=request.form["judul"]
    kota=request.form["kota"]
    penerbit=request.form["penerbit"]
    tahun=request.form["tahun"]
    
    data={
        'penulis':penulis,
        'judul':judul,
        'kota':kota,
        'penerbit':penerbit,
        'tahun':tahun
    }
    
    mongo.insert(data)

    return redirect(url_for('buku'))
  

@app.route("/buku/edit/<id>")
def edit(id):
    title="Edit"
    
    Buku=[]
    data = mongo.find({"_id":ObjectId(id)})
    for buku in data :
        Buku.append(buku)
    return render_template("edit.html",data=Buku,title=title)


   
@app.route("/buku/update/<id>",methods=["POST"])
def update(id):
    penulis=request.form["penulis"]
    judul=request.form["judul"]
    kota=request.form["kota"]
    penerbit=request.form["penerbit"]
    tahun=request.form["tahun"]
    
    data_update={
        'penulis':penulis,
        'judul':judul,
        'kota':kota,
        'penerbit':penerbit,
        'tahun':tahun
    }
   
    mongo.update({"_id":ObjectId(id)}, {'$set':data_update})
    return redirect(url_for('buku'))

@app.route("/buku/delete/<id>")
def delete(id):
    mongo.remove({"_id":ObjectId(id)})
    return redirect(url_for('buku'))
    
if __name__ == '__main__':
    app.run(debug=True)
