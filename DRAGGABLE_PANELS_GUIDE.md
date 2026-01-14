# 🎯 Draggable Panel System - Chrome-Style Layout

Your Python Coding Challenges app now has a **Chrome-like tab dragging system**! Rearrange the three main panels (Description, Editor, Console) into any layout you want.

## 🚀 Quick Start

The app features three main draggable panels:
- **📋 Problem Description** - Challenge details and requirements
- **✏️ Python Editor** - Monaco-powered code editor
- **🖥️ Console Output** - Test results and output

## 🎨 How to Rearrange Panels

### Drag Any Panel Header
1. Click and hold on any panel's header bar (the colored bar with the panel name)
2. Drag it around the screen
3. Watch for the **blue drop indicator** showing where the panel will land
4. Release to place the panel

### Drop Zones

When dragging, move your mouse to different areas of another panel to see different drop positions:

- **Left Edge** (left 1/3): Place panel to the LEFT of target
- **Right Edge** (right 1/3): Place panel to the RIGHT of target  
- **Top Edge** (top 1/3): Place panel ABOVE target
- **Bottom Edge** (bottom 1/3): Place panel BELOW target
- **Center**: SWAP positions with target panel

The blue indicator line/box shows exactly where your panel will go!

## 🔧 Layout Preset Buttons

Click the quick layout buttons in the header for instant arrangements:

### ⬌ Side by Side
- Description on left (50%)
- Editor and Console stacked on right (50%)
- Classic split view

### ☰ Stacked
- All three panels stacked vertically
- Equal focus on all components
- Good for ultrawide monitors

### ||| Three Column
- Three panels side by side
- Maximum workspace
- Great for large screens

### ✏️ Focus Editor
- Description on left (25%)
- **Editor in center (50%)** ← Main focus
- Console on right (25%)
- Perfect for coding

## 💾 Automatic Saving

Your custom layout is **automatically saved** to browser storage! 

- Drag panels to create your perfect layout
- Close the browser
- Reopen the app → Your layout is restored! 🎉

## 🎯 Pro Tips

1. **Start with a preset** - Click a layout button, then fine-tune by dragging
2. **Visual feedback** - The panel you're dragging shows at 50% opacity
3. **Ghost indicator** - A floating label follows your cursor during drag
4. **Flex sizing** - Panels automatically adjust to fill available space
5. **Editor refresh** - Monaco editor automatically resizes when layout changes

## 🔄 Reset to Default

To reset to the default layout:
1. Open browser DevTools (F12)
2. Go to Console
3. Run: `localStorage.removeItem('panelLayout')`
4. Refresh the page

## 🎪 Example Layouts

### For Reading Challenges
```
┌─────────────┬─────────────┐
│ Description │   Editor    │
│             ├─────────────┤
│             │   Console   │
└─────────────┴─────────────┘
```

### For Coding Focus
```
┌────┬────────────┬────────┐
│Desc│   Editor   │Console │
│    │            │        │
└────┴────────────┴────────┘
```

### For Testing
```
┌─────────────────────────┐
│      Description        │
├─────────────────────────┤
│        Editor           │
├─────────────────────────┤
│        Console          │
└─────────────────────────┘
```

## 🛠️ Technical Notes

- **Vanilla JavaScript** - No external drag-drop libraries
- **Flexible grid system** - Supports rows, columns, and nested layouts
- **Monaco integration** - Editor automatically relayouts on position change
- **LocalStorage persistence** - Layout saved as JSON structure
- **Responsive design** - Works on all screen sizes

## ⌨️ Keyboard Shortcuts (Still Work!)

- **Ctrl/Cmd + Enter** - Run code
- All Monaco editor shortcuts (Ctrl+F, Ctrl+H, etc.)

---

**Enjoy your fully customizable coding workspace!** 🎨✨

*Drag, drop, and code your way! The panels are your canvas.*
