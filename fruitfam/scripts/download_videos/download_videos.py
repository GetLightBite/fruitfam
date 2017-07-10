import os
import sys

os.environ["APP_CONFIG_FILE"] = "../config/devel.py"

from datetime import datetime, timedelta
from fruitfam import db
from fruitfam.models.comment import Comment
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.editor import *
from moviepy.video.VideoClip import TextClip
from sqlalchemy import desc, or_, not_, and_
import urllib

recent_vids = Comment.query.filter(
  Comment.user_id!=6528
).filter(
  Comment.user_id!=20278
).filter(
  Comment.user_id!=50870
).filter(
  Comment.user_id!=18980
).filter(
  Comment.user_id!=61267
).filter(
  Comment.user_id!=68074
).filter(
  Comment.user_id!=88469
).order_by(
  desc(Comment.created)
).limit(100).all()

recent_vids = recent_vids[::-1]

for vid in recent_vids:
  print vid.message
  print vid.created
  print vid.user_id
  print ''

videos_to_concat = []
url_opener=urllib.FancyURLopener()
for x in recent_vids:
  url = x.message
  if 'http' in url:
    print url
    name = url.split('/')[-1]
    url_opener.retrieve(url, name+'.mp4')
    videos_to_concat.append((name+'.mp4', x.user_id, x.created))


all_clips = []
last_user_id = None
last_time = datetime.min

for video, user_id, created in videos_to_concat:
  
  clip = VideoFileClip(video)
  w,h = moviesize = clip.size
  clip = clip.resize((w*3, h*3))
  
  if user_id != last_user_id or created - last_time > timedelta(minutes=30):
    pst = created - timedelta(hours=7)
    date = pst.strftime('%a %H:%M')
    message = '%s, %s PST' % (str(user_id), date)
    txt = TextClip(message, font='Amiri-regular',
                 color='white',fontsize=15)
    txt_col = txt.on_color(size=(clip.w + txt.w,txt.h),
                      color=(0,0,0), pos=(0,20), col_opacity=0.3)
    txt_mov = txt_col.set_pos((0,0))
    txt_mov = txt_mov.set_duration(2)
    final = CompositeVideoClip([clip,txt_mov])
    final = final.set_duration(clip.duration)
    all_clips.append(final)
  else:
    all_clips.append(clip)
  
  last_user_id = user_id
  last_time = created

final_clip = concatenate_videoclips(all_clips)
final_clip.fps=30
final_clip.write_videofile("face_filter_videos.mp4")

for vid, _, _ in videos_to_concat:
  os.remove(vid)