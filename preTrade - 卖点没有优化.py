#coding=utf-8
import os
mis=2
maday=20
stoplossmis=2

#对价格gap再细化选择，这样gap之间太小了
#卖出点如何？

def writeLog(str,f):
	f.write(str+'\n')

def historyRecord(high,low):
	return max(high),min(low)
	
def malist(price,day):
	ma=[0 for i in range(len(price))]
	for i in range(day,len(price)):
		ma[i]=sum(price[(i-day):i])/day
	return ma
	


def tops(high,ran):
	topl=[]
	for i in range(ran,len(high)-ran):
		ifTop=True
		for j in range(-ran,ran+1):
			if high[i+j]>high[i]:
				ifTop=False
		if ifTop==True:
			topl.append(i)
	return topl

def bottoms(low,ran):
	bottoml=[]
	for i in range(ran,len(low)-ran):
		ifBot=True
		for j in range(-ran,ran+1):
			if low[i+j]<low[i]:
				ifBot=False
		if ifBot==True:
			bottoml.append(i)	
	return bottoml
	
def readList(file):
	f=open(file)
	lines=f.readlines()
	infos=[]
	for line in lines:
		infos.append([line.strip().split(',')[0]]+map(lambda x:float(x),line.strip().split(',')[1:]))
	return infos
	
def buy(index,infos,ff):
	ff.write('buy,%s,%s,%s,%s,%s\n' %(infos[index][0],infos[index][1],infos[index][2],infos[index][3],infos[index][4]))

def sell(index,gaps,infos,mas):
	i=index
	j=0
	
	cut=gaps[0]
	
	while i<len(infos):
		if j>=len(gaps)-1:
			cut=max(gaps[j],mas[i])
		else:
			if infos[i][3]>gaps[j+1]: 
				#raise stop prices
				j=j+1
				cut=gaps[j]
			
		if cut-infos[i][3]>stoplossmis:
			#sell
			return i

		i=i+1
	
def main():

	ff=open('recode.txt','w')
	flog=open('log.txt','w')
	
	infos=readList('SZ000002.TXT')
	print len(infos)
	mas=malist(map(lambda x:x[4],infos),maday)
	
	highs=map(lambda x:x[2],infos)
	lows=map(lambda x:x[3],infos)
	
	varis=[info[2]-info[3] for info in infos]
	varis.sort()
	p95=varis[int(len(varis)*0.95)]
	print p95
	
	maxs=tops(highs,2)
	mins=bottoms(lows,2)
	
	bits=[0 for i in range(len(infos))]
	for i in maxs:
		bits[i]=2
	for i in mins:
		bits[i]=1
		
#	print bits
	
	foreDay=120
	
	i=foreDay
	while i<len(infos):
		priceGaps_t=[]
		for j in range(i-foreDay,i):
			#之前的极值点钟，比当前价格的最低价高，或者比前一个的最低价高，而且当前的最低价高于之前最高价（跳空的情形，需要有一个gap）
			#if bits[j]==2 and (infos[j][2]>=infos[i][3] or (infos[j][2]>=infos[i-1][3] and infos[i][3]>infos[i-1][2])):
			if bits[j]==2:
				priceGaps_t.append(infos[j][2])
		
		priceGaps_t.sort()
		priceGaps_t.reverse()
		
		priceGaps=[]
		
		for jjj in range(len(priceGaps_t)):
			if priceGaps_t[jjj]>=infos[i][3]:
				priceGaps.append(priceGaps_t[jjj])
			else:
				break

		if infos[i][3]-priceGaps_t[jjj]<p95:
			priceGaps.append(priceGaps_t[jjj])
		
		priceGaps.reverse()
#		print priceGaps
		writeLog(','.join([str(x) for x in priceGaps]),flog)
		
		gaps=[]
	
		# if len(priceGaps)<=0:
			# gaps.append(infos[i][3])
			# bits[i]=2
		y=priceGaps[0]
		gaps.append(y)
		for ii in range(1,len(priceGaps)):
			if (priceGaps[ii]-y)>0.1*y:
				y=priceGaps[ii]
				gaps.append(y)
			elif (priceGaps[ii]-y)>0:
				y=priceGaps[ii]
				gaps[-1]=y
		
#		print i
#		print gaps
		writeLog(infos[i][0],flog)
		writeLog(','.join([str(x) for x in gaps]),flog)
		#最高价比gap0大于阈值则买入
#		if infos[i][2]-gaps[0]>p95 and (len(gaps)==1 or (gaps[1]-gaps[0])>0.1*gaps[0]):
		#应该是下一gap与当前价格比较
		if infos[i][2]-gaps[0]>min(p95,0.1*gaps[0]) and (len(gaps)==1 or (gaps[1]-infos[i][4])>0.1*gaps[0]):
#			os.system('pause')
			writeLog('~~~~~~~~~~~buy at '+str(i),flog)
			buy(i,infos,ff)
			i=sell(i+1,gaps,infos,mas)
#			print i
			ff.write('close,%s,%s,%s,%s,%s\n' %(infos[i][0],infos[i][1],infos[i][2],infos[i][3],infos[i][4]))
			continue
		i=i+1	
		
	
	
	
	
if __name__=="__main__":
	main()
