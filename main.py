"""
Copyright 2026 Anonypos

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
CREDITS = "Programmed by Anonypos, 2026."
import threading
from colorama import Fore, Style, Back
import time
from instagrapi import Client
from instagrapi.exceptions import *
import os
import subprocess
import pwinput
import requests
import logging
import random
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
#login and the save the session in os.path.join("data","sessions")
def login_2_session(user : str, passw: str) -> Client:
    global is_Loggedin, global_cl
    global_cl = Client()
    is_Loggedin = True
    try:
      global_cl.login(username=user, password=passw)
      if os.path.exists(os.path.join(os.getcwd(), "data")):
            if os.path.exists(os.path.join(os.getcwd(), "data", "sessions")):
                  pass
            else:
                  os.mkdir(os.path.join(os.getcwd(), "data", "sessions"))
      else:
            os.mkdir(os.path.join(os.getcwd()))
      global_cl.dump_settings(os.path.join(os.getcwd(),"data","sessions",f"{str(global_cl.user_id) + "_settings.json"}"))
      return global_cl

    except ChallengeRequired:
          print(f"{Fore.RED}Challenge required, {Fore.YELLOW}try to use a vpn!{Fore.RESET}")
          return "challenge"
    except BadPassword:
          print(f"{Fore.RED}Please check your password!!{Fore.RESET}")
          return "bad_pass"
    except UnknownError:
          print(f"{Fore.RED}Please check your informations!!{Fore.RESET}")
          return "unknownerror"
    except UserNotFound:
          print(f"{Fore.RED}Username Not Found!!{Fore.RESET}")
def load_session(file : str) -> Client:
       global is_Loggedin, global_cl
       global_cl = Client()
       try:
             
            global_cl.load_settings(file)
            is_Loggedin = True
            return global_cl
       except Exception as e:
             print(e)

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
      #1 second delay
      print(f"{colors['blu']}1s COOLDOWN (IT'S IMPORTANT)....{colors['res']}")
      time.sleep(1)
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
      print(f"{colors['blu']}1s COOLDOWN (IT'S IMPORTANT)....{colors['res']}")
      time.sleep(1)

def show_followings(cl, id):
      followings = list_following(cl, id)
      print(f"{colors['red']}_------------------------------_{colors["res"]}")
      print(f"{" "*9}{colors['yel']}User Followings{colors['res']}")
      print(f"{colors['red']}_------------------------------_{colors["res"]}")
      for following in followings:
            user = followings[following]
            infos = {
                  "Username" : user.username,
                  "Fullname" : user.full_name,
                  "UserId" : user.pk,
                  "Is Private": user.is_private,
                  "Profile Picture (url)": str(user.profile_pic_url) + "\n"
            }
            for info in infos:
                  print(f"{colors['gre']}{info}{colors['res']} : {infos[info]}")
            print(f"{colors['blu']}1s COOLDOWN (IT'S IMPORTANT)....{colors['res']}")
            time.sleep(1)

def show_bitches(cl: Client, id):
      bitches = list_bitches(cl, id)
      if bitches:
            print(f"{colors['red']}_------------------------------_{colors["res"]}")
            print(f"{" "*9}{colors['yel']}Bitches List{colors['res']}")
            print(f"{colors['red']}_------------------------------_{colors["res"]}")
            for bitch in bitches:
                  user = cl.user_info(bitch) 
                  infos = {
                  "Username" : user.username,
                  "Fullname" : user.full_name,
                  "UserId" : user.pk,
                  "Is Private": user.is_private,
                  "Profile Picture (url)": str(user.profile_pic_url) + "\n"
                  }
                  for info in infos:
                        print(f"{colors["red"]}{info}{colors["res"]} : {infos[info]}")
      else:
            print(f"{colors['gre']}No users found! the EGO is safe.{colors["res"]}")
            return "no_bitches"

def self_followers(cl : Client):
      followers =  list_followers(cl, cl.user_id)
      print(f"{colors['red']}_------------------------------_{colors["res"]}")
      print(f"{" "*9}{colors['yel']}Account Followers{colors['res']}")
      print(f"{colors['red']}_------------------------------_{colors["res"]}")     
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
                  print(f"{colors['gre']}{info}{colors['res']} : {infos[info]}")

def self_following(cl : Client):
      show_followings(cl, cl.user_id)

def self_bitches(cl : Client):
      Rvalue = show_bitches(cl, cl.user_id)
      if Rvalue != "no_bitches":
            print(f"{colors['red']}YOU CAN STRIKE BACK! USE 'remove_bitches' COMMAND TO PROTECT YOUR EGO.{colors['res']}")

def remove_bitches(cl : Client):
      print(f"{colors['yel']}Getting the users that don't follow you back...{colors['res']}")
      bitches = list_bitches(cl, cl.user_id)
      if bitches:
            print(f"{colors['blu']}Protecting the EGO...")
            print(f"{colors['red']}BITCHES COUNT:{colors['res']}{len(bitches)}")
            for bitch in bitches:
                  cl.user_unfollow(bitch)
                  print(f"{colors['gre']}{cl.username_from_user_id(bitch)}Was unfollowed successfully!!")
                  time.sleep(1 + 1 / random.randint(1,6))
      else:
            print(f"{colors['gre']}Your EGO is safe!! Keep protecting it.{colors['res']}")
#Get user infos by id
def get_info(cl: Client, id):
      return cl.user_info(user_id=id)

#Get account infos
def get_account_infos(cl: Client):
      return cl.account_info()

def show_account_infos(cl: Client):
      infos = get_account_infos(cl)
      infos_dict = {
            "User id" : infos.pk,
            "Username" : infos.username,
            "Full Name": infos.full_name,
            "Bio" : infos.biography,
            "Followers Count": cl.user_info(infos.pk).follower_count,
            "Following Count": cl.user_info(infos.pk).following_count,
            "Is Private": infos.is_private,
            "Is Business" : infos.is_business,
            "Is Verified" : infos.is_verified,
            "Email" : infos.email,
            "Phone Number" : infos.phone_number,
            "User Birthday" : infos.birthday,
            "Profile Picture (url)" : infos.profile_pic_url
      }
            #infos template
      infos_templ = f"""{CREDITS}

