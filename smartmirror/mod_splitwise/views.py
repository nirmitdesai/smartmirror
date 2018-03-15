# -*- coding: utf-8 -*-
from flask import Blueprint, url_for, session, redirect, request
import requests,json
import utils
from splitwise import Splitwise
from splitwise.expense import Expense
from splitwise.user import ExpenseUser
from flask_assistant import tell
from smartmirror.extensions import assist

splitwiseBlueprint = Blueprint('splitwise', 
                             __name__,
                             static_folder='../static')

@splitwiseBlueprint.route('/splitwise', methods=['GET', 'POST'])
def home():
	if 'access_token' in session:
		return redirect(url_for("splitwise.friends"))
	print "in home.."
	consumer_key = ''
	consumer_secret = ''
	sObj = Splitwise(consumer_key,consumer_secret)
	url, secret = sObj.getAuthorizeURL()
	print "secret = ", secret
	session['secret'] = secret
	with open('secret','w') as f:
		f.write(secret)
	session.permanent = True
	print "Redirecting to url", url
	return redirect(url)

@splitwiseBlueprint.route("/authorize",methods=["GET"])
def authorize():
	print session
	secret = ""
	with open('secret','r') as f:
		secret = f.readline()
		secret = secret.strip()

	oauth_token    = request.args.get('oauth_token')
	oauth_verifier = request.args.get('oauth_verifier')
	consumer_key = ''
	consumer_secret = ''
	sObj = Splitwise(consumer_key, consumer_secret)
	access_token = sObj.getAccessToken(oauth_token,secret,oauth_verifier)
	print "type of access = ", type(access_token)
	with open('accesstoken.json','w') as f:
		json.dump(access_token,f)
	session['access_token'] = access_token
	print "*"*50
	print url_for("splitwise.friends")
	return redirect(url_for("splitwise.friends"))

@splitwiseBlueprint.route("/friends",methods=["GET"])
def friends():
	if 'access_token' not in session:
		return redirect(url_for("home"))

	consumer_key = ''	
	consumer_secret = ''
	sObj = Splitwise(consumer_key,consumer_secret)
	access_token = 0
	with open('accesstoken.json','r') as f:
		access_token = json.load(f)
		print access_token
	sObj.setAccessToken(access_token)


	return "friends\n"



@assist.action("friend")
def addMoney(friendName, currency, expenseReason):
	speech = "hello"
	print "name =", friendName
	print currency
	print "inside add money"
	if not friendName or not currency:
		print "error in name or currency"
		return tell("sorry couldn't proceed with transaction")


	consumer_key = ''	
	consumer_secret = ''
	sObj = Splitwise(consumer_key,consumer_secret)

	with open('accesstoken.json','r') as f:
		access_token = json.load(f)
		print access_token
	sObj.setAccessToken(access_token)


	amountOwed = currency['amount']
	expense = Expense()
	expense.setCost(amountOwed)
	expense.setDescription(expenseReason)

	user1 = ExpenseUser()
	user1.setId(utils.getSplitwiseId('nirmit'))
	user1.setPaidShare(str(amountOwed))
	user1.setOwedShare('0.0')

	user2 = ExpenseUser()
	user2.setId(utils.getSplitwiseId(friendName))
	user2.setPaidShare('0.00')
	user2.setOwedShare(str(amountOwed))

	users = []
	users.append(user1)
	users.append(user2)
	expense.setUsers(users)

	expense = sObj.createExpense(expense)
	print expense

