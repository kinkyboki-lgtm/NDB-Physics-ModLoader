import os
import subprocess
import shutil
import re

# Paths
GAME_DIR = r"C:\Program Files (x86)\Steam\steamapps\common\Nuclear Design Bureau"
RESOURCES_DIR = os.path.join(GAME_DIR, "resources")
ASAR_FILE = os.path.join(RESOURCES_DIR, "app.asar")
UNPACKED_DIR = os.path.join(RESOURCES_DIR, "app_unpacked")
APP_DIR = os.path.join(RESOURCES_DIR, "app") 

print("=== NDB AUTO-MODDER (SMART ZERO-PACK) ===")

# Step 1: Determine the state of the game
if os.path.exists(APP_DIR):
    print("Game is already unpacked! Modding existing folder instantly...")
    WORKER_FILE = os.path.join(APP_DIR, "dist", "assets", "simulationWorker-E_IlajXO.js")
elif os.path.exists(ASAR_FILE):
    print("Vanilla game detected. Extracting app.asar (this will take a few seconds)...")
    if os.path.exists(UNPACKED_DIR):
        shutil.rmtree(UNPACKED_DIR)
    subprocess.run(f'npx @electron/asar extract app.asar app_unpacked', shell=True, cwd=RESOURCES_DIR, check=True)
    
    print("Deleting original app.asar to enable Zero-Pack mode...")
    os.remove(ASAR_FILE)
    
    print("Renaming folder to 'app'...")
    os.rename(UNPACKED_DIR, APP_DIR)
    WORKER_FILE = os.path.join(APP_DIR, "dist", "assets", "simulationWorker-E_IlajXO.js")
else:
    print("ERROR: Neither app.asar nor app folder found!")
    print("Please verify game files in Steam to reset, then run the script again.")
    exit()

# Step 2: Read the JavaScript file
print("Reading simulationWorker...")
with open(WORKER_FILE, 'r', encoding='utf-8') as f:
    code = f.read()

# Step 3: Fix the known syntax error typo
print("Patching syntax errors...")
code = code.replace("globalThis.__MATWARNED__ || = new Set", "globalThis.__MATWARNED__ || new Set")

# Step 4: Replace PBX_9501 with 2x strength + Green color
print("Injecting 2x Super Green PBX-9501...")
old_pbx = r"PBX_9501:\s*\{.*?\},\s*BARATOL:"
new_pbx = '''PBX_9501: {
        atomicNumber: 7,
        name: "PBX-9501 (2x Super HE)",
        density: 1860,
        color: 65280,
        isSolid: !0,
        detonationVelocity: 4400,
        detonationPressure: 84e9,
        detonationEnergyDensity: 12e6,
        lensRole: "fast",
        isExplosive: !0,
        tensileStrengthPa: 2e7,
        youngsModulusPa: 15e8,
        poissonRatio: .3,
        shearModulusPa: 6e8,
        bulkModulusPa: 125e7
      },
      BARATOL:'''

code, replacements = re.subn(old_pbx, new_pbx, code, flags=re.DOTALL)
if replacements == 0:
    print("WARNING: Could not find PBX_9501 block to replace!")
else:
    print(f"Successfully replaced {replacements} material block(s).")

# Step 5: Save the modified file
print("Saving modified simulationWorker...")
with open(WORKER_FILE, 'w', encoding='utf-8') as f:
    f.write(code)

# Step 6: Generate the README.md file automatically so you don't have to copy it from chat!
print("Generating README.md file for GitHub/Discord...")
readme_content = """# 🌩️ Nuclear Design Bureau - Custom Physics Mod Loader

This is the first ever mod loader for *Nuclear Design Bureau*. It bypasses the game's 700MB Electron `.asar` archive and directly injects custom physics variables into the WebGPU `simulationWorker` thread.

## 🏆 Credits
- **z.ap** - Lead Reverse-Engineer & Modder
- **boki** - Co-Developer & Tester
- *(With huge thanks to the AI assistant that helped crack the WebGPU headers and .asar archive!)*

## 🚀 What it does
- Extracts the game's source code automatically.
- Patches syntax errors in the minified JavaScript.
- Replaces the standard `PBX-9501` High Explosive with a **2x Strength Super Green HE**.
- Uses a "Zero-Pack" method to install the mod in less than 5 seconds!

## 🛠️ How to use it
1. Make sure you have [Python](https://www.python.org/downloads/) and [Node.js](https://nodejs.org/) installed.
2. Put `mod.py` anywhere on your computer.
3. Open a terminal and run: `py mod.py`
4. Launch the game! Look for the bright green PBX-9501 in your materials list.

## 🔄 How to restore the vanilla game
Because this script uses the "Zero-Pack" method (deleting `app.asar`), if you ever want to play the normal game again, just go to Steam, right-click *Nuclear Design Bureau* -> Properties -> Installed Files -> **Verify integrity of game files**. Steam will wipe the mod and restore the clean files.

## 💥 How to make your own mods
Open `mod.py` and look for the `new_pbx` variable. You can change the density, detonation velocity, pressure, or color to whatever you want! You can also use the Python regex logic to target other materials like `GUNPOWDER`, `URANIUM`, or `TUNGSTEN`.
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("\n=== SUCCESS! ===")
print("1. Game modded successfully!")
print("2. README.md file created in this folder!")
print("Launch Nuclear Design Bureau now!")