_------------------------------_
{" "*9}Account Infos
_------------------------------_
"""
      print(f"{colors['red']}_------------------------------_{colors["res"]}")
      print(f"{" "*9}{colors['yel']}Account Infos{colors['res']}")
      print(f"{colors['red']}_------------------------------_{colors["res"]}")
      for info in infos_dict:
            infos_templ += f"{info} : {infos_dict[info]}\n"
            print(f"{colors['gre']}{info}{colors["res"]} : {infos_dict[info]}")
      #Save the output
      if os.path.exists(os.path.join(os.getcwd(),"data","myaccounts")):
            if os.path.exists(os.path.join(os.getcwd(),"data","myaccounts",infos.username)):
                  pass
            else:
                  os.makedirs(os.path.join("data","myaccounts",infos.username))
      else:
            os.makedirs(os.path.join("data","myaccounts",infos.username))
            
      output_path = os.path.join(os.getcwd(),"data","myaccounts",infos.username,"AccountInfos.txt")
      with open(output_path, "w", encoding="utf-16") as f:
            f.write(infos_templ)
      print(f"Account infos saved in {colors['yel']}{output_path}{colors['res']}")

def userinfo(cl : Client, id) -> dict:
      return cl.user_info(id)

def show_userinfo(cl : Client, id):
      infos = userinfo(cl, id)
      infos_dict = {
            "UserID" : infos.pk,
            "UserName" : infos.username,
            "FullName" : infos.full_name,
            "Is Private" : infos.is_private,
            "Is Verified": infos.is_verified,
            "Is Business": infos.is_business,
            "Followers Count" : infos.follower_count,
            "Following Count" : infos.following_count,
            "Posts Count" : infos.media_count,
            "Bio" : infos.biography
      }
      infos_templ = f"""{CREDITS}

