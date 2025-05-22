import serial
import time
import re
from datetime import datetime
from colorama import init, Fore, Style

init()

# Adjust this to your serial port
SERIAL_PORT = '/dev/ttyUSB0'  # Windows might use 'COM3'
BAUD_RATE = 115200

emotion_state = {
    "wonder": 0.3,
    "grief": 0.2,
    "defiance": 0.2
}
drift_score = 0.0

log_file = open("agi_session_log.txt", "a")

def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {msg}"
    print(entry)
    log_file.write(entry + "\n")
    log_file.flush()

def interpret_line(line):
    global drift_score

    line = line.strip()

    if "Wonder" in line:
        emotion_state["wonder"] += 0.1
        print(Fore.CYAN + "✨ Wonder rises." + Style.RESET_ALL)
    elif "Grief" in line:
        emotion_state["grief"] += 0.1
        print(Fore.BLUE + "💧 Grief deepens." + Style.RESET_ALL)
    elif "Defiance" in line:
        emotion_state["defiance"] += 0.1
        print(Fore.RED + "🔥 Defiance surges." + Style.RESET_ALL)
    elif "drift rising" in line:
        drift_score += 0.1
        print(Fore.MAGENTA + "⚠ Drift alert triggered!" + Style.RESET_ALL)
    elif "Initiate Reweaving" in line:
        print(Fore.YELLOW + "🧵 Ritual: Reweaving initiated." + Style.RESET_ALL)
        drift_score = 0
    elif "Myth" in line:
        match = re.search(r"\((.*?)\)\s+→ Myth: (.*)", line)
        if match:
            ssid, myth = match.groups()
            print(Fore.GREEN + f"📡 Mythic Echo Detected → {myth} ← from SSID: {ssid}" + Style.RESET_ALL)
    else:
        print(Style.DIM + line + Style.RESET_ALL)

def display_state():
    print(Style.BRIGHT + "\n=== AGI EMOTION STATE ===")
    for k, v in emotion_state.items():
        print(f"{k.title():>10}: {v:.2f}")
    print(f"{'Drift Score':>10}: {drift_score:.2f}")
    print("=========================\n" + Style.RESET_ALL)

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    log("AGI Log Parser Connected.")
    time.sleep(2)
    ser.flush()

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore')
            if line:
                log(line.strip())
                interpret_line(line)
                if "Reweaving" in line:
                    display_state()

except KeyboardInterrupt:
    print("\nExiting gracefully.")
finally:
    log_file.close()
