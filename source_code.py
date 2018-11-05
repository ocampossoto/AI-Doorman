import RPi.GPIO as GPIO
from picamera import PiCamera
import time
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import _thread
fromaddr = "ocampossoto1@gmail.com"
toaddr = "ocampossoto1@gmail.com"
GPIO.setmode(GPIO.BCM) #set up board
GPIO.setwarnings(False) # ignore warnings
GPIO.setup(18,GPIO.OUT) #Set up relay GPIO, output
GPIO.setup(4,GPIO.IN) # setup motion sensor GPIO, input

def lightOn():
    print ("LED on")
    GPIO.output(18,GPIO.HIGH)
    time.sleep(1)
    print ("LED off")
    GPIO.output(18,GPIO.LOW)
    
def send_video(file_name):
    fromaddr = "Your email" #insert your email
    toaddr = "recipient email" #insert recipeint email
     
    msg = MIMEMultipart()
     
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "video at " + file_name 
     
    body = "Motion was detected here is the video"
     
    msg.attach(MIMEText(body, 'plain'))
     
    filename = file_name + '.mp4'
    attachment = open("/home/pi/Hackathon_Video/" + filename, "rb")
     
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
     
    msg.attach(part)
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "Your password")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    os.remove("/home/pi/Hackathon_Video/" + filename)
    os.remove("/home/pi/Hackathon_Video/" + file_name + '.h264')

recording = False
lightOn() #
camera = PiCamera() #Set up camera
camera.resolution = (640, 480)
time.sleep(2) #let everything set up
video_name = ""
while True:
    if(GPIO.input(4)): #if there is motion
        if(not recording):  #check if we are
            print ("LED on")
            GPIO.output(18,GPIO.HIGH)
            camera.start_preview()
            date_time = datetime.datetime.now()
            video_name = date_time.strftime("%m-%d_%H:%M:%S")
            camera.start_recording('/home/pi/Hackathon_Video/' + video_name + '.h264')
            recording = True
    else:
        temp = False
        if(recording):
            
            GPIO.output(18,GPIO.LOW)
            camera.stop_recording()
            camera.stop_preview()
            os.system('ffmpeg -i /home/pi/Hackathon_Video/' + video_name + '.h264 -c copy /home/pi/Hackathon_Video/' + video_name + '.mp4')
            print("video converted")
            send_video(video_name)
            print ("LED off")
            recording = False
    




