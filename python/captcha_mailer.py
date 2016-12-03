#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64
import magic 
import StringIO
import sys

import smtplib
from smtplib import SMTPException
import imaplib

import email
from email.Header import Header
from email.header import decode_header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 

from logger import g_logger

class CaptchaSmtper:

	smtp_obj = None
	reset_flag = 0
	_charset = 'utf-8'

	# setting
	host = ''
	port = ''
	user = ''
	password = ''
	
	def __init__(self, user, password, host, port = 25):
		self.host = host
		self.port = port
		self.user = user
		self.password = password 
		reset_flag = 1

	def reset(self, user, password, host, port = 25):
		self.host = host
		self.port = port
		self.user = user
		self.password = password 
		reset_flag = 1


	def simple_send(self, sender, receiver, subject, content):
		try:
			if(self.smtp_obj == None or self.reset == 1):
				self.smtp_obj = smtplib.SMTP(self.host, self.port)
				self.reset = 0
				# error handle

			#message = simple_mesage_build(sender, receiver, subject, content)
			#print "Mail mesasge: %s" % (message)
			self.smtp_obj.ehlo()
			self.smtp_obj.starttls()
			self.smtp_obj.ehlo()
			self.smtp_obj.login(self.user, self.password)
			self.smtp_obj.sendmail(sender, receiver, message) 
			self.smtp_obj.quit()        
			print "Successfully sent email"
		except SMTPException as err:
			err_msg = err[1].decode('GBK')
			print "Send email failed: [%d]%s" % (err[0], err_msg)

	def captcha_mail_send(self, sender, receiver, subject, captcha_file):
		try:
			if(self.smtp_obj == None or self.reset == 1):
				self.smtp_obj = smtplib.SMTP_SSL(self.host, self.port)
				self.reset = 0
				# error handle

			# set subject
			msg_from = "%s <%s>" % (Header(sender,'utf-8'), sender)
			msg_to = "%s <%s>" % (Header(receiver,'utf-8'), receiver)
			msg = MIMEMultipart('alternative')
			msg['Subject'] = Header(subject,'utf-8')	
			msg['From'] = msg_from
			msg['to'] = msg_to

			# set image file
			fp = open(captcha_file,'rb')
			image_base64 = base64.b64encode(fp.read())
			mime = magic.Magic(mime=True)
			image_src = 'data:%s;base64,%s' % (mime.from_file(captcha_file), image_base64)
			fp.close()

			# set tips
			html = '<html><body><img src="%s"><p style="color:red;">注: 仅回复验证码。</p><body></html>' % (image_src) 
			html_mime = MIMEText(html, 'html', 'utf-8')
			msg.attach(html_mime)

			#print "html mesasge: %s" % (html)
			#print "Mail mesasge: %s" % (msg.as_string())

			# login and send
			self.smtp_obj.login(self.user, self.password)
			self.smtp_obj.sendmail(sender, receiver, msg.as_string()) 
			self.smtp_obj.quit()        

			return 0

		except SMTPException as err:
			err_msg = err[1].decode('GBK')
			print "Send email failed: [%d]%s" % (err[0], err_msg)
			return -1

