from flask import Flask,render_template,request,session,redirect
from requests_oauthlib import OAuth2Session
import json
from oauthlib.oauth2 import TokenExpiredError
import requests
import os

app = Flask(__name__)  
key=os.environ['key']
app.secret_key= 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
def inicio():
	return render_template("index.html")


@app.route('/sugerencias')
def sugerencias():
	
	if token_valido():
		token=json.loads(session["token"])
		oauth2 = OAuth2Session(os.environ["client_id"], token=token, scope=scope)
		url="https://www.googleapis.com/books/v1/volumes/recommended"
		campos='items(id,volumeInfo(imageLinks/thumbnail,title))'
		payload={'fields':campos,'key':key}
	
		r=oauth2.get(url,params=payload)

		if r.status_code==200:
			a=r.json()
			lista=[]
			for i in a["items"]:
				lista.append(i)
			return render_template('sugerencias.html',l=lista)
		else:
			return "fallo"
	else:
		return redirect('/entrar')




@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
	if session["token"]:
		url="https://www.googleapis.com/books/v1/mylibrary/bookshelves/0/volumes"
		campos='items(id)'
		payload={'fields':campos,'key':key}
		r=oauth2.get(url,params=payload)

		if r.status_code==200:
			a=r.json()
			lista_colecc=[]
			for i in a["items"]:
				lista_colecc.append(i["id"])	
	else:
		lista_colecc=None


	busca=request.form.get("buscar")
	url="https://www.googleapis.com/books/v1/volumes"
	busqueda=busca
	campos='items(id,volumeInfo(authors,imageLinks/smallThumbnail,title))'
	payload={'q':busqueda,'maxResults':'40','fields':campos,'key':key}
	r=requests.get(url, params=payload)
	
	if r.status_code==200:
		a=r.json()
		lista=[]
		for i in a["items"]:
			lista.append(i)
		return render_template('mostrar.html',l=lista,lc=lista_colecc)

@app.route('/detalle/<id_libro>',methods=['GET', 'POST'])
def detalles(id_libro):
	url="https://www.googleapis.com/books/v1/volumes/"+id_libro
	campos='saleInfo(buyLink,country,isEbook,listPrice),volumeInfo(authors,averageRating,categories,description,imageLinks/small,imageLinks/smallThumbnail,previewLink,ratingsCount,subtitle,title)'
	payload={'fields':campos,'key':key}
	r=requests.get(url,params=payload)

	if r.status_code==200:
		datos=r.json()		
		return render_template('detalles.html',datos=datos)



@app.route('/contact.html')
def contacto():
	return render_template("contact.html")


@app.route('/mi_coleccion')
def coleccion():
	if token_valido():
		token=json.loads(session["token"])
		oauth2 = OAuth2Session(os.environ["client_id"], token=token, scope=scope)
		url="https://www.googleapis.com/books/v1/mylibrary/bookshelves/0/volumes"
		campos='items(id,volumeInfo(imageLinks/smallThumbnail,title))'
		payload={'fields':campos,'key':key}
	
		r=oauth2.get(url,params=payload)

		if r.status_code==200:
			a=r.json()
			lista=[]
			for i in a["items"]:
				lista.append(i)
			return render_template('mi_coleccion.html',l=lista)
		else:
			return "fallo"
	else:
		return redirect('/entrar')


@app.route('/añadir/<id_libro>')
def añadir(id_libro):
	if token_valido():
		token=json.loads(session["token"])
		oauth2 = OAuth2Session(os.environ["client_id"], token=token, scope=scope)
		url="https://www.googleapis.com/books/v1/mylibrary/bookshelves/0/addVolume"
		payload={'volumeId':id_libro,'key':key}
	
		r=oauth2.post(url,params=payload)

		if r.status_code==204:
			return "Libro añadido con éxito a su colección"
		else:
			return "Fallo"
	else:
		return redirect('/entrar')

@app.route('/eliminar/<id_libro>')
def eliminar(id_libro):
	if token_valido():
		token=json.loads(session["token"])
		oauth2 = OAuth2Session(os.environ["client_id"], token=token, scope=scope)
		url="https://www.googleapis.com/books/v1/mylibrary/bookshelves/0/removeVolume"
		payload={'volumeId':id_libro,'key':key}
	
		r=oauth2.post(url,params=payload)

		if r.status_code==204:
			return "Libro eliminado con éxito de su colección"
		else:
			return "Fallo"
	else:
		return redirect('/entrar')


#### Oauth2
redirect_uri = 'https://bookeando.herokuapp.com/google_callback'
scope = ['https://www.googleapis.com/auth/books']
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

@app.route('/entrar')
def login():
	if token_valido():
		return redirect("/")
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
	return redirect("/")



if __name__ == '__main__':
	port=os.environ["PORT"]    
	app.run('0.0.0.0',int(port),debug=True)