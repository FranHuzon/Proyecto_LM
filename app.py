from flask import Flask,render_template
import json
#import os 
#key=os.environ['key']
#url="https://www.googleapis.com/books/v1/volumes"
#payload={"q":"Idhún+inauthor:Laura Gallego","key":key}
#r=requests.get(url,params=payload)


#if r.status_code==200:
	#a=json.loads(r.text[1:-2])
	#a=r.json()
#	a=json.loads(r.text)
#	print(a["items"][0]["volumeInfo"]["title"])

@app.route('/',methods=["GET","POST"])
def inicio():
	if request.method=="GET":
		return render_template("index.html")












































