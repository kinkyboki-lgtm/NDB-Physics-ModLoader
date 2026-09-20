import os
import subprocess
import shutil
import re
import sys

def get_game_dir():
    """Dynamically detects the game directory regardless of installation drive."""
    # 1. Check current directory first (in case user drops the script into the game folder)
    if os.path.exists("resources/app.asar") or os.path.exists("resources/app"):
        return os.getcwd()

    # 2. Check standard C: drive path
    default_path = r"C:\Program Files (x86)\Steam\steamapps\common\Nuclear Design Bureau"
    if os.path.exists(default_path):
        return default_path
    
    # 3. Look up Steam's registry key on Windows to find the base install directory
    if sys.platform == "win32":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
            steam_path = winreg.QueryValueEx(key, "SteamPath")[0]
            winreg.CloseKey(key)
            
            fallback_path = os.path.join(steam_path, "steamapps", "common", "Nuclear Design Bureau")
            if os.path.exists(fallback_path):
                return fallback_path
        except Exception:
            pass
            
    return None

print("=== NDB AUTO-MODDER (SMART ZERO-PACK) ===")

GAME_DIR = get_game_dir()
if not GAME_DIR:
    print("\n❌ ERROR: Could not automatically locate 'Nuclear Design Bureau'.")
    print("👉 FIX: Please move this 'mod.py' file directly inside your game's")
    print("   main installation folder (where the game .exe lives) and run it again.")
    sys.exit(1)

RESOURCES_DIR = os.path.join(GAME_DIR, "resources")
ASAR_FILE = os.path.join(RESOURCES_DIR, "app.asar")
UNPACKED_DIR = os.path.join(RESOURCES_DIR, "app_unpacked")
APP_DIR = os.path.join(RESOURCES_DIR, "app") 

# Step 1: Determine the state of the game
if os.path.exists(APP_DIR):
    print("Game is already unpacked! Modding existing folder instantly...")
    WORKER_FILE = os.path.join(APP_DIR, "dist", "assets", "simulationWorker-E_IlajXO.js")
elif os.path.exists(ASAR_FILE):
    print("Vanilla game detected. Extracting app.asar (this will take a few seconds)...")
    if os.path.exists(UNPACKED_DIR):
        shutil.rmtree(UNPACKED_DIR)
        
    try:
        subprocess.run('npx @electron/asar extract app.asar app_unpacked', shell=True, cwd=RESOURCES_DIR, check=True)
    except subprocess.CalledProcessError:
        print("\n❌ ERROR: Failed to extract .asar archive.")
        print("👉 FIX: Make sure Node.js is installed on your computer so 'npx' can run.")
        sys.exit(1)
    
    print("Deleting original app.asar to enable Zero-Pack mode...")
    os.remove(ASAR_FILE)
    
    print("Renaming folder to 'app'...")
    os.rename(UNPACKED_DIR, APP_DIR)
    WORKER_FILE = os.path.join(APP_DIR, "dist", "assets", "simulationWorker-E_IlajXO.js")
else:
    print("❌ ERROR: Neither app.asar nor app folder found!")
    print("Please verify game files in Steam to reset, then run the script again.")
    sys.exit(1)

# Ensure the targeted simulation worker script exists
if not os.path.exists(WORKER_FILE):
    print(f"❌ ERROR: Expected file missing: {WORKER_FILE}")
    print("The game version may have changed or updated.")
    sys.exit(1)

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
    print("⚠️ WARNING: Could not find PBX_9501 block to replace!")
else:
    print(f"Successfully replaced {replacements} material block(s).")

# Step 5: Save the modified file
print("Saving modified simulationWorker...")
with open(WORKER_FILE, 'w', encoding='utf-8') as f:
    f.write(code)

print("\n=== SUCCESS! ===")
print("Game modded successfully! Launch Nuclear Design Bureau now!")
