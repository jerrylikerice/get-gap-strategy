#coding=utf-8

#解析mytrader的日交易文件

import struct,time

def anaDayByte():
	binfile=open('00010050.dat','rb').read()
	i=0
	f=open('if_conti.txt','w')
#	timestamp,op,clo,high,low,vol,hol,aver,=struct.unpack('ifffffff',binfile[0:32])
#	print '%s,%f,%f,%f,%f,%f,%f,%f' %(time.strftime('%Y%m%d',time.localtime(timestamp)),op,clo,high,low,vol,hol,aver)

	while i<len(binfile):
		dataL=binfile[i:i+32]
		timestamp,op,clo,high,low,vol,hol,aver,=struct.unpack('ifffffff',dataL)
		f.write('%s,%.0f,%.0f,%.0f,%.0f,%.0f,%.0f,%.0f\n' %(time.strftime('%Y%m%d',time.localtime(timestamp)),op,clo,high,low,vol,hol,aver))		
		i=i+37
	
def main():
	anaDayByte()

if __name__=='__main__':
	main()
	