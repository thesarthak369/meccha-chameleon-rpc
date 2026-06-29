# 🦎 MECCHA CHAMELEON — Discord Rich Presence

Shows your **MECCHA CHAMELEON** session live on Discord with a custom status, elapsed play time, and rotating chameleon-themed messages.

---

## 📋 Prerequisites

- **Python 3.10+** — [Download here](https://www.python.org/downloads/)
- **Discord** running on your PC
- A **Discord Developer Application** (free, 2 minutes to set up)

---

## ⚙️ One-Time Setup

### Step 1 — Create a Discord Application

1. Go to [https://discord.com/developers/applications](https://discord.com/developers/applications)
2. Click **"New Application"** → name it **`MECCHA CHAMELEON`**
3. Copy the **Application ID** (also called Client ID) shown on the General Information page

### Step 2 — Add Art Assets *(optional but recommended)*

1. In your Discord application, go to **Rich Presence → Art Assets**
2. Upload images and use these exact key names:

| Key name       | What it shows             |
|----------------|---------------------------|
| `meccha_logo`  | Main large image (game logo/chameleon) |
| `hiding`       | Small icon for "hiding" state |
| `hunting`      | Small icon for "hunting" state |

> You can use any image you like. Screenshot the game or grab art from the Steam store page.

### Step 3 — Configure the script

Open `rpc.py` and find line 45:

```python
CLIENT_ID = "YOUR_CLIENT_ID_HERE"
```

Replace `YOUR_CLIENT_ID_HERE` with the Client ID you copied in Step 1.

### Step 4 — Install dependencies

Open a terminal in this folder and run:

```bash
pip install pypresence psutil
```

Or just **double-click `start_rpc.bat`** — it installs everything automatically.

---

## 🚀 Running

**Option A — Double-click:**
```
start_rpc.bat
```

**Option B — Terminal:**
```bash
python rpc.py
```

Then just **launch MECCHA CHAMELEON** normally. The RPC will detect it and update your Discord status automatically!

---

## 🎮 What It Shows on Discord

```
Playing MECCHA CHAMELEON
🦎 Playing MECCHA CHAMELEON
Blending into the environment...
▶ 00:42:15 elapsed
```

The status **cycles through** fun messages every 20 seconds:
- *Blending into the environment...*
- *Hunting down the chameleons!*
- *Perfectly camouflaged 🎨*
- *In a match — can you spot me?*
- *Color-matching like a pro 🌈*
- and more!

---

## 🔧 Customization

Edit `rpc.py` to customize:

| Variable | What it does |
|---|---|
| `CLIENT_ID` | Your Discord App ID |
| `REFRESH_INTERVAL` | Seconds between updates (min 15) |
| `GAME_STATES` | The rotating status messages |

---

## ❓ Troubleshooting

| Problem | Solution |
|---|---|
| "Discord not running" | Open Discord before running the script |
| Images not showing | Make sure asset key names match exactly in the Developer Portal |
| Script crashes | Make sure `pypresence` and `psutil` are installed |
| No status shown | Ensure Discord → Settings → Activity Privacy → "Display current activity" is ON |
