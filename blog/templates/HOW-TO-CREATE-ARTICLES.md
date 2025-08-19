# How to Create New Blog Articles

## 📝 Quick Start Guide

### 1. Copy the Template
Copy `article-template.html` to create a new article:
```bash
cp blog/templates/article-template.html blog/posts/your-article-name.html
```

### 2. Replace Placeholders
Replace the following placeholders in your new article:

- `[ARTICLE_TITLE]` - Your article title
- `[ARTICLE_DATE]` - ISO date format (e.g., 2024-01-15)
- `[ARTICLE_DATE_FORMATTED]` - Human-readable date (e.g., January 15, 2024)
- `[READING_TIME]` - Estimated reading time in minutes
- `[ARTICLE_CONTENT]` - Your article content

### 3. Add Tags (Optional)
Replace the tags section with your tags:
```html
<div class="article-tags">
    <span class="tag">Technology</span>
    <span class="tag">Web Development</span>
    <span class="tag">JavaScript</span>
</div>
```

### 4. Write Your Content
Replace the content section with your article content. You can use:

#### Headings
```html
<h2>Main Section</h2>
<h3>Subsection</h3>
```

#### Paragraphs
```html
<p>Your paragraph content here...</p>
```

#### Lists
```html
<ul>
    <li>List item 1</li>
    <li>List item 2</li>
</ul>

<ol>
    <li>Numbered item 1</li>
    <li>Numbered item 2</li>
</ol>
```

#### Code Blocks
```html
<pre><code>
// Your code here
function example() {
    console.log('Hello, World!');
}
</code></pre>
```

#### Inline Code
```html
<p>Use the <code>console.log()</code> function to output text.</p>
```

#### Quotes
```html
<blockquote>
    <p>Your quote here...</p>
</blockquote>
```

#### Links
```html
<p>Check out <a href="https://example.com">this link</a>.</p>
```

#### Images
```html
<img src="path/to/your/image.jpg" alt="Description of image">
```

### 5. Update Blog Index
Add your new article to the blog index page (`blog/index.html`):

```html
<article class="post-item">
    <div class="post-content">
        <h3 class="post-title">
            <a href="posts/your-article-name.html">Your Article Title</a>
        </h3>
        <p class="post-summary">Brief summary of your article...</p>
    </div>
    <div class="post-meta">
        <time datetime="2024-01-15">January 15, 2024</time>
        <span class="reading-time">5 min</span>
        <span class="author">Joyce Gu</span>
    </div>
</article>
```

## 📁 File Structure
```
blog/
├── index.html              # Blog home page
├── blog-styles.css         # Main blog styles
├── blog-script.js          # Blog JavaScript
├── posts/                  # Your articles go here
│   ├── article-1.html
│   ├── article-2.html
│   └── ...
└── templates/              # Templates and guides
    ├── article-template.html
    ├── article-styles.css
    └── HOW-TO-CREATE-ARTICLES.md
```

## 🎨 Styling Tips

1. **Keep it simple** - The template follows PaperMod's minimalist design
2. **Use semantic HTML** - Proper heading hierarchy (h1 > h2 > h3)
3. **Add alt text** - Always include alt attributes for images
4. **Test responsiveness** - Check how your article looks on mobile devices

## 🔗 Navigation

- Articles automatically include navigation back to the blog home
- Update the "Previous/Next Article" links manually in the article footer
- Consider creating an archives page to list all articles

## 💡 Best Practices

1. **SEO-friendly titles** - Use descriptive, keyword-rich titles
2. **Meta descriptions** - Add meta descriptions for better SEO
3. **Reading time** - Estimate ~200 words per minute for reading time
4. **Consistent formatting** - Follow the same structure across articles
5. **Test links** - Ensure all internal and external links work correctly

Happy writing! 🚀
