# -*- coding:utf-8 -*-
import mechanize
import spynner
import facebook
import base64
import os
import time
import math
from PIL import Image
import smtplib
import atexit
import subprocess
from xvfbwrapper import Xvfb
from email.MIMEImage import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from config import *
import urllib2
import socket

EMAIL_URL = "http://msn.unist.ac.kr/portalbot/carpedm20.txt"

def send_mail(text, filename=''):
  global email_username, email_password
  fromaddr = 'hexa.portal@gmail.com'

  r = urllib2.urlopen(EMAIL_URL)
  t = r.read()

  recipients = t.split('\n')
  toaddrs  = ", ".join(recipients)

  username = email_username
  password = email_password

  msgRoot = MIMEMultipart('related')
  msgRoot['Subject'] = text
  msgRoot['From'] = fromaddr
  msgRoot['To'] = toaddrs

  msgAlternative = MIMEMultipart('alternative')
  msgRoot.attach(msgAlternative)

  msgText = MIMEText("""<img src="cid:carpedm20"><br><div style="font-size:10px;color:#666666;line-height:100%;font-family:Helvetica">
You are receiving this email because you signed up at <a href="http://portalbot.us.to" target="_blank">http://portalbot.us.to</a>.
<br>
<br>
<a href="http://portalbot.us.to" style="color:#17488a;text-decoration:underline;font-weight:normal" target="_blank">Unsubscribe</a>
<br>
<em>Copyright (C) 2014 <span class="il">Kim Tae Hoon (carpedm20)</span> All rights reserved.</em>
<br>

</div>""", 'html')
  msgAlternative.attach(msgText)

  if filename is not '':
    img = MIMEImage(open(filename,"rb").read(), _subtype="png")
    img.add_header('Content-ID', '<carpedm20>')
    msgRoot.attach(img)
    
  server = smtplib.SMTP('smtp.gmail.com:587')
  server.starttls()
  server.login(username,password)
  server.sendmail(fromaddr, recipients, msgRoot.as_string())
  server.quit()
  print " - mail sended"

def exit_handler():
        print "DEAD"
        vdisplay.stop()
        #send_mail("Bot is DEAD")

def long_slice(image_path, out_name, outdir, number):
        img = Image.open(image_path)
        width, height = img.size

        slice_size = height/number
        upper = 0
        left = 0
        slices = int(math.ceil(height/slice_size))

        count = 1
        for slice in range(slices):
                if count == slices:
                        lower = height
                else:
                        lower = int(count * slice_size)
                bbox = (left, upper-30, width, lower+30)
                working_slice = img.crop(bbox)
                upper += slice_size
                working_slice.save(os.path.join(outdir, out_name + "_" + str(count)+".png"))
                count +=1

def width_slice(image_path, out_name, outdir, number):
        img = Image.open(image_path)
        width, height = img.size

        slice_size = width/number
        upper = 0
        left = 0
        slices = int(math.ceil(width/slice_size))

        count = 1
        for slice in range(slices):
                if count == slices:
                        right = width
                else:
                        right = int(count * slice_size)
                bbox = (left-50, 0, right+50, height)
                working_slice = img.crop(bbox)
                left += slice_size
                working_slice.save(os.path.join(outdir, out_name + "_" + str(count)+".png"))
                count +=1

atexit.register(exit_handler)
#send_mail("Bot is Alive")
vdisplay = Xvfb()
vdisplay.start()

