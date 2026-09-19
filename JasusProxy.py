"""
=========================================================
  JASUS PROXY - High Performance Proxy Harvester & Filter
  GUI Edition (CustomTkinter)
  Author: EZZELDIN MESBAH
=========================================================
"""

import os
import re
import sys
import time
import queue
import threading
import requests
from PIL import Image
import customtkinter as ctk
from tkinter import filedialog, messagebox
from concurrent.futures import ThreadPoolExecutor

# Fix Windows console UTF-8 output if run from terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Import Proxy Harvester if available
try:
    from ProxyReaper import fetch_proxies
    HAS_REAPER = True
except ImportError:
    try:
        from JasusReaper import fetch_proxies
        HAS_REAPER = True
    except ImportError:
        HAS_REAPER = False

# Base Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PNG = os.path.join(BASE_DIR, "assets", "logo.png")
LOGO_ICO = os.path.join(BASE_DIR, "assets", "logo.ico")

# Theme Configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

THEME = {
    "bg": "#080C14",
    "card_bg": "#0F172A",
    "card_border": "#1E293B",
    "primary": "#00E5FF",       # Neon Cyan
    "primary_hover": "#00B4D8",
    "secondary": "#FF5722",     # Electric Orange
    "secondary_hover": "#E64A19",
    "success": "#10B981",       # Emerald Green
    "fail": "#EF4444",          # Crimson Red
    "warning": "#F59E0B",       # Amber
    "purple": "#8B5CF6",        # Neon Violet
    "purple_hover": "#7C3AED",
    "text_main": "#F8FAFC",
    "text_muted": "#94A3B8",
    "input_bg": "#1E293B",
    "console_bg": "#020617"
}

TARGET_PRESETS = {
    "⚡ Fast Ping (Cloudflare CDN)": "https://1.1.1.1/cdn-cgi/trace",
    "🌐 Fast IP Check (HttpBin)": "http://httpbin.org/ip",
    "🔍 Fast SSL (Api.ipify)": "https://api.ipify.org?format=json",
    "🌍 Google Connectivity": "https://www.google.com/generate_204",
    "▶️ YouTube Access": "https://www.youtube.com",
    "🎯 Custom URL...": ""
}

PROTOCOLS = ["Auto (HTTP + SOCKS5)", "HTTP / HTTPS", "SOCKS5", "SOCKS4"]

