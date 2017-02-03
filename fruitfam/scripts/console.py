import cStringIO
from datetime import datetime, timedelta, date
from datetime import time as dtime
from functools import wraps
import heapq
import json
from sqlalchemy import and_, or_, distinct, desc, not_, func
from sqlalchemy.orm import defer, joinedload, joinedload_all, sessionmaker, subqueryload, load_only, Load
import time
import traceback
import os
import random

os.environ["APP_CONFIG_FILE"] = "../config/devel.py"

from fruitfam import app, auth, db
from fruitfam.models.user import User
from fruitfam.models.component import Component
from fruitfam.models.food_item import FoodItem
from fruitfam.models.like import Like