import threading
from colorama import Fore
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

####CLI
#Text colors
colors = {
      "yel" : Fore.YELLOW,
      "red" : Fore.RED,
      "blu" : Fore.BLUE,
      "gre" : Fore.GREEN,
      "res" : Fore.RESET
}

#Program Logo
anonista_logo =r"""    _                      _     _        
   / \   _ __   ___  _ __ (_)___| |_ __ _ 
  / _ \ | '_ \ / _ \| '_ \| / __| __/ _` |
 / ___ \| | | | (_) | | | | \__ \ || (_| |
/_/   \_\_| |_|\___/|_| |_|_|___/\__\__,_|
      V1.0 BETA (CLI)"""
help_msg = f"""   -=Programmed by Anonypos=-
{colors['red']}_-----------------------_
{colors["gre"]}** {colors['blu']}Login managment {colors["gre"]}**
{colors["red"]}_-----------------------_{colors['res']}
{colors['yel']}login{colors['res']} - {colors['blu']}Login to your Instagram account using username and password.
{colors['yel']}sessions{colors['res']} - {colors['blu']}List all the logged sessions.
{colors['yel']}dump_session <id> - {colors['blu']}Login by dumping a saved session.
{colors["red"]}-______________________-

{colors['res']}
"""
print(anonista_logo)
print(f"Type {colors['yel']}'help'{colors["res"]} to show the commands.")
while True:
      try:
            cmd = input("Anonista>> ")
            if cmd.lower() == "exit":
                  print(f"\nGood byeeee! {colors['red']}See u soon +-+{colors["res"]}")
                  exit(0)
            elif cmd.lower() == "help":
                  print(help_msg)
      except KeyboardInterrupt:
            print(f"\nGood byeeee! {colors['red']}See u soon +-+{colors["res"]}")
            break
