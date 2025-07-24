import requests, random, string, json
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# ========== Konfigurasi ==========
AUTH_TOKEN = "j1UWp7wPPTJh3CF0V1EGs7oehVCjfHCUgrHyw296VS0cX4aMixC61RDApxdrwdsU6z"
URL_REGISTER = "https://www.gtechofficial.com/api/gtech-register.php"
URL_LOGIN = "https://www.gtechofficial.com/api/gtech-login.php"
URL_MINE = "https://www.gtechofficial.com/api/gtech-mining_process.php"

USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 15; Pixel 7 Pro) AppleWebKit/537.36 Chrome/124.0.6367.156 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 15; SM-S928B) AppleWebKit/537.36 Chrome/125.0.6422.140 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 15; Xiaomi 13T Pro) AppleWebKit/537.36 Chrome/126.0.6478.76 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5) AppleWebKit/605.1.15 Version/15.5 Mobile Safari/604.1",
    "Mozilla/5.0 (Linux; Android 15; Realme RMX3851) AppleWebKit/537.36 Chrome/126.0.6478.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 15; OnePlus 12R) AppleWebKit/537.36 Chrome/126.0.6478.96 Mobile Safari/537.36"
]

EMAIL_DOMAINS = ["@gmail.com", "@yahoo.com", "@outlook.com", "@mail.com", "@protonmail.com"]
NAMA_DEPAN = ["Andi", "Budi", "Citra", "Dina", "Eka", "Fajar", "Gilang", "Hana", "Ivan", "Joko"]
NAMA_BELAKANG = ["Saputra", "Wahyuni", "Santoso", "Pratama", "Rahmawati", "Wijaya", "Nugroho", "Putri"]

HEADERS_BASE = {
    "Accept": "*/*",
    "Content-Type": "application/json",
    "Origin": "https://www.gtechofficial.com",
    "Referer": "https://www.gtechofficial.com/app/SignupPage"
}

# ========== Utils ==========
def random_email():
    prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    domain = random.choice(EMAIL_DOMAINS)
    return prefix + domain

def random_name():
    return random.choice(NAMA_DEPAN) + " " + random.choice(NAMA_BELAKANG)

def random_phone():
    return '8' + ''.join(random.choices(string.digits, k=9))

def save_account(email, password, user_id):
    with open("accounts.txt", "a") as f:
        f.write(f"{email}|{password}|{user_id}\n")

def load_proxies():
    try:
        with open("proxy.txt") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def get_session(proxy=None):
    session = requests.Session()
    headers = HEADERS_BASE.copy()
    headers["User-Agent"] = random.choice(USER_AGENTS)
    headers["Accept-Language"] = random.choice(["id-ID,id;q=0.9", "en-US,en;q=0.9"])
    session.headers.update(headers)

    if proxy:
        if "@" in proxy:
            ip_port, creds = proxy.split("@")
            proxy_url = f"http://{creds}@{ip_port}"
        else:
            proxy_url = f"http://{proxy}"
        session.proxies.update({
            "http": proxy_url,
            "https": proxy_url
        })
        try:
            session.get("https://httpbin.org/ip", timeout=5, verify=False)
        except Exception as e:
            print(f"[⚠️] Proxy error: {proxy} → {e}")
            return None
    return session

# ========== Bot Logic ==========
def register_user(session, referral_code):
    email = random_email()
    password = "Kontol456@@"
    full_name = random_name()
    phone = random_phone()

    payload = {
        "full_name": full_name,
        "username": email,
        "password": password,
        "referral_code": referral_code,
        "auth_token": AUTH_TOKEN,
        "country_code": "62",
        "mobile_number": phone
    }

    try:
        r = session.post(URL_REGISTER, json=payload, timeout=10, verify=False)
        data = r.json()
        if data.get("response") == "1":
            print(f"[✓] Berhasil daftar: {email} | No HP: {phone}")
            return email, password
        else:
            print(f"[✗] Gagal daftar: {data}")
    except Exception as e:
        print(f"[✗] Error daftar: {e}")
    return None, None

def login_user(session, email, password):
    payload = {
        "username": email,
        "password": password,
        "auth_token": AUTH_TOKEN
    }
    try:
        r = session.post(URL_LOGIN, json=payload, timeout=10, verify=False)
        data = r.json()
        if data.get("response") == "1":
            user_id = data.get("user_id")
            print(f"[✓] Login sukses: {email} | user_id: {user_id}")
            return user_id
        else:
            print(f"[✗] Login gagal: {data}")
    except Exception as e:
        print(f"[✗] Error login: {e}")
    return None

def mining_loop(session, user_id, mining_count):
    for i in range(mining_count):
        payload = {
            "user_id": user_id,
            "auth_token": AUTH_TOKEN
        }
        try:
            r = session.post(URL_MINE, json=payload, timeout=10, verify=False)
            if "Success" in r.text:
                print(f"  ⛏️ Mining {i+1}/{mining_count} berhasil!")
            else:
                print(f"  ⚠️ Mining gagal: {r.text}")
        except Exception as e:
            print(f"  ⚠️ Error mining: {e}")

# ========== Main ==========
def main():
    print("[🚀] Bot GTech Auto Miner + Proxy + UA + Skip Mining\n")
    try:
        referral_code = input("Kode referral (tekan ENTER jika tidak ada): ").strip()
        jumlah = int(input("Jumlah akun yang ingin dibuat: "))
        use_proxy = input("Gunakan proxy? (y/n): ").strip().lower() == "y"
        enable_mining = input("Aktifkan mining? (y/n): ").strip().lower() == "y"
    except KeyboardInterrupt:
        print("\n[!] Dibatalkan oleh pengguna.")
        return

    proxies = load_proxies() if use_proxy else []
    proxy_index = 0

    for i in range(jumlah):
        print(f"\n[🔥] Akun #{i+1}")
        session = None
        retry = 0
        while retry < 5:
            proxy = None
            if use_proxy:
                if proxy_index >= len(proxies):
                    print("[✗] Tidak ada lagi proxy tersedia.")
                    return
                proxy = proxies[proxy_index]
                print(f"[🔌] Menggunakan proxy: {proxy}")
            session = get_session(proxy)
            if session:
                break
            else:
                retry += 1
                proxy_index += 1

        if not session:
            print(f"[✗] Gagal membuat sesi setelah 5 percobaan. Lewatkan akun.")
            continue

        email, password = register_user(session, referral_code)
        if email:
            user_id = login_user(session, email, password)
            if user_id:
                save_account(email, password, user_id)
                if enable_mining:
                    mining_count = random.randint(1, 6)
                    print(f"⛏️ Mining {mining_count}x dimulai...")
                    mining_loop(session, user_id, mining_count)
                else:
                    print("⏭️ Mining dilewati.")

        proxy_index += 1

if __name__ == "__main__":
    main()
