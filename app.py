import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from flask import Flask, render_template, request
import tweepy,csv
import matplotlib.pyplot as plt 
#import pandas as pd
from collections import Counter
from textblob import TextBlob
import numpy as np
import os
import pygal
from pygal.style import DarkSolarizedStyle

app = Flask(__name__)

#signifies a decorator - way to wrap a function and modifying its behaviour
@app.route("/")
def home():
	return render_template("index.html")

@app.route("/result")
def result():
	userText1 = request.args.get('Key')
	#print(type(userText1))
	#print(userText1)
	#print(str(userText1))
	userText2 = request.args.get('Frequency')
	#print(type(userText2))
	#print(userText2)
	#print(str(userText2))
	
	#Customer or Consumer key of twitter API 
	customer_key = 'uzhxTPv5zDFvl2sF2U1bEF2Ts'
	#Customer or Consumer sceret key
	customer_secret = 'A78y59572s9gUBvTcCQzK7dhHNe5URK1tKyolKPbBX5BkVBEPd'
	#Access Key
	access_key = '1006982604204064768-F7VxOTGf3mktlfujHQKxwiPVXiKfkT'
	#Access secret token
	access_secret ='ejnDlEm2Razpar46mzAAh7NtumFRC2BhZisgfIuVXNXsD'
	#Authenticating customer
	auth = tweepy.OAuthHandler(customer_key, customer_secret)
	auth.set_access_token(access_key,access_secret)
	api = tweepy.API(auth)

	results = api.search(q=userText1,count=userText2)
	#print(results)
	# We add the additional step of iterating through the list of sentences and calculating and printing polarity scores for each one.
	polarity = []
	positive = []
	negative = []
	neutral = []
	for i in results:
		i.text
		print(i)
		analysis = TextBlob(i.text)
		polarity.append(analysis.sentiment[0])
	for i in range(0,len(polarity)):
	    if polarity[i]>0:
		positive.append(polarity[i])
	    elif polarity[i]<0:
		negative.append(polarity[i])
	    else:
		neutral.append(polarity[i])
	#print(polarity)
	#print(positive)
	#print(negative)
	#print(neutral)
	result = [len(positive),len(negative),len(neutral),len(polarity)]
	#print(type(result))
	#print(result)
	labels=["pos","neg","neu","pol"]
	labels_graph=[i for i in labels]
	result_graph=[i for i in result]
	# create a bar chart
        title = "Twitter sentiment analysis"
        bar_chart = pygal.Bar(width=1200, height=600,explicit_size=True, title=title, style=DarkSolarizedStyle)
        bar_chart.x_labels = labels_graph
        bar_chart.add('Temps in F', result_graph)

	pie_chart = pygal.Pie(style=DarkSolarizedStyle)
	pie_chart.add(labels[0], result[0])
	pie_chart.add(labels[1], result[1])
	pie_chart.add(labels[2], result[2])
	return render_template('result.html',result=result,bar_chart=bar_chart,pie_chart=pie_chart)

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True,host='0.0.0.0', port=4000)
