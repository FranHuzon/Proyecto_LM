from flask import Flask,render_template,request
import json
app = Flask(__name__)   

import os 
key=os.environ['key']
#url="https://www.googleapis.com/books/v1/volumes"
#payload={"q":"Idhún+inauthor:Laura Gallego","key":key}
#r=requests.get(url,params=payload)


#if r.status_code==200:
	#a=json.loads(r.text[1:-2])
	#a=r.json()
#	a=json.loads(r.text)
#	print(a["items"][0]["volumeInfo"]["title"])

@app.route('/')
def inicio():
	return render_template("index.html")

@app.route('/buscar',methods=['GET','POST'])
def buscar():
	titulo=request.form.get("titulo")
	autor=request.form.get("autor")
	url="https://www.googleapis.com/books/v1/volumes"
	payload={}
	payload["q"]=titulo
	payload["+inauthor"]=input('Autor: ')
	payload["key"]=key
	r=requests.get(url,params=payload)
	
	if r.status_code==200:
		a=r.json()
		resultado=a["items"][0]["volumeInfo"]["title"]
		return resultado







app.run('0.0.0.0',8080,debug=True)


































