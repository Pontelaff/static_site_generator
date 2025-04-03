# Static Site Generator

A Python tool that converts nested Markdown documents into static HTML pages. This project was developed during the [Static Site Generator](https://www.boot.dev/courses/build-static-site-generator-python) course on [Boot.dev](https://www.boot.dev).

## ✅ Supported Markdown Elements

This tool processes valid Markdown syntax. Refer to the [Markdown Guide](https://www.markdownguide.org/basic-syntax/) for more details.

### 📌 Block Elements

- Headings
- Code Blocks
- Blockquotes
- Unordered Lists
- Ordered Lists

### ✨ Inline Elements

- **Bold Text**
- *Italic Text*
- `Code`
- [Links](#)
- [Images](#)

### ❌ Currently Unsupported

- Tables
- Nested inline formatting
- Nested blockquotes
- Nested lists
- Heading IDs
- Horizontal rules

## 📂 Project Structure

```
content/     - Directory for Markdown files to be converted into HTML
docs/        - Output directory where generated HTML files are stored
src/         - Python scripts for Markdown conversion and HTML generation
static/      - Contains static content like images and CSS
build.sh     - Script for generating HTML for GitHub Pages
main.sh      - Script for generating HTML and deploying locally
```

## 🛠️ Usage

This tool was developed using Python 3.12.3.

### 🖥️ Generate and Host Files Locally

1. Place all Markdown files into the `content/` directory.
2. Place static assets (CSS, images, etc.) in `static/`.
3. Run `./main.sh` to generate HTML files in `/docs`.
4. View your website at `http://0.0.0.0:8888/`.

### 🌍 Deploy to GitHub Pages

1. Ensure your GitHub repository is **public** (or has GitHub Premium features enabled).
2. Go to your repository **Settings → Pages**.
3. Set `Branch: main` and `Folder: /docs`, then save.
4. Update `REPO_NAME` in `build.sh` if necessary.
5. Run `./build.sh` to generate the HTML files.
6. Push the generated `/docs` folder to GitHub.
7. Your site will be available at: `https://<user_name>.github.io/<repo_name>/`.
