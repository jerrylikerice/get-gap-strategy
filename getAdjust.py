#coding=utf-8

flog=open('periods_log.txt','w')

def writeLog(str,f):
	f.write(str+'\n')
	
def readList(file):
	f=open(file)
	lines=f.readlines()
	infos=[]
	for line in lines:
		infos.append([line.strip().split(',')[0]]+map(lambda x:float(x),line.strip().split(',')[1:]))
	return infos

def getAllPeriod(lowestPrice,highestPrice,spread,infos):
	AllPeriod=[]
	startPrice=lowestPrice
	while startPrice<highestPrice:
		endPrice=startPrice*(1+0.08)
		tempPeriod=getAdjustPeriod(infos,startPrice,endPrice)
		AllPeriod+=tempPeriod
		writeLog(("*******%f*******%f*********" %(startPrice,endPrice)),flog)
		for t in tempPeriod:
			writeLog(("%s,%s" %(infos[t[0]][0],infos[t[1]][0])),flog)
		
		startPrice+=spread
	return AllPeriod
	
def getAdjustPeriod(infos,startPrice,endPrice):
	bits=[0 for i in range(len(infos))]
	for i in range(len(bits)):
		high=infos[i][2]
		low=infos[i][3]
		if (high>endPrice and low<endPrice) or (high>startPrice and high<endPrice) or (high<endPrice and low>startPrice):
			bits[i]=1
	
	AdjustPeriod=[]
	#计算bits中连续长度符合要求者
	start=0
	end=0
	length=0
	lenThre=30
	
	i=0
	while i<len(bits):
		if bits[i]==1:
			if start==0:
				start=i
			length+=1
			i+=1
		else:
			if length>0:
				end=start+length
				AdjustPeriod.append((start,end))
				i=end
				start=0
				end=0
				length=0
			else:
				i+=1
	
	periods=filter(lambda x:x[1]-x[0]>lenThre,AdjustPeriod)
	return periods
	
def main():
	ff=open('periods.txt','w')
	
	infos=readList('SZ000004.TXT')
	
	highs=map(lambda x:x[2],infos)
	lows=map(lambda x:x[3],infos) 

	highestPrice=max(highs)
	lowestPrice=min(lows)
	spread=0.2
	
	periods=getAllPeriod(lowestPrice,highestPrice,spread,infos)
#	print periods
	
#	periods.sort(key=lambda x:x[0]-x[1])
	periods.sort(key=lambda x:x[0])
	
	for sta,end in periods:
#		print '%s,%s' %(infos[sta][0],infos[end][0])
		writeLog('%s,%s' %(infos[sta][0],infos[end][0]),ff)
	
if __name__=="__main__":
	main()