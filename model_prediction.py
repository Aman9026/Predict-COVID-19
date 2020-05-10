from keras.models import load_model
from keras.preprocessing import image
from PIL import Image
import numpy as np
import pandas as pd
import wget
import smtplib
import os
import shutil
import sys

# function to extract images in a directory
def url_to_jpg(ID,dir_path,file_name):
    img_format = '.jpg'
    full_path = '{}{}{}'.format(dir_path, file_name, img_format)
    wget.download(f'https://docs.google.com/uc?export=download&id={ID}', out = full_path)

# function to send email    
def send_mail(sender_mail,sender_pass,recipient_mail,message): 
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(sender_mail,sender_pass)

    server.sendmail(sender_mail,recipient_mail,message) 

    server.quit() 
    
    
# function to get result
def get_result(img):
    img = image.load_img(img,target_size=(224,224))
    img = image.img_to_array(img)
    img = np.expand_dims(img,axis=0)
    out = model.predict_classes(img)
    return out


# load model
model = load_model('model_Covid19.h5')

# get csv_file name
csv_file = sys.argv[1];

data = pd.read_csv(csv_file)

size = data['Upload'].shape[0]

# path where the images will be store after downloading
dir_path = sys.argv[2]

# make folder in the dir_path to save the images
if os.path.isdir(dir_path):
    os.mkdir(dir_path+'\images')
    
file_path = dir_path+'\images/'

# get the images download from each link
for i in range(size):
    ID = data['Upload'].iloc[i].split('=')[-1]
    file_name = data['Email Address'].iloc[i]
    url_to_jpg(ID,file_path,file_name)
    
# load images
load_images = os.listdir(file_path)

# dict to represent the disease
res = {1:'Disclaimer: Visit our nearest hospital if you have any symptoms, This test is only for research purpose and should not be used for diagnosis. According to our test the result is NORMAL but precautionary measures must be taken. Contact Central Helpline Number for corona-virus: - +91-11-23978046', 0:'Disclaimer: Visit our nearest hospital if you have any symptoms, This test is only for research purpose and should not be used for diagnosis. According to our test the result is COVID Positive and precautionary measures must be taken. Contact Central Helpline Number for corona-virus: - +91-11-23978046'}
    
# sender email id
sender_mail = sys.argv[3]

# sender email password
sender_pass = sys.argv[4]

# iterate through each image and send the test result through mail associated with it
for img in load_images:
    out = get_result(file_path+img)[0][0]
    recipient_mail = img.split('.jpg')[0]
    message = res[out]
    print('{}\t{}'.format(recipient_mail,message))
    send_mail(sender_mail,sender_pass,recipient_mail,message)

# remove the image dir
#shutil.rmtree(path+'\images')
