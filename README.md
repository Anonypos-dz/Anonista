# 🔐 Anonista - Instagram CLI Tool

A powerful command-line tool for Instagram account management, user enumeration, and data analysis. Built with Python and the `instagrapi` library.

```
    _                      _     _        
   / \   _ __   ___  _ __ (_)___| |_ __ _ 
  / _ \ | '_ \ / _ \| '_ \| / __| __/ _` |
 / ___ \| | | | (_) | | | | \__ \ || (_| |
/_/   \_\_| |_|\___/|_| |_|_|___/\__\__,_|
            V1.0 BETA (CLI)
```

## 📋 Features

### 🔑 Login Management
- **Login** - Authenticate with Instagram username and password
- **SessionID Login** - Login using Instagram session cookies
- **Sessions** - List all saved sessions
- **Load Session** - Quickly load a previously saved session

### 👤 Account Management
- **Account Info** - Display detailed profile information
- **Followers** - List your followers with full details
- **Following** - List accounts you follow
- **Bitches List** - Identify users who don't follow you back
- **Remove Bitches** - Unfollow all non-reciprocal followers
- **Unfollow** - Unfollow specific users

### 🔍 User Enumeration
- **User Info** - Get comprehensive information about any user
- **User Posts** - View all posts from a specific user
- **Dump Posts** - Download all user posts (photos and videos)
- **Followers** - List any user's followers
- **Following** - List accounts a user follows
- **Bitches** - Find users that don't follow a specific user back

## 🚀 Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Anonypos-dz/Anonista.git
   cd Anonista
   ```

2. **Install dependencies**
   ```bash
   pip install instagrapi colorama pwinput requests
   ```

   **Required packages:**
   - `instagrapi` - Instagram API wrapper
   - `colorama` - Terminal color output
   - `pwinput` - Secure password input
   - `requests` - HTTP library

3. **Run the tool**
   ```bash
   python main.py
   ```

## 📖 Usage

### Login
```
Anonista>> login
Username: your_username
Password: ••••••••••
```

### Using SessionID (Faster Login)
```
Anonista>> sessionid_login YOUR_SESSION_ID_HERE
```

### View Account Information
```
Anonista>> getinfo
```

### Check Followers
```
Anonista>> self_followers
```

### Find Users Who Don't Follow You Back
```
Anonista>> self_bitches
```

### Unfollow Non-Reciprocal Followers
```
Anonista>> remove_bitches
```

### Get User Information (by username or ID)
```
Anonista>> userinfo username_or_userid
```

### View User Posts
```
Anonista>> userposts username_or_userid
```

### Download All User Posts
```
Anonista>> dump_posts username_or_userid
```

### List User Followers
```
Anonista>> followers username_or_userid
```

### List User Following
```
Anonista>> following username_or_userid
```

### Load Saved Session
```
Anonista>> sessions           # View saved sessions
Anonista>> load_session 0     # Load session by ID
```

## 📁 Directory Structure

```
data/
├── sessions/          # Stored session files
├── users/             # User data
│   └── {username}/
│       ├── followers.txt
│       ├── following.txt
│       ├── bitches.txt
│       ├── userinfos.txt
│       ├── media.txt
│       ├── posts/     # Downloaded posts
│       └── reels/     # Downloaded videos
└── myaccounts/        # Your account data
    └── {username}/
        └── AccountInfos.txt
```

## ⚙️ Configuration

The tool automatically creates necessary directories:
- `data/sessions/` - Stores session cookies for quick re-login
- `data/users/` - Stores enumerated user data
- `data/myaccounts/` - Stores your account information

## ⚡ Rate Limiting & Cooldowns

The tool includes built-in cooldowns to avoid Instagram rate limiting:
- **3-second cooldown** between follower/following operations
- **5-second cooldown** after media downloads
- **Automatic handling** of rate limit errors with 5-minute sleep

## 🛡️ Important Notes

⚠️ **Disclaimer:**
- This tool is for educational and authorized use only
- Respect Instagram's Terms of Service and local laws
- Use VPN if you encounter too many requests errors
- Account may be temporarily blocked if rate limits are exceeded
- Be responsible and ethical in your usage

### Instagram Security
- Use strong passwords
- Enable 2FA on your Instagram account
- Keep sessions secure
- If you see "Challenge Required" errors, use a VPN

## 🔧 Troubleshooting

### "Challenge Required" Error
**Solution:** Use a VPN or wait and try again later.

```
Anonista>> login
[RED]Challenge required, try to use a vpn!
```

### "BadPassword" Error
**Solution:** Check your credentials.

```
Anonista>> login
[RED]Please check your password!!
```

### "Too Many Requests"
**Solution:** Wait 5 minutes or use a VPN. The tool will automatically sleep for 5 minutes.

```
Anonista>> [Command]
[RED]Wooah Bro chill!! Too many requists. Sleeping for 5min....
```

### "Session Expired"
**Solution:** Login again or use `sessionid_login` with a fresh session.

## 📊 Output Examples

### Account Information
```
_------------------------------_
         Account Infos
_------------------------------_
User id : 123456789
Username : your_username
Full Name: Your Full Name
Bio : Your bio here
Followers Count: 1000
Following Count: 500
Is Private: False
Is Business: False
Is Verified: False
...
```

Data is automatically saved to text files for reference.

## 🎮 Commands List

| Category | Command | Description |
|----------|---------|-------------|
| **Login** | `login` | Login with credentials |
| | `sessionid_login <id>` | Login with session ID |
| | `sessions` | List saved sessions |
| | `load_session <id>` | Load a saved session |
| **Account** | `getinfo` | Show your profile |
| | `self_followers` | List your followers |
| | `self_following` | List your following |
| | `self_bitches` | List non-reciprocal followers |
| | `remove_bitches` | Unfollow non-reciprocal followers |
| **Enum** | `userinfo <user>` | Get user information |
| | `userposts <user>` | View user posts |
| | `dump_posts <user>` | Download user posts |
| | `followers <user>` | List user followers |
| | `following <user>` | List user following |
| | `bitches <user>` | Find non-reciprocal followers |
| **System** | `help` | Show help menu |
| | `clear` | Clear terminal |
| | `exit` | Exit the tool |

## 📝 License

```
Copyright 2026 Anonypos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 👨‍💻 Author

**Programmed by Anonypos, 2026**

---

## ⭐ Features Highlights

✅ Fast session-based login  
✅ Comprehensive user enumeration  
✅ Automatic media downloading  
✅ Built-in rate limit handling  
✅ Colorful CLI interface  
✅ Persistent session storage  
✅ Detailed data export  

## 🤝 Contributing

Found a bug or have suggestions? Feel free to open an issue or submit a pull request.

## ⚠️ Legal Disclaimer

This tool is provided for educational purposes only. Users are responsible for compliance with Instagram's Terms of Service and all applicable laws. Unauthorized access or misuse of this tool may violate laws and Instagram's policies. The author assumes no liability for misuse.

---

**Enjoy using Anonista! 🚀**
