#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import  Flask,render_template,session,url_for,redirect,flash,json,request
from flask_bootstrap import Bootstrap
from forms import LoginForm,touzi,caigou,xiaoshou,shengchan,yanfa,gongnengkaForm,debtform,trade,fineform,nextform,daikuan   #导入表单
from gl import material_a,material_b,capacity,coef_k
import dealwith
from dealwith import path,OperationFail
import os
import gl
# login(num,types,choose)注册 num为公司编号，types为公司类型，choose为公司选择的起始资源包

app= Flask(__name__)  #推荐singlemodule使用


app.config['BOOTSTRAP_SERVE_LOCAL'] = True#todo:仅开发环境使用本地css

bootstrap = Bootstrap(app)   #bootstrap的实例
app.config['SECRET_KEY'] = "you guess" #防止CSRF攻击

#
#
#
#  -------------------- route -----------------------------------------------
#
#
#//输入小组组号进入相应url，选择小组类型，然后正式进入游戏
@app.route("/<int:number>",methods= ['GET','POST'])    #操作员输入域名/序号
def LoginPage(number):
	form = LoginForm()
	session["number"]=number
	if form.validate_on_submit(): #点击确定后，保存选择
		# session['resourcepack']= form.resourcepack.data
		# if session.get("resourcepack")=="0":
		# 	choose = 0;
		# else: 
		# 	choose = 1;
		dealwith.login(number,int(form.companytype.data))    #login(num,types,choose)
		return redirect(url_for("index"))
	return render_template("login.html",form = form)
#
#
#
#

@app.route('/index',methods= ['GET','POST'])	
def index():
	# Touziform = touzi()
	# Caigouform = caigou()
	Xiaoshouform = xiaoshou()
	Shengchanform = shengchan()
	Yanfaform = yanfa()
	Daikuanform = daikuan()
	num = session.get("number")
	
	if request.method == 'POST' :		
		form_name = request.form["submit"]

		if form_name == '确定' and Xiaoshouform.validate_on_submit():  #提交第二个表单：销售投入
			amount_south = float(Xiaoshouform.investamount_south.data)
			amount_north = float(Xiaoshouform.investamount_north.data)
			amount_west = float(Xiaoshouform.investamount_west.data)
			try:
				dealwith.saleinvest(amount_south,amount_north,amount_west,num)
			except OperationFail as e:
				flash("%r" % e)						#异常
			finally:
				return redirect(url_for("index"))
		elif form_name == '确定投入' and Yanfaform.validate_on_submit():
			amount_research = float(Yanfaform.research_amount.data)
			try:
				dealwith.researchinvest(amount_research,num)
			except OperationFail as e:
				flash("%r" % e)						#异常
			finally:
				return redirect(url_for("index"))
		elif form_name == "确定还贷" and Daikuanform.validate_on_submit():
			amount_loan = float(Daikuanform.loan_amount.data)
			amount_repayment = float(Daikuanform.repayment_amount.data)
			try:
				dealwith.loaninvest(amount_loan,amount_repayment,num)
			except OperationFail as e:
				flash("%r" % e)						#异常
			finally:
				return redirect(url_for("index"))
		else:               #提交第三个表单：生产
			position = int(Shengchanform.position.data)
			amount = float(Shengchanform.produceamount.data)
			if Shengchanform.produceprice.data:
				firstcost = float(Shengchanform.produceprice.data)
			else:
				firstcost = 0.0
			if Shengchanform.sellprice.data and Shengchanform.producequality.data:
				sellprice = float(Shengchanform.sellprice.data)
				quality = float(Shengchanform.producequality.data)
			else:
				sellprice = 0.0
				quality = 0.0
			try:
				dealwith.produce(num,amount,firstcost,sellprice,position,quality)
			except OperationFail as e:
				flash("%r" % e)						#异常
			finally:
				return redirect(url_for("index"))
		
	f=open(path+str(session.get("number"))+".json","r")
	temp_txt=f.read()
	now_info=json.loads(temp_txt)
	f.close()
	
	if os.path.exists(path+"log.json"):
		f=open(path+"log.json","r")
		temp_txt=f.read()
		log=json.loads(temp_txt)
		f.close()
	else:
		log = [{},{},{},{},{},{},{},{},{},{}]
		
	# print("dealwith.game_round:")
	# print(dealwith.game_round)
	print("game_round:")
	print(gl.game_round)
	return render_template("user.html",Accountdata=now_info,Shengchanform=Shengchanform,Xiaoshouform=Xiaoshouform,Yanfaform=Yanfaform,Daikuanform = Daikuanform,game_round = gl.game_round, material_a = material_a ,material_b = material_b,Thislog = log[session["number"]],chip_space=gl.chip_space,product_space=gl.product_space)


