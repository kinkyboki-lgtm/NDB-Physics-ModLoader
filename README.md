# 🌩️ Nuclear Design Bureau - Custom Physics Mod Loader

This is the first ever mod loader for *Nuclear Design Bureau*. It bypasses the game's 700MB Electron `.asar` archive and directly injects custom physics variables into the WebGPU `simulationWorker` thread.

## 🏆 Credits
- **z.ap** - Lead Reverse-Engineer & Modder
- **boki** - Co-Developer & Tester

## 🚀 What it does
- Extracts the game's source code automatically regardless of your Steam installation drive.
- Patches minified JavaScript compilation hiccups.
- Replaces the standard `PBX-9501` High Explosive with a **2x Strength Super Green HE**.
- Uses an efficient "Zero-Pack" method to safely run the unpacked code instantly.

## 🛠️ How to use it
1. Make sure you have [Python](https://python.org) and [Node.js](https://nodejs.org) installed.
2. Download `mod.py` and place it anywhere on your computer (if auto-detection fails, drop it directly into the game's main installation directory).
3. Open a terminal, navigate to the folder containing the file, and run:
   ```bash
   python mod.py
   ```
4. Launch the game! Look for the bright green PBX-9501 in your materials list.

## 🔄 How to restore the vanilla game
Because this script utilizes the "Zero-Pack" folder deployment method, removing your modifications is incredibly straightforward:
1. Open your **Steam Library**.
2. Right-click *Nuclear Design Bureau* -> **Properties** -> **Installed Files**.
3. Click **Verify integrity of game files**. 
4. Steam will wipe the mod directories and restore the clean files in seconds.

## 💥 How to make your own mods
Open `mod.py` and look for the `new_pbx` variable block. You can change the density, detonation velocity, pressure, or element color properties to whatever values you like! You can adapt the Python regex logic to target and edit other materials in the game array like `GUNPOWDER`, `URANIUM`, or `TUNGSTEN`.