class JasusProxy(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window Title & Geometry
        self.title("Jasus Proxy - Made by EZZELDIN MESBAH")
        self.geometry("1080x890")
        self.minsize(920, 720)
        self.configure(fg_color=THEME["bg"])
        
        # Set App Window Icon
        self._set_app_icon()
        
        # State Variables
        self.input_path = ctk.StringVar(value="raw_proxies.txt")
        self.output_path = ctk.StringVar(value="live_proxies.txt")
        self.target_preset = ctk.StringVar(value="⚡ Fast Ping (Cloudflare CDN)")
        self.custom_url = ctk.StringVar(value="https://1.1.1.1/cdn-cgi/trace")
        self.protocol_mode = ctk.StringVar(value="Auto (HTTP + SOCKS5)")
        self.threads_count = ctk.IntVar(value=70)
        self.timeout_sec = ctk.IntVar(value=5)
        
        self.proxies_list = []
        self.live_proxies = []
        self.dead_count = 0
        self.processed_count = 0
        self.is_running = False
        self.stop_event = threading.Event()
        self.ui_queue = queue.Queue()
        
        self._build_ui()
        self._process_queue()

    def _set_app_icon(self):
        if os.path.exists(LOGO_ICO):
            try:
                self.iconbitmap(LOGO_ICO)
            except Exception:
                pass

    def _build_ui(self):
        # Main scrollable container
        self.container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both", padx=15, pady=10)

        # Header section with Logo & Mission Description
        self._build_header()

        # Input & Output Configuration Card
        self._build_io_card()

        # Engine Settings Card (Threads, Target, Timeout, Protocol)
        self._build_settings_card()

        # Live Stats Dashboard Cards
        self._build_stats_card()

        # Action Buttons Row
        self._build_actions_row()

        # Real-time Console & Log Output
        self._build_console_card()

    def _build_header(self):
        hdr = ctk.CTkFrame(self.container, fg_color="transparent")
        hdr.pack(fill="x", pady=(10, 15))

        # Brand Header (Logo + Title)
        top_brand_frame = ctk.CTkFrame(hdr, fg_color="transparent")
        top_brand_frame.pack()

        # Load & display Jasus Logo image
        if os.path.exists(LOGO_PNG):
            try:
                pil_logo = Image.open(LOGO_PNG)
                self.logo_ctk = ctk.CTkImage(light_image=pil_logo, dark_image=pil_logo, size=(75, 75))
                logo_lbl = ctk.CTkLabel(top_brand_frame, image=self.logo_ctk, text="")
                logo_lbl.pack(side="left", padx=(0, 15))
            except Exception:
                pass

        text_title_frame = ctk.CTkFrame(top_brand_frame, fg_color="transparent")
        text_title_frame.pack(side="left")

        title_lbl = ctk.CTkLabel(
            text_title_frame, 
            text="JASUS PROXY", 
            font=("Impact", 46), 
            text_color=THEME["primary"]
        )
        title_lbl.pack(anchor="w")

        author_badge = ctk.CTkLabel(
            text_title_frame,
            text="MADE BY EZZELDIN MESBAH",
            font=("Consolas", 11, "bold"),
            text_color="#38BDF8",
            fg_color="#0C4A6E",
            corner_radius=6,
            padx=8,
            pady=2
        )
        author_badge.pack(anchor="w", pady=(2, 0))

        # Clear Mission Description
        mission_frame = ctk.CTkFrame(hdr, fg_color=THEME["card_bg"], corner_radius=10, border_width=1, border_color=THEME["card_border"])
        mission_frame.pack(fill="x", pady=(12, 0), padx=5)

        mission_en = ctk.CTkLabel(
            mission_frame, 
            text="⚡ Automated Multi-Source Proxy Harvester & Ultra-Fast Live Verification Engine", 
            font=("Segoe UI", 12, "bold"), 
            text_color=THEME["primary"]
        )
        mission_en.pack(pady=(8, 2))

        mission_sub = ctk.CTkLabel(
            mission_frame, 
            text="Scrapes thousands of public proxies, tests live connectivity & latency, and filters out dead proxies instantly", 
            font=("Segoe UI", 11), 
            text_color=THEME["text_muted"]
        )
        mission_sub.pack(pady=(0, 8))

    def _build_io_card(self):
        card = ctk.CTkFrame(self.container, fg_color=THEME["card_bg"], corner_radius=12, border_width=1, border_color=THEME["card_border"])
        card.pack(fill="x", pady=6)

        # Input Row
        r1 = ctk.CTkFrame(card, fg_color="transparent")
        r1.pack(fill="x", padx=15, pady=(12, 6))
        ctk.CTkLabel(r1, text="📥 INPUT LIST:", font=("Segoe UI", 12, "bold"), text_color=THEME["primary"], width=110, anchor="w").pack(side="left")
        ctk.CTkEntry(r1, textvariable=self.input_path, height=36, fg_color=THEME["input_bg"], border_color=THEME["card_border"]).pack(side="left", fill="x", expand=True, padx=8)
        ctk.CTkButton(r1, text="Browse 📂", width=90, height=36, fg_color="#334155", hover_color="#475569", command=self._browse_input).pack(side="left", padx=2)
        if HAS_REAPER:
            ctk.CTkButton(r1, text="⚡ Harvest 15K+", width=130, height=36, fg_color=THEME["purple"], hover_color=THEME["purple_hover"], font=("Segoe UI", 12, "bold"), command=self._trigger_reaper).pack(side="left", padx=4)

        # Output Row
        r2 = ctk.CTkFrame(card, fg_color="transparent")
        r2.pack(fill="x", padx=15, pady=(4, 12))
        ctk.CTkLabel(r2, text="💾 CLEAN OUTPUT:", font=("Segoe UI", 12, "bold"), text_color=THEME["success"], width=110, anchor="w").pack(side="left")
        ctk.CTkEntry(r2, textvariable=self.output_path, height=36, fg_color=THEME["input_bg"], border_color=THEME["card_border"]).pack(side="left", fill="x", expand=True, padx=8)
        ctk.CTkButton(r2, text="Save As 💾", width=90, height=36, fg_color="#334155", hover_color="#475569", command=self._browse_output).pack(side="left", padx=2)

    def _build_settings_card(self):
        card = ctk.CTkFrame(self.container, fg_color=THEME["card_bg"], corner_radius=12, border_width=1, border_color=THEME["card_border"])
        card.pack(fill="x", pady=6)

        # Row 1: Target Selection & Protocol
        r1 = ctk.CTkFrame(card, fg_color="transparent")
        r1.pack(fill="x", padx=15, pady=(10, 5))

        ctk.CTkLabel(r1, text="🎯 Target Test:", font=("Segoe UI", 11, "bold"), text_color=THEME["text_muted"]).pack(side="left", padx=(0, 5))
        self.preset_menu = ctk.CTkOptionMenu(
            r1, 
            values=list(TARGET_PRESETS.keys()), 
            variable=self.target_preset, 
            command=self._on_preset_change,
            width=240, 
            height=32,
            fg_color="#1E293B",
            button_color="#334155"
        )
        self.preset_menu.pack(side="left", padx=(0, 15))

        ctk.CTkLabel(r1, text="🔒 Protocol:", font=("Segoe UI", 11, "bold"), text_color=THEME["text_muted"]).pack(side="left", padx=(0, 5))
        self.proto_menu = ctk.CTkOptionMenu(
            r1, 
            values=PROTOCOLS, 
            variable=self.protocol_mode, 
            width=180, 
            height=32,
            fg_color="#1E293B",
            button_color="#334155"
        )
        self.proto_menu.pack(side="left")

        # Row 2: Sliders for Threads & Timeout
        r2 = ctk.CTkFrame(card, fg_color="transparent")
        r2.pack(fill="x", padx=15, pady=(5, 10))

        # Threads slider
        ctk.CTkLabel(r2, text="⚡ Threads:", font=("Segoe UI", 11, "bold"), text_color=THEME["text_muted"]).pack(side="left", padx=(0, 5))
        self.threads_lbl = ctk.CTkLabel(r2, text="70", font=("Consolas", 12, "bold"), text_color=THEME["primary"], width=30)
        self.threads_lbl.pack(side="left", padx=(0, 5))
        self.threads_slider = ctk.CTkSlider(
            r2, from_=5, to=200, number_of_steps=39, 
            variable=self.threads_count, 
            command=lambda val: self.threads_lbl.configure(text=str(int(val))),
            width=150
        )
        self.threads_slider.pack(side="left", padx=(0, 20))

        # Timeout slider
        ctk.CTkLabel(r2, text="⏱️ Timeout:", font=("Segoe UI", 11, "bold"), text_color=THEME["text_muted"]).pack(side="left", padx=(0, 5))
        self.timeout_lbl = ctk.CTkLabel(r2, text="5s", font=("Consolas", 12, "bold"), text_color=THEME["warning"], width=30)
        self.timeout_lbl.pack(side="left", padx=(0, 5))
        self.timeout_slider = ctk.CTkSlider(
            r2, from_=1, to=15, number_of_steps=14, 
            variable=self.timeout_sec, 
            command=lambda val: self.timeout_lbl.configure(text=f"{int(val)}s"),
            width=120
        )
        self.timeout_slider.pack(side="left")

    def _build_stats_card(self):
        stats_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        stats_frame.pack(fill="x", pady=6)
        stats_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.stat_loaded = self._create_metric_card(stats_frame, "TOTAL LOADED", "0", THEME["primary"], 0)
        self.stat_live = self._create_metric_card(stats_frame, "LIVE / ALIVE", "0", THEME["success"], 1)
        self.stat_dead = self._create_metric_card(stats_frame, "DEAD / FAILED", "0", THEME["fail"], 2)
        self.stat_rate = self._create_metric_card(stats_frame, "SUCCESS RATE", "0%", THEME["warning"], 3)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.container, height=10, fg_color="#1E293B", progress_color=THEME["primary"])
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(4, 8))

    def _create_metric_card(self, parent, title, initial_val, color, col):
        card = ctk.CTkFrame(parent, fg_color=THEME["card_bg"], corner_radius=10, border_width=1, border_color=THEME["card_border"])
        card.grid(row=0, column=col, padx=5, pady=2, sticky="nsew")
        
        ctk.CTkLabel(card, text=title, font=("Segoe UI", 10, "bold"), text_color=THEME["text_muted"]).pack(pady=(8, 0))
        val_lbl = ctk.CTkLabel(card, text=initial_val, font=("Impact", 28), text_color=color)
        val_lbl.pack(pady=(0, 8))
        return val_lbl

    def _build_actions_row(self):
        btn_row = ctk.CTkFrame(self.container, fg_color="transparent")
        btn_row.pack(fill="x", pady=8)

        self.start_btn = ctk.CTkButton(
            btn_row, 
            text="🚀 START ENGINE", 
            font=("Impact", 22), 
            fg_color=THEME["secondary"], 
            hover_color=THEME["secondary_hover"], 
            height=54, 
            corner_radius=12, 
            command=self.toggle_engine
        )
        self.start_btn.pack(side="left", fill="x", expand=True, padx=4)

        self.copy_btn = ctk.CTkButton(
            btn_row, 
            text="📋 Copy Live", 
            font=("Segoe UI", 12, "bold"), 
            fg_color="#1E293B", 
            hover_color="#334155", 
            height=54, 
            width=130, 
            corner_radius=12, 
            command=self._copy_live_to_clipboard
        )
        self.copy_btn.pack(side="left", padx=4)

        self.clear_btn = ctk.CTkButton(
            btn_row, 
            text="🧹 Clear Logs", 
            font=("Segoe UI", 12, "bold"), 
            fg_color="#1E293B", 
            hover_color="#334155", 
            height=54, 
            width=110, 
            corner_radius=12, 
            command=self._clear_logs
        )
        self.clear_btn.pack(side="left", padx=4)

    def _build_console_card(self):
        console_frame = ctk.CTkFrame(self.container, fg_color=THEME["console_bg"], corner_radius=10, border_width=1, border_color=THEME["card_border"])
        console_frame.pack(fill="both", expand=True, pady=6)

        header = ctk.CTkFrame(console_frame, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(6, 2))
        ctk.CTkLabel(header, text="💻 REALTIME ACTIVITY CONSOLE", font=("Consolas", 11, "bold"), text_color=THEME["text_muted"]).pack(side="left")
        
        self.log_box = ctk.CTkTextbox(
            console_frame, 
            height=240, 
            font=("Consolas", 12), 
            fg_color="transparent", 
            text_color=THEME["primary"],
            wrap="none"
        )
        self.log_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _on_preset_change(self, choice):
        if choice in TARGET_PRESETS and TARGET_PRESETS[choice]:
            self.custom_url.set(TARGET_PRESETS[choice])
        elif choice == "🎯 Custom URL...":
            dialog = ctk.CTkInputDialog(text="Enter custom URL to test proxies against:", title="Custom Target URL")
            url = dialog.get_input()
            if url:
                self.custom_url.set(url.strip())
            else:
                self.target_preset.set("⚡ Fast Ping (Cloudflare CDN)")
                self.custom_url.set(TARGET_PRESETS["⚡ Fast Ping (Cloudflare CDN)"])

    def _browse_input(self):
        f = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if f:
            self.input_path.set(f)

    def _browse_output(self):
        f = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if f:
            self.output_path.set(f)

    def _copy_live_to_clipboard(self):
        if not self.live_proxies:
            messagebox.showwarning("Empty", "No live proxies found yet!")
            return
        self.clipboard_clear()
        self.clipboard_append("\n".join(self.live_proxies))
        self._enqueue_log(f"📋 Copied {len(self.live_proxies)} live proxies to clipboard!", "success")

    def _clear_logs(self):
        self.log_box.delete("1.0", "end")

    def _trigger_reaper(self):
        if self.is_running:
            messagebox.showwarning("Busy", "Cannot harvest while checking engine is running.")
            return
        threading.Thread(target=self._run_reaper_task, daemon=True).start()

    def _run_reaper_task(self):
        self._enqueue_log("⚡ Launching Jasus Proxy Harvester...", "info")
        try:
            proxies = fetch_proxies(output_file="raw_proxies.txt", log_callback=lambda m: self._enqueue_log(m, "info"))
            self.input_path.set(os.path.abspath("raw_proxies.txt"))
            self.ui_queue.put(("set_loaded", len(proxies)))
            self._enqueue_log(f"🎉 Harvested & loaded {len(proxies):,} proxies automatically!", "success")
        except Exception as e:
            self._enqueue_log(f"❌ Harvester failed: {str(e)}", "fail")

    def toggle_engine(self):
        if self.is_running:
            self.is_running = False
            self.stop_event.set()
            self.start_btn.configure(text="🚀 START ENGINE", fg_color=THEME["secondary"])
            self._enqueue_log("🛑 Engine stop signal requested. Finishing pending tasks...", "fail")
        else:
            self.is_running = True
            self.stop_event.clear()
            self.start_btn.configure(text="🛑 STOP ENGINE", fg_color=THEME["fail"])
            threading.Thread(target=self._engine_worker, daemon=True).start()

    def _enqueue_log(self, msg, status="info"):
        self.ui_queue.put(("log", (msg, status)))

    def _process_queue(self):
        try:
            while True:
                item = self.ui_queue.get_nowait()
                action, data = item
                if action == "log":
                    msg, status = data
                    icon = "»" if status == "info" else "✔" if status == "success" else "✘"
                    line = f"{icon} {time.strftime('%H:%M:%S')} | {msg}\n"
                    self.log_box.insert("end", line)
                    self.log_box.see("end")
                elif action == "update_stats":
                    live, dead, total, processed = data
                    self.stat_live.configure(text=str(live))
                    self.stat_dead.configure(text=str(dead))
                    rate = (live / processed * 100) if processed > 0 else 0
                    self.stat_rate.configure(text=f"{rate:.1f}%")
                    prog = (processed / total) if total > 0 else 0
                    self.progress_bar.set(prog)
                elif action == "set_loaded":
                    self.stat_loaded.configure(text=str(data))
                elif action == "finished":
                    self.is_running = False
                    self.start_btn.configure(text="🚀 START ENGINE", fg_color=THEME["secondary"])
                    self._save_results()
        except queue.Empty:
            pass
        self.after(50, self._process_queue)

    def _engine_worker(self):
        in_file = self.input_path.get()
        if not os.path.exists(in_file):
            self._enqueue_log(f"❌ Input file not found: {in_file}", "fail")
            self.ui_queue.put(("finished", None))
            return

        self._enqueue_log(f"📖 Parsing raw proxy list from {os.path.basename(in_file)}...", "info")
        self.live_proxies = []
        self.dead_count = 0
        self.processed_count = 0
        
        try:
            with open(in_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            raw_matches = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}:\d{2,5}\b', content)
            self.proxies_list = sorted(list(set(raw_matches)))
            total = len(self.proxies_list)
            
            self.ui_queue.put(("set_loaded", total))
            self._enqueue_log(f"✨ Loaded {total:,} unique proxies. Starting verification...", "info")
            
            if total == 0:
                self._enqueue_log("⚠️ No valid IP:Port proxies detected in file!", "fail")
                self.ui_queue.put(("finished", None))
                return

            target = self.custom_url.get() or TARGET_PRESETS.get(self.target_preset.get(), "https://1.1.1.1/cdn-cgi/trace")
            timeout = self.timeout_sec.get()
            proto_mode = self.protocol_mode.get()
            workers = self.threads_count.get()

            self._enqueue_log(f"🚀 Launching {workers} concurrent workers (Target: {target}, Timeout: {timeout}s)...", "info")

            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = []
                for p in self.proxies_list:
                    if self.stop_event.is_set():
                        break
                    futures.append(executor.submit(self._check_single_proxy, p, target, timeout, proto_mode, total))
                
                # Wait for running batch
                for f in futures:
                    if self.stop_event.is_set():
                        break
                    try:
                        f.result()
                    except Exception:
                        pass

            self._enqueue_log(f"🏁 Verification finished! Total Live: {len(self.live_proxies):,}", "success")
            self.ui_queue.put(("finished", None))

        except Exception as e:
            self._enqueue_log(f"❌ Critical Engine Error: {str(e)}", "fail")
            self.ui_queue.put(("finished", None))

    def _check_single_proxy(self, proxy, target, timeout, proto_mode, total):
        if self.stop_event.is_set():
            return

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        protocols_to_try = []
        if proto_mode == "HTTP / HTTPS":
            protocols_to_try = ["http"]
        elif proto_mode == "SOCKS5":
            protocols_to_try = ["socks5h"]
        elif proto_mode == "SOCKS4":
            protocols_to_try = ["socks4"]
        else: # Auto
            protocols_to_try = ["http", "socks5h"]

        is_live = False
        elapsed_ms = 0

        for proto in protocols_to_try:
            if self.stop_event.is_set():
                return
            proxies = {
                "http": f"{proto}://{proxy}",
                "https": f"{proto}://{proxy}"
            }
            try:
                start_t = time.time()
                resp = requests.get(target, proxies=proxies, headers=headers, timeout=timeout, allow_redirects=True)
                if resp.status_code in [200, 204, 301, 302]:
                    elapsed_ms = int((time.time() - start_t) * 1000)
                    is_live = True
                    break
            except Exception:
                continue

        if is_live:
            self.live_proxies.append(proxy)
            self._enqueue_log(f"LIVE: {proxy} ({elapsed_ms}ms)", "success")
        else:
            self.dead_count += 1

        self.processed_count += 1
        self.ui_queue.put(("update_stats", (len(self.live_proxies), self.dead_count, total, self.processed_count)))

    def _save_results(self):
        out_file = self.output_path.get()
        if not out_file:
            out_file = "live_proxies.txt"
        
        try:
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(self.live_proxies))
            self._enqueue_log(f"💾 Saved {len(self.live_proxies):,} clean live proxies to {os.path.basename(out_file)}", "success")
        except Exception as e:
            self._enqueue_log(f"❌ Failed to save output file: {e}", "fail")

if __name__ == "__main__":
    app = JasusProxy()
    app.mainloop()