@app.route("/seller/<int:num>",methods=["GET","POST"])
def forseller(num):	
	f=open(path+str(num)+".json","r")
	temp_txt=f.read()
	now_info=json.loads(temp_txt)
	f.close()
	return render_template("forseller.html",Accountdata = now_info)
#
#
#
#
#

@app.route("/admin",methods=["GET","POST"])
def admin():
	form = nextform()
	if request.method == 'POST':
		if "submit2" in request.form:
			return redirect(url_for("loan"))
		elif "submit3" in request.form:
			return redirect(url_for("trade"))
		elif "submit4" in request.form:
			return redirect(url_for("fine"))
		elif "submit8" in request.form:
			return redirect(url_for("gongnengka"))
		else:  #清算
			#dealwith.nextround()  #生成的Log存进文件
			return redirect(url_for("admin"))
	return render_template("admin.html",form = form,round =gl.game_round,capacity=gl.capacity)


@app.route("/others",methods=["GET","POST"])
def others():
	form = nextform()
	# if request.method == 'POST':
		# if "submit1" in request.form:
		# 	company1 = int(form.company1.data)
		# 	dealwith.reducefee(company1)
		# 	return redirect(url_for("others"))
		# elif "submit6" in request.form:
		# 	company2=int(form.company2.data)
		# 	dealwith.rentStorage(company2)
		# 	return redirect(url_for("others"))
		# elif "submit7" in request.form:
		# 	company3=int(form.company3.data)
		# 	dealwith.finance(company3)
		# 	return redirect(url_for("others"))

	# if form.validate_on_submit():
	dealwith.nextround()  #生成的Log存进文件
		#return redirect(url_for("others"))
	return render_template("others.html",form = form,round =gl.game_round,capacity=gl.capacity)




#
#
#
#
@app.route("/loan",methods=["GET","POST"])	
def inloan():
	form = debtform()
	if form.validate_on_submit():
		To = int(form.debtTo.data)
		From = int(form.debtFrom.data)
		debt = float(form.debt.data)
		interest = float(form.interest.data)/100
		time = int(form.debtTime.data)
		try:
			dealwith.getloan(debt,interest,time,From,To)	
		except OperationFail as e:
			flash("%r" % e)						#异常
		finally:
			return redirect(url_for("inloan"))
	return render_template("loan.html",form=form,round =gl.game_round,capacity=gl.capacity[gl.game_round])
#
#
#
#
#
@app.route("/trade",methods=["GET","POST"])	
def intrade():
	form = trade()
	if form.validate_on_submit():
		seller = int(form.seller.data)
		buyer = int(form.buyer.data)
		amount = float(form.amount.data)
		position = int(form.position.data)
		quality = float(form.quality.data)
		sellprice = float(form.price.data)
		try:
			dealwith.buychip(position,amount,sellprice,quality,seller,buyer)
		except OperationFail as e:
			flash("%r" % e)						#异常
		finally:
			return redirect(url_for("intrade"))
	return render_template("trade.html",form=form,round =gl.game_round,capacity=gl.capacity)
#
#
#
#
#
@app.route("/fine",methods=["GET","POST"])
def fine():        #某公司扣除一定现金
	form = fineform()
	if form.validate_on_submit():
		company = int(form.company.data)
		money = float(form.money.data)    #扣款可能导致负数
		choice = int(form.choice.data)
		dealwith.fine(money,company,choice)
		return redirect(url_for("fine"))
	return render_template("fine.html",form = form,round =gl.game_round,capacity=gl.capacity)
	

@app.route("/gongnengka",methods=["GET","POST"])
def gongnengka():	#功能卡购买
	form=gongnengkaForm()
	if form.validate_on_submit():
		company = int(form.company.data)
		money = float(form.price.data)    #扣款可能导致负数
		num = int(form.num.data)
		dealwith.buyCard(company,money,num)
		return redirect(url_for("gongnengka"))
	return render_template("gongnengka.html",form = form,round =gl.game_round,capacity=gl.capacity)


@app.route("/rank")
def rank():
	term, capacity_result = dealwith.asset_sort()
	return render_template("rank.html",round=gl.game_round,term=term,material_a=material_a[gl.game_round-1],capacity_result=capacity_result,max_price=gl.max_price)


if __name__ == '__main__':
	app.run(debug = True)
