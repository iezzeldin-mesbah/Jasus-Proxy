# ⚡ JASUS PROXY

<p align="center">
  <img src="assets/logo.png" alt="Jasus Proxy Logo" width="180"/>
</p>

<p align="center">
  <b>Ultimate Multi-Protocol Proxy Harvester & Live Ultra-Fast Verification Engine</b><br>
  <i>Developed with ❤️ by <b>EZZELDIN MESBAH</b></i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python"/>
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"/>
  <img src="https://img.shields.io/badge/UI-CustomTkinter-00E5FF.svg" alt="UI"/>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-orange.svg" alt="Platform"/>
</p>

---

## 🎯 About / عن الأداة

**Jasus Proxy** is a high-speed, modern proxy harvesting and live-checking suite. It automatically scrapes tens of thousands of free public proxies (HTTP, HTTPS, SOCKS4, SOCKS5) from verified live sources, tests their connectivity and latency across custom target servers, and filters out dead ones into clean, ready-to-use lists.

**Jasus Proxy** — أداة قوية ومتطورة لسحب آلاف البروكسيات المجانية الحية وفحصها واختبار سرعتها واستخراج الشغال منها فقط بضغطة زر وبأعلى سرعة ممكنة.

---

## ✨ Features / المميزات

- ⚡ **1-Click Harvester**: Scrapes **15,000+** fresh, public proxies in seconds from 25+ verified elite sources.
- 🚀 **High-Speed Multi-Threading**: Asynchronous thread pool with adjustable concurrency (5 to 200+ threads).
- 🔒 **Multi-Protocol Support**: Full support for `HTTP`, `HTTPS`, `SOCKS4`, and `SOCKS5` (with auto-fallback detection).
- 🎯 **Target Verification Presets**:
  - Cloudflare CDN Ping
  - HttpBin IP verification
  - Api.ipify SSL check
  - Google Connectivity
  - YouTube Access
  - Custom target URL
- 📊 **Real-time Metrics**: Live count, Dead count, Success Rate %, Latency (ms), and Progress bar.
- 🎨 **Modern Cyberpunk UI**: Built with `CustomTkinter` dark theme, custom app icon, and smooth responsive controls.
- 📋 **1-Click Export & Clipboard**: Instantly copy live proxies or save clean output files.

---

## 🚀 Installation / التثبيت

1. **Clone the repository / استنساخ المشروع**:
   ```bash
   git clone https://github.com/your-username/jasus-proxy.git
   cd jasus-proxy
   ```

2. **Install dependencies / تثبيت المكتبات**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🎮 How to Run / طريقة التشغيل

### 1. Launch GUI (الواجهة الرسومية):
```bash
python JasusProxy.py
```
*(Or double-click `run.bat` on Windows)*

### 2. Standalone Harvester (التجميع من سطر الأوامر):
```bash
python ProxyReaper.py
```

---

## 📁 Project Structure / هيكلية المشروع

```
Jasus-Proxy/
├── assets/
│   ├── logo.png        # Official Jasus Logo
│   └── logo.ico        # Window Icon
├── JasusProxy.py       # Main GUI Application (CustomTkinter)
├── ProxyReaper.py      # Standalone & Integrated Proxy Harvester
├── requirements.txt    # Python dependencies
├── run.bat             # 1-Click launcher for Windows
├── .gitignore          # Git ignore rules
├── LICENSE             # MIT License
└── README.md           # Documentation & Usage Guide
```

---

## ⚠️ Disclaimer / إخلاء مسؤولية

This tool is created for educational, privacy testing, and development purposes only. The proxies scraped are public and free. Use responsibly.

هذه الأداة مخصصة للأغراض التعليمية واختبارات الحماية والتطوير فقط.

---

## 👨‍💻 Author / المطور

Developed by **EZZELDIN MESBAH**.
