import pandas as pd
import wget
import smtplib
import sys

# function to extract images in a directory
def url_to_jpg(ID,file_path,file_name):
    img_format = '.jpg'
    full_path = '{}{}{}'.format(file_path, file_name, img_format)
    wget.download(f'https://docs.google.com/uc?export=download&id={ID}', out = full_path)

# function to send email    
def send_mail(sender_mail,sender_pass,recipient_mail,message): 
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(sender_mail,sender_pass)

    server.sendmail(sender_mail,recipient_mail,message) 

    smtpserver.quit() 
    
# get csv_file name
csv_file = sys.argv[1];

data = pd.read_csv(csv_file)

size = data['upload image'].shape[0]

# path where the images will be store after downloading
file_path = sys.argv[2]

# get the images download from each link
for i in range(size):
    ID = data['upload image'].iloc[i].split('=')[-1]
    file_name = data['email'].iloc[i]
    url_to_jpg(ID,file_path,file_name)
    
# sender email id
sender_mail = sys.argv[3]

# sender email password
sender_pass = sys.argv[4]


for i in range(size):
    recipient_mail = data['email'].iloc[i]
    # message = model prediction
    send_mail(sender_mail,sender_pass,recipient_mail,message)
