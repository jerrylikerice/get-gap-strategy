#coding=utf-8

#����mytrader���ս����ļ�

import struct,time

def anaDayByte():
	binfile=open('4.dat','rb').read()
	i=76
	f=open('if_conti.txt','w')
#	timestamp,op,clo,high,low,vol,hol,aver,=struct.unpack('ifffffff',binfile[0:32])
#	print '%s,%f,%f,%f,%f,%f,%f,%f' %(time.strftime('%Y%m%d %H:%M:%S',time.localtime(timestamp)),op,clo,high,low,vol,hol,aver)

	
	while i<len(binfile):
		dataL=binfile[i:i+32]
		timestamp,op,clo,high,low,vol,hol,aver,=struct.unpack('ifffffff',dataL)
		f.write('%s,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n' %(time.strftime('%Y%m%d %H:%M',time.localtime(timestamp)),op,clo,high,low,vol,hol,aver))		
		i=i+36
	f.close()
def main():
	anaDayByte()

if __name__=='__main__':
	main()
	