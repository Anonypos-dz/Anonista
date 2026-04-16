"""
Copyright 2026 Anonypos

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import threading
from colorama import Fore, Style, Back
import time
from instagrapi import Client
from instagrapi.exceptions import *
import os
import subprocess
import pwinput
import urllib3
import requests
import logging
colors = {
      "yel" : Fore.YELLOW,
      "red" : Fore.RED,
      "blu" : Fore.BLUE,
      "gre" : Fore.GREEN,
      "res" : Fore.RESET
}
#Login handling
is_Loggedin = False
global_cl : Client = None

#Hide urllib3 warns
logging.disable(logging.CRITICAL)
def login_2_session(user : str, passw: str) -> Client:
    global is_Loggedin, global_cl
    global_cl = Client()
    is_Loggedin = True
    try:
      global_cl.login(username=user, password=passw)
      try:
            #Setting-up sessions data
            os.mkdir(os.path.join(os.getcwd(),"data"))
            os.chdir(os.path.join(os.getcwd(),"data"))
            os.mkdir(os.path.join(os.getcwd(),"sessions"))
            os.chdir(os.path.join(os.getcwd(),"sessions"))
            #Dump the session
            global_cl.dump_settings(os.path.join("data","sessions",f"{str(global_cl.user_id) + "_settings.json"}"))
      except FileExistsError:
            global_cl.dump_settings(os.path.join("data","sessions",f"{str(global_cl.user_id) + "_settings.json"}"))
      return global_cl

    except ChallengeRequired:
          print(f"{Fore.RED}Challenge required, {Fore.YELLOW}try to use a vpn!{Fore.RESET}")
          return "challenge"
    except BadPassword:
          print(f"{Fore.RED}Please check your password!!{Fore.RESET}")
          return "bad_pass"

def load_session(file : str) -> Client:
       global is_Loggedin, global_cl
       global_cl = Client()
       global_cl.load_settings(file)
       is_Loggedin = True
       return global_cl

def list_sessions():
    try:
      entrys = os.scandir(os.path.join("data", "sessions"))
      sessions = []
      for entry in entrys:
           if entry.is_file():
                 sessions.append(entry.name.split("_")[0])
      return sessions
    except FileNotFoundError:
            os.mkdir(os.path.join(os.getcwd(),"data"))
            os.chdir(os.path.join(os.getcwd(),"data"))
            os.mkdir(os.path.join(os.getcwd(),"sessions"))
            os.chdir(os.path.join(os.getcwd(),"sessions"))
            return []
login_before_error = f"{Fore.RED}Please login to your account before using this command!{colors["res"]}"
def list_followers(cl, id) -> dict:
      return cl.user_followers(id)
      

def list_following(cl, id) -> dict:
      return cl.user_following(id)


def list_bitches(cl, id) -> list:
      """Return the users that don't follow back."""
      followers_obg = list_followers(cl, id)
      following_obg = list_following(cl, id)
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
def show_followers(cl : Client, id):
      followers = list_followers(cl=cl,id=id)
      print(f"{colors['red']}_------------------------------_{colors["res"]}")
      print(f"{" "*9}{colors['yel']}User Followers{colors['res']}")
      print(f"{colors['red']}_------------------------------_{colors["res"]}")
      print(f"{colors["yel"]}Followers count: {colors['blu']}{cl.user_info(id).follower_count}{colors['res']}")
      for follower in followers:
            user = followers[follower]
            infos = {
                  "Username" : user.username,
                  "Fullname" : user.full_name,
                  "UserId" : user.pk,
                  "Is Private": user.is_private,
                  "Profile Picture (url)": str(user.profile_pic_url) + "\n"
            }
            for info in infos:
                  print(f"{colors['gre']}{info}{colors["res"]} : {infos[info]}")
            

      
def self_followers(cl : Client) -> list:
      return list_followers(cl, cl.user_info.id)
#Get user infos by id
def get_info(cl: Client, id):
      return cl.user_info(user_id=id)

#Get account infos
def get_account_infos(cl: Client):
      return cl.account_info()

####CLI
#Program Logo
anonista_logo =rf"""{colors['gre']}    _                      _     _        
   / \   _ __   ___  _ __ (_)___| |_ __ _ 
  / _ \ | '_ \ / _ \| '_ \| / __| __/ _` |{colors['red']}
 / ___ \| | | | (_) | | | | \__ \ || (_| |{colors['res']}
/_/   \_\_| |_|\___/|_| |_|_|___/\__\__,_|
            {Style.DIM}V1.0 {Style.RESET_ALL}{Style.BRIGHT}BETA {Style.DIM}(CLI){Style.RESET_ALL}"""
