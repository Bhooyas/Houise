from flask import Flask,render_template,flash,request,session,redirect,url_for,jsonify
import os
from room import join_room,create_room
from ticketgenerator import tickect_generator
from Play import claim,generate_num
import shutil
from python_interpretor import execute

loc = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.secret_key = "BAk Housie"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/join",methods=["GET","POST"])
def join():
	if session.get('tickect') != None:
		tickect = session['tickect']
		userfile = session['userfile']
		users = open(userfile).read().split('\n')
		users = list(dict.fromkeys(users))
		users.remove('')
		numbersfile = session['numbersfile']
		numbers_temp = open(numbersfile).read().strip().split('\n')
		temp = []
		for i in numbers_temp:
			temp.append(i.split(','))
		numbers=temp
		try:
			numbers.remove([''])
			numbers.remove(' ')
		except:
			pass
		winnerfile = session['winnerfile']
		winner_temp = open(winnerfile).read().split('\n')
		temp = []
		remaining_winners = []
		for i in winner_temp:
			m = i.split(',')
			if i != "":
				temp.append(m)
				if m[1] == '-':
					remaining_winners.append(m[0])
		winner=temp
		try:
			winner.remove('')
		except:
			pass
		a = max([x.count('-') for x in winner])
		if a == 0:
			return redirect(url_for('game_over'))
		return render_template("Play Game.html",tickect=tickect,users=users,numbers=numbers,winners=winner,remaining_winners=remaining_winners)
	elif request.method == "POST":
		got,userfile,numbersfile,winnerfile = join_room(request.form['name'], request.form['pwd'], request.form['user'])
		if got:
			if session.get('tickect') == None:
				session['user'] = request.form['user']
				user = request.form['user'] + "\n"
				tickect,tickect_num = tickect_generator()
				session['tickect'] = tickect
				session['tickect_num'] = tickect_num
				session['userfile'] = userfile
				ufile = open(userfile,'a')
				#print(user)
				ufile.write(user)
				ufile.close()
				users = open(userfile).read().split('\n')
				users = list(dict.fromkeys(users))
				users.remove('')
				session['numbersfile'] = numbersfile
				numbers_temp = open(numbersfile).read().split('\n')
				temp = []
				for i in numbers_temp:
					temp.append(i.split(','))
				numbers=temp
				try:
					numbers.remove('')
				except:
					pass
				session['winnerfile'] = winnerfile
				winner_temp = open(winnerfile).read().split('\n')
				temp = []
				remaining_winners = []
				for i in winner_temp:
					m = i.split(',')
					if i != "":
						temp.append(m)
						if m[1] == '-':
							remaining_winners.append(m[0])
				winner=temp
				try:
					winner.remove('')
				except:
					pass
			else:
				tickect = session['tickect']
				userfile = session['userfile']
				users = open(userfile).read().split('\n')
				users = list(dict.fromkeys(users))
				users.remove('')
				numbersfile = session['numbersfile']
				numbers_temp = open(numbersfile).read().split('\n')
				temp = []
				for i in numbers_temp:
					temp.append(i.split(','))
				numbers=temp
				try:
					numbers.remove('')
					numbers.remove(' ')
				except:
					pass
				winnerfile = session['winnerfile']
				winner_temp = open(winnerfile).read().split('\n')
				temp = []
				remaining_winners = []
				for i in winner_temp:
					m = i.split(',')
					if i != "":
						temp.append(m)
						if m[1] == '-':
							remaining_winners.append(m[0])
				winner=temp
				try:
					winner.remove('')
				except:
					pass
			return render_template("Play Game.html",tickect=tickect,users=users,numbers=numbers,winners=winner,remaining_winners=remaining_winners)
		else:
			flash("Invalid room","error")
	return render_template("join.html")

@app.route("/create",methods=["GET","POST"])
def create():
	if session.get('start') != None:
		return render_template('game_on.html')
	elif session.get('pwd') != None:
		userfile = session['userfile']
		users = open(userfile).read().split("\n")
		name = session['name']
		pwd = session['pwd']
		users = list(dict.fromkeys(users))
		try:
			users.remove('')
		except:
			pass
		return render_template("startgame.html",name=name,pwd=pwd,users=users)
	elif request.method == "POST":
		if session.get('pwd')==None:
			session['user'] = request.form['user']
			user = session['user']
			name,pwd,userfile,numbersfile,winnerfile = create_room(user)
			users = open(userfile).read().split("\n")
			session['userfile'] = userfile
			session['numbersfile'] = numbersfile
			session['winnerfile'] = winnerfile
			session['name']=name
			session['pwd']=pwd
			users = list(dict.fromkeys(users))
			try:
				users.remove('')
			except:
				pass
		else:
			userfile = session['userfile']
			users = open(userfile).read().split("\n")
			name = session['name']
			pwd = session['pwd']
			users = list(dict.fromkeys(users))
			try:
				users.remove('')
			except:
				pass
		return render_template("startgame.html",name=name,pwd=pwd,users=users)
	return render_template("create.html")