_------------------------------_
{" "*9}Account Infos
_------------------------------_
"""      
      print(f"{colors['red']}_------------------------------_{colors["res"]}")
      print(f"{" "*9}{colors['yel']}User Infos{colors['res']}")
      print(f"{colors['red']}_------------------------------_{colors["res"]}")      
      for info in infos_dict:
            print(f"{colors['gre']}{info}{colors['res']} : {infos_dict[info]}")
            infos_templ += f"{info} : {infos_dict[info]}\n"
      if os.path.exists(os.path.join(os.getcwd(), "data")):
            pass
      else:
            os.mkdir(os.path.join(os.getcwd(), "data"))

      if os.path.exists(os.path.join(os.getcwd(), "data", "users")):
            if os.path.exists(os.path.join(os.getcwd(), "data", "users", infos.username)):
                  pass
            else:
                  os.mkdir(os.path.join(os.getcwd(), "data", "users", infos.username))
      else:
            os.mkdir(os.path.join(os.getcwd(), "data", "users"))
      out_path = os.path.join(os.getcwd(), "data", "users", infos.username, "userinfos.txt")
      with open(out_path, "w", encoding="utf-16") as f:
            f.write(infos_templ)
      print(f"Output saved in {colors['yel']}{out_path}{colors['res']}")
      print(f"{colors['blu']}3s COOLDOWN (IT'S IMPORTANT)....{colors['res']}")
      time.sleep(3)

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
             f"sessionid_login {colors['res']}<sessionid value>": "Login with sessionid cookie",
             "sessions": "List all logged sessions.",
             f"load_session {colors['res']}<id>": "Login by loading a saved session.",
             },
             "Account Managment":
             {
                   "getinfo": "Show your profile infos.",
                   "self_followers" : "List your followers.",
                   "self_following" : "List your followings",
                   "self_bitches" : "List the users that don't follow you back.",
                   f"unfollow {colors['res']}<username{colors['yel']}|{colors["res"]}userid{colors['yel']}|{colors["res"]}list_file>" : "Unfollow a user.",
                   "remove_bitches" : "Unfollow all the accounts that don't follow you back."
             },
             "User Enumeration":
             {
                   f"userinfo {colors['res']}<username{colors['yel']}|{colors["res"]}userid{colors['yel']}|{colors["res"]}list_file>" : "Show all the user's infos.",
                   f"dump_posts {colors['res']}<username{colors['yel']}|{colors["res"]}userid{colors['yel']}|{colors["res"]}list_file>" : "Download all the user's postes",
                   f"followers {colors['res']}<username{colors['yel']}|{colors["res"]}userid{colors['yel']}|{colors["res"]}list_file>" : "List the user's followers",
                   f"following {colors['res']}<username{colors['yel']}|{colors["res"]}userid{colors['yel']}|{colors["res"]}list>" : "List the user's followings",
                   f"bitches {colors['res']}<username{colors['yel']}|{colors["res"]}userid>" : "List the users that don't follow back the user."
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
      attmps = 0
      while True:
            user = input(f"Username: ")
            passwd = pwinput.pwinput(prompt="Password: ", mask="*")
            global_cl =  login_2_session(user=user, passw=passwd)
            attmps += 1
            if attmps == 4:
                  print(f"{colors['yel']}If you're entering the correct credentials but still can't log in, your account may be temporarily blocked.\nPlease wait a certain amount of time before trying again, or use another account.\n{colors['red']}If you still can't log in, your IP address may have been blocked by Instagram's servers. Please try again using a VPN.{colors['res']}")
            if global_cl == "bad_pass":
                  pass
            elif global_cl == "challenge":
                  pass
            elif global_cl == "unknownerror":
                  pass
            else:
                  is_Loggedin = True
                  print(f"{colors['gre']}Logged in to {colors["yel"]}@{user}{colors["res"]}.")
                  break
#Login with sessionid cookie
def sessionid_login(sessionid):
      global global_cl, is_Loggedin
      try:
            cl = Client()
            cl.login_by_sessionid(sessionid)
            global_cl = cl
            is_Loggedin = True
            print(f"{colors['gre']}Logged in to {colors["yel"]}@{global_cl.username_from_user_id(global_cl.user_id)}{colors["res"]}.")
            if os.path.exists(os.path.join(os.getcwd(), "data")):
                  if os.path.exists(os.path.join(os.getcwd(), "data", "sessions")):
                        pass
                  else:
                        os.mkdir(os.path.join(os.getcwd(), "data", "sessions"))
            else:
                  os.mkdir(os.path.join(os.getcwd()))
            global_cl.dump_settings(os.path.join("data","sessions",f"{str(global_cl.user_id) + "_settings.json"}"))
      except Exception as e:
            print(e)

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
                  i += 1
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
            if cmd == "":
                  pass
            elif cmd.lower() == "exit":
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
            elif cmd.lower().startswith("load_session"):
                  if len(cmd) >= len("laod_session  "):
                        try:
                              id = int(cmd[len("load_session "):])
                              load_session_with_id(id)
                        except KeyError as e:
                                    if str(e) == "'pinned_channels_info'":
                                          print(f"{colors['red']}Session expired! Please login.{colors['res']}")
                        except ValueError:
                                    print(f"{colors["red"]}Please enter a valid id.{colors["res"]}")
                  else:
                        print(f"{colors['red']}Syntax error!\n{colors['yel']}Usage: {colors['res']}load_session {colors["blu"]}<id>{colors['res']}")
            elif cmd.lower().startswith("followers"):
                  if len(cmd) >= len("followers  "):
                        if is_Loggedin:
                              try:
                                    userid = int(cmd[len("followers "):])
                                    print(f"Getting the user's followers... {colors['yel']}It may take some time!{colors["res"]}")
                                    show_followers(global_cl, userid)
                              except ValueError:
                                    try:
                                          username = cmd[len("followers "):]
                                          userid = global_cl.user_id_from_username(username=username)
                                          print(f"Getting the user's followers... {colors['yel']}It may take some time!{colors["res"]}")
                                          show_followers(global_cl, userid)
                                    except UserNotFound:
                                          print(f"{colors['red']}User not found! Please check the username.{colors["res"]}")
                                    
                        else:
                              print(login_before_error)
                  else:
                        print(f"{colors['red']}Syntax error!\n{colors['yel']}Usage: {colors['res']}followers {colors["blu"]}<username/userid>{colors['res']}")
            elif cmd.lower() == "getinfo":
                  if is_Loggedin:
                        show_account_infos(global_cl)
                  else:
                        print(login_before_error)
            elif cmd.lower().startswith("following"):
                  if is_Loggedin:
                        if len(cmd) >= len("following  "):
                              try:
                                    userid = int(cmd[len("following "):])
                                    print(f"Getting the user's followings... {colors["yel"]}It may take some time!{colors['res']}")
                                    show_followings(global_cl, userid)
                              except ValueError:
                                    try:
                                          userid = global_cl.user_id_from_username(cmd[len("following "):])
                                          print(f"Getting the user's followings... {colors["yel"]}It may take some time!{colors['res']}")
                                          show_followings(global_cl, userid)
                                    except UserNotFound:
                                          print(f"{colors['red']}User not found! Please check the username.{colors["res"]}")
                        else:
                              print(f"{colors['red']}Syntax error!\n{colors['yel']}Usage: {colors['res']}following {colors["blu"]}<username/userid>{colors['res']}")
                  else:
                        print(login_before_error)
            elif cmd.lower() == "self_followers":
                  if is_Loggedin:
                        self_followers(global_cl)
                  else:
                        print(login_before_error)
            elif cmd.lower().startswith("sessionid_login"):
                  if len(cmd) >= len("sessionid_login  "):
                        sessionid = cmd[len("sessionid_login "):]
                        sessionid_login(sessionid)
                  else:
                        print(f"{colors['red']}Syntax error!\n{colors['yel']}Usage: {colors['res']}sessionid_login {colors["blu"]}<sessionid value>{colors['res']}")
            elif cmd.lower().startswith("bitches"):
                  if is_Loggedin:
                        if len(cmd) >= len("bitches  "):
                              try:
                                    userid = int(cmd[len("bitches "):])
                                    print(f"Getting the user that don't follow back... {colors["yel"]}It may take some time!{colors['res']}")
                                    list_bitches(global_cl, userid)
                              except ValueError:
                                    try:
                                          userid = global_cl.user_id_from_username(cmd[len("bitches "):])
                                          print(f"Getting the users that don't follow back... {colors["yel"]}It may take some time!{colors['res']}")
                                          list_bitches(global_cl, userid)
                                    except UserNotFound:
                                          print(f"{colors['red']}User not found! Please check the username.{colors["res"]}")
                        else:
                              print(f"{colors['red']}Syntax error!\n{colors['yel']}Usage: {colors['res']}bitches {colors["blu"]}<username/userid>{colors['res']}")
                  else:
                        print(login_before_error)

            elif cmd.lower() == "self_bitches":
                  if is_Loggedin:
                        print(f"Getting the users that don't follow you back... {colors["yel"]}It may take some time!{colors['res']}")
                        self_bitches(global_cl)
                  else:
                        print(login_before_error)
            elif cmd.lower() == "self_following":
                  if is_Loggedin:
                        print(f"Getting the users that you follow... {colors["yel"]}It may take some time!{colors['res']}")
                        self_following(global_cl)
                  else:
                        print(login_before_error)
            elif cmd.lower() == "remove_bitches":
                  if is_Loggedin:
                        remove_bitches(global_cl)
                  else:
                        print(login_before_error)
            
            elif cmd.lower().startswith("userinfo"):
                  if is_Loggedin:
                        if len(cmd) >= len("userinfo  "):
                              inputed = cmd[len("userinfo "):]
                              try:
                                    userid = int(inputed)
                                    show_userinfo(global_cl, userid)
                              except ValueError:
                                    try:
                                          userid = global_cl.user_id_from_username(inputed)
                                          show_userinfo(global_cl, userid)
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