help_dic = {"Login Managment":
            {"login": "Login to your Instagram account using username and password.",
             "sessions": "List all logged sessions.",
             "load_session <id>": "Login by loading a saved session.",
             },
             "Account Managment":
             {
                   "getinfo": "Show your profile infos.",
                   "self_followers" : "List your followers.",
                   "self_following" : "List your followings",
                   "self_bitches" : "List the users that don't follow you back."
             },
             "User Enumeration":
             {
                   "userinfo <username>" : "Show all the user's infos.",
                   "dump_posts <username>" : "Download all the user's postes",
                   "followers <username>" : "List the user's followers",
                   "following <username>" : "List the user's followings",
                   "bitches <username>" : "List the users that don't follow back the user."
             }
            }
def print_help():
      print("   -=Programmed by Anonypos=-")
      for cmd_class in help_dic:
            print(f"{colors['red']}_------------------------------_{colors["res"]}")
            print(f"{" "*9}{colors['yel']}{cmd_class}{colors['res']}")
            print(f"{colors['red']}_------------------------------_{colors["res"]}\n")
            for cmd in help_dic[cmd_class]:
                  print(f"  {colors['gre']}{cmd}{colors["res"]} : {help_dic[cmd_class][cmd]}")
            

print(anonista_logo)
print(f"Type {colors['yel']}'help'{colors["res"]} to show the commands.")
def login():
      global is_Loggedin
      global global_cl
      while True:
            user = input(f"Username: ")
            passwd = pwinput.pwinput(prompt="Password: ", mask="*")
            global_cl =  login_2_session(user=user, passw=passwd)
            if global_cl == "bad_pass":
                  pass
            elif global_cl == "challenge":
                  pass
            else:
                  is_Loggedin = True
                  print(f"{colors['gre']}Logged in to {colors["yel"]}@{user}{colors["res"]}.")
#sessions handling
def sessions():
      sessions = list_sessions()
      if sessions == []:
            print(f"{colors["yel"]}No sessions found!{colors['res']} Please use {colors['blu']}'login'{colors["res"]} command to save a new session.")
      else:
            print(f"""
                  _------------------------------_
                           Stored Sessions
                  _------------------------------_""")
            print(f"{" "*20}ID |{" "*5}USER ID")
            i = 0
            for session in sessions:
                  print(f"{" "*20}<{i}>|{" "*5}{session}")
#Login to a session using the session's ID
def load_session_with_id(id : int):
      try:
            session_file = os.path.join("data","sessions",f"{list_sessions()[id]}_settings.json")
            cl = load_session(session_file)
            print(f"{colors['gre']}Logged in to {colors["yel"]}@{cl.user_info(user_id=cl.user_id).username}{colors["res"]}.")
      except IndexError:
            print(f"{colors["red"]}Invalid session id!{colors['res']}")

#Main loop
while True:
      try:
            cmd = input(f"{colors['gre']}Ano{colors['red']}nis{colors["res"]}ta{colors['blu']}>>{colors['res']} ")
            if cmd.lower() == "exit":
                  print(f"\nGood byeeee! {colors['red']}See u soon +-+{colors["res"]}")
                  exit(0)
            elif cmd.lower() == "help":
                  print_help()
            elif cmd.lower() == "clear":
                  if os.name == "nt":
                        subprocess.run("cls", shell=True)
            elif cmd.lower() == "login":
                  login()
            elif cmd.lower() == "sessions":
                  sessions()
            elif cmd.lower().startswith("load_session "):
                  try:
                        id = int(cmd[len("load_session "):])
                        load_session_with_id(id)
                  except:
                        print(f"{colors["red"]}Please enter a valid id.{colors["res"]}")
            elif cmd.lower().startswith("followers "):
                  if is_Loggedin:
                        try:
                              username = cmd[len("followers "):]
                              userid = global_cl.user_id_from_username(username=username)
                              print(f"Getting the user's followers... {colors['yel']}It may take some time!{colors["res"]}")
                              show_followers(global_cl, userid)
                        except Exception as e:
                              print("Error: ", e)
                        except UserNotFound:
                              print(f"{colors['red']}User not found! Please check the username.{colors["res"]}")
                  else:
                        print(login_before_error)
            #Command not found
            else:
                  print(f"{colors["red"]}Command not found!{colors['res']} Type {colors["yel"]}'help'{colors["red"]} -_-{colors['res']}")
      except KeyboardInterrupt:
            print(f"\nGood byeeee! {colors['red']}See u soon +-+{colors["res"]}")
            break
