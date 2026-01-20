// Minimal JavaScript for PaperMod-style blog

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    initSmoothScrolling();
    
    // Handle external links
    initExternalLinks();
    
    // Initialize search functionality
    initSearch();
    
    // Initialize subscription functionality
    initSubscription();
    
    // Simple fade-in animation for posts
    initPostAnimations();
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
    
    // Set initial styles and observe all posts
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

// Subscription functionality
function initSubscription() {
    const subscribeBtn = document.getElementById('subscribeBtn');
    const modal = document.getElementById('subscriptionModal');
    const closeBtn = document.getElementById('closeModal');
    const subscriptionForm = document.getElementById('subscriptionForm');
    const emailInput = document.getElementById('emailInput');
    const formMessage = document.getElementById('formMessage');
    const submitBtn = subscriptionForm.querySelector('.submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoading = submitBtn.querySelector('.btn-loading');

    // Open modal
    subscribeBtn.addEventListener('click', function() {
        modal.classList.add('show');
        emailInput.focus();
        // Clear previous messages
        hideMessage();
    });

    // Close modal
    closeBtn.addEventListener('click', closeModal);
    
    // Close modal when clicking outside
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            closeModal();
        }
    });

    function closeModal() {
        modal.classList.remove('show');
        subscriptionForm.reset();
        hideMessage();
        resetSubmitButton();
    }

    // Handle form submission
    subscriptionForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = emailInput.value.trim();
        
        if (!isValidEmail(email)) {
            showMessage('Please enter a valid email address.', 'error');
            return;
        }

        // Check if already subscribed
        if (isAlreadySubscribed(email)) {
            showMessage('This email is already subscribed! 🎉', 'success');
            return;
        }

        // Show loading state
        setLoadingState(true);

        // Simulate API call delay
        setTimeout(() => {
            try {
                // Save subscription
                saveSubscription(email);
                
                // Show success message
                showMessage('🎉 Successfully subscribed! Thank you for joining my digital garden.', 'success');
                
                // Reset form after delay
                setTimeout(() => {
                    closeModal();
                }, 2000);
                
            } catch (error) {
                showMessage('Something went wrong. Please try again.', 'error');
            } finally {
                setLoadingState(false);
            }
        }, 1000);
    });

    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function isAlreadySubscribed(email) {
        const subscribers = getSubscribers();
        return subscribers.some(sub => sub.email.toLowerCase() === email.toLowerCase());
    }

    function saveSubscription(email) {
        const subscribers = getSubscribers();
        const newSubscriber = {
            email: email,
            subscribedAt: new Date().toISOString(),
            id: generateId()
        };
        
        subscribers.push(newSubscriber);
        localStorage.setItem('blogSubscribers', JSON.stringify(subscribers));
        
        console.log('New subscriber added:', newSubscriber);
    }

    function getSubscribers() {
        try {
            const stored = localStorage.getItem('blogSubscribers');
            return stored ? JSON.parse(stored) : [];
        } catch (error) {
            console.error('Error reading subscribers:', error);
            return [];
        }
    }

    function generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    function showMessage(text, type) {
        formMessage.textContent = text;
        formMessage.className = `form-message ${type}`;
    }

    function hideMessage() {
        formMessage.className = 'form-message';
        formMessage.textContent = '';
    }

    function setLoadingState(loading) {
        if (loading) {
            submitBtn.disabled = true;
            btnText.style.display = 'none';
            btnLoading.style.display = 'inline-flex';
        } else {
            submitBtn.disabled = false;
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
        }
    }

    function resetSubmitButton() {
        setLoadingState(false);
    }

    // Expose function for admin use
    window.getSubscribers = getSubscribers;
    window.exportSubscribers = function() {
        const subscribers = getSubscribers();
        const dataStr = JSON.stringify(subscribers, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `blog-subscribers-${new Date().toISOString().split('T')[0]}.json`;
        link.click();
        URL.revokeObjectURL(url);
    };
}
