#!/usr/bin/env python
#Import necessary Python packages import RPi.GPIO as GPIO
import time
#import picamera
import sys
import urllib
import smtplib
#import picamera
import mimetypes
import email.mime.application 
import subprocess
from email.mime.text import MIMEText
#Check for the type of connection either wlan or ethernet 
def connect_type(word_list):
    if 'wlan0' in word_list or 'wlan1' in word_list:
        con_type = 'wifi'
    elif 'eth0' in word_list: 
        con_type = 'Ethernet'
    else:
        con_type = 'current'
    return con_type #gmail settings

toaddrs = 'boyr47@gmail.com' 
username = 'owarerobert' 
fromaddrs = 'owarerobert@gmail.com' 
password = 'p@ssword'

#setting up server to use to send mail
smtpserver = smtplib.SMTP('smtp.gmail.com', 587) 
smtpserver.ehlo()
#smtpserver.starttls()
smtpserver.ehlo() 
smtpserver.auth_login(username, password)
arg='ip route list'
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data=p.communicate()
ip_lines = data[0].splitlines() 
split_lines_a = ip_lines[1].split() 
split_lines_b = ip_lines[1].split()

ip_type_a = connect_type(split_lines_a)
ip_type_b = connect_type(split_lines_b)
ipaddr_a = split_lines_a[split_lines_a.index('src')+1]
ipaddr_b = split_lines_b[split_lines_b.index('src')+1]
my_ip_a = 'Your %s IP address is %s' % (ip_type_a, ipaddr_a)
my_ip_b = 'Your %s IP address is %s' % (ip_type_b, ipaddr_b)
msg1 = MIMEText(my_ip_a)
msg1['Subject'] = 'BOOT IP'
msg1['From'] = 'owarerobert@gmail.com'
arg='ip route list'
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data=p.communicate()
ip_lines = data[0].splitlines()
split_lines_a = ip_lines[1].split() 
split_lines_b = ip_lines[1].split()
ip_type_a = connect_type(split_lines_a)
ip_type_b = connect_type(split_lines_b)
ipaddr_a = split_lines_a[split_lines_a.index('src')+1]
ipaddr_b = split_lines_b[split_lines_b.index('src')+1]
my_ip_a = 'Your %s IP address is %s' % (ip_type_a, ipaddr_a) 
my_ip_b = 'Your %s IP address is %s' % (ip_type_b, ipaddr_b)
msg1 = MIMEText(my_ip_a)
msg1['Subject'] = 'BOOT IP'
msg1['From'] = 'owarerobert@gmail.com'
msg1['To'] = 'toaddrs'
smtpserver.sendmail(fromaddrs, toaddrs, msg1.as_string())
smtpserver.quit() 
time.sleep(10)

#GPIO Pin set up and initialization using board pin numbering GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
pir_pin = 11
GPIO.setup(11, GPIO.IN)
led_pin = 13
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.LOW)
#Initialize the channel as input #Read value from channel
#initialize the channel as output #Drive the channel
#A function to blink an LED(represent the automatic light system)
def led_light():
    valueX = GPIO.input(11)
    if valueX == True:
        time.sleep(2)
    elif valueX == False:
        GPIO.output(13, False)
        time.sleep(1)
        
# A function that captures video
def video_capture():
    with picamera.PiCamera() as camera: 
        camera.resolution = (640, 480) 
        camera.sharpness = 0 
        camera.contrast = False 
        camera.ISO = 0
        camera.saturation = 0 
        camera.exposure_mode = 'auto' 
        camera.exposure_compensation = 0 
        camera.video_stabilization = False 
        camera.crop = (0.0, 0.0, 1.0, 1.0) 
        camera.hflip = True
        camera.vflip = True 
        camera.brightness = 60
        
        # set filename and capture video to that file.
        filename = 'my_camera.h264' 
        camera.start_preview() 
        time.sleep(1)
        print ('Taking Video..Wait')
        camera.start_recording(filename) 
        camera.wait_recording(10)
        camera.stop_recording()
        
        print ('Video taken..checking for internet connectivity.')
# Main program loop try:
while True:
    for i in range(0, 10000000):
        value1 = GPIO.input(11) 
        if value1 == False:
            print ('system not alarmed...')
            time.sleep(5)
        elif value1 == True:
            print ('Motion Detected...alert start')
            led_light()
            video_capture()
            try:
                stri = "https://www.google.co.in" 
                e = 'no connection'
                data = urllib.urlopen(stri) 
                print("Connected")
                print ("Sending mail....")
                #send gmail to prescribed mailhub
                
                fromaddrs = 'owarerobert@gmail.com'
                password = 'P@ssword'
                username = "owarerobert"
                toaddrs = "boyr47@gmail.com"
                
                Subject = 'PIR Activated!!!'
                body = email.mime.Text.MIMEText('PIR Sensor detected motion') 
                msg = email.mime.Multipart.MIMEMultipart()
                msg['Subject'] = 'PIR Triggered!'
                msg['fromaddrs'] = 'owarerobert@gmail.com'
                msg['toaddrs'] = 'boyr47@gmail.com'
                msg.attach(body)
                #send the attached file
                filename = 'my_camera.h264'
                
                fp = open(filename, 'rb')
                att = email.mime.application.MIMEApplication(fp.read())
                fp.close()
                att.add_header('Content-Disposition','attachment',filename=filename) 
                msg.attach(att)
                
                server = smtplib.SMTP('smtp.gmail.com', 587) 
                server.ehlo()
                server.starttls()
                body = email.mime.Text.MIMEText('PIR Sensor detected motion')
                msg = email.mime.Multipart.MIMEMultipart()
                msg['Subject'] = 'PIR Triggered!'
                msg['fromaddrs'] = 'owarerobert@gmail.com'
                msg['toaddrs'] = 'boyr47@gmail.com' 
                msg.attach(body)
                
                #send the attached file
                filename = 'my_camera.h264'
                fp = open(filename, 'rb')
                att = email.mime.application.MIMEApplication(fp.read())
                fp.close()
                att.add_header('Content-Disposition','attachment',filename=filename)
                msg.attach(att)
                
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(username, password)
                server.sendmail(fromaddrs, toaddrs, msg.as_string())
                server.quit()
                
                GPIO.output(13, False)
                
            except e:
                print ("not connected") 
                if True:
                    print("Wait...")
                    time.sleep(5)
                    stri = "https://www.google.co.in" 
                    data = urllib.urlopen(stri)
                else:
                    print ("Sending mail ....")
                #Exit upon keyboard press 
            except KeyboardInterrupt():
                GPIO.clenup() 
                time.sleep(2)
                raise
