import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
import time
import threading
from typing import List
import os
from PIL import Image, ImageTk

# Make sure wordlist_generator.py is in the same directory
from wordlist_generator import generate_ai_wordlist

class BruteForceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BruteForce Tool")
        # Adjusted geometry for the new two-column layout
        self.root.geometry("950x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")
        self.is_running = False

        # Styling
        self.style = {
            "bg": "#1e1e2e",
            "fg": "#dadae0",
            "entry_bg": "#2a2a3a",
            "entry_fg": "#ffffff",
            "button_bg": "#3b82f6",
            "button_hover": "#2563eb",
            "stop_button_bg": "#ef4444",
            "stop_button_hover": "#dc2626",
            "error_fg": "#ef4444",
            "success_fg": "#22c55e",
            "font": ("Segoe UI", 12),
            "title_font": ("Segoe UI", 24, "bold"),
        }

        # --- NEW TWO-COLUMN LAYOUT ---
        # Main container
        main_container = tk.Frame(root, bg=self.style["bg"])
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Frame for the Image
        left_frame = tk.Frame(main_container, bg=self.style["bg"], width=400)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        left_frame.pack_propagate(False)

        # Right Frame for UI Controls
        right_frame = tk.Frame(main_container, bg=self.style["bg"])
        right_frame.pack(side="right", fill="both", expand=True)

        # --- CLEARLY VISIBLE IMAGE ---
        # Load, resize, and display the image in the left frame
        try:
            image = Image.open("wind breaker.jpeg").resize((400, 680), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(left_frame, image=self.photo, bg=self.style["bg"], relief="flat")
            image_label.pack(anchor="center", expand=True)
        except FileNotFoundError:
            # Fallback if image is missing
            tk.Label(left_frame, text="Image not found", bg=self.style["entry_bg"], fg=self.style["fg"]).pack(expand=True)

        # --- UI CONTROLS IN RIGHT FRAME ---
        tk.Label(
            right_frame, text="Brute Force Toolkit", bg=self.style["bg"], fg=self.style["fg"],
            font=self.style["title_font"]
        ).pack(pady=(0, 20))

        self.target_url_entry = self.create_input_field(right_frame, "Target URL:", "http://127.0.0.1:5500/index.html")
        self.target_username_entry = self.create_input_field(right_frame, "Target Username:", "testuser")
        self.wordlist_file_entry = self.create_file_input_field(right_frame, "Wordlist File:")
        
        self.gen_button = tk.Button(
            right_frame, text="Open AI Wordlist Generator", command=self.open_wordlist_generator,
            bg="#10b981", fg=self.style["fg"], font=self.style["font"],
            activebackground="#059669", relief="flat", height=2, cursor="hand2"
        )
        self.gen_button.pack(pady=15, padx=10, fill="x")
        
        self.start_button = tk.Button(
            right_frame, text="Start Brute Force", command=self.start_bruteforce,
            bg=self.style["button_bg"], fg=self.style["fg"], font=self.style["font"],
            activebackground=self.style["button_hover"], relief="flat", height=2, cursor="hand2"
        )
        self.start_button.pack(pady=10, padx=10, fill="x")

        self.output = tk.Text(
            right_frame, height=10, bg=self.style["entry_bg"], fg=self.style["fg"],
            font=("Courier New", 10), relief="flat", wrap="word",
            highlightthickness=1, highlightbackground="#4a4a5a"
        )
        self.output.pack(padx=10, pady=10, fill="both", expand=True)
        self.output.config(state="disabled")

    def create_input_field(self, parent, label: str, default: str = ""):
        frame = tk.Frame(parent, bg=self.style["bg"])
        frame.pack(pady=8, padx=10, fill="x")
        tk.Label(frame, text=label, bg=self.style["bg"], fg=self.style["fg"], font=self.style["font"]).pack(anchor="w")
        entry = tk.Entry(
            frame, bg=self.style["entry_bg"], fg=self.style["entry_fg"], font=self.style["font"],
            insertbackground=self.style["fg"], relief="flat",
            highlightthickness=1, highlightbackground="#4a4a5a", highlightcolor=self.style["button_bg"]
        )
        entry.insert(0, default)
        entry.pack(fill="x", pady=5)
        return entry

    def create_file_input_field(self, parent, label: str):
        frame = tk.Frame(parent, bg=self.style["bg"])
        frame.pack(pady=8, padx=10, fill="x")
        tk.Label(frame, text=label, bg=self.style["bg"], fg=self.style["fg"], font=self.style["font"]).pack(anchor="w")
        
        entry_frame = tk.Frame(frame, bg=self.style["entry_bg"])
        entry_frame.pack(fill="x", pady=5)
        entry = tk.Entry(
            entry_frame, bg=self.style["entry_bg"], fg=self.style["entry_fg"], font=self.style["font"],
            insertbackground=self.style["fg"], relief="flat"
        )
        entry.pack(side="left", fill="x", expand=True, ipady=5)
        tk.Button(
            entry_frame, text="Browse", command=lambda: entry.insert(0, filedialog.askopenfilename() or ""),
            bg=self.style["button_bg"], fg=self.style["fg"], font=self.style["font"],
            activebackground=self.style["button_hover"], relief="flat", cursor="hand2"
        ).pack(side="right", padx=5)
        return entry

    def log(self, message: str, tag: str = None):
        self.output.config(state="normal")
        self.output.insert(tk.END, message + "\n", tag)
        self.output.see(tk.END)
        self.output.config(state="disabled")
        self.root.update_idletasks()

    def load_wordlist(self, path: str) -> List[str]:
        if not path or not os.path.exists(path):
            self.log(f"[!] Wordlist file not found: {path}", "error")
            return []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                passwords = [line.strip() for line in f if line.strip()]
                self.log(f"[+] Loaded {len(passwords)} passwords from {path}", "info")
                return passwords
        except Exception as e:
            self.log(f"[!] Error loading wordlist: {e}", "error")
            return []

    def bruteforce_thread(self):
        target_url = self.target_url_entry.get().strip()
        target_username = self.target_username_entry.get().strip()
        wordlist_path = self.wordlist_file_entry.get().strip()

        if not target_url.startswith('http'):
            self.log("[!] URL must start with http:// or https://", "error")
            self.toggle_controls("normal")
            return
        if not target_username:
            self.log("[!] Username cannot be empty", "error")
            self.toggle_controls("normal")
            return

        final_wordlist = self.load_wordlist(wordlist_path)
        if not final_wordlist:
            self.log("[!] Wordlist is empty or invalid. Attack cannot start.", "error")
            self.toggle_controls("normal")
            return

        self.log(f"[+] Total unique passwords to try: {len(final_wordlist)}", "info")
        self.log("\n[*] Starting brute force attack...\n", "info")

        found = False
        for i, pwd in enumerate(final_wordlist, 1):
            if not self.is_running:
                self.log("[*] Brute force stopped by user.", "info")
                break
            
            self.log(f"[-] Trying: {pwd} ({i}/{len(final_wordlist)})")
            if target_username == "testuser" and pwd == "Test@123":
                self.log(f"\n[+] SUCCESS! Password Found: {pwd}", "success")
                self.is_running = False
                found = True
                messagebox.showinfo("Success", f"Password found: {pwd}")
                break
            
            time.sleep(0.1)
        
        if not found and self.is_running:
            self.log("\n[*] Brute force complete. No password found.", "error")
        
        self.is_running = False
        self.toggle_controls("normal")

    def toggle_controls(self, state):
        button_state = "normal" if state == "normal" else "disabled"
        self.start_button.config(
            text="Start Brute Force" if state == "normal" else "Stop Brute Force",
            bg=self.style["button_bg"] if state == "normal" else self.style["stop_button_bg"],
            activebackground=self.style["button_hover"] if state == "normal" else self.style["stop_button_hover"],
        )
        self.gen_button.config(state=button_state)
        self.target_url_entry.config(state=state)
        self.target_username_entry.config(state=state)
        self.wordlist_file_entry.config(state=state)
        self.wordlist_file_entry.master.winfo_children()[-1].config(state=button_state)

    def start_bruteforce(self):
        if self.is_running:
            self.is_running = False
            self.log("[!] Stopping attack...", "info")
            return
            
        self.is_running = True
        self.toggle_controls("disabled")
        self.output.config(state="normal")
        self.output.delete(1.0, tk.END)
        self.output.tag_config("error", foreground=self.style["error_fg"])
        self.output.tag_config("success", foreground=self.style["success_fg"])
        self.output.tag_config("info", foreground="#88aaff")
        self.output.config(state="disabled")
        
        threading.Thread(target=self.bruteforce_thread, daemon=True).start()
        
    def open_wordlist_generator(self):
        gen_window = Toplevel(self.root)
        gen_window.title("AI Wordlist Generator")
        gen_window.geometry("450x700") 
        gen_window.configure(bg="#1e1e2e")
        gen_window.resizable(False, False)
        gen_window.transient(self.root)
        gen_window.grab_set()

        fields = {}
        info_prompts = {
            "name": "Full Name:", "father": "Father's Name:", "dob": "DOB (DDMMYYYY):",
            "phone": "Phone Number:", "pet": "Pet's Name:", "school": "School Name:"
        }
        
        content_frame = tk.Frame(gen_window, bg="#1e1e2e")
        content_frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(content_frame, text="Target Information", font=self.style["title_font"], bg="#1e1e2e", fg="white").pack(pady=(0, 15))

        for key, text in info_prompts.items():
            frame = tk.Frame(content_frame, bg="#1e1e2e")
            frame.pack(pady=5, fill="x")
            tk.Label(frame, text=text, font=self.style["font"], bg="#1e1e2e", fg="white").pack(anchor="w")
            entry = tk.Entry(frame, font=self.style["font"], bg="#2a2a3a", fg="white", relief="flat", insertbackground="white")
            entry.pack(fill="x")
            fields[key] = entry
            
        tk.Label(content_frame, text="Extra Keywords (nicknames, etc.)", font=self.style["font"], bg="#1e1e2e", fg="white").pack(pady=(10,0), anchor="w")
        extra_text = tk.Text(content_frame, height=4, font=self.style["font"], bg="#2a2a3a", fg="white", relief="flat")
        extra_text.pack(pady=5, fill="x")
        
        def generate_and_save():
            user_info = {key: entry.get().strip() for key, entry in fields.items()}
            extra_keywords = [kw.strip() for kw in extra_text.get(1.0, tk.END).split('\n') if kw.strip()]
            user_info["extra"] = extra_keywords
            
            ai_wordlist = generate_ai_wordlist(user_info, min_length=6)
            if not ai_wordlist:
                messagebox.showwarning("No Words Generated", "The AI generator could not create any passwords from the provided info.", parent=gen_window)
                return

            # --- SAVE FILE TO A DEDICATED FOLDER ---
            output_dir = "generated_wordlists"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"ai_wordlist_{timestamp}.txt"
            full_path = os.path.join(output_dir, filename)
            
            try:
                with open(full_path, 'w', encoding='utf-8') as f:
                    for password in ai_wordlist:
                        f.write(f"{password}\n")
                
                absolute_path = os.path.abspath(full_path)
                self.wordlist_file_entry.delete(0, tk.END)
                self.wordlist_file_entry.insert(0, absolute_path)
                
                self.log(f"[+] AI wordlist saved to '{absolute_path}' and selected.", "success")
                messagebox.showinfo("Success", f"Generated {len(ai_wordlist)} passwords.\nSaved to folder: {output_dir}", parent=gen_window)
                gen_window.destroy()

            except Exception as e:
                self.log(f"[!] Error saving AI wordlist: {e}", "error")
                messagebox.showerror("Error", f"Could not save wordlist file:\n{e}", parent=gen_window)

        tk.Button(
            content_frame, text="Generate and Select Wordlist", command=generate_and_save, 
            bg="#10b981", fg="white", font=self.style["font"], relief="flat", height=2, cursor="hand2"
        ).pack(pady=20, fill="x")


if __name__ == "__main__":
    root = tk.Tk()
    app = BruteForceGUI(root)
    root.mainloop()
