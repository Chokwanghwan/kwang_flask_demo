# -*- coding:utf-8 -*-
# 1~4강모듈화 전 python 서버쪽? 코드
import flask, flask.views   #플라스크를 사용하기 위해서 flask 임포트 flask.views는flask로 작성한 것들을 화면에 출력하는 기능을 가진것 같음.
import os   
import functools
app = flask.Flask(__name__) #os, functools 모르겠다.. 
# Don't do this!
app.secret_key = "bacon" #bacon도 모르겠다.

users = {"cho" : "kwang"} #users에 id와 passwd에 해당하는 값 저장

class Main(flask.views.MethodView): #Main 클래스 선언
	def get(self): #index.html을 띄워줌
		return flask.render_template('index.html')

	def post(self): 
		if 'logout' in flask.request.form: #로그아웃 상태면 session에 들어있는 username을 pop한 후 index 페이지를 리턴한다.
			flask.session.pop('username', None)
			return flask.redirect(flask.url_for('index'))
		required = ['username', 'passwd'] #required 선언
		for r in required: #id 조회
			if r not in flask.request.form: #flask.request.form에 해당 id가 없으면 에러메시지를 출력 후 index 페이지를 리턴한다
				flask.flash("Error: {0} is required.".format(r))
				return flask.redirect(flask.url_for('index'))
		username = flask.request.form['username'] #username을 정의한다.
		passwd = flask.request.form['passwd'] #passwd를 정의한다.
		if username in users and users[username] == passwd: #만약 username이 passwd와 같다면sesson의 username에 대입한다.
			flask.session['username'] = username
		else: #같지않다면 해당 메시지를 출력하고 index 페이지를 리턴한다.
			flask.flash("Username doesn't exist or incorrect password")
		return flask.redirect(flask.url_for('index'))

def login_required(method): #login_required 함수 선언
	@functools.wraps(method) #데코레이터 >> 자세한 기능을 모르겠음.
	def wrapper(*args, **kwargs): #세션에 username이 들어있으면 해당 메서드를 리턴한다 >> method에 뭐가 들어가지?
		if 'username' in flask.session:
			return method(*args, **kwargs)
		else: #그렇지 않으면 메시지 출력후 index 페이지 리턴
			flask.flash("A login is required to see the page!")
			return flask.redirect(flask.url_for('index'))
	return wrapper	#이 메서드는 로그인을 하지않고 서비스를 이용하려할 때 로그인하라는 메시지를 출력해주는 메서드 같음.

class Remote(flask.views.MethodView): #Remote 클래스는 로그인이 되어있는 상태에서 remote.html을 불러옴 get과 post 개념파악이 정확히 안됨.
	@login_required
	def get(self):
		return flask.render_template ("remote.html")

	@login_required
	def post(self):
		result = eval(flask.request.form['expression'])
		flask.flash(result)
		return flask.redirect(flask.url_for('remote'))

class Music(flask.views.MethodView): # 음악재생 클래스
	@login_required
	def get(self):
		songs = os.listdir('static/music/')
		return flask.render_template('music.html', songs=songs) #render_template의 기능이 정확히 뭘까?

app.add_url_rule('/',
				view_func=Main.as_view('index'),
				methods=["GET", "POST"]) #index를 현재창에 띄움
app.add_url_rule('/remote/', 
				view_func=Remote.as_view('remote'), 
				methods=['GET', 'POST']) #remote를 remote에 띄움
app.add_url_rule('/music/', 
				view_func=Music.as_view('music'), 
				methods=['GET']) #music을 music에 띄움

app.debug = True #디버그를 사용하고
app.run() #어플을 가동시킨다
