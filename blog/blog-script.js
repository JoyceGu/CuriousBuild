// Minimal JavaScript for PaperMod-style blog

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    initSmoothScrolling();
    
    // Simple fade-in animation for posts
    initPostAnimations();
    
    // Handle external links
    initExternalLinks();
    
    // Initialize search functionality
    initSearch();
    
    // Initialize language switcher
    initLanguageSwitcher();
});

// Smooth scrolling for anchor links
function initSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Simple fade-in animation for posts
function initPostAnimations() {
    const posts = document.querySelectorAll('.post-item');
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Initially hide posts and add transition
    posts.forEach((post, index) => {
        post.style.opacity = '0';
        post.style.transform = 'translateY(20px)';
        post.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(post);
    });
}

// Handle external links
function initExternalLinks() {
    const externalLinks = document.querySelectorAll('a[href^="http"]');
    
    externalLinks.forEach(link => {
        // Add external link indicator
        if (!link.querySelector('svg')) {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });
}

// Simple keyboard navigation
document.addEventListener('keydown', function(e) {
    // Press 'h' to go home
    if (e.key === 'h' && !e.ctrlKey && !e.metaKey && !e.altKey) {
        const activeElement = document.activeElement;
        if (activeElement.tagName !== 'INPUT' && activeElement.tagName !== 'TEXTAREA') {
            window.location.href = '/';
        }
    }
});

// Add minimal loading animation
window.addEventListener('load', function() {
    document.body.style.opacity = '1';
});

// Set initial opacity to 0 for loading animation
document.body.style.opacity = '0';
document.body.style.transition = 'opacity 0.3s ease';

// Search functionality
function initSearch() {
    console.log('initSearch called');
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    const searchResults = document.getElementById('searchResults');
    
    console.log('Search elements:', { searchInput, searchBtn, searchResults });
    
    if (!searchInput || !searchBtn || !searchResults) {
        console.error('Search elements not found!');
        return;
    }
    
    console.log('Search functionality initialized successfully');
    
    // Article data for search
    const articles = [
        {
            title: "How to Set Up Notion and Blog Sync",
            summary: "Overview This integration system allows you to write blog posts directly in Notion and automatically sync them to your website! Fully compatible with ...",
            date: "2025-08-18",
            url: "posts/how-to-set-up-notion-and-blog-sync.html",
            content: "notion integration blog sync automatic website markdown"
        },

        {
            title: "Hello to My Little World",
            summary: "Welcome to my personal corner of the internet! This is where I'll be sharing my thoughts, discoveries, and adventures in technology, life, and everything in between.",
            date: "2024-01-18",
            url: "posts/hello-to-my-little-world.html",
            content: "personal blog welcome introduction digital garden technology life thoughts discoveries adventures"
        }
    ];
    
    let searchTimeout;
    
    // Search function
    function performSearch(query) {
        console.log('Performing search for:', query);
        if (!query.trim()) {
            hideSearchResults();
            return;
        }
        
        const results = articles.filter(article => {
            const searchText = (article.title + ' ' + article.summary + ' ' + article.content).toLowerCase();
            return searchText.includes(query.toLowerCase());
        });
        
        console.log('Search results:', results);
        displaySearchResults(results, query);
    }
    
    // Display search results
    function displaySearchResults(results, query) {
        if (results.length === 0) {
            searchResults.innerHTML = '<div class="search-no-results">No articles found matching your search.</div>';
        } else {
            const resultsHTML = results.map(article => {
                const highlightedTitle = highlightText(article.title, query);
                const highlightedSummary = highlightText(article.summary, query);
                const date = new Date(article.date).toLocaleDateString('en-US', { 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric' 
                });
                
                return `
                    <div class="search-result-item" onclick="window.location.href='${article.url}'">
                        <div class="search-result-title">${highlightedTitle}</div>
                        <div class="search-result-summary">${highlightedSummary}</div>
                        <div class="search-result-meta">${date}</div>
                    </div>
                `;
            }).join('');
            
            searchResults.innerHTML = resultsHTML;
        }
        
        searchResults.style.display = 'block';
    }
    
    // Hide search results
    function hideSearchResults() {
        searchResults.style.display = 'none';
    }
    
    // Highlight search terms
    function highlightText(text, query) {
        if (!query.trim()) return text;
        
        const regex = new RegExp(`(${escapeRegExp(query)})`, 'gi');
        return text.replace(regex, '<span class="search-highlight">$1</span>');
    }
    
    // Escape special regex characters
    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
    
    // Event listeners
    searchInput.addEventListener('input', function() {
        console.log('Search input changed:', this.value);
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            performSearch(this.value);
        }, 300);
    });
    
    searchBtn.addEventListener('click', function() {
        console.log('Search button clicked');
        performSearch(searchInput.value);
    });
    
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            performSearch(this.value);
        }
        if (e.key === 'Escape') {
            hideSearchResults();
            this.blur();
        }
    });
    
    // Hide search results when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-container')) {
            hideSearchResults();
        }
    });
}

// Language switcher functionality
function initLanguageSwitcher() {
    const langButtons = document.querySelectorAll('.lang-btn');
    const postItems = document.querySelectorAll('.post-item');
    
    // Get current language from URL parameter or default to 'English'
    const urlParams = new URLSearchParams(window.location.search);
    let currentLang = urlParams.get('lang') || 'English';
    
    // Set active button based on current language
    function setActiveButton(lang) {
        langButtons.forEach(btn => {
            if (btn.getAttribute('data-lang') === lang) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }
    
    // Filter posts by language
    function filterPostsByLanguage(lang) {
        postItems.forEach(item => {
            const postLang = item.getAttribute('data-language') || 'English';
            
            // Match language (data-language uses "Chinese" from Notion, button uses "Chinese" too)
            if (postLang === lang) {
                item.style.display = '';
                // Trigger animation
                setTimeout(() => {
                    item.style.opacity = '1';
                    item.style.transform = 'translateY(0)';
                }, 10);
            } else {
                item.style.opacity = '0';
                item.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    item.style.display = 'none';
                }, 300);
            }
        });
    }
    
    // Initialize with current language
    setActiveButton(currentLang);
    filterPostsByLanguage(currentLang);
    
    // Add click handlers to language buttons
    langButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const selectedLang = this.getAttribute('data-lang');
            currentLang = selectedLang;
            
            // Update URL without reload
            const url = new URL(window.location);
            url.searchParams.set('lang', selectedLang);
            window.history.pushState({}, '', url);
            
            // Update UI
            setActiveButton(selectedLang);
            filterPostsByLanguage(selectedLang);
        });
    });
}