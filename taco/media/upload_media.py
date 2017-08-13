import base64
import cStringIO
import io
import json
import numpy as np
import os
from PIL import Image
import requests
import time
from taco import db
from taco.utils.upload_image import upload_image, upload_image_from_object, upload_image_from_bytes, upload_video_from_bytes
from taco.models.memory import Memory

def request_to_img_object(request, key='docfile'):
  image_data = request.files.get(key, None)
  if image_data != None:
    # It's from a phone!
    stream_data = image_data.stream.read()
    img_data = cStringIO.StringIO(stream_data)
    img = Image.open(img_data)
    return img

def request_to_video_binary_data(request):
  raw_video_data = request.files.get('docfile', None)
  if raw_video_data != None:
    # It's from a phone!
    stream_data = raw_video_data.stream.read()
    # binary_data = cStringIO.StringIO(stream_data)
    #img = Image.open(img_data)
    return stream_data

def upload_image_memory_from_request(request, user, groups):
  img = request_to_img_object(request)
  width, height = img.size
  url_original = upload_image_from_object(img)
  url_fullscreen = upload_image_from_object(img, 720)
  url_small = upload_image_from_object(img, 414)
  url_icon = upload_image_from_object(img, 240, True)
  for group in groups:
    m = Memory(user, group, url_icon, url_small, url_fullscreen, width, height, url_original, 'photo')
    db.session.add(m)

def upload_video_memory_from_request(request, user, groups):
  video_binary = request_to_video_binary_data(request)
  video_binary_url = upload_video_from_bytes(video_binary)
  
  # Get first frame
  img = request_to_img_object(request, 'firstFrame')
  width, height = img.size
  url_first_frame = upload_image_from_object(img, 240, True)
  
  
  for group in groups:
    m = Memory(user, group, url_first_frame, video_binary_url, video_binary_url, width, height, video_binary_url, 'video')
    db.session.add(m)
