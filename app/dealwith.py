#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
from gl import product_space,chip_space,capacity,store_fee,profit,material_a,material_b,processfee_a,processfee_b,depreciation_material_a,depreciation_material_b,storage_cost,depreciation_a,depreciation_b,end_round,chip_price,reduced_fee,resource_price_a,resource_price_b,product_price,add_store,cost_store
#import gl
import os
import shutil
from gl import path
import gl
# gl.game_round:当前游戏轮数
# capacity[gl.game_round]: 当前轮的市场容量
# profit[x][y]:第x个行业在第y轮的收益情况
# material_a[x]:原料a在第x轮的价格
# material_b[x]:原料b在第x轮的价格
# bot_price[x]:在第x轮机器人的系统回收价格
# path:文件路径


class OperationFail(Exception):  #定义异常：操作失败
    pass


# 以下为各公司对应json文件dict中的信息
# 公司类型：type 值0为碳纤维材料公司(5家) 值1为无人机公司(4家)
# #功能卡x数量：card[x]
# 现金：cash
# 原料：material
# 产品实际库存：product
# 最大总仓储:storage
# 房地产投资：invest[1]
# 新能源投资：invest[2]
# 医疗投资：invest[3]
# 物流投资：invest[4]
# 生产费：fee
# 机器人公司芯片数量：chip
# 公司借贷情况：loan[x][0]为第x笔贷款金额，loan[x][1]为第x笔贷款利息，loan[x][2]为第x笔贷款还款时间，loan[x][3]为第x笔贷款目标公司，金额正为借出，金额负为借入
# 资源包结算：result 资源包1值为1，资源包2值为0.65

# 投资 I1 I2 I3 I4分别为对四种行业的投资金额，num为公司编号
def invest(I1,I2,I3,I4,num):
    f=open(path+chr(48+num)+".json","r")
    temp_txt=f.read()
    now_info=json.loads(temp_txt)
    f.close()
    now_info['invest'][1]+=I1
    now_info['invest'][2]+=I2
    now_info['invest'][3]+=I3
    now_info['invest'][4]+=I4
    total=(I1+I2+I3+I4)
    if now_info['cash'] < total: #钱不够
        raise OperationFail("现金不足，操作失败")
    now_info['cash']-=total
    now_info['cash'] = round(now_info['cash'],1)
    shutil.copyfile(path+chr(48+num)+".json",path+chr(48+num)+"_bak.json")
    f=open(path+chr(48+num)+".json","w")
    json.dump(now_info,f)
    f.close()

# 采购原料 total为原材料采购数量，num为公司编号
def purchase(total,num):
    f=open(path+chr(48+num)+".json","r")
    temp_txt=f.read()
    now_info=json.loads(temp_txt)
    f.close()
#
#  判断是否买得起
#	
    if now_info['type']==0:
        if now_info['cash'] < material_a[gl.game_round]*total:
            raise OperationFail("现金不足，操作失败")
        else:
            now_info['cash']-=material_a[gl.game_round]*total   #定价曲线函数 待做》》》》》》》》》》》》》》》》》》》》》》
    else:
        if now_info['cash'] < (material_b[gl.game_round] * total):
            raise OperationFail("现金不足，操作失败")
        else:
            now_info['cash'] -= material_b[gl.game_round]*total
    now_info['material']+=total
    now_info['cash'] = round(now_info['cash'],1)
    shutil.copyfile(path+chr(48+num)+".json",path+chr(48+num)+"_bak.json")
    f=open(path+chr(48+num)+".json","w")
    json.dump(now_info,f)
    f.close()

# 公司生产 total为生产数量，num为公司编号，price为当前产品定价
def produce(num,total,price,sellprice,position):
	f=open(path+chr(48+num)+".json","r")
	temp_txt=f.read()
	now_info=json.loads(temp_txt)
	f.close()
	