@app.route('/changer')
def change():
	tickect = session['tickect']
	change = request.args.get("value")
	if change != None:
		new_ticket = []
		for row in tickect:
			temp = []
			for i,k in row:
				if str(i) == str(change):
					k = not k
				temp.append([i,k])
			new_ticket.append(temp)
	session['tickect'] = new_ticket
	return ("nothing")

@app.route('/chooser')
def choose():
	prise = request.args.get("value")
	tickect = session['tickect_num']
	remaing_numbers = list(range(1,91))
	numbersfile = session['numbersfile']
	if prise != None:
		for i in open(numbersfile).read().split('\n'):
			m = i.split(',')
			try:
				remaing_numbers.remove(int(m[0]))
			except:
				pass
		got = claim(tickect, int(prise), remaing_numbers)
		if got:
			winnerfile = session['winnerfile']
			wfile = open(winnerfile).read().split('\n')
			if wfile[int(prise)].split(',')[1]=='-':		
				wfile[int(prise)] = "".join([wfile[int(prise)].split(',')[0],',',session['user']])
			else:
				wfile[int(prise)] += session['user']
			#print(wfile)
			w_temp = open(winnerfile,'w')
			for i in wfile:
				w_temp.write(i)
				w_temp.write('\n')
			w_temp.close()
			return redirect(url_for('logout'))
		flash("Your claim is invalid")
	return redirect(url_for('join'))

@app.route('/logout')
def logout():
	session.clear()
	return render_template('logout.html')

@app.route('/start')
def start():
	session['start'] = True
	numbersfile = session['numbersfile']
	numbers = open(numbersfile).read().split('\n')
	if session.get('remaining_numbers')==None:
		number, remaining_numbers,color = generate_num()
	else:
		remaining_numbers = session['remaining_numbers']
		number,remaining_numbers,color = generate_num(remaining_numbers)
	session['remaining_numbers'] = remaining_numbers
	temp = str(number)+','+color
	numbers = [temp]+numbers
	num = open(numbersfile,'w')
	for n in numbers:
		num.write(n)
		num.write('\n')
	num.close()
	userfile = session['userfile']
	users = open(userfile).read().split('\n')
	users = list(dict.fromkeys(users))
	users.remove('')
	numbersfile = session['numbersfile']
	numbers_temp = open(numbersfile).read().split('\n')
	temp = []
	for i in numbers_temp:
		temp.append(i.split(','))
	numbers=temp
	try:
		numbers.remove('')
	except:
		pass
	winnerfile = session['winnerfile']
	winner_temp = open(winnerfile).read().split('\n')
	temp = []
	remaining_winners = []
	for i in winner_temp:
		m = i.split(',')
		if i != "":
			temp.append(m)
			if m[1] == '-':
				remaining_winners.append(m[0])
	winner=temp
	try:
		winner.remove('')
	except:
		pass
	a = max([x.count('-') for x in winner])
	if a == 0:
		return redirect(url_for('game_over_admin'))
	return render_template('game_on.html',numbers=numbers,users=users,winners=winner)

@app.route('/game_over_admin')
def game_over_admin():
	winnerfile = session['winnerfile']
	winner_temp = open(winnerfile).read().split('\n')
	temp = []
	remaining_winners = []
	for i in winner_temp:
		m = i.split(',')
		if i != "":
			temp.append(m)
			if m[1] == '-':
				remaining_winners.append(m[0])
	winner=temp
	name = session['name']
	pwd = session['pwd']
	path = "{}\{}.{}".format(loc,name,pwd)
	# shutil.rmtree(path)
	session.clear()
	return render_template('game_over_admin.html',winners=winner)

@app.route('/game_over')
def game_over():
	winnerfile = session['winnerfile']
	winner_temp = open(winnerfile).read().split('\n')
	temp = []
	remaining_winners = []
	for i in winner_temp:
		m = i.split(',')
		if i != "":
			temp.append(m)
			if m[1] == '-':
				remaining_winners.append(m[0])
	winner=temp
	session['tickect'] = None
	session.clear()
	return render_template('game_over.html',winners=winner)

@app.route("/pyin",methods=["POST"])
def pyin():
	query = "".join(dict(request.form)['query'])
	return jsonify({"response" : execute(query)})

if __name__ == "__main__":
	app.run(debug=True)