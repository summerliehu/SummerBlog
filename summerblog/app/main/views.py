from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@main.route('/user/<name>')
def user(name):
	return render_template('user.html', name = name)
