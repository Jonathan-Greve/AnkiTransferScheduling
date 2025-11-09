# Anki Add-on: Transfer Scheduling Data + FSRS

**[Install from AnkiWeb](https://ankiweb.net/shared/info/21426450)**

Transfer scheduling data, review history, and FSRS memory state from one card to another in Anki.

This is an enhanced fork of Samuel Allain's [original addon](https://gitlab.com/S.Allain/anki-add-on-transfer-scheduling-data), with added FSRS support.

## Features

### Core Functionality (Original)
- Transfer scheduling data between cards (due dates, intervals, ease, etc.)
- Transfer complete review history (revlog entries)
- Useful for merging duplicate cards or migrating between note types
- Keyboard shortcuts: `Ctrl+Alt+C` (copy) and `Ctrl+Alt+V` (paste)

### New in This Version (2025)
✅ **FSRS Support** - Transfers FSRS memory state:
- Stability (expected memory lifetime)
- Difficulty (0-100% scale)
- Desired retention
- Decay factor
- Last review time

## Installation

### From AnkiWeb (Recommended)

1. In Anki, go to `Tools` → `Add-ons` → `Get Add-ons`
2. Enter code: **21426450**
3. Restart Anki

### Manual Installation

1. Download or clone this repository
2. Open Anki → `Tools` → `Add-ons` → `View Files`
3. Create a new folder (e.g., `transfer_scheduling_fsrs`)
4. Copy these files into the folder:
   - `__init__.py`
   - `config.json`
   - `manifest.json`
   - `meta.json`
5. Restart Anki

## Usage

### Basic Transfer

1. Open Anki Browser (Browse button)
2. **Important**: Switch to **Card mode** (not Note mode) - toggle at the top
3. Select the **OLD card** (has review history you want to keep)
4. Press `Ctrl+Alt+C` or go to `Cards` → `Scheduling data : Transfer from`
5. Select the **NEW card** (will receive the data)
6. Press `Ctrl+Alt+V` or go to `Cards` → `Scheduling data : Transfer to`
7. Verify the transfer in the card's Info tab

### What Gets Transferred?

✅ **Basic Scheduling**:
- Due date
- Interval (ivl)
- Ease factor
- Queue type & card type
- Number of reviews (reps)
- Number of lapses
- Card flags

✅ **FSRS Data** (NEW!):
- Stability
- Difficulty
- Desired retention
- Decay factor
- Memory state

✅ **Review History**:
- Complete revlog (all past reviews)
- Timestamps
- Button presses (ease ratings)
- Intervals at time of review
- Review types (learning, review, relearning)

### Configuration

Access via `Tools` → `Add-ons` → Select addon → `Config`:

```json
{
  "Delete old card" : "No",        // Auto-delete source card after transfer
  "Change deck" : "No",            // Also transfer deck assignment
  "Transfer FSRS data" : "Yes",    // Transfer FSRS memory state (NEW!)
  "Shortcut : Copy" : "Ctrl+Alt+C",
  "Shortcut : Paste" : "Ctrl+Alt+V"
}
```

## Use Case: Fixing Duplicate Cards

If you've regenerated your Anki deck with new GUIDs (e.g., to fix inconsistent card metadata):

1. Import the new deck → Creates new cards with correct GUIDs
2. For each pair of old/new duplicate cards:
   - Copy from OLD card (`Ctrl+Alt+C`) - has your review history
   - Paste to NEW card (`Ctrl+Alt+V`) - has the correct GUID
3. Delete old cards (or set `"Delete old card": "Yes"` to auto-delete)
4. Result: Cards with correct GUIDs AND complete review history!

## Credits

- **Original Author**: [Samuel Allain](https://gitlab.com/S.Allain) (2020)
- **FSRS Enhancements**: Jonathan Greve (2025)
- **License**: GNU GPL v3

## License

GNU General Public License v3.0 or later

See [LICENSE](LICENSE) for full text.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

## Links

- **Original Addon**: https://gitlab.com/S.Allain/anki-add-on-transfer-scheduling-data
- **Anki Manual**: https://docs.ankiweb.net/
- **FSRS Documentation**: https://github.com/open-spaced-repetition/fsrs4anki

**[Install from AnkiWeb](https://ankiweb.net/shared/info/21426450)**
