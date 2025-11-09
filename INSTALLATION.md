# Installation Instructions - FSRS-Enhanced Transfer Scheduling Data Addon

## What's New in This Version?

This modified version now transfers **FSRS (Free Spaced Repetition Scheduler) data** in addition to regular scheduling data, including:

- ✅ **FSRS Memory State**: Stability, Difficulty, and Desired Retention
- ✅ **Review History**: Complete revlog (already supported in original)
- ✅ **All Standard Scheduling Data**: Due dates, intervals, lapses, etc.

## Installation Methods

### Method 1: Manual Installation (Recommended for Development)

1. **Locate your Anki addons folder**:
   - Open Anki
   - Go to `Tools` → `Add-ons`
   - Click `View Files` button
   - This opens your addons folder (usually `C:\Users\YourName\AppData\Roaming\Anki2\addons21\`)

2. **Create a new addon folder**:
   ```
   Create a new folder named: "transfer_scheduling_fsrs" (or any name you prefer)
   ```

3. **Copy the files**:
   - Copy these files from the repo into your new addon folder:
     - `__init__.py`
     - `config.json`
     - `manifest.json`
     - `meta.json`

4. **Restart Anki**

5. **Verify installation**:
   - Open Anki Browser (Browse button)
   - Go to `Cards` menu
   - You should see:
     - `Scheduling data : Transfer from` (Ctrl+Alt+C)
     - `Scheduling data : Transfer to` (Ctrl+Alt+V)

### Method 2: Create .ankiaddon Package

1. **Navigate to the addon directory**:
   ```bash
   cd "C:\Users\Jonathan\Documents\repos\QuestLang\anki-add-on-transfer-scheduling-data"
   ```

2. **Create a ZIP file** containing these files:
   - `__init__.py`
   - `config.json`
   - `manifest.json`
   - `meta.json`

3. **Rename the ZIP file** from `.zip` to `.ankiaddon`

4. **Double-click the .ankiaddon file** to install it in Anki

## Usage

### Step 1: Copy Scheduling Data (Ctrl+Alt+C)
1. Open Anki Browser
2. Switch to **Card mode** (not Note mode) - click the toggle at top
3. Select the OLD card (the one with the review history you want to keep)
4. Press `Ctrl+Alt+C` or go to `Cards` → `Scheduling data : Transfer from`
5. You'll see a tooltip: "Data transferred from [card name]"

### Step 2: Paste Scheduling Data (Ctrl+Alt+V)
1. Still in Card mode
2. Select the NEW card (the one from your new deck with updated GUID)
3. Press `Ctrl+Alt+V` or go to `Cards` → `Scheduling data : Transfer to`
4. You'll see: "Data transferred from [old card] to [new card]"

### What Gets Transferred?

✅ **Basic Scheduling**:
- Due date
- Interval (ivl)
- Ease factor
- Queue type
- Card type
- Number of reviews (reps)
- Number of lapses
- Flags

✅ **FSRS Data** (NEW!):
- Stability
- Difficulty
- Desired retention
- Memory state

✅ **Review History**:
- Complete revlog (all past reviews with timestamps, buttons pressed, intervals)

### Configuration

Access configuration: `Tools` → `Add-ons` → Select addon → `Config`

```json
{
  "Delete old card" : "No",        // Auto-delete old card after transfer
  "Change deck" : "No",            // Also transfer deck assignment
  "Transfer FSRS data" : "Yes",    // Transfer FSRS memory state (NEW!)
  "Shortcut : Copy" : "Ctrl+Alt+C",
  "Shortcut : Paste" : "Ctrl+Alt+V"
}
```

## How It Works

### Review History Transfer (Automatic)
The addon uses a clever technique:
1. It swaps the card IDs between the old and new card
2. This automatically transfers all `revlog` entries (review history) to the new card
3. The old card gets a new ID, freeing its history

### FSRS Data Transfer (New Feature)
- Reads the `data` field from the old card (contains FSRS state as JSON/protobuf)
- Copies it to the new card
- Preserves stability, difficulty, and other FSRS parameters

## Troubleshooting

### "Please toggle the card mode instead of the note mode"
- Solution: Click the toggle at the top of the browser to switch from Notes to Cards view

### FSRS data not transferring?
- Check if FSRS is enabled in Anki: `Tools` → `Preferences` → `Scheduling` → FSRS
- Check config: Make sure `"Transfer FSRS data" : "Yes"`
- Check console output (Tools → Add-ons → Select addon → "View Files" → restart Anki with console visible)

### Old card still appears after transfer
- This is normal if `"Delete old card" : "No"` in config
- You can safely delete it manually after verifying the transfer worked

## Use Case: Fixing Duplicate Cards from New GUIDs

If you've regenerated your Anki deck with new GUIDs (to fix the QuestTitle issue):

1. Import the new deck → This creates new cards with correct GUIDs
2. For each pair of old/new duplicate cards:
   - Copy from OLD card (Ctrl+Alt+C) - has your review history
   - Paste to NEW card (Ctrl+Alt+V) - has the correct GUID
3. Delete the old cards (or set `"Delete old card" : "Yes"` to do it automatically)
4. Result: Cards with correct GUIDs AND your complete review history!

## Credits

- **Original Author**: Samuel Allain
- **FSRS Enhancement**: Added FSRS data transfer support
- **License**: GNU GPL v3
- **Original Repository**: https://gitlab.com/S.Allain/anki-add-on-transfer-scheduling-data
