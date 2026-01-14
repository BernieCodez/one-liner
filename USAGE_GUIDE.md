# Quick Start Guide - Code Saving & Settings

## Code Saving Feature

### How It Works

1. **Start Typing**
   - Simply write your code in the Monaco editor
   - After you stop typing for 2 seconds, your code is automatically saved
   - You'll see a "Saving..." indicator in the editor header
   - When complete, you'll see "✓ Saved" briefly

2. **Manual Save**
   - Click the "💾 Save" button to save immediately
   - Useful when you want to ensure your code is saved right away

3. **Viewing Saved Code**
   - Switch between challenges - your code is preserved for each challenge
   - Close and reopen your browser - your code is still there
   - Code is saved in two places:
     - Browser localStorage (instant, local to your browser)
     - Server-side files (in `saved_code/` directory)

4. **Where Code is Stored**
   - **Browser**: `localStorage` with key pattern `code_challenge_X`
   - **Server**: Files in `/saved_code/challenge_X.py`

## Settings Feature

### Opening Settings

1. Click the "⚙️ Settings" button in the top-right corner
2. A modal will appear with all available settings
3. Settings are organized into sections: Appearance, Editor Behavior, and Features

### Appearance Settings

**Color Theme**
- VS Dark (Default) - The standard dark theme
- VS Light - A light theme for daytime coding
- High Contrast - Enhanced contrast for accessibility
- High Contrast Light - Light version with high contrast

**Font Size**
- Range: 10px to 24px
- Default: 14px
- Adjust to your comfort level

### Editor Behavior Settings

**Tab Size (Indentation)**
- Range: 2 to 8 spaces
- Default: 4 spaces
- Controls how many spaces each tab/indentation level uses
- Example: Python typically uses 4 spaces

**Insert Spaces**
- Checked: Tab key inserts spaces
- Unchecked: Tab key inserts tab character
- Default: Checked (spaces)
- Recommended: Keep checked for Python (PEP 8 compliant)

**Word Wrap**
- On - Long lines wrap at viewport width
- Off - Lines extend beyond viewport (horizontal scroll)
- At Column - Wrap at a specific column number
- Bounded - Wrap at minimum of viewport or column
- Default: On

### Feature Settings

**Minimap**
- Shows a small overview of your entire code on the right side
- Useful for navigating large files
- Default: Enabled

**Line Numbers**
- On - Show line numbers on the left
- Off - Hide line numbers
- Relative - Show relative distances from current line
- Default: On

**Auto-Save**
- When enabled, code is automatically saved after 2 seconds of inactivity
- When disabled, you must use the "💾 Save" button
- Default: Enabled
- Recommended: Keep enabled

**Format On Paste**
- Automatically formats code when you paste it
- Fixes indentation and spacing
- Default: Enabled

### Applying Settings

1. Change any settings you want
2. Click "Apply Settings" button at the bottom
3. Settings take effect immediately
4. Settings are saved to:
   - localStorage (for quick access)
   - Server (`saved_code/settings.json`)

### Closing Settings

- Click the X button in the top-right of the modal
- Click outside the modal
- Press ESC key (standard modal behavior)

## Example Workflow

### First Time Setup
1. Open the application
2. Click "⚙️ Settings"
3. Choose your preferred theme (e.g., VS Dark)
4. Set font size (e.g., 16px if you want larger text)
5. Adjust tab size if needed (4 is standard for Python)
6. Click "Apply Settings"

### Working on Challenges
1. Read the challenge description
2. Start typing your solution
3. Code auto-saves every 2 seconds
4. Run your code with Ctrl/Cmd + Enter or "Run Code" button
5. Switch to another challenge - your code is saved
6. Come back later - your code is still there

### Customizing Your Experience
1. Try different themes to find what's comfortable
2. Adjust font size for readability
3. Toggle minimap if you don't need it
4. Change indentation settings to match your style

## Keyboard Shortcuts

- **Ctrl/Cmd + Enter** - Run code
- **Tab** - Insert indentation (spaces or tab based on settings)
- **Shift + Tab** - Decrease indentation
- Monaco Editor includes many built-in shortcuts (autocomplete, multi-cursor, etc.)

## Tips & Tricks

1. **Auto-Save Delay**: Code saves 2 seconds after you stop typing to avoid excessive saves
2. **Dual Storage**: Both localStorage and server storage provide backup
3. **Per-Challenge**: Each challenge's code is independent
4. **Settings Sync**: Settings apply across all challenges
5. **Visual Feedback**: Watch the save status indicator to confirm saves
6. **Persistent**: Close your browser and come back - everything is saved

## Troubleshooting

**Code Not Saving?**
- Check if auto-save is enabled in settings
- Try manual save with the "💾 Save" button
- Check browser console for errors
- Ensure server is running

**Settings Not Persisting?**
- Ensure you clicked "Apply Settings"
- Check if cookies/localStorage are enabled in your browser
- Clear browser cache and try again

**Theme Not Changing?**
- Make sure you clicked "Apply Settings"
- Try refreshing the page
- Check browser compatibility (Monaco Editor requires modern browsers)

## Technical Details

### Storage Locations

**Browser (localStorage)**
```javascript
// Code storage
localStorage.setItem('code_challenge_1', '...your code...');
localStorage.setItem('code_challenge_2', '...your code...');

// Settings storage
localStorage.setItem('editorSettings', '{...settings json...}');

// Completed challenges
localStorage.setItem('completedChallenges', '[1,2,3]');
```

**Server (files)**
```
saved_code/
├── challenge_1.py
├── challenge_2.py
├── challenge_3.py
├── ...
└── settings.json
```

### API Endpoints

- `POST /api/save-code` - Save code for a challenge
- `GET /api/load-code/<id>` - Load code for a challenge
- `POST /api/save-settings` - Save editor settings
- `GET /api/load-settings` - Load editor settings

## Advanced Usage

### Exporting Your Code

All saved code is in the `saved_code/` directory:
```bash
# View your saved code for challenge 1
cat saved_code/challenge_1.py

# Copy all your solutions
cp -r saved_code/ my_solutions_backup/
```

### Sharing Settings

Share your `saved_code/settings.json` file with others:
```bash
# Export settings
cp saved_code/settings.json my_settings.json

# Import someone else's settings
# (they can copy it to their saved_code/ directory)
```
