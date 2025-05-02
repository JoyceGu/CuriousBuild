// DOM 元素
const fruitsContainer = document.getElementById('fruits-container');
const tooltip = document.getElementById('tooltip');

// 创建所有果实
function createFruits() {
    // 使用从fruits-config.js加载的fruitLinks数组
    fruitLinks.forEach(fruit => {
        // 创建果实容器，包含果实和标签
        const fruitContainer = document.createElement('div');
        fruitContainer.className = 'fruit-container';
        fruitContainer.style.position = 'absolute';
        fruitContainer.style.left = `${fruit.position.x}%`;
        fruitContainer.style.top = `${fruit.position.y}%`;
        fruitContainer.style.display = 'flex';
        fruitContainer.style.flexDirection = 'column';
        fruitContainer.style.alignItems = 'center';
        fruitContainer.style.width = '80px'; // 为标签预留空间
        fruitContainer.style.transform = 'translateX(-40px)'; // 居中对齐
        
        // 创建果实元素
        const fruitElement = document.createElement('div');
        fruitElement.id = fruit.id;
        fruitElement.className = `fruit fruit-${fruit.type}`;
        
        // 添加果实阴影和纹理
        fruitElement.style.backgroundImage = `radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.4) 0%, transparent 40%), radial-gradient(circle at 70% 70%, rgba(0, 0, 0, 0.1) 0%, transparent 40%)`;
        
        // 添加悬停效果
        fruitElement.addEventListener('mouseover', (e) => showTooltip(e, fruit.name));
        fruitElement.addEventListener('mousemove', (e) => moveTooltip(e));
        fruitElement.addEventListener('mouseout', hideTooltip);
        
        // 添加点击事件
        fruitElement.addEventListener('click', () => {
            window.open(fruit.url, '_blank');
        });
        
        // 创建标签元素
        const labelElement = document.createElement('div');
        labelElement.className = 'fruit-label';
        labelElement.textContent = fruit.shortName || fruit.name; // 使用简短名称，如果没有则使用完整名称
        labelElement.style.marginTop = '5px';
        labelElement.style.fontSize = '12px';
        labelElement.style.fontWeight = 'bold';
        labelElement.style.textAlign = 'center';
        labelElement.style.color = '#333';
        labelElement.style.textShadow = '0px 0px 3px white, 0px 0px 3px white, 0px 0px 3px white, 0px 0px 3px white';
        labelElement.style.pointerEvents = 'none'; // 防止影响果实点击
        
        // 将果实和标签添加到容器
        fruitContainer.appendChild(fruitElement);
        fruitContainer.appendChild(labelElement);
        
        // 将容器添加到页面
        fruitsContainer.appendChild(fruitContainer);
    });
}

// 显示工具提示
function showTooltip(event, text) {
    tooltip.textContent = text;
    moveTooltip(event);
    // 使用setTimeout确保先设置位置，再显示动画
    setTimeout(() => {
        tooltip.style.opacity = 1;
        tooltip.style.transform = 'translateY(0)';
    }, 5);
}

// 移动工具提示
function moveTooltip(event) {
    const x = event.clientX;
    const y = event.clientY;
    
    // 根据窗口边界调整提示位置
    const tooltipWidth = tooltip.offsetWidth;
    const tooltipHeight = tooltip.offsetHeight;
    
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;
    
    // 减少偏移量，使提示更靠近鼠标
    let tooltipX = x + 5;
    let tooltipY = y - tooltipHeight - 5; // 默认显示在鼠标上方
    
    // 防止提示框超出窗口右侧
    if (tooltipX + tooltipWidth > windowWidth) {
        tooltipX = x - tooltipWidth - 5;
    }
    
    // 防止提示框超出窗口顶部，则显示在鼠标下方
    if (tooltipY < 0) {
        tooltipY = y + 5;
    }
    
    tooltip.style.left = `${tooltipX}px`;
    tooltip.style.top = `${tooltipY}px`;
}

// 隐藏工具提示
function hideTooltip() {
    tooltip.style.opacity = 0;
    tooltip.style.transform = 'translateY(5px)';
}

