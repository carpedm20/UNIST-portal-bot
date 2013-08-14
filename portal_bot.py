# -*- coding:utf-8 -*-
import mechanize
import spynner
import facebook
import base64
import os
import time
import math
import Image
import atexit
import subprocess
from xvfbwrapper import Xvfb
import socket

facebook_id = 'hexa.portal@gmail.com'
facebook_pass = ''
facebook_id2 = 'hexa.food@gmail.com'
facebook_pass2 = ''

encrypted_password = ''
login_url = 'https://portal.unist.ac.kr/EP/web/login/login_chk.jsp?loginid=carpedm20&password=' + encrypted_password + '&cookie=off&LangSet=ko&loginmethod=Id&lang=K&roundkey=&browsertype=MSIE'
token_request_url = 'https://www.facebook.com/dialog/oauth?scope=publish_stream,publish_actions,&redirect_uri=http://carpedm20.blogspot.kr&response_type=token&client_id=256972304447471'
token_request_url2 = 'https://www.facebook.com/dialog/oauth?scope=publish_stream,publish_actions,&redirect_uri=http://carpedm20.blogspot.kr&response_type=token&client_id=530042293708395'

def exit_handler():
	print "DEAD"
	vdisplay.stop()
	#send_mail("Bot is DEAD")

atexit.register(exit_handler)

vdisplay = Xvfb()
vdisplay.start()