import cookielib
cj = cookielib.CookieJar()
from cookielib import Cookie
c=Cookie(version=0, name='JSESSIONID', value=jsession, port=None, port_specified=False, domain='portal.unist.ac.kr', domain_specified=False, domain_initial_dot=False, path='/EP', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
cj.set_cookie(c)


while 1:
        print '.'
        br_mech = mechanize.Browser()
        br_mech.set_handle_robots(False)
        #br_spy = spynner.Browser()
        #br_spy.load('http://portal.unist.ac.kr/EP/web/collaboration/bbs/jsp/BB_BoardLst.jsp?boardid=B200902281833482321051&nfirst='+str(i))

        br_mech.open(login_url)
        br_mech.set_cookie('JSESSIONID=' + jsession)
        br_mech.set_cookiejar(cj)

        new_board_list = ['B201309091034272615665','B200912141432112623720','B201309090952407345581']
        old_board_list = ['B200902281833482321051','B200902281833016691048']

        for boardid in ['B201309091034272615665', # new announcement
                  'B200912141432112623720', # internship
                  'B201309090952407345581', # student support announcement
                  ###########################
                  'B200902281833482321051', # old announcement
                  'B200902281833016691048']:
                r = br_mech.open('http://portal.unist.ac.kr/EP/web/collaboration/bbs/jsp/BB_BoardLst.jsp?boardid='+boardid+'&nfirst=1')
                html=r.read()
                print ' [*] START : http://portal.unist.ac.kr/EP/web/collaboration/bbs/jsp/BB_BoardLst.jsp?boardid='+boardid+'&nfirst=1'

                id_list=[]

                for str1 in html.split('clickBulletin('):
                        if boardid in new_board_list:
                          a = str1.split("\', \'")[0]
                          if a.find(';') != -1:
                            continue
                          a = a.replace("'",'').replace('"','')
                          id_list.append(a)
                        else:
                          a = str1.split('","')[0]
                          if a.find(';') != -1:
                            continue
                          a = a.replace("'",'').replace('"','')
                          id_list.append(a)

                id_list.remove(id_list[0])
                print "[*] Length : " + str(len(id_list))

                for id_item in id_list:
                        files = [f for f in os.listdir('.') if os.path.isfile(f)]

                        new = False

                        for f in files:
                                if f.find(id_item) is not -1:
                                        new = True

                        if new is False:
                                link='https://www.facebook.com/dialog/oauth?scope=publish_stream,publish_actions,&redirect_uri=http://carpedm20.blogspot.kr&response_type=token&client_id=256972304447471'

                                br_mech = mechanize.Browser()
                                br_mech.set_handle_robots(False)

                                #print '[1] open link'
                                br_mech.open(link)

                                #print '[2] current url : ' + br_mech.geturl()

                                br_mech.form = list(br_mech.forms())[0]
                                control = br_mech.form.find_control("email")
                                control.value=fb_email
                                control = br_mech.form.find_control("pass")
                                control.value=fb_pass

                                #print '[3] submit'
                                br_mech.submit()

                                #print '[4] current url : ' + br_mech.geturl()

                                app_access = br_mech.geturl().split('token=')[1].split('&expires')[0]
                                print '[5] access token : ' + app_access

                                br_spy = spynner.Browser()
                                #br_spy.load(login_url)
                                br_spy.set_cookies('portal.unist.ac.kr\tFALSE\t/EP\tFALSE\t4294967295\tJSESSIONID\t'+jsession)
                                br_spy.load('http://portal.unist.ac.kr/EP/web/collaboration/bbs/jsp/BB_BoardLst.jsp?boardid='+boardid+'&nfirst=1')
                                br_spy.load("http://portal.unist.ac.kr/EP/web/collaboration/bbs/jsp/BB_BoardView.jsp?boardid="+boardid+"&bullid="+id_item)

                                print '[6] save : '
                                br_spy.snapshot().save(id_item + '.png')

                                print (id_item + '.png')
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
                                        link='https://www.facebook.com/dialog/oauth?scope=publish_stream,publish_actions,&redirect_uri=http://carpedm20.blogspot.kr&response_type=token&client_id=530042293708395'

                                        #print '[1] open link'
                                        food_br = mechanize.Browser()
                                        food_br.set_handle_robots(False)
                                        food_br.open(link)

                                        #print '[2] current url : ' + br_mech.geturl()

                                        food_br.form = list(food_br.forms())[0]
                                        control = food_br.form.find_control("email")
                                        control.value=fb_email
                                        control = food_br.form.find_control("pass")
                                        control.value=fb_pass

                                        #print '[3] submit'
                                        food_br.submit()

                                        #print '[4] current url : ' + br_mech.geturl()

                                        app_access = food_br.geturl().split('token=')[1].split('&expires')[0]
                                        print '[5] access token : ' + app_access

                                        br_mech.open(login_url)
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

                                                data = get[13:]
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

                                                                #graph.put_photo( open(f_name + '_' + str(nums) + '.png'), '부활 성공? :)\r\n\r\n' + title + ' ['+str(nums)+'/'+str(slice_num)+']'+'\r\n\r\nDesigned by carpedm20', "")

                                                #graph.put_photo( open(f_name + '.png'), title+'\r\n\r\nDesigned by carpedm20', "")
                                                print "put_photo finished"
                                        link='https://www.facebook.com/dialog/oauth?scope=publish_stream,publish_actions,&redirect_uri=http://carpedm20.blogspot.kr&response_type=token&client_id=256972304447471'

                                        br_mech = mechanize.Browser()
                                        br_mech.set_handle_robots(False)
                                        #print '[1] open link'
                                        br_mech.open(link)

                                        #print '[2] current url : ' + br_mech.geturl()
                                        br_mech.form = list(br_mech.forms())[0]
                                        control = br_mech.form.find_control("email")
                                        control.value=fb_email
                                        control = br_mech.form.find_control("pass")
                                        control.value=fb_pass

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
                                                        print '    TITLE : ' + br_spy.html.split('class="tb_left">')[1].split('>')[1].split('</')[0].strip().encode('utf-8')
                                                        graph.put_photo( open(id_item + '_' + str(nums) + '.png'), br_spy.html.split('class="tb_left">')[1].split('>')[1].split('</')[0].strip().encode('utf-8')+' ['+str(nums)+'/'+str(slice_num)+']'+'\r\n\r\n제작자 : 김태훈(carpedm20)', "")
                                        else:
                                                graph.put_photo( open(id_item + '.png'), title+'\r\n\r\n제작자 : 김태훈(carpedm20)\r\n\r\n포탈 공지 메일로 받기 : http://portalbot.us.to/', "")
                                send_mail(title, id_item+'.png')

        time.sleep(300)
