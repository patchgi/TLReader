#coding:utf-8

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import urllib2
import json
import re
import BeautifulSoup
from PIL import Image
from PIL import ImageOps
from itertools import product

CK=""
CS=""
AT=""
AS=""


def aa_art(input_image):
    w,h=input_image.size
    input_pix=input_image.load()

    for y in range(0,h,w/64):
        line=""
        character=""
        for x in range(0,w,w/64):

            r,g,b=input_pix[x,y]
            gray=r*0.2126+g*0.7152+b*0.0722
            if gray > 250:
                character = " "
            elif gray > 230:
                character = "`"
            elif gray > 200:
                character = ":"
            elif gray > 175:
                character = "*"
            elif gray > 150:
                character = "+"
            elif gray > 125:
                character = "#"
            elif gray > 50:
                character = "W"
            line+=character

        image_raw.append(line)

    for line in image_raw:
        print line

def download(_url,_path):
    fp=urllib2.urlopen(_url)
    local=open("temp.jpg", 'wb')
    local.write(fp.read())
    local.close()
    fp.close()



class StdOutListener(StreamListener):
    def on_data(self,data):
        if data[2]=="c":
            data=json.loads(data)
            print data['user']['name']+" @"+data['user']['screen_name']
            text=unicode(data['text'])

            print text
            media=""
            mediaURL=[]
            if len(data['entities'])!=4:
                media=data['entities']['media']

            if media!="":
                for url in media:
                    mediaURL.append(url['media_url'])

            if mediaURL!=[]:
                for url in mediaURL:
                    download(url,"./")
                    input_image = Image.open("temp.jpg")
                    aa_art(input_image)

            print data['created_at']
            print "--------------------------------------------------------------------------------"
        return True



    def on_error(self,status):
        print status

if __name__=="__main__":
    l=StdOutListener()
    auth=OAuthHandler(CK,CS)
    auth.set_access_token(AT,AS);

    stream=Stream(auth,l)
    stream.userstream()
