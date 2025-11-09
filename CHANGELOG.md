# Changelog - Transfer Scheduling Data + FSRS Enhancement

## Version 1.1 - FSRS Support + Bug Fix

### Fixed
- **CRITICAL BUG FIX**: Card attributes were not being transferred correctly
  - Issue: `mw.col.update_card()` was called BEFORE the card ID swap
  - Result: All scheduling data was written to the wrong card ID
  - Fix: Now all attributes are transferred via SQL AFTER the ID swap
  - This ensures review history, scheduling data, and FSRS data all transfer correctly

### Added
- **FSRS Data Transfer**: Now transfers FSRS memory state (stability, difficulty, retrievability)
  - Adds `data` field to SQL UPDATE statement
  - Controlled by new config option: `"Transfer FSRS data": "Yes"`
  - Preserves FSRS learning state when moving cards between decks

### Changed
- Refactored to use SQL UPDATE for all field transfers (more reliable)
- Removed object property assignments in favor of single SQL statement
- Better logging for debugging

## How the Fix Works

### Before (Buggy):
```python
card2.due = card1.due
card2.factor = card1.factor
# ... set all properties ...
mw.col.update_card(card2)  # Saves to card2's original ID
# THEN swap IDs
mw.col.db.execute("update cards set id = ? where id = ?", cid1, cid2)
# Result: Data is on wrong card!
```

### After (Fixed):
```python
# FIRST swap the IDs
mw.col.db.execute("update cards set id = ? where id = ?", cid1, cid2)
# THEN update all attributes via SQL
mw.col.db.execute("UPDATE cards SET due = ?, factor = ?, ... WHERE id = ?", ..., cid1)
# Result: Data is on correct card with review history!
```

## Testing

To verify the fix worked:
1. Transfer scheduling data from old card to new card
2. Check new card's info - should now show:
   - ✅ First Review date
   - ✅ Latest Review date
   - ✅ Ease percentage
   - ✅ Average/Total Time
   - ✅ Complete review history table
   - ✅ FSRS data (if enabled): Stability, Difficulty, Retrievability
