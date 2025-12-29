# Clipy Website

A beautiful, terminal-themed static website for the Clipy Clipboard Manager Tool.

## 🎨 Design

- **Theme**: Vim Terminal Aesthetic
- **Style**: Single-page, clean, minimalist
- **Color Scheme**: DuoTone Dark Forest
  - Base Dark: `#2A2D2A`
  - Accent Yellow-Green: `#e7f98b`
  - Various shades of green and gray

## 📁 Files

```
website/
├── index.html      # Main HTML structure
├── styles.css      # All styling (terminal theme)
├── script.js       # Interactive JavaScript
├── script.ts       # TypeScript source (optional)
└── README.md       # This file
```

## ✨ Features

- **ASCII Art Logo**: Eye-catching "CLIPY" header
- **Terminal Commands**: Interactive command-line aesthetic
- **Smooth Animations**: Scroll-based animations and transitions
- **Video Section**: Ready-to-use demo video container
- **Download Button**: Direct link to Windows executable
- **GitHub Integration**: Link to repository
- **Keyboard Shortcuts**:
  - `Ctrl/Cmd + K`: Scroll to top
  - `Ctrl/Cmd + D`: Jump to download section
- **Responsive Design**: Works on all screen sizes
- **Console Easter Eggs**: Fun messages in browser console

## 🚀 Setup Instructions

### 1. Add Your Demo Video

Place your demo video in the website folder and update the video source in `index.html`:

```html
<video controls poster="thumbnail.jpg">
    <source src="your-video-name.mp4" type="video/mp4">
</video>
```

### 2. Add Download File

Copy your Windows executable to the `download` folder:

```
website/
└── download/
    └── clipy-setup.exe
```

Or update the download link in `index.html`:

```html
<a href="path/to/your/exe" class="btn btn-primary" download>
```

### 3. Update GitHub URL

Replace the placeholder GitHub URL in `index.html`:

```html
<a href="https://github.com/YOUR_USERNAME/clipboard-manager-tool" 
   target="_blank" class="btn btn-secondary">
```

### 4. Deploy

#### Option A: GitHub Pages
1. Push the website folder to a GitHub repository
2. Enable GitHub Pages in repository settings
3. Select the branch and folder containing your website

#### Option B: Netlify
1. Drag and drop the `website` folder to [Netlify Drop](https://app.netlify.com/drop)
2. Get instant deployment

#### Option C: Local Server
```bash
# Python 3
cd website
python -m http.server 8000

# Node.js
npx serve website

# PHP
cd website
php -S localhost:8000
```

Then open: `http://localhost:8000`

## 🎯 Customization

### Change Colors

Edit CSS variables in `styles.css`:

```css
:root {
    --base-dark: #2A2D2A;
    --uno-1: #ddf8dd;
    --duo-1: #e7f98b;
    /* ... more colors */
}
```

### Modify ASCII Art

Replace the ASCII art in `index.html` with your own:

```html
<pre class="ascii-art">
   Your ASCII art here
</pre>
```

You can generate ASCII art at: [patorjk.com/software/taag/](https://patorjk.com/software/taag/)

### Update Features

Edit the feature list in `index.html`:

```html
<ul class="feature-list">
    <li><span class="bullet">▸</span> Your feature</li>
</ul>
```

## 🛠️ Technologies Used

- Pure HTML5
- CSS3 (with animations and transitions)
- Vanilla JavaScript (compiled from TypeScript)
- No frameworks or dependencies

## 📱 Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Opera (latest)

## 📝 Notes

- The website is fully static (no backend required)
- All interactions happen client-side
- Optimized for performance
- SEO-friendly structure
- Accessible and semantic HTML

## 👨‍💻 Created By

**Rudra**

---

## 📄 License

Same as the main Clipy project.

## 🐛 Issues?

If you encounter any issues with the website, feel free to modify the HTML/CSS/JS files directly. They're well-commented and easy to understand!