#   无法生产
# material： 上游公司生产(市场，价格/成本，数量)
# chip：	   上游公司卖给下游公司的材料（市场，价格/成本，数量）
# product：  下游公司生产（市场，价格/成本，数量, 卖价, 公司id，竞争力）

	flag1 = 0
	if now_info['type'] == 0 and total * price > now_info["cash"]:   #钱不够
		raise OperationFail("现金不足，操作失败")
	elif now_info['type'] == 1:    #材料不够
		for i in range(len(now_info["chip"])):
			if position == now_info["chip"][i][0] and price == now_info["chip"][i][1]:
				flag1 = 1
				if total > now_info["chip"][i][2]:
					raise OperationFail("材料不足，操作失败")
				break
		if flag1 == 0:
			raise OperationFail("该市场无此原材料，操作失败")

	flag2 = 0
	if now_info['type'] == 1:
		for i in range(len(now_info["product"])):
			if position == now_info["product"][i][0] and price == now_info["product"][i][1]:
				now_info["product"][i][2] += total
				now_info["chip"][i][2] -=total
				flag2 = 1
				break
		if flag2 == 0:
			product = []
			product.append(position)
			product.append(price)
			product.append(total)
			product.append(sellprice)
			product.append(num)
			product.append(0) 	#产品竞争力
			now_info['product'].append(product)

	elif now_info['type'] == 0:
		for i in range(len(now_info["material"])):
			if position == now_info["material"][i][0] and price == now_info["material"][i][1]:
				now_info["material"][i][2] += total
				flag2 = 1
				break
		if flag2 == 0:
			material = []
			material.append(position)
			material.append(price)
			material.append(total)
			now_info['material'].append(material)

	now_info['cash'] -= total * price  # 余额

	now_info['cash'] = round(now_info['cash'],1)
	shutil.copyfile(path+chr(48+num)+".json",path+chr(48+num)+"_bak.json")
	f=open(path+chr(48+num)+".json","w")
	json.dump(now_info,f)
	f.close()

# 违规罚款 total为罚款金额，num为公司编号
def fine(total,num):
	f=open(path+chr(48+num)+".json","r")
	temp_txt=f.read()
	now_info=json.loads(temp_txt)
	f.close()
	if now_info['cash'] < total: #钱不够
		# raise OperationFail("现金不足，操作失败")
		pass
	now_info['cash']-=total
	now_info['cash'] = round(now_info['cash'],1)
	shutil.copyfile(path+chr(48+num)+".json",path+chr(48+num)+"_bak.json")
	f=open(path+chr(48+num)+".json","w")
	json.dump(now_info,f)
	f.close()

# 注册 num为公司编号，types为公司类型，choose为公司选择的仓储类型 
def login(num,types):
	try:
		f=open(path+chr(48+num)+".json","r")
	except Exception as e:
		print("%r" % e)
	temp_txt=f.read()
	now_info=json.loads(temp_txt)
	f.close()
	now_info['type']=types
	# if types==0:
	# 	now_info['fee']= processfee_a  #碳纤维材料公司生产费
	# else:
	# 	now_info['fee']= processfee_b #无人机公司公司生产费

	# if choose==0:
	# 	now_info['storage']=500   #500平米仓库
	# 	now_info['store_cost']=storage_a
	# else:
	# 	now_info['storage']=800     #800平米仓库
	# 	now_info['store_cost']=storage_b
	# now_info['store_cost']=storage_cost
	now_info['cash']=now_info['value']=1000
	now_info['result']=1
	now_info['cash'] = round(now_info['cash'],1)
	shutil.copyfile(path+chr(48+num)+".json",path+chr(48+num)+"_bak.json")
	f=open(path+chr(48+num)+".json","w")
	json.dump(now_info,f)
	f.close()

#借贷 total为贷款数额，interest为利率，period为还款时间，num1为放贷公司编号，num2为借贷公司编号
def getloan(total,interest,period,num1,num2):
	f1=open(path+chr(48+num1)+".json","r")
	f2=open(path+chr(48+num2)+".json","r")
	temp1=f1.read()
	temp2=f2.read()
	info1=json.loads(temp1)
	info2=json.loads(temp2)
	f1.close()
	f2.close()
	if info1["cash"] < total:  #没钱可以贷
		raise OperationFail("现金不足，操作失败")
	info1['cash']-=total
	info2['cash']+=total
	info1['loan'].append([total,interest,period,num2])
	info2['loan'].append([-total,interest,period,num1])
	shutil.copyfile(path+chr(48+num1)+".json",path+chr(48+num1)+"_bak.json")
	shutil.copyfile(path+chr(48+num2)+".json",path+chr(48+num2)+"_bak.json")
	f1=open(path+chr(48+num1)+".json","w")
	f2=open(path+chr(48+num2)+".json","w")
	json.dump(info1,f1)
	json.dump(info2,f2)
	f1.close()
	f2.close()

