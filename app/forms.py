#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import SelectField,SubmitField,StringField
from wtforms.validators import Regexp

class LoginForm(Form):   #登陆页面， 资源包选择  
	companytype = SelectField("请选择公司类型",choices=[("0","A"),("1","B")])
	# resourcepack = SelectField("请选择仓库类型",choices = [("0","500平米仓库"),("1","800平米仓库")])  #choices=[value,label],default str type
	submit = SubmitField("确定")


class touzi(Form):   #投资页面表单，包含四个行业投资决策
	investFangchan = StringField("房地产行业（单位：万元，下同）",validators=[Regexp(r'\d*\.?\d?')],default=0)
	investNengyuan = StringField("新能源行业",validators=[Regexp(r'\d*\.?\d?')],default=0)
	investYiliao = StringField("医疗行业",validators=[Regexp(r'\d*\.?\d?')],default=0)
	investWuliu = StringField("物流行业",validators=[Regexp(r'\d*\.?\d?')],default=0)
	submit = SubmitField("确定投资")


class caigou(Form):   #采购页面表单，输入采购量
	buyamount = StringField("请输入采购量",validators=[Regexp(r'\d*')],default=0)
	submit = SubmitField("确定")


class shengchan(Form):   #生产页面表单，输入生产量
	position = SelectField("请选择投入市场", choices=[("0", "南方市场"), ("1", "北方市场"),("2","西方市场")])
	produceamount = StringField("请输入投入数量/万",validators=[Regexp(r'\d*')],default=0)
	produceprice = StringField("请输入每件产品的成本（质量）/元",validators=[Regexp(r'\d*')],default=0)
	sellprice = StringField("请输入每件产品的卖价/元", validators=[Regexp(r'\d*')], default=0)
	submit = SubmitField("确定生产")


class xiaoshou(Form):   #销售投入表单，输入销售投入
	investamount = StringField("请输入销售投入/万元",validators=[Regexp(r'\d*')],default=0)
	submit = SubmitField("确定")

#
#
#--------------------------管理员表单----------------------------------------#
#
#
#

class nextform(Form):
	company1 = StringField("公司序号")
	company2 = StringField("公司序号")
	company3 = StringField("公司序号")
	submit = SubmitField("确定")
	submit1 = SubmitField("降低加工费")
	submit2 = SubmitField("贷款")
	submit3 = SubmitField("交易")
	submit4 = SubmitField("扣款")
	submit5 = SubmitField("清算")
	submit6 = SubmitField("仓库租赁")
	submit7 = SubmitField("500万融资")
	submit8 = SubmitField("功能卡购买")

class gongnengkaForm(nextform):   #XX公司以XX价格购入XX号功能卡
	company = StringField()
	price = StringField()
	num = StringField()
	submit = SubmitField("确定")
	

class debtform(nextform):  #XX公司向XX公司借得XX万元，约定第X轮后归还，总利息为XX%
	debtTo = StringField()
	debtFrom = StringField()
	debt= StringField()   #小数点后？
	debtTime = StringField()
	interest= StringField()  #小数点后一位，如5.3%
	submit = SubmitField("确定")

class trade(nextform):  #XX公司向XX公司购买XX市场上的成本为XX的产品，卖价为XX，数量为XX
	seller = StringField()
	buyer = StringField()
	amount = StringField()
	position = StringField()
	price = StringField()
	quality = StringField()
	submit = SubmitField("确定")



class fineform(nextform):
	company = StringField()
	money = StringField()
