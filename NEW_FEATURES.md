# New Features Added

## 1. Code Saving Functionality

### Local Storage (Browser-based)
- **Automatic saving**: Your code is automatically saved to browser's localStorage every 2 seconds after you stop typing
- **Per-challenge storage**: Each challenge's code is saved separately
- **Persistent across sessions**: Your code remains saved even after closing the browser
- **Instant loading**: When you switch challenges, your previous code is automatically loaded

### Server-side Storage
- **Dual saving**: Code is saved both to localStorage and to the server
- **File-based storage**: Each challenge's code is saved as a separate Python file in the `saved_code` directory
- **Manual save option**: Click the "💾 Save" button to manually trigger a save
- **Save status indicator**: Visual feedback shows when code is being saved or has been saved

## 2. Settings Page Features

### Access Settings
- Click the "⚙️ Settings" button in the top-right corner to open the settings modal
- Settings are organized into logical sections

### Appearance Settings
- **Color Theme**: Choose from 4 themes
  - VS Dark (Default) - Dark theme similar to Visual Studio Code
  - VS Light - Light theme
  - High Contrast - High contrast dark theme for accessibility
  - High Contrast Light - High contrast light theme
- **Font Size**: Adjustable from 10px to 24px (default: 14px)

### Editor Behavior Settings
- **Tab Size (Indentation)**: Choose indentation width from 2 to 8 spaces (default: 4)
- **Insert Spaces**: Toggle between spaces and tabs for indentation
- **Word Wrap**: Control how long lines are displayed
  - On - Wrap at viewport width
  - Off - No wrapping (horizontal scroll)
  - At Column - Wrap at specific column
  - Bounded - Wrap at min(viewport, column)

### Feature Settings
- **Minimap**: Toggle the code overview minimap on the right side of the editor
- **Line Numbers**: Choose line number display
  - On - Show line numbers
  - Off - Hide line numbers
  - Relative - Show relative line numbers
- **Auto-Save**: Enable/disable automatic code saving (enabled by default)
- **Format On Paste**: Automatically format code when pasting (enabled by default)

### Settings Persistence
- **Local storage**: Settings are saved to browser localStorage
- **Server storage**: Settings are also saved to the server in `saved_code/settings.json`
- **Cross-session**: Your settings persist across browser sessions
- **Apply button**: Click "Apply Settings" to save and apply all changes

## 3. User Interface Improvements

### Save Status Indicator
- Located in the editor header
- Shows "Saving..." while saving
- Shows "✓ Saved" briefly after successful save
- Provides visual feedback for save operations

### Auto-Save Information
- Editor header shows "Auto-save enabled" text
- Auto-save triggers 2 seconds after you stop typing
- Can be disabled in settings if you prefer manual saves only

## 4. Technical Implementation

### Backend (Flask)
- New API endpoints:
  - `POST /api/save-code` - Save code for a challenge
  - `GET /api/load-code/<challenge_id>` - Load saved code
  - `POST /api/save-settings` - Save editor settings
  - `GET /api/load-settings` - Load editor settings
- Files stored in `saved_code/` directory:
  - `challenge_1.py`, `challenge_2.py`, etc. - Individual challenge code
  - `settings.json` - Editor settings

### Frontend (JavaScript)
- Auto-save timer with 2-second debounce
- Dual storage system (localStorage + server)
- Settings modal with live preview
- Monaco Editor configuration updates
- Keyboard shortcuts maintained (Ctrl/Cmd + Enter to run)

## How to Use

### Saving Code
1. Simply start typing - your code is automatically saved
2. Or click the "💾 Save" button to save immediately
3. Watch the save status indicator for confirmation
4. Switch between challenges - your code is preserved for each one

### Changing Settings
1. Click "⚙️ Settings" in the top-right corner
2. Adjust any settings you want to change
3. Click "Apply Settings" to save and apply changes
4. Settings take effect immediately
5. Close the modal by clicking outside or pressing the X button

### Viewing Saved Code
- Switch to any challenge to see your previously saved code
- If no server code exists, it falls back to localStorage
- If no saved code exists, you see the default template

## Benefits

1. **Never lose your work**: Auto-save ensures your code is always preserved
2. **Personalized experience**: Customize the editor to match your preferences
3. **Cross-device sync**: Server storage allows accessing your code from different browsers (on the same server)
4. **Improved accessibility**: High contrast themes and adjustable font sizes
5. **Better workflow**: Indentation and formatting settings match your coding style
