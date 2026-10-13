// 站点双语支持（English / 中文）
// 用法：给元素加 data-i18n="key"（替换文本）、data-i18n-placeholder / data-i18n-title（替换属性），
// 放一个 data-lang-toggle 容器放切换按钮（没有的话按钮固定在右上角）。
// 语言优先级：URL ?lang= → 上次选择（localStorage）→ 浏览器语言。
(function () {
    const STORAGE_KEY = 'cb-lang';
    const SUPPORTED = ['en', 'zh'];

    const messages = {
        en: {
            'home.title': "Joyce's Playground",
            'home.hint': 'Hover over the fruits on the tree and click to visit websites created by Joyce',

            'nav.site': "Joyce's Playground",
            'nav.backToPlayground': "Back to Joyce's Playground",
            'nav.home': 'Home',
            'nav.archives': 'Archives',
            'nav.tags': 'Tags',

            'blog.pageTitle': "Joyce's Blog",
            'blog.greeting': 'Hi there 👋',
            'blog.welcome': 'Welcome to my digital garden!',
            'blog.subscribe': 'Stay updated with my latest thoughts',
            'blog.or': 'or',
            'blog.rss': 'RSS Feed',
            'blog.rssTitle': 'Subscribe via RSS',
            'blog.searchPlaceholder': 'Search articles...',
            'blog.noResults': 'No articles found matching your search.',
            'blog.onlyIn.zh': '中文',
            'blog.onlyIn.en': 'EN',

            'modal.title': 'Stay in the loop! 📬',
            'modal.desc': 'Get notified when I publish new articles about technology, growth, and life insights.',
            'modal.emailPlaceholder': 'Enter your email address',
            'modal.submit': 'Subscribe',
            'modal.privacy': '📝 Your email will only be used for blog updates. No spam, unsubscribe anytime.',
            'modal.preferRss': 'Prefer RSS?',
            'modal.rssLink': 'Subscribe via RSS feed',
            'msg.invalidEmail': 'Please enter a valid email address.',
            'msg.already': 'This email is already subscribed! 🎉',
            'msg.success': '🎉 Successfully subscribed! Thank you for joining my digital garden.',
            'msg.error': 'Something went wrong. Please try again.',

            'post.minutes': '{n} min',
            'post.backToBlog': '← Back to Blog',
            'post.next': 'Next Article →',
            'post.share': 'Share this article:',
            'post.copyLink': 'Copy Link',
            'post.copied': 'Link copied to clipboard!',
            'post.aiTranslated': 'This version was translated with AI from the original article.',

            'toggle.label': '中文',
            'toggle.title': '切换到中文',
        },
        zh: {
            'home.title': 'Joyce 的游乐场',
            'home.hint': '把鼠标悬停在树上的果实上，点击即可访问 Joyce 做的网站',

            'nav.site': 'Joyce 的游乐场',
            'nav.backToPlayground': '返回 Joyce 的游乐场',
            'nav.home': '首页',
            'nav.archives': '归档',
            'nav.tags': '标签',

            'blog.pageTitle': 'Joyce 的博客',
            'blog.greeting': '你好呀 👋',
            'blog.welcome': '欢迎来到我的数字花园！',
            'blog.subscribe': '订阅我的最新文章',
            'blog.or': '或',
            'blog.rss': 'RSS 订阅',
            'blog.rssTitle': '通过 RSS 订阅',
            'blog.searchPlaceholder': '搜索文章…',
            'blog.noResults': '没有找到相关文章。',
            'blog.onlyIn.zh': '中文',
            'blog.onlyIn.en': 'EN',

            'modal.title': '订阅更新 📬',
            'modal.desc': '有关于技术、增长和生活感悟的新文章时，第一时间通知你。',
            'modal.emailPlaceholder': '输入你的邮箱地址',
            'modal.submit': '订阅',
            'modal.privacy': '📝 邮箱只用于博客更新通知，不会发垃圾邮件，随时可以退订。',
            'modal.preferRss': '更喜欢 RSS？',
            'modal.rssLink': '通过 RSS 订阅',
            'msg.invalidEmail': '请输入有效的邮箱地址。',
            'msg.already': '这个邮箱已经订阅过啦！🎉',
            'msg.success': '🎉 订阅成功！欢迎来到我的数字花园。',
            'msg.error': '出了点问题，请再试一次。',

            'post.minutes': '{n} 分钟',
            'post.backToBlog': '← 返回博客',
            'post.next': '下一篇 →',
            'post.share': '分享这篇文章：',
            'post.copyLink': '复制链接',
            'post.copied': '链接已复制！',
            'post.aiTranslated': '本文由 AI 根据原文翻译。',

            'toggle.label': 'EN',
            'toggle.title': 'Switch to English',
        },
    };

    function readStored() {
        try {
            return localStorage.getItem(STORAGE_KEY);
        } catch (e) {
            return null;
        }
    }

    function writeStored(lang) {
        try {
            localStorage.setItem(STORAGE_KEY, lang);
        } catch (e) {
            // 隐私模式等情况下忽略
        }
    }

    function detectLang() {
        const fromUrl = new URLSearchParams(window.location.search).get('lang');
        if (SUPPORTED.includes(fromUrl)) {
            writeStored(fromUrl);
            return fromUrl;
        }
        const stored = readStored();
        if (SUPPORTED.includes(stored)) return stored;
        const browser = (navigator.language || '').toLowerCase();
        return browser.startsWith('zh') ? 'zh' : 'en';
    }

    let currentLang = detectLang();

    function t(key, vars) {
        let text = (messages[currentLang] && messages[currentLang][key]) || messages.en[key] || key;
        if (vars) {
            Object.keys(vars).forEach(name => {
                text = text.replace(`{${name}}`, vars[name]);
            });
        }
        return text;
    }

    function formatDate(isoDate) {
        const date = new Date(`${isoDate}T00:00:00`);
        if (isNaN(date)) return isoDate;
        return date.toLocaleDateString(currentLang === 'zh' ? 'zh-CN' : 'en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
        });
    }

    function applyTranslations(root) {
        root = root || document;
        root.querySelectorAll('[data-i18n]').forEach(el => {
            el.textContent = t(el.dataset.i18n);
        });
        root.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            el.placeholder = t(el.dataset.i18nPlaceholder);
        });
        root.querySelectorAll('[data-i18n-title]').forEach(el => {
            el.title = t(el.dataset.i18nTitle);
        });
        root.querySelectorAll('time[datetime][data-i18n-date]').forEach(el => {
            el.textContent = formatDate(el.getAttribute('datetime'));
        });
        root.querySelectorAll('[data-minutes]').forEach(el => {
            el.textContent = t('post.minutes', { n: el.dataset.minutes });
        });
    }

    // 文章页：如果有另一种语言的版本（<link rel="alternate" hreflang>），切换语言时直接跳过去
    function alternateUrl(lang) {
        const link = document.querySelector(`link[rel="alternate"][hreflang="${lang}"]`);
        return link ? link.getAttribute('href') : null;
    }

    function setLang(lang) {
        if (!SUPPORTED.includes(lang)) return;
        writeStored(lang);
        const pageLang = document.documentElement.dataset.contentLang;
        const alt = alternateUrl(lang);
        if (pageLang && pageLang !== lang && alt) {
            window.location.href = alt;
            return;
        }
        currentLang = lang;
        render();
    }

    function render() {
        if (!document.documentElement.dataset.contentLang) {
            document.documentElement.lang = currentLang === 'zh' ? 'zh-CN' : 'en';
        }
        document.documentElement.dataset.uiLang = currentLang;
        if (document.body && document.body.dataset.i18nTitleKey) {
            document.title = t(document.body.dataset.i18nTitleKey);
        }
        applyTranslations();
        document.querySelectorAll('.lang-toggle').forEach(btn => {
            btn.textContent = t('toggle.label');
            btn.title = t('toggle.title');
            btn.setAttribute('aria-label', t('toggle.title'));
        });
        document.dispatchEvent(new CustomEvent('langchange', { detail: { lang: currentLang } }));
    }

    function injectStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .lang-toggle {
                font: inherit;
                font-size: 14px;
                font-weight: 500;
                padding: 4px 12px;
                border: 1px solid currentColor;
                border-radius: 999px;
                background: transparent;
                color: inherit;
                cursor: pointer;
                opacity: 0.75;
                transition: opacity 0.2s ease;
            }
            .lang-toggle:hover, .lang-toggle:focus-visible { opacity: 1; }
            .lang-toggle-floating {
                position: fixed;
                top: 16px;
                right: 16px;
                z-index: 1000;
                background: rgba(255, 255, 255, 0.85);
                color: #333;
            }
        `;
        document.head.appendChild(style);
    }

    function mountToggle() {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'lang-toggle';
        btn.addEventListener('click', () => setLang(currentLang === 'zh' ? 'en' : 'zh'));
        const slot = document.querySelector('[data-lang-toggle]');
        if (slot) {
            slot.appendChild(btn);
        } else {
            btn.classList.add('lang-toggle-floating');
            document.body.appendChild(btn);
        }
    }

    window.I18n = {
        t,
        formatDate,
        setLang,
        apply: applyTranslations,
        get lang() {
            return currentLang;
        },
    };

    document.addEventListener('DOMContentLoaded', () => {
        injectStyles();
        mountToggle();
        render();
    });
})();
