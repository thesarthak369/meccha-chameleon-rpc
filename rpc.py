"""
╔══════════════════════════════════════════════════════════════╗
║         MECCHA CHAMELEON — Discord Rich Presence             ║
║                                                              ║
║  Automatically shows your Meccha Chameleon status on         ║
║  Discord when you're playing the game.                       ║
║                                                              ║
║  Requirements:                                               ║
║    pip install pypresence psutil                             ║
║                                                              ║
║  Setup:                                                      ║
║    1. Go to https://discord.com/developers/applications      ║
║    2. Create a new application named "MECCHA CHAMELEON"      ║
║    3. Copy the Client ID and paste it as CLIENT_ID below     ║
║    4. Go to Rich Presence -> Art Assets and upload images:   ║
║       - "meccha_logo"   (game logo / chameleon art)         ║
║       - "hiding"        (hiding state image)                 ║
║       - "hunting"       (hunting state image)                ║
║    5. Run this script and launch the game!                   ║
╚══════════════════════════════════════════════════════════════╝
"""

import time
import psutil
import random
import logging
import subprocess
import sys
from datetime import datetime

try:
    from pypresence import Presence, InvalidID, DiscordNotFound, PipeClosed
except ImportError:
    print("❌  pypresence is not installed.")
    print("   Run:  pip install pypresence psutil")
    sys.exit(1)

# ─────────────────────────────────────────────
#  CONFIGURATION  ← Edit this section
# ─────────────────────────────────────────────

CLIENT_ID = "1521129275565019228"   # <- Paste your Discord App Client ID here

# The game's process name (do NOT change this)
GAME_PROCESS = "PenguinHotel-Win64-Shipping.exe"

# Full path to the game executable — used to auto-launch if not running
GAME_EXE_PATH = r"E:\C folder\Downloads\MECCHA.CHAMELEON-SteamRIP.com\MECCHA CHAMELEON\PenguinHotel.exe"

# How long to wait (seconds) after launching the game before connecting RPC
GAME_LAUNCH_WAIT = 5

# How often (in seconds) to refresh the presence (min 15 per Discord's rate limit)
REFRESH_INTERVAL = 20

# ─────────────────────────────────────────────
#  GAME STATE DEFINITIONS
# ─────────────────────────────────────────────

# These states cycle randomly to give variety to the status display.
# Since the game has no public API we can't detect real in-game state,
# so we rotate through fun chameleon-themed messages.

GAME_STATES = [
    {
        "details": "🦎 Playing MECCHA CHAMELEON",
        "state":   "Blending into the environment...",
        "large_image": "meccha_logo",
        "large_text":  "MECCHA CHAMELEON",
        "small_image": "hiding",
        "small_text":  "Hiding Mode",
    },
    {
        "details": "🦎 Playing MECCHA CHAMELEON",
        "state":   "Hunting down the chameleons!",
        "large_image": "meccha_logo",
        "large_text":  "MECCHA CHAMELEON",
        "small_image": "hunting",
        "small_text":  "Hunter Mode",
    },
    {
        "details": "🦎 Playing MECCHA CHAMELEON",
        "state":   "Perfectly camouflaged 🎨",
        "large_image": "meccha_logo",
        "large_text":  "MECCHA CHAMELEON",
        "small_image": "hiding",
        "small_text":  "Camouflage Expert",
    },
    {
        "details": "🦎 Playing MECCHA CHAMELEON",
        "state":   "In a match — can you spot me?",
        "large_image": "meccha_logo",
        "large_text":  "MECCHA CHAMELEON",
        "small_image": "hunting",
        "small_text":  "In Match",
    },
    {
        "details": "🦎 Playing MECCHA CHAMELEON",
        "state":   "Waiting in lobby...",
        "large_image": "meccha_logo",
        "large_text":  "MECCHA CHAMELEON",
        "small_image": None,
        "small_text":  None,
    },
    {
        "details": "🦎 Playing MECCHA CHAMELEON",
        "state":   "Color-matching like a pro 🌈",
        "large_image": "meccha_logo",
        "large_text":  "MECCHA CHAMELEON",
        "small_image": "hiding",
        "small_text":  "Master of Disguise",
    },
]

# ─────────────────────────────────────────────
#  LOGGING SETUP
# ─────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("meccha-rpc")

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────

def is_game_running() -> bool:
    """Return True if MECCHA CHAMELEON is running."""
    try:
        for proc in psutil.process_iter(["name"]):
            if proc.info["name"] and GAME_PROCESS.lower() in proc.info["name"].lower():
                return True
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
    return False