#碳纤维交易 position为市场位置，total为碳纤维交易数量，price为交易单价,quality为质量/成本，num1为出售公司，num2为购买公司
def buychip(position,total,price,quality,num1,num2):
	f1=open(path+chr(48+num1)+".json","r")
	f2=open(path+chr(48+num2)+".json","r")
	temp1=f1.read()
	temp2=f2.read()
	info1=json.loads(temp1)
	info2=json.loads(temp2)
	f1.close()
	f2.close()

# 交易失败
	flag1 = 0
	if info2['cash'] < total*price:
		raise OperationFail("现金不足，操作失败")
	for i in range(len(info1["material"])):
		if position == info1['material'][i][0] and quality == info1['material'][i][1]:
			flag1 = 1
			if total > info1['material'][i][2]:
				raise OperationFail("材料不足，操作失败")
			break
	if flag1 == 0:
		raise OperationFail("该市场无此原材料，操作失败")

	# if info2['storage']-4*info2['product']-2*info2['chip']-2*total<0:
	# 	raise OperationFail("购买方库存不足，操作失败")
	info1['cash'] += total * price
	info2['cash'] -= total * price

	for i in range(len(info1["material"])):
		if position == info1['material'][i][0] and quality == info1['material'][i][1]:
			info1['material'][i][2] -= total

	flag2 = 0
	for i in range(len(info2["chip"])):
		if position == info2['chip'][i][0] and quality == info2['chip'][i][1]:
			flag2 = 1
			info2['chip'][i][2] += total
	if flag2 == 0:
		chip = []
		chip.append(position)
		chip.append(quality)
		chip.append(total)
		info2['chip'].append(chip)

	shutil.copyfile(path+chr(48+num1)+".json",path+chr(48+num1)+"_bak.json")
	shutil.copyfile(path+chr(48+num2)+".json",path+chr(48+num2)+"_bak.json")
	f1=open(path+chr(48+num1)+".json","w")
	f2=open(path+chr(48+num2)+".json","w")
	json.dump(info1,f1)
	json.dump(info2,f2)
	f1.close()
	f2.close()

#降低X号加工费
def reducefee(num):
	f=open(path+chr(48+num)+".json","r")
	temp_txt=f.read()
	now_info=json.loads(temp_txt)
	f.close()
	now_info['fee']=reduced_fee
	shutil.copyfile(path+chr(48+num)+".json",path+chr(48+num)+"_bak.json")
	f=open(path+chr(48+num)+".json","w")
	json.dump(now_info,f)
	f.close()

#仓库租赁
def rentStorage(num):
	f=open(path+chr(48+num)+".json","r")
	temp_txt=f.read()
	now_info=json.loads(temp_txt)
	f.close()
	now_info['storage']+=add_store
	now_info['store_cost']+=cost_store
	shutil.copyfile(path+chr(48+num)+".json",path+chr(48+num)+"_bak.json")
	f=open(path+chr(48+num)+".json","w")
	json.dump(now_info,f)
	f.close()
	
#500万融资
def finance(num):
	f=open(path+chr(48+num)+".json","r")
	temp_txt=f.read()
	now_info=json.loads(temp_txt)
	f.close()
	# oldCash=now_info['cash']
	oldValue=now_info['value']
	now_info['value']+=500
	now_info['result']=round(now_info['result']*oldValue/now_info['value'],3)
	now_info['cash']+=500
	shutil.copyfile(path+chr(48+num)+".json",path+chr(48+num)+"_bak.json")
	f=open(path+chr(48+num)+".json","w")
	json.dump(now_info,f)
	f.close()

#购买功能卡
def buyCard(company,money,num):
	f=open(path+chr(48+company)+".json","r")
	temp_txt=f.read()
	now_info=json.loads(temp_txt)
	f.close()
	now_info['cash']-=money
	# 不记录功能卡，由观察员记录
	shutil.copyfile(path+chr(48+company)+".json",path+chr(48+company)+"_bak.json")
	f=open(path+chr(48+company)+".json","w")
	json.dump(now_info,f)
	f.close()

