from flask import Flask,render_template
import json
app = Flask(__name__)   

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

@app.route('/')
def inicio():
	return render_template("index.html")


app.run('0.0.0.0',8080,debug=True)









































