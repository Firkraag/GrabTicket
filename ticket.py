#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import urllib2
import json

status = False
msg = ""
from_addr = 'XXXXXXXXXXXXXXXXXXXX'
password = 'XXXXXXXXXXXXXXXXXXXX'
smtp_server = 'XXXXXXXXXXXXXXXXXXXX'
to_addr = 'XXXXXXXXXXXXXXXXXXXX'
infos = [['SmilingWang', '2015-01-01', 'RAH', 'SZQ']]

def inquiry(url):
	global status, msg
	sit = ['yz_num', 'rz_num', 'yw_num', 'rw_num', 'gr_num', 'zy_num', 'ze_num', 'tz_num', 'gg_num', 'yb_num', 'qt_num', 'swz_num']
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	the_page = response.read() # string
	decodejson = json.loads(the_page)
	try:
		data = decodejson['data']
	except:
		status = False
		return 255
	for i in range(len(data)):
		left = data[i][u'queryLeftNewDTO']
		for j in sit:
			if left[j] == u'有':
				msg  =  msg + left['station_train_code'] + " : " + j + " "	
				status = True	
	if status == False:
		msg = msg + ":  no ticket"
	status = False
	msg = msg + "\n"
def email(): 
	global msg, status

	from email import encoders
	from email.header import Header
	from email.mime.text import MIMEText
	from email.utils import parseaddr, formataddr
	import smtplib
	
	def _format_addr(s):
		name, addr = parseaddr(s)
		return formataddr(( \
		Header(name, 'utf-8').encode(), \
		addr.encode('utf-8') if isinstance(addr, unicode) else addr))

	server = smtplib.SMTP(smtp_server) # SMTP协议默认端口是25
	server.set_debuglevel(1)
	server.login(from_addr, password)
	text = MIMEText(msg, 'plain', 'utf-8')
	text['From'] = _format_addr('SmilingWang <%s>' % from_addr)
	text['To'] = _format_addr('SmilingWang <%s>' % to_addr)
	text['Subject'] = Header('Left ticket info', 'utf-8').encode()
	server.sendmail(from_addr, [to_addr], text.as_string())
	server.quit()		
	

for i in range(len(infos)):
	info = infos[i]	
	url = 'https://kyfw.12306.cn/otn/leftTicket/queryT?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT' % (info[1], info[2], info[3])
	print url
	msg = msg + info[0] + info [1] + ": "
	inquiry(url)
email()
