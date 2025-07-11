import re
from typing import Dict, List

def collect_user_info() -> Dict[str, any]:
    """Collect user information for AI-based wordlist generation."""
    print("[+] Enter known details about the target user (leave blank if unknown)")
    info = {
        "name": input("Full Name: ").strip(),
        "father": input("Father's Name: ").strip(),
        "dob": input("DOB (DDMMYYYY): ").strip(),
        "phone": input("Phone: ").strip(),
        "pet": input("Pet's Name: ").strip(),
        "school": input("School Name: ").strip(),
        "extra": []
    }
    while True:
        extra = input("Add extra info (friend name, nickname)? (blank to stop): ").strip()
        if not extra:
            break
        info['extra'].append(extra)
    return info

def generate_ai_wordlist(info: Dict[str, any], min_length: int = 6) -> List[str]:
    """Generate a password wordlist based on user information."""
    wordlist = set()
    base = [
        info.get("name", ""),
        info.get("father", ""),
        info.get("school", ""),
        info.get("pet", "")
    ]
    base = [w.lower().replace(" ", "") for w in base if w.strip()]
    extras = [e.lower().replace(" ", "") for e in info.get("extra", []) if e.strip()]
    dob = info.get("dob", "")
    dob_year = dob[-4:] if dob and len(dob) == 8 and dob.isdigit() else ""
    dob_short = dob[-2:] if dob_year else ""
    phone = re.sub(r"\D", "", info.get("phone", ""))
    phone_last4 = phone[-4:] if len(phone) >= 4 else ""
    phone_first5 = phone[:5] if len(phone) >= 5 else ""
    suffixes = ["123", "@123", "!", "2025"]
    special_chars = ["@", "!"]

    for word in base + extras:
        if not word:
            continue
        word_variations = [word, word.capitalize()]
        for w in word_variations:
            if len(w) >= min_length:
                wordlist.add(w)
            for suffix in suffixes:
                candidate = w + suffix
                if len(candidate) >= min_length:
                    wordlist.add(candidate)
            for char in special_chars:
                candidate = w + char
                if len(candidate) >= min_length:
                    wordlist.add(candidate)
                for suffix in suffixes:
                    candidate = w + char + suffix
                    if len(candidate) >= min_length:
                        wordlist.add(candidate)
            if dob_year:
                wordlist.add(w + dob_year)
                wordlist.add(w + dob_short)
    if phone_last4:
        wordlist.add(phone_last4)
    result = sorted([w for w in wordlist if w and len(w) >= min_length])
    print(f"[DEBUG] Generated AI wordlist: {result}")
    return result
