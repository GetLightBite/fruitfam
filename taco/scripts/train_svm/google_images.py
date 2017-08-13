from upload_image import upload_image
from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import json

def get_soup(url, header):
  return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

default_search_result = {
  'water' : 'http://forestcountypublichealth.org/wp-content/uploads/2015/11/Clean-water-in-glass.jpg',
  'orange' : 'http://hdwallpaperbackgrounds.net/wp-content/uploads/2016/08/Orange-Images-8.jpg'
}

def image_results_iterator(query):
  image_type="ActiOn"
  query= query.split()
  query='+'.join(query)
  url="https://www.google.com/search?q=%s&source=lnms&tbm=isch&tbs=isz:m,itp:photo" % query
  header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
  }
  soup = get_soup(url, header)
  ActualImages=[]# contains the link for Large original images, type of image
  for a in soup.find_all("div",{"class":"rg_meta"}):
    link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
    ActualImages.append((link,Type))
  
  for i , (img , Type) in enumerate(ActualImages):
    if Type == 'jpg':
      try:
        aws_link = upload_image(img)
        yield aws_link
      except Exception as e:
        pass