while 1:
	br_mech = mechanize.Browser()
	br_mech.set_handle_robots(False)
	br_mech.open(login_url)
	
	for boardid in ['B200902281833482321051', 'B200902281833016691048']:
		r = br_mech.open('http://portal.unist.ac.kr/EP/web/collaboration/bbs/jsp/BB_BoardLst.jsp?boardid='+boardid+'&nfirst=1')
		html=r.read()

		id_list=[]

		for str1 in html.split('javascript:clickBulletin("'):
			id_list.append(str1.split('","')[0])

		id_list.remove(id_list[0])

		for id_item in id_list:
			files = [f for f in os.listdir('.') if os.path.isfile(f)]

			new = False

			for f in files:
				if f.find(id_item) is not -1:
					new = True

			if new is False:
				link = token_request_url

				#print '[1] open link'
				br_mech.open(link)

				#print '[2] current url : ' + br_mech.geturl()

				br_mech.form = list(br_mech.forms())[0]
				control = br_mech.form.find_control("email")
				control.value = facebook_id
				control = br_mech.form.find_control("pass")
				control.value = facebook_pass

				#print '[3] submit'
				br_mech.submit()

				#print '[4] current url : ' + br_mech.geturl()

				app_access = br_mech.geturl().split('token=')[1].split('&expires')[0]
				print '[5] access token : ' + app_access

				br_spy = spynner.Browser()
				br_spy.load(login_url)
				br_spy.load('http://portal.unist.ac.kr/EP/web/collaboration/bbs/jsp/BB_BoardLst.jsp?boardid='+boardid+'&nfirst=1')
				br_spy.load("http://portal.unist.ac.kr/EP/web/collaboration/bbs/jsp/BB_BoardView.jsp?boardid="+boardid+"&bullid="+id_item)

				print '[6] save : '
				br_spy.snapshot().save(id_item + '.png')

				img=Image.open(id_item + '.png')
				width, height = img.size
				print 'height : ' + str(height)

				slice_num=1
				sliced=False

				if height > 1200:
					slice_num=2
					sliced=True
				if height > 2000:
					slice_num=3
					sliced=True
				if height > 2800:
					slice_num=4
					sliced=True
				if height > 3600:
					slice_num=5
					sliced=True

				print 'sliced num : ' + str(slice_num)

				if sliced is True:
					long_slice(id_item + '.png',id_item,os.getcwd(),slice_num)

				graph = facebook.GraphAPI(app_access)

				title = br_spy.html.split('class="tb_left">')[1].split('>')[1].split('</')[0].strip().encode('utf-8')

				print '[7] upload : ' + id_item
				if title.find('주간메뉴표') is not -1:
					link = token_request_url2

					#print '[1] open link'
					food_br = mechanize.Browser()
					food_br.set_handle_robots(False)
					food_br.open(link)

					#print '[2] current url : ' + br_mech.geturl()

					food_br.form = list(food_br.forms())[0]
					control = food_br.form.find_control("email")
					control.value = facebook_id2
					control = food_br.form.find_control("pass")
					control.value = facebook_pass2

					#print '[3] submit'
					food_br.submit()

					#print '[4] current url : ' + br_mech.geturl()

					app_access = food_br.geturl().split('token=')[1].split('&expires')[0]
					print '[5] access token : ' + app_access

					r = br_mech.open("http://portal.unist.ac.kr/EP/web/collaboration/bbs/jsp/BB_BoardView.jsp?boardid="+boardid+"&bullid="+id_item)
					r = r.read()
					r = r[r.find('fid=')+4:]
					fid = r[:r.find('&jndiname=')]

					r = br_mech.open("http://portal.unist.ac.kr/EP/web/common/attach/att_list.jsp?fid="+fid+"&jndiname=BB_Attach")

					br_mech.select_form(name="frmList")

					try:
					   file0 = br_mech.form['sInfo0']
					except:
					   file0 = ''

					try:
					   file1 = br_mech.form['sInfo1']
					except:
					   file1 = ''

					br_mech.select_form(name="frmSubmit")
					br_mech.form.find_control("fileinfos").readonly = False

					if file1 is '':
						br_mech.form['fileinfos'] = file0 + "\x1F"
					else:
						br_mech.form['fileinfos'] = file0 + "\x1F" + file1 + "\x1F"

					br_mech.form.find_control("viewdown").readonly = False
					br_mech.form['viewdown']='view'

					r = br_mech.submit()
					data= str(r.read())
					#print data

					data = data[data.find("/wwasdata/acube/ep/acube_sftptemp/")+1:]

					start0 = data.find("/wwasdata/acube/ep/acube_sftptemp/")
					end0 = data.find("\x1d",start0)
					start1 = data.find("/wwasdata/acube/ep/acube_sftptemp/",end0)
					end1= data.find("\x1d",start1)

					sh0 = data[start0:end0]
					sh1 = data[start1:end1]

					print "[*] 0 : " + sh0
					print "[*] 1 : " + sh1

					f_count = 0
					h = br_spy.html
					for sh in [sh0, sh1]:
						if h.find('sAttachReal" value=') is not -1:
							h = h[h.find('sAttachReal" value=')+len('sAttachReal" value=')+1:]
						title = h[:h.find('.xls')].encode('utf-8')
						h = h[h.find('.xls')+5:]

						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.connect(('sftp.unist.ac.kr', 7775))
						s.settimeout(0.5)

						send_data = "DOWNLOAD\x091\x091\x09"+sh

						send_len = str(len(send_data))
						i = len(send_len)

						while i< 10:
							send_len = "0"+send_len
							i=i+1

						print "[#] Send : " + send_len
						s.send(send_len)
						s.send(send_data)

						get = s.recv(1024)
						print "[1] " + get
						get = s.recv(1024)
						print "[2] " + get

						data = ''
						while True:
							try:
								dd = s.recv(1024)

								if len(dd) is 0:
									print "[$] File END"
									break

								data += dd
								print ".",
							except:	
								s.send('\x30\x30\x30\x30\x30\x30\x30\x30\x30\x30')
								print "[#] Again"
						s.close()

						f_name = sh[sh.find('temp/')+5:]

						f = open(f_name,'wb')
						f.write(data)
						f.close()

						print "[*] " + sh + " END"

						subprocess.call('cp '+f_name+' ~/public_html/',shell=True)
						br_spy.load('http://hexa.perl.sh/~carpedm30/excel.php?name='+f_name)
						f_name = 'food_'+base64.b64encode(title)+'.png'
						br_spy.snapshot().save(f_name)
						img=Image.open(f_name)
						width, height = img.size
						print 'width : ' + str(width)

						slice_num=3
						sliced=True

						print 'sliced num : ' + str(slice_num)

						if sliced is True:
							width_slice(f_name,f_name,os.getcwd(),slice_num)

						graph = facebook.GraphAPI(app_access)

						if sliced is True:
							for nums in range(1, slice_num+1):
								nums=slice_num-nums+1
								print '[7] upload : ' + f_name + '_' + str(nums)

								graph.put_photo( open(f_name + '_' + str(nums) + '.png'), '부활 성공? :)\r\n\r\n' + title + ' ['+str(nums)+'/'+str(slice_num)+']'+'\r\n\r\nDesigned by carpedm20', "")

						#graph.put_photo( open(f_name + '.png'), title+'\r\n\r\nDesigned by carpedm20', "")
						print "put_photo finished"
						
					link = token_request_url

					#print '[1] open link'
					br_mech.open(link)

					#print '[2] current url : ' + br_mech.geturl()

					br_mech.form = list(br_mech.forms())[0]
					control = br_mech.form.find_control("email")
					control.value = facebook_id
					control = br_mech.form.find_control("pass")
					control.value = facebook_pass

					#print '[3] submit'
					br_mech.submit()

					#print '[4] current url : ' + br_mech.geturl()

					app_access = br_mech.geturl().split('token=')[1].split('&expires')[0]
					print '[5] access token : ' + app_access
				else:
					if sliced is True:
						for nums in range(1, slice_num+1):
							nums=slice_num-nums+1
							print '[7] upload : ' + id_item + '_' + str(nums)
							graph.put_photo( open(id_item + '_' + str(nums) + '.png'), br_spy.html.split('class="tb_left">')[1].split('>')[1].split('</')[0].strip().encode('utf-8')+' ['+str(nums)+'/'+str(slice_num)+']'+'\r\n\r\nDesigned by carpedm20', "")
					else:
						graph.put_photo( open(id_item + '.png'), title+'\r\n\r\nDesigned by carpedm20', "")
				send_mail(title, id_item+'.png')

	time.sleep(10)