#销售投入
def saleinvest(amount,num):
	f=open(path+chr(48+num)+".json","r")
	temp_txt=f.read()
	now_info=json.loads(temp_txt)
	f.close()
	now_info['sale'] = amount
	now_info['cash'] -= amount
	shutil.copyfile(path+chr(48+num)+".json",path+chr(48+num)+"_bak.json")
	f=open(path+chr(48+num)+".json","w")
	json.dump(now_info,f)
	f.close()


	
# 进入下一轮 
# 返回所有数据的变动值 格式为：
# 无人机出售收益；(四个行业)投资本息和；仓储费；折旧费
# log[{},
#{{gain_sell:XXX},{investFDC_total:XXX},{investNY_total:XXX},{investYL_total:XXX},{investWL_total:XXX},{storage:XXX},{depreciation:XXX},{loan:XXX}}
# {……}
# {……}
# ]
def nextround():
	gl.max_price=0
	now_info = []
	log = [{},{},{},{},{},{},{},{},{},{}]   #流水记录
	#global gl.game_round
	for i in [1,2,3,4,5,6,7,8,9]:
		f=open(path+chr(48+i)+".json","r")
		temp_txt=f.read()
		now_info.append(json.loads(temp_txt))
		f.close()
	# 清算前资金
	for i in [1,2,3,4,5,6,7,8,9]:
		log[i]["initmoney"] = now_info[i]["cash"]

	# 无人机公司抛售产品
	# for i in [1,2,3,4,5,6,7,8,9]:
	# 	if now_info[i].get("type")==1:
	# 		log[i]["gain_sell"] = round(now_info[i]['product']*bot_price[gl.game_round],1)
	# 		now_info[i]['cash']+= log[i]["gain_sell"]
	# 		now_info[i]['product']=0
	# 	else:
	# 		log[i]["gain_sell"] = 0

	# 计算竞争力
	product_list = []
	for i in [1,2,3,4,5,6,7,8,9]:
		if now_info[i]['type']==0:
			continue
		for j in range(len(now_info[i]['product'])):
			now_info[i]['product'][j][5] = (50 + now_info[i]['sale']) * now_info[i]['product'][1]/now_info[i]['product'][3]
			product_list.append(now_info[i]['product'][j])

	product_list.sort(key=takecompetition,reverse=True)

	# 市场收购+系统回收
	for i in range(len(product_list)):
		market = product_list[i][0]
		cap = capacity[market][gl.game_round]
		quality = product_list[i][1]
		amount = product_list[i][2]
		price = product_list[i][3]
		num = product_list[i][4]

		for j in range(len(cap)):
			if quality >= cap[j][0] and quality < cap[j+1][0] and j + 1 < len(cap):
				if amount <= cap[j][1]:
					now_info[num]['cash'] += amount * price
					log[num]['gain_sell'] += amount * price
					cap[j][1] -= amount
				else:
					now_info[num]['cash'] += cap[j][1] * price
					now_info[num]['cash'] += (amount - cap[j][1]) * quality
					log[num]['gain_sell'] += cap[j][1] * price + (amount - cap[j][1]) * quality
					cap[j][1] = 0
				break
			elif quality >= cap[-1][0]:
				if amount <= cap[-1][1]:
					now_info[num]['cash'] += amount * price
					log[num]['gain_sell'] += amount * price
					cap[j][1] -= amount
				else:
					now_info[num]['cash'] += cap[j][1] * price
					now_info[num]['cash'] += (amount - cap[j][1]) * quality
					log[num]['gain_sell'] += cap[j][1] * price + (amount - cap[j][1]) * quality
					cap[j][1] = 0
				break
			elif quality < cap[0][0]:
				now_info[num]['cash'] += amount * quality
				log[num]['gain_sell'] += amount * quality
				break

	for i in [1,2,3,4,5,6,7,8,9]:
		if now_info[i]['type'] == 0:
			for j in range(len(now_info[i]['material'])):
				now_info[i]['cash'] -= store_fee * now_info[i]['material'][j][2]
				log[i]["depreciation"] += store_fee * now_info[i]['material'][j][2]
		elif now_info[i]['type'] == 1:
			now_info[i]['product'] = []
			for j in range(len(now_info[i]['chip'])):
				now_info[i]['cash'] -= store_fee * now_info[i]['chip'][j][2]
				log[i]["depreciation"] += store_fee * now_info[i]['chip'][j][2]



	#记录生产量
	# temp_cap=0
	# for i in [1,2,3,4,5,6,7,8,9]:
	# 	if now_info[i]['type']==0:
	# 		continue
	# 	temp_cap+=now_info[i]['product']
	#系统梯度收购
	# class_info=[[0 for col in range(11)] for row in range(11)]
	# cap=south_capacity[gl.game_round]
	# info=now_info[:]
	# info=sorted(info,key=lambda x:x['curr_price'])
	# row=col=1
	# sum=0

	# 归类算法，按照相同的定价分类
	# for i in [1,2,3,4,5,6,7,8,9]:
	# 	if info[i]['type']==0:
	# 		continue
	# 	temp=info[i]
	# 	if col!=1 and class_info[row][col-1]['curr_price']!=temp['curr_price']:
	# 		class_info[row][-1]=sum
	# 		row+=1
	# 		col=1
	# 		temp=info[i]
	# 		sum=0
	# 	sum+=info[i]['product']
	# 	if i==len(now_info)-1:
	# 		class_info[row][-1]=sum		#将该类企业的产品总数量存于数组末尾
	# 	class_info[row][col]=temp
	# 	col+=1
	
	#梯度回收算法 复杂度约为O(N^2)
	# for i in [1,2,3,4,5,6,7,8,9]:
	# 	if cap==0 or class_info[i][1]==0:     #市场容量已满
	# 		break
	# 	gl.max_price=class_info[i][1]['curr_price']
	# 	if class_info[i][-1] < cap:
	# 		cap-=class_info[i][-1]
	# 		for j in [1,2,3,4,5,6,7,8,9]:
	# 			if class_info[i][j]==0:
	# 				break
	# 			class_info[i][j]['cash']+=class_info[i][j]['product']*class_info[i][j]['curr_price']
	# 			log[class_info[i][j]['id']]['gain_sell']=class_info[i][j]['product']*class_info[i][j]['curr_price']	#记录收益
	# 			class_info[i][j]['product']=0
	# 	else:
	# 		for j in [1,2,3,4,5,6,7,8,9]:
	# 			if class_info[i][j]==0:
	# 				break
	# 			sellAmount=round(class_info[i][j]['product']/class_info[i][-1]*cap)
	# 			class_info[i][j]['product']-=sellAmount
	# 			class_info[i][j]['cash']+=sellAmount*class_info[i][j]['curr_price']
	# 		cap=0
	#
	# for i in [1,2,3,4,5,6,7,8,9]:
	# 	for j in [1,2,3,4,5,6,7,8,9]:
	# 		if isinstance(class_info[i][j],dict):
	# 			now_info[class_info[i][j]['id']]['product']=class_info[i][j]['product']  #id在此处发挥作用
	# 		else:
	# 			break

	#投资结算
	for i in [1,2,3,4,5,6,7,8,9]:
		#for j in [1,2,3,4]:
		log[i]["investFDC_total"] = round(now_info[i]['invest'][1]*(1+profit[1][gl.game_round]),1)
		log[i]["investNY_total"] = round(now_info[i]['invest'][2]*(1+profit[2][gl.game_round]),1)
		log[i]["investYL_total"] = round(now_info[i]['invest'][3]*(1+profit[3][gl.game_round]),1)
		log[i]["investWL_total"] = round(now_info[i]['invest'][4]*(1+profit[4][gl.game_round]),1)
		
		now_info[i]['cash'] += log[i]["investFDC_total"]+log[i]["investNY_total"] +log[i]["investYL_total"]+log[i]["investWL_total"]
			#now_info[i]['cash']+=now_info[i]['invest'][j]*profit[j][gl.game_round]
		for j in [1,2,3,4]:
			now_info[i]['invest'][j]=0
			
	# 折旧与仓储结算
	# for i in [1,2,3,4,5,6,7,8,9]:
	# 	if now_info[i]['type']==0:
	# 		log[i]["depreciation"] = depreciation_a*now_info[i]['product']+depreciation_material_a*now_info[i]['material']
	# 		# log[i]["storage"] = round((storage_a*now_info[i]['material'] + storage_chip*now_info[i]['product']),1)
	# 		log[i]["storage"]=now_info[i]['store_cost']
	# 		now_info[i]['cash']-= log[i]["depreciation"]  #折旧、仓储
	# 		now_info[i]['cash']-= log[i]["storage"]
	#
	# 		if now_info[i]['fee'] == reduced_fee:
	# 			now_info[i]['fee'] = processfee_a	#恢复为正常加工费
	# 	else:
	# 		log[i]["depreciation"] = depreciation_a*now_info[i]['chip']+depreciation_b*now_info[i]['product']+depreciation_material_b*now_info[i]['material']
	# 		# log[i]["storage"] = round((storage_b*now_info[i]['material'] + storage_chip*now_info[i]['chip']),1)
	# 		log[i]["storage"]=now_info[i]['store_cost']
	# 		now_info[i]['cash']-= log[i]["depreciation"]
	# 		now_info[i]['cash']-= log[i]["storage"]
	# 		if now_info[i]['fee'] == reduced_fee:
	# 			now_info[i]['fee'] = processfee_b
	# 	if now_info[i]['storage']==1000 or now_info[i]['storage']==700: #使用了仓储卡的玩家
	# 		now_info[i]['store_cost']+=cost_store
	
	# 还款结算
	for i in [1,2,3,4,5,6,7,8,9]:
		log[i]["loan"] = 0
		for j in range(len(now_info[i]["loan"])):
			if now_info[i]["loan"][j][0] != 0 and now_info[i]["loan"][j][2]==gl.game_round:
				log[i]["loan"] += round(now_info[i]["loan"][j][0] * (1+now_info[i]["loan"][j][1]),1)
				now_info[i]["loan"][j][0] = 0
		now_info[i]["cash"] += log[i]["loan"]
		
	# 破产
	for i in [1,2,3,4,5,6,7,8,9]:
		if now_info[i]["cash"] < 0:
			selloff(now_info[i])
			if now_info[i]["cash"] <= 0:  #淘汰
				#淘汰提示
				eliminate(now_info,i)  
				#债务取消
				pass
			
	
	if gl.game_round == end_round:  #游戏结束，变卖所有资产
		for i in [1,2,3,4,5,6,7,8,9]:
			selloff(now_info[i])
			if now_info[i]["result"]!=1:
				now_info[i]["cash"]=round(now_info[i]["cash"]*now_info[i]["result"],2)
				
				
	for i in [1,2,3,4,5,6,7,8,9]:
		now_info[i]["cash"] = round(now_info[i]["cash"],1)
		shutil.copyfile(path+chr(48+i)+".json",path+chr(48+i)+"_bak.json")
		f=open(path+chr(48+i)+".json","w")
		json.dump(now_info[i],f)
		f.close()
		
	f=open(path+"log.json","w")  #将日志写到文件里保存
	json.dump(log,f)
	f.close()
	
	#游戏结束
	if gl.game_round == end_round: 
		gl.game_round=6
	else:
		# 轮数标记+1
		gl.game_round+=1
	f=open(path+"game.txt","w")
	f.write(str(gl.game_round))
	f.close()

