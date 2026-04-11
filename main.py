import threading
import time
from instagrapi import Client
import os
import sys
def login_2_session(user : str, passw: str) -> Client:
    cl = Client()
    cl.login(username=user, password=passw)
    try:
            #Setting-up sessions data
            os.mkdir(os.path.join(os.getcwd(),"data"))
            os.chdir(os.path.join(os.getcwd(),"data"))
            os.mkdir(os.path.join(os.getcwd(),"sessions"))
            os.chdir(os.path.join(os.getcwd(),"sessions"))
            #Dump the session
            cl.dump_settings(f"data/sessions/{str(cl.user_id) + "_settings.json"}")
    except FileExistsError:
            cl.dump_settings(f"data/sessions/{str(cl.user_id) + "_settings.json"}")
    return cl

def load_session(file : str) -> Client:
       cl = Client()
       cl.load_settings(file)
       return cl

def list_sessions():
    entrys = os.scandir("data/sessions")
    sessions = []
    for entry in entrys:
           if entry.is_file():
                 sessions.append(entry.name.split("_")[0])
    return sessions

def list_followers(cl) -> dict:
      return cl.user_followers(cl.user_id)

def list_following(cl) -> dict:
      return cl.user_following(cl.user_id)

def list_bitches(cl) -> list:
    """Return the users that don't follow back."""
    followers_obg = list_followers(cl)
    following_obg = list_following(cl)
    followers_ids = []
    following_ids = []
    bitches = []

    for follower in followers_obg:
          followers_ids.append(followers_obg[follower].pk)
    
    for following in following_obg:
          following_ids.append(following_obg[following].pk)

    for following in following_ids:
          if following not in followers_ids:
                bitches.append(following)
    return bitches

####GUI
