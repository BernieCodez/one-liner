# Drag and Resize Features

I've successfully added drag-and-drop and resize functionality to all the "mini windows" in your Python Coding Challenges application!

## ✨ New Features

### 1. **Draggable Settings Modal**
- Click and hold the **Settings Modal header** (⚙️ Editor Settings)
- Drag it anywhere on the screen
- The modal automatically centers when first opened
- Position is maintained while the modal stays open
- Cursor changes to indicate draggability

### 2. **Resizable Left/Right Panels**
- A **blue vertical divider** now separates the challenge description (left) and editor (right)
- Hover over the divider to see the resize cursor
- Click and drag to adjust panel widths
- Panel widths are constrained between 20% and 80%
- **Positions are saved** to localStorage and restored on page reload

### 3. **Resizable Console Output**
- A **blue horizontal bar** appears at the top of the console output
- Hover over it to see the resize cursor
- Drag up/down to resize the console height
- Console height is constrained between 100px and 600px
- **Height is saved** to localStorage and restored on page reload

### 4. **Visual Feedback**
- Dividers turn lighter blue on hover
- Active dragging shows a darker blue color
- Smooth transitions and cursor changes
- All resize handles use VS Code's signature blue (#007acc)

## 🎯 Usage Tips

1. **Reset to Default**: Clear your browser's localStorage to reset all panel positions to defaults
2. **Settings Modal**: The modal can be resized by clicking and dragging its bottom-right corner
3. **Optimal Layout**: Find your preferred layout and it will be remembered across sessions
4. **Keyboard Shortcut**: The existing Ctrl/Cmd + Enter shortcut to run code still works

## 🔧 Technical Details

- All drag/resize functionality is implemented in vanilla JavaScript
- No external libraries required
- Smooth animations with CSS transitions
- Responsive design maintained
- State persistence using localStorage

Enjoy your customizable coding environment! 🚀