// 添加果实摇晃动画
function addFruitAnimations() {
    const fruits = document.querySelectorAll('.fruit');
    
    fruits.forEach((fruit, index) => {
        // 添加轻微的随机动画以模拟风吹动果实
        const delay = index * 0.2;
        const duration = 3 + Math.random() * 2;
        
        fruit.style.animation = `sway ${duration}s ease-in-out ${delay}s infinite alternate`;
    });
    
    // 添加CSS动画规则
    const styleSheet = document.styleSheets[0];
    styleSheet.insertRule(`
        @keyframes sway {
            0% { transform: rotate(-3deg) translateY(0); }
            50% { transform: rotate(3deg) translateY(5px); }
            100% { transform: rotate(-3deg) translateY(0); }
        }
    `, styleSheet.cssRules.length);
}

// 页面加载完成后初始化
window.addEventListener('load', () => {
    createFruits();
    addFruitAnimations();
});

// 提供自定义函数供用户更新果实链接
window.updateFruitLink = function(id, newName, newUrl) {
    const fruitIndex = fruitLinks.findIndex(fruit => fruit.id === id);
    
    if (fruitIndex !== -1) {
        fruitLinks[fruitIndex].name = newName;
        fruitLinks[fruitIndex].url = newUrl;
        
        // 更新DOM中的提示文本和标签
        const fruitElement = document.getElementById(id);
        if (fruitElement) {
            fruitElement.title = newName;
            // 更新标签文本
            const labelElement = fruitElement.parentNode.querySelector('.fruit-label');
            if (labelElement) {
                labelElement.textContent = fruitLinks[fruitIndex].shortName || newName;
            }
        }
        
        console.log(`Updated fruit ${id} to: ${newName} (${newUrl})`);
        return true;
    }
    
    console.error(`Fruit with id ${id} not found`);
    return false;
};

// 添加新的果实
window.addNewFruit = function(name, url, positionX, positionY, type = 1, shortName = null) {
    const id = `fruit${fruitLinks.length + 1}`;
    
    const newFruit = {
        id,
        name,
        shortName: shortName || name,
        url,
        position: { x: positionX, y: positionY },
        type: type > 0 && type <= 5 ? type : 1
    };
    
    fruitLinks.push(newFruit);
    
    // 创建果实容器
    const fruitContainer = document.createElement('div');
    fruitContainer.className = 'fruit-container';
    fruitContainer.style.position = 'absolute';
    fruitContainer.style.left = `${newFruit.position.x}%`;
    fruitContainer.style.top = `${newFruit.position.y}%`;
    fruitContainer.style.display = 'flex';
    fruitContainer.style.flexDirection = 'column';
    fruitContainer.style.alignItems = 'center';
    fruitContainer.style.width = '80px';
    fruitContainer.style.transform = 'translateX(-40px)';
    
    // 创建果实元素
    const fruitElement = document.createElement('div');
    fruitElement.id = id;
    fruitElement.className = `fruit fruit-${newFruit.type}`;
    
    // 添加果实阴影和纹理
    fruitElement.style.backgroundImage = `radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.4) 0%, transparent 40%), radial-gradient(circle at 70% 70%, rgba(0, 0, 0, 0.1) 0%, transparent 40%)`;
    
    // 添加悬停效果
    fruitElement.addEventListener('mouseover', (e) => showTooltip(e, newFruit.name));
    fruitElement.addEventListener('mousemove', (e) => moveTooltip(e));
    fruitElement.addEventListener('mouseout', hideTooltip);
    
    // 添加点击事件
    fruitElement.addEventListener('click', () => {
        window.open(newFruit.url, '_blank');
    });
    
    // 创建标签元素
    const labelElement = document.createElement('div');
    labelElement.className = 'fruit-label';
    labelElement.textContent = newFruit.shortName;
    labelElement.style.marginTop = '5px';
    labelElement.style.fontSize = '12px';
    labelElement.style.fontWeight = 'bold';
    labelElement.style.textAlign = 'center';
    labelElement.style.color = '#333';
    labelElement.style.textShadow = '0px 0px 3px white, 0px 0px 3px white, 0px 0px 3px white, 0px 0px 3px white';
    labelElement.style.pointerEvents = 'none';
    
    // 将果实和标签添加到容器
    fruitContainer.appendChild(fruitElement);
    fruitContainer.appendChild(labelElement);
    
    // 将容器添加到页面
    fruitsContainer.appendChild(fruitContainer);
    
    console.log(`Added new fruit: ${name} (${url})`);
    return id;
}; 