def takecompetition(product):
	return product[5]

#资产变卖
def selloff(now_info):
	if now_info["type"]==0:
		for i in range(len(now_info["material"])):
			now_info["cash"] += now_info["material"][i][1]     #成本价回收
	else:
		for i in range(len(now_info["chip"])):
			now_info["cash"] += now_info["chip"][i][1]         #成本价回收
	now_info["material"] = []
	now_info["chip"] = []
	now_info["product"] = []

def eliminate(now_info,outer):
	for i in [1,2,3,4,5,6,7,8,9]:
		if i == outer:  #自己的所有债都取消了
			for j in range(len(now_info[outer]["loan"])):
				now_info[i]["loan"][j][0] = 0
		else:  #别人借得也取消
			for j in range(len(now_info[i]["loan"])):
				if now_info[i]["loan"][j][3] == outer: #有债务关系，一律解除
					now_info[i]["loan"][j][0] = 0

#资产排序
def asset_sort():
	#global term
	term=[]
	for i in [1,2,3,4,5,6,7,8,9]:
		f=open(path+chr(48+i)+".json","r")
		temp_txt=f.read()
		now_info=json.loads(temp_txt)
		f.close()
		if gl.game_round<6 and now_info['cash']>=0:
			final_cash=round(now_info['cash']*now_info['result'],2)
		else:
			final_cash=now_info['cash']
		term.append([final_cash,i,now_info["type"]])

	term.sort(reverse = True)
	return term


