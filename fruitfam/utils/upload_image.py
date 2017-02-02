import requests
import boto
from boto.s3.key import Key
import urllib
import cStringIO
import io
import PIL
from PIL import Image
import string
import random

def upload_image(url, width=720, return_dict=None, is_square=True):
  c = boto.connect_s3('AKIAJHC3KOM63KGQA7TA', '85mJiGnhWFjvSXOa5cmLCOflHNr+Ze8XgaKa6+Dr')
  bucket_name = 'fruitfam'
  b = c.get_bucket(bucket_name, validate=False)
  r = requests.get(url)
  if r.status_code == 200:
    random_image_name = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(50))
    #upload the file
    k = Key(b)
    k.key = random_image_name
    k.content_type = r.headers['content-type']
    img = img_from_response(r)
    if is_square:
      img = crop_img_to_square(img)
    img = resize_image(img, width)
    k.set_contents_from_string(return_img_bytes(img))
    url_to_return = 'https://s3.amazonaws.com/%s/%s' % (bucket_name, random_image_name)
    # print url_to_return
    if return_dict != None:
      # print 'got here1'
      return_dict['img' + str(width)] = url_to_return
    # print 'got here2'
    return url_to_return

def upload_image_from_bytes_parallel(img_bytes, return_dict):
  url = upload_image_from_bytes(img_bytes)
  return_dict['url'] = url
  return url

def upload_image_from_bytes(img_bytes):
  c = boto.connect_s3('AKIAJUIYTUCUG3HRDTPA', '9tmBDWQ2Vve+bZOsaE3vOgTWoK8tNsrFg7WJjFw1')
  bucket_name = 'fruitfam'
  b = c.get_bucket(bucket_name, validate=False)
  random_image_name = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(50))
  k = Key(b)
  k.key = random_image_name
  k.set_contents_from_string(img_bytes)
  return 'https://s3.amazonaws.com/%s/%s' % (bucket_name, random_image_name)

def upload_image_from_object(img, width=None, is_square=False):
  if is_square:
    img = crop_img_to_square(img)
  if width != None:
    img = resize_image(img, width)
  # Upload the image
  c = boto.connect_s3('AKIAJHC3KOM63KGQA7TA', '85mJiGnhWFjvSXOa5cmLCOflHNr+Ze8XgaKa6+Dr')
  bucket_name = 'fruitfam'
  b = c.get_bucket(bucket_name, validate=False)
  random_image_name = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(50))
  k = Key(b)
  k.key = random_image_name
  k.set_contents_from_string(return_img_bytes(img))
  url_to_return = 'https://s3.amazonaws.com/%s/%s' % (bucket_name, random_image_name)
  return url_to_return

def img_from_response(r):
  file = cStringIO.StringIO(r.content)
  img = Image.open(file)
  return img

def resize_image(img, newwidth):
  wpercent = (newwidth/float(img.size[0]))
  hsize = int((float(img.size[1])*float(wpercent)))
  img = img.resize((newwidth,hsize), PIL.Image.ANTIALIAS)
  return img

def crop_img_to_square(img):
  img = img.crop(get_square_crop_dims(img))
  return img

def crop_img_to_diary_dims(img):
  img = img.crop(get_diary_dims(img))
  return img

def get_diary_dims(img):
  width, height = img.size
  new_width = width
  new_height = height
  if height*0.7 > width: # constrained by width, bring height down
    new_height = int(new_width / 0.7)
  else: # constrainged by height, bring width down
    new_width = int(new_height * 0.7)
  wstart = (width - new_width)/2
  hstart = (height - new_height)/2
  return (wstart, hstart, wstart + new_width, hstart + new_height)

def get_square_crop_dims(img):
  width, height = img.size
  min_dim = min(width, height)
  wstart = (width - min_dim)/2
  hstart = (height - min_dim)/2
  return (wstart, hstart, wstart + min_dim, hstart + min_dim)

def return_img_bytes(img):
  imgByteArr = io.BytesIO()
  img.save(imgByteArr, format='JPEG')
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

# upload_image('https://scontent-sea1-1.cdninstagram.com/t51.2885-15/e35/14701110_541980752676255_2355483330687795200_n.jpg', 50)