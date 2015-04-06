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
from config import *
import urllib2
import socket

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

import requests

session = requests.Session()

url = "http://portal.unist.ac.kr/EP/web/collaboration/bbs/jsp/BB_BoardLst.jsp?boardid=B200902281833016691048&p=1"
cookies = dict(#cookie='off',
               JSESSIONID=jsession,
               #MYSAPSSO2='AjExMDAgAA9wb3J0YWw6MjAxMTExNjeIABNiYXNpY2F1dGhlbnRpY2F0aW9uAQAIMjAxMTExNjcCAAMwMDADAANVRVAEAAwyMDE1MDQwNjA3NDgFAAQAAAAICgAIMjAxMTExNjf%2FAQUwggEBBgkqhkiG9w0BBwKggfMwgfACAQExCzAJBgUrDgMCGgUAMAsGCSqGSIb3DQEHATGB0DCBzQIBATAiMB0xDDAKBgNVBAMTA1VFUDENMAsGA1UECxMESjJFRQIBADAJBgUrDgMCGgUAoF0wGAYJKoZIhvcNAQkDMQsGCSqGSIb3DQEHATAcBgkqhkiG9w0BCQUxDxcNMTUwNDA2MDc0ODU0WjAjBgkqhkiG9w0BCQQxFgQU%2FC06MkY9DIhASkG6Dp2nyjAbY8MwCQYHKoZIzjgEAwQvMC0CFAhu89lHgeNY0WKyiMr41vrcE1E!AhUAmkL5gM5ZvU!%2Fo6UyZPQ1LxrwiUo%3D',
               #SAPWP_active='1')
               )

while 1:
	r = session.get(url, cookies=cookies)
        print '.'
        br_mech = mechanize.Browser()
        br_mech.set_handle_robots(False)
        #br_spy = spynner.Browser()
        #br_spy.load('http://portal.unist.ac.kr/EP/web/collaboration/bbs/jsp/BB_BoardLst.jsp?boardid=B200902281833482321051&nfirst='+str(i))

        br_mech.open('http://portal.unist.ac.kr/EP/web/collaboration/bbs/jsp/BB_BoardLst.jsp?boardid=B200902281833016691048&p=1')
        br_mech.set_cookie('JSESSIONID=' + jsession)
        br_mech.set_cookiejar(cj)

        new_board_list = ['B201309091034272615665','B200912141432112623720','B201309090952407345581']
        old_board_list = ['B200902281833482321051','B200902281833016691048']

        for boardid in ['B201309091034272615665', # new announcement
                  'B200912141432112623720', # internship
                  'B201309090952407345581', # student support announcement
                  'B201003111719010571299',
                  ###########################
                  'B200902281833482321051', # old announcement
                  'B200902281833016691048']: # total announcement
                #r = br_mech.open('http://portal.unist.ac.kr/EP/web/collaboration/bbs/jsp/BB_BoardLst.jsp?boardid='+boardid+'&nfirst=1')
                #html=r.read()
                r = session.get('http://portal.unist.ac.kr/EP/web/collaboration/bbs/jsp/BB_BoardLst.jsp?boardid='+boardid+'&nfirst=1', cookies=cookies)
                html = r.text
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
                                link='https://www.facebook.com/dialog/oauth?scope=publish_stream,publish_actions,&redirect_uri=http://carpedm20.github.io&response_type=token&client_id=256972304447471'

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
                                if True:
                                        if sliced is True:
                                                for nums in range(1, slice_num+1):
                                                        nums=slice_num-nums+1
                                                        print '[7] upload : ' + id_item + '_' + str(nums)
                                                        print '    TITLE : ' + br_spy.html.split('class="tb_left">')[1].split('>')[1].split('</')[0].strip().encode('utf-8')
                                                        graph.put_photo( open(id_item + '_' + str(nums) + '.png'), message=br_spy.html.split('class="tb_left">')[1].split('>')[1].split('</')[0].strip().encode('utf-8')+' ['+str(nums)+'/'+str(slice_num)+']'+'\r\n\r\n제작자 : 김태훈(carpedm20)')
							#new_photo = graph.post('107469732792015/photos',  params={'message':r_spy.html.split('class="tb_left">')[1].split('>')[1].split('</')[0].strip().encode('utf-8')+' ['+str(nums)+'/'+str(slice_num)+']'+'\r\n\r\n제작자 : 김태훈(carpedm20)', 'source': open(id_item + '_' + str(nums) + '.png')})
                                        else:
                                                graph.put_photo( open(id_item + '.png'), message=title+'\r\n\r\n제작자 : 김태훈(carpedm20)')
						#new_photo = graph.post('107469732792015/photos' , params={'message':title+'\r\n\r\n제작자 : 김태훈(carpedm20)', 'source': open(id_item + '.png')})

                                #send_mail(title, id_item+'.png')

        time.sleep(300)