class CaptchaImap4er:

	imap4_obj = None
	reset_flag = 0

	# setting
	host = ''
	port = ''
	user = ''
	password = ''
	
	def __init__(self, user, password, host, port = 143):
		self.host = host
		self.port = port
		self.user = user
		self.password = password 
		reset_flag = 1

	def reset(self, user, password, host, port = 143):
		self.host = host
		self.port = port
		self.user = user
		self.password = password 
		reset_flag = 1

	def get_text_from_payload(self, payload):
		text = ""
		maintype = payload.get_content_maintype()
		if(payload.is_multipart()):
			for pl in payload.get_payload():
				text += self.get_text_from_payload(pl)
		elif(maintype == 'text'):
			enc = payload['Content-Transfer-Encoding']
			charset = payload.get_content_charset()
			#print "charset = '%s'" % payload.get_content_charset()
			if(charset == 'gb18030' or charset == 'gbk' or charset == 'GBK'):
				charset = 'GBK' 

			if(enc == 'base64'):
				text = base64.b64decode(payload.get_payload())
			else:
				text = payload.get_payload()

			if(charset != 'utf-8'):
				text = text.decode(charset).encode('utf-8')
		else:
			#print "ignore maintype = '%s'" % maintype 
			g_logger.warning("ignore maintype = '%s'" % maintype)
		return text

	def captcha_mail_receive(self, sender, receiver, subject0):
		try:
			if(self.imap4_obj == None or self.reset == 1):
				self.imap4_obj = imaplib.IMAP4_SSL(self.host, self.port)
				self.reset = 0
				# error handle

			captcha = ''
			self.imap4_obj.login(self.user, self.password)
			self.imap4_obj.select("inbox")
			result, data = self.imap4_obj.search(None, 'ALL')
			#i = 0
			mailid_list = data[0].split()
			count = len(mailid_list)
			fetch_list = reversed(xrange(count-10, count+1))
			#print "mailid_list length: %d, %s" % (len(mailid_list), mailid_list[3])
			g_logger.warning("mailid_list length: %d, %s" % (len(mailid_list), mailid_list[3]))
			for num in fetch_list:
				result, data = self.imap4_obj.fetch(num, '(RFC822)')
				raw_email = data[0][1]
				email_message = email.message_from_string(raw_email)

				charset = 'utf-8'

				# parse subject, from, to
				subject_info = decode_header(email_message['Subject'])[0]
				if(subject_info[1] == 'gb18030'):
					charset = 'GBK'
					subject = subject_info[0].decode(charset).encode('utf-8')
				else:
					subject = subject_info[0]

				# check if it's reply of captcha email by subject
				if(subject.find(subject0) < 0):
					continue

				msg_from = email.utils.parseaddr(email_message['From'])
				msg_to = email.utils.parseaddr(email_message['To'])
				#print "Subject: %s" % (subject)
				#print "From: %s" % (msg_from[1])
				#print "To: %s" % (msg_to[1])
				g_logger.info("Subject: %s" % (subject))
				g_logger.info("From: %s" % (msg_from[1]))
				g_logger.info("To: %s" % (msg_to[1]))

				text = self.get_text_from_payload(email_message)
				buf = StringIO.StringIO(text)
				captcha = buf.readline().splitlines()[0]
				#print "captcha = '%s'" % captcha 
				g_logger.info("captcha = '%s'" % captcha)
				#print "Body: \n%s" % text
				#print "==========================================="
				break # finished if found the reply email

			self.imap4_obj.close()
			self.imap4_obj.logout()

			return captcha

		except SMTPException as err:
			err_msg = err[1].decode('GBK')
			#print "Send email failed: [%d]%s" % (err[0], err_msg)
			g_logger.error("Send email failed: [%d]%s" % (err[0], err_msg))
			return '-1'

def unit_test_1(argv):
	if(len(argv) != 3):
		print "Usage: %s <user> <passwd>" % argv[0]
		return

	user = argv[1] 
	password = argv[2] 
	host = "smtp.qq.com"
	port = 465
	mailer = CaptchaSmtper(user, password, host, port)

	#mailer.simple_send("519916178@qq.com", "me@liudonghua.net", "Hello World", "Hi all, good day!")
	mailer.captcha_mail_send("519916178@qq.com", "me@liudonghua.net", "亚马逊验证码-请10分钟内回复", "samples/captcha_amazon.jpg")

def unit_test_2(argv):
	if(len(argv) != 3):
		print "Usage: %s <user> <passwd>" % argv[0]
		return

	user = argv[1] 
	password = argv[2] 
	host = "imap.qq.com"
	port = 993
	mailer = CaptchaImap4er(user, password, host, port)

	#mailer.simple_send("519916178@qq.com", "me@liudonghua.net", "Hello World", "Hi all, good day!")
	captcha = mailer.captcha_mail_receive("519916178@qq.com", "me@liudonghua.net", "亚马逊验证码-请10分钟内回复")

def unit_test_3():
	captcha = 'xmkleo'
	g_logger.info("test log in captcha mailer. %s" % (captcha))

def __init__():
	#unit_test_1(sys.argv)
	#unit_test_2(sys.argv)
	#unit_test_3()
	
