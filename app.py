from flask import Flask,render_template,request,session,redirect
from requests_oauthlib import OAuth2Session
import json
app = Flask(__name__)   

import requests
import os
key=os.environ['key']

@app.route('/')
def inicio():
	return render_template("index.html")

@app.route('/buscar',methods=['GET', 'POST'])
def buscar():
	busca=request.form.get("buscar")
	url="https://www.googleapis.com/books/v1/volumes"
	busqueda=busca
	campos='items(selfLink,volumeInfo(authors,categories,imageLinks/smallThumbnail,title))'
	payload={'q':busqueda,'fields':campos,'key':key}
	r=requests.get(url, params=payload)
	
	if r.status_code==200:
		a=r.json()
		lista=[]
		for i in a["items"]:
			lista.append(i)
		return render_template('mostrar.html',l=lista)

#### Oauth2
redirect_uri = 'https://oauth-jd.herokuapp.com/google_callback'
scope = ['https://www.googleapis.com/auth/userinfo.profile']
token_url = "https://accounts.google.com/o/oauth2/token"

@app.route('/google')
def google():
	return render_template("oauth2.html")
 
def token_valido():
	try:
		token=json.loads(session["token"])
	except:
		token = False
	if token:
		token_ok = True
		try:
			oauth2 = OAuth2Session(os.environ["client_id"], token=token)
			r = oauth2.get('https://www.googleapis.com/oauth2/v1/userinfo')
		except TokenExpiredError as e:
			token_ok = False
	else:
		token_ok = False
	return token_ok

@app.route('/perfil')
def info_perfil():
	if token_valido():
		return redirect("/perfil_usuario")
	else:
		oauth2 = OAuth2Session(os.environ["client_id"], redirect_uri=redirect_uri,scope=scope)
		authorization_url, state = oauth2.authorization_url('https://accounts.google.com/o/oauth2/auth')
		session.pop("token",None)
		session["oauth_state"]=state
		return redirect(authorization_url)  

@app.route('/google_callback')
def get_token():
	oauth2 = OAuth2Session(os.environ["client_id"], state=session["oauth_state"],redirect_uri=redirect_uri)
	token = oauth2.fetch_token(token_url, client_secret=os.environ["client_secret"],authorization_response=request.url[:4]+"s"+request.url[4:])
	session["token"]=json.dumps(token)
	return redirect("/mi_coleccion")



@app.route('/logout')
def salir():
	session.pop("token",None)
	return redirect("/perfil")

@app.route('/mi_coleccion')
def coleccion():
	if token_valido():
		token=json.loads(session["token"])
		oauth2 = OAuth2Session(os.environ["client_id"], token=token)
	
		url="https://www.googleapis.com/books/v1/mylibrary/bookshelves/0/volumes"
		campos='items(selfLink,volumeInfo(imageLinks/smallThumbnail,title))'
		payload={'fields':campos,'key':key}
	
		r=requests.get(url,params=payload)

		if r.status_code==200:
			a=r.json()
			lista=[]
			for i in a["items"]:
				lista.append(i)
			return render_template('mi_coleccion.html',l=lista)
	else:
		return redirect('/')



if __name__ == '__main__':
	port=os.environ["PORT"]    
	app.run('0.0.0.0',int(port),debug=True)