def launch_game_if_needed():
    """Launch the game if it's not already running."""
    if is_game_running():
        log.info("Game is already running.")
        return

    import os
    if not os.path.exists(GAME_EXE_PATH):
        log.warning(f"Game exe not found at: {GAME_EXE_PATH}")
        log.warning("Update GAME_EXE_PATH in rpc.py to match your install location.")
        return

    log.info("Game is not running. Launching MECCHA CHAMELEON...")
    subprocess.Popen([GAME_EXE_PATH], cwd=str(os.path.dirname(GAME_EXE_PATH)))
    log.info(f"Waiting {GAME_LAUNCH_WAIT}s for game to start...")
    time.sleep(GAME_LAUNCH_WAIT)
    log.info("Game launched!")


def connect_rpc() -> Presence | None:
    """Attempt to connect to Discord RPC. Returns Presence object or None."""
    if CLIENT_ID == "YOUR_CLIENT_ID_HERE":
        log.error("You haven't set your CLIENT_ID yet!")
        log.error("Edit rpc.py and replace YOUR_CLIENT_ID_HERE with your Discord App Client ID.")
        log.error("Get one at: https://discord.com/developers/applications")
        return None

    try:
        rpc = Presence(CLIENT_ID)
        rpc.connect()
        log.info("✅  Connected to Discord RPC")
        return rpc
    except DiscordNotFound:
        log.warning("Discord is not running. Will retry when Discord is detected...")
        return None
    except InvalidID:
        log.error("Invalid CLIENT_ID! Double-check your Discord application's Client ID.")
        return None
    except Exception as e:
        log.warning(f"Could not connect to Discord: {e}")
        return None


def update_presence(rpc: Presence, start_time: int, state_index: int) -> int:
    """Push a presence update. Returns the next state index."""
    state = GAME_STATES[state_index]

    kwargs = {
        "details":     state["details"],
        "state":       state["state"],
        "start":       start_time,
        "large_image": state["large_image"],
        "large_text":  state["large_text"],
    }

    # Only add small image if defined
    if state["small_image"]:
        kwargs["small_image"] = state["small_image"]
        kwargs["small_text"]  = state["small_text"]

    rpc.update(**kwargs)

    log.info(f"🎮  Updated → {state['state']}")

    # Advance to next state (wrap around)
    return (state_index + 1) % len(GAME_STATES)


# ─────────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────────

def main():
    print()
    print("╔══════════════════════════════════════════════════╗")
    print("║   🦎  MECCHA CHAMELEON — Discord RPC  🦎          ║")
    print("╚══════════════════════════════════════════════════╝")
    print()

    if CLIENT_ID == "YOUR_CLIENT_ID_HERE":
        print("⚠️  ACTION REQUIRED:")
        print("   Open rpc.py and set your CLIENT_ID.")
        print("   Get one free at: https://discord.com/developers/applications")
        print()
        input("Press Enter to exit...")
        return

    rpc: Presence | None = None
    game_was_running = False
    game_start_time: int = 0
    state_index = 0

    # Auto-launch game if not already running
    launch_game_if_needed()

    log.info(f"Watching for process: {GAME_PROCESS}")
    log.info(f"Refresh interval: {REFRESH_INTERVAL}s")
    log.info("Waiting for MECCHA CHAMELEON to launch...")
    print()

    while True:
        try:
            game_running = is_game_running()

            # ── Game just launched ──────────────────────────
            if game_running and not game_was_running:
                log.info("🎮  MECCHA CHAMELEON detected! Connecting to Discord...")
                game_start_time = int(datetime.now().timestamp())
                state_index = random.randint(0, len(GAME_STATES) - 1)
                rpc = connect_rpc()
                game_was_running = True

            # ── Game is running — update presence ───────────
            if game_running and rpc is not None:
                state_index = update_presence(rpc, game_start_time, state_index)

            # ── Game just closed ────────────────────────────
            elif not game_running and game_was_running:
                log.info("🔴  MECCHA CHAMELEON closed. Clearing presence...")
                if rpc:
                    try:
                        rpc.clear()
                        rpc.close()
                    except Exception:
                        pass
                rpc = None
                game_was_running = False
                log.info("Waiting for MECCHA CHAMELEON to launch again...")

            # ── Discord reconnect attempt ───────────────────
            elif game_running and rpc is None:
                log.info("Attempting to reconnect to Discord...")
                rpc = connect_rpc()

        except PipeClosed:
            log.warning("Discord pipe closed. Will attempt to reconnect...")
            rpc = None

        except KeyboardInterrupt:
            print()
            log.info("Shutting down...")
            if rpc:
                try:
                    rpc.clear()
                    rpc.close()
                except Exception:
                    pass
            print("Goodbye! 🦎")
            break

        except Exception as e:
            log.error(f"Unexpected error: {e}")
            if rpc:
                try:
                    rpc.close()
                except Exception:
                    pass
            rpc = None

        time.sleep(REFRESH_INTERVAL)


if __name__ == "__main__":
    main()
