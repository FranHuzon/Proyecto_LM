from flask import Flask,render_template,request
import json
app = Flask(__name__)   

import requests
import os 
key=os.environ['key']

@app.route('/')
def inicio():
	return render_template("index.html")

@app.route('/buscar',methods=['GET','POST'])
def buscar():
	buscar=request.form.get("buscar")
	url="https://www.googleapis.com/books/v1/volumes"
	busqueda=buscar
	payload={"q":busqueda,"key":key}
	r=requests.get(url,params=payload)
	
	if r.status_code==200:
		a=r.json()
		lista=[]
		for i in a["items"]:
			lista.append(i["volumeInfo"]["title"])
		print(lista)
		#resultado=a["items"][0]["volumeInfo"]["title"]
		return render_template('mostrar.html',l=lista)







app.run('0.0.0.0',8080,debug=True)


































