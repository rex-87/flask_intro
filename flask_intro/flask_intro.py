# -*- coding: utf-8 -*-
"""
	flask_intro
	
	This project is an example of a Python project generated from cookiecutter-python.
"""

## -------- COMMAND LINE ARGUMENTS ---------------------------
## https://docs.python.org/3.7/howto/argparse.html
import argparse
CmdLineArgParser = argparse.ArgumentParser()
CmdLineArgParser.add_argument(
	"-v",
	"--verbose",
	help = "display debug messages in console",
	action = "store_true",
)
CmdLineArgs = CmdLineArgParser.parse_args()

## -------- LOGGING INITIALISATION ---------------------------
import misc
misc.MyLoggersObj.SetConsoleVerbosity(ConsoleVerbosity = {True : "DEBUG", False : "INFO"}[CmdLineArgs.verbose])
LOG, handle_retval_and_log = misc.CreateLogger(__name__)

try:
	
	from flask import Flask, render_template, url_for, request, redirect
	from flask_sqlalchemy import SQLAlchemy
	from datetime import datetime
	import os
	
	app = Flask(__name__)
	
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
	db = SQLAlchemy(app)	
	
	class Todo(db.Model):
		id = db.Column(db.Integer, primary_key = True)
		content = db.Column(db.String(200), nullable = False)
		date_created = db.Column(db.DateTime, default = datetime.utcnow)
		
		def __repr__(self):
			return '<Task {}>'.format(self.id)
			
	if not os.path.exists(r'flask_intro\test.db'):
		db.create_all()
	
	@app.route('/', methods = ['POST', 'GET'])
	def index():
		if request.method == 'POST':
		
			# ---- create new task from user input
			task_content = request.form['content']
			new_task = Todo(content=task_content)
			
			# ---- update db with new task
			db.session.add(new_task)
			db.session.commit()
			
			# ---- redirect to root page
			return redirect('/')

		else:
		
			# ---- query all tasks from db
			tasks = Todo.query.order_by(Todo.date_created).all()
			
			# ---- display root page
			return render_template('index.html', tasks = tasks)
	
	@app.route('/delete/<int:id>')
	def delete(id):
		task_to_delete = Todo.query.get_or_404(id)
		
		db.session.delete(task_to_delete)
		db.session.commit()
		return redirect('/')
	
	@app.route('/update/<int:id>', methods=['GET', 'POST'])
	def update(id):
		task = Todo.query.get_or_404(id)
	
		if request.method == 'POST':
			task.content = request.form['content']

			# ---- update db with updated task
			db.session.commit()

			# ---- redirect to root page
			return redirect('/')

		else:
			return render_template('update.html', task = task)
		
	if __name__ == "__main__":
		app.run(debug = True)

## -------- SOMETHING WENT WRONG -----------------------------	
except:

	import traceback
	LOG.error("Something went wrong! Exception details:\n{}".format(traceback.format_exc()))

## -------- GIVE THE USER A CHANCE TO READ MESSAGES-----------
finally:
	
	pass
