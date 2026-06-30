/* ============================================
   绿色生活馆 - 主JavaScript文件
   包含：轮播图、商品数据、购物车、搜索等功能
   作者：网络程序设计实践课程
   日期：2026年5月
   ============================================ */

// ===== 商品数据 =====
const products = [
    // 环保家居
    {
        id: 1,
        name: '竹纤维环保毛巾套装',
        desc: '天然竹纤维材质，柔软亲肤，可降解环保',
        price: 39.9,
        originalPrice: 59.9,
        image: 'https://picsum.photos/seed/eco1/400/400',
        category: 'eco',
        badge: 'hot',
        rating: 4.8,
        sales: 2568
    },
    {
        id: 2,
        name: '可降解垃圾袋100只装',
        desc: 'PLA+PBAT全降解材料，环保无污染',
        price: 29.9,
        originalPrice: 45.0,
        image: 'https://picsum.photos/seed/eco2/400/400',
        category: 'eco',
        badge: 'hot',
        rating: 4.7,
        sales: 3890
    },
    {
        id: 3,
        name: '天然藤编收纳篮',
        desc: '手工编织，自然环保，美观实用',
        price: 68.0,
        originalPrice: 88.0,
        image: 'https://picsum.photos/seed/eco3/400/400',
        category: 'eco',
        badge: 'new',
        rating: 4.9,
        sales: 1234
    },
    {
        id: 4,
        name: '环保竹制牙刷4支装',
        desc: '竹柄+软毛，可替换刷头，减少塑料浪费',
        price: 25.9,
        originalPrice: 35.9,
        image: 'https://picsum.photos/seed/eco4/400/400',
        category: 'eco',
        badge: '',
        rating: 4.6,
        sales: 4521
    },
    // 绿色厨房
    {
        id: 5,
        name: '不锈钢环保吸管套装',
        desc: '食品级304不锈钢，可重复使用，附清洁刷',
        price: 35.0,
        originalPrice: 49.0,
        image: 'https://picsum.photos/seed/kit1/400/400',
        category: 'kitchen',
        badge: 'hot',
        rating: 4.5,
        sales: 3210
    },
    {
        id: 6,
        name: '蜂蜡保鲜布3片装',
        desc: '可重复使用，替代保鲜膜，天然蜂蜡材质',
        price: 58.0,
        originalPrice: 78.0,
        image: 'https://picsum.photos/seed/kit2/400/400',
        category: 'kitchen',
        badge: 'new',
        rating: 4.7,
        sales: 1890
    },
    {
        id: 7,
        name: '硅胶折叠餐盒',
        desc: '食品级硅胶，可折叠收纳，微波炉可用',
        price: 45.0,
        originalPrice: 65.0,
        image: 'https://picsum.photos/seed/kit3/400/400',
        category: 'kitchen',
        badge: '',
        rating: 4.6,
        sales: 2156
    },
    {
        id: 8,
        name: '天然丝瓜络洗碗刷',
        desc: '天然植物纤维，去油污强，可降解',
        price: 15.9,
        originalPrice: 22.0,
        image: 'https://picsum.photos/seed/kit4/400/400',
        category: 'kitchen',
        badge: '',
        rating: 4.4,
        sales: 5678
    },
    // 个人护理
    {
        id: 9,
        name: '天然手工皂礼盒',
        desc: '植物精油配方，无添加，温和不刺激',
        price: 88.0,
        originalPrice: 128.0,
        image: 'https://picsum.photos/seed/per1/400/400',
        category: 'personal',
        badge: 'hot',
        rating: 4.9,
        sales: 1890
    },
    {
        id: 10,
        name: '竹炭洗发皂',
        desc: '天然竹炭成分，控油去屑，环保无包装',
        price: 42.0,
        originalPrice: 58.0,
        image: 'https://picsum.photos/seed/per2/400/400',
        category: 'personal',
        badge: 'new',
        rating: 4.5,
        sales: 2345
    },
    {
        id: 11,
        name: '可降解棉柔巾6包',
        desc: '100%天然棉，可降解材质，柔软亲肤',
        price: 49.9,
        originalPrice: 69.9,
        image: 'https://picsum.photos/seed/per3/400/400',
        category: 'personal',
        badge: '',
        rating: 4.7,
        sales: 6789
    },
    {
        id: 12,
        name: '天然润唇膏（蜂蜡配方）',
        desc: '有机蜂蜡+植物油，滋润保湿，无化学添加',
        price: 28.0,
        originalPrice: 38.0,
        image: 'https://picsum.photos/seed/per4/400/400',
        category: 'personal',
        badge: '',
        rating: 4.6,
        sales: 3456
    },
    // 户外出行
    {
        id: 13,
        name: '可折叠环保购物袋',
        desc: '轻便耐用，可收纳成小包，随身携带',
        price: 19.9,
        originalPrice: 29.9,
        image: 'https://picsum.photos/seed/out1/400/400',
        category: 'outdoor',
        badge: 'hot',
        rating: 4.8,
        sales: 8901
    },
    {
        id: 14,
        name: '不锈钢保温杯500ml',
        desc: '316不锈钢内胆，保温12小时，环保耐用',
        price: 128.0,
        originalPrice: 168.0,
        image: 'https://picsum.photos/seed/out2/400/400',
        category: 'outdoor',
        badge: '',
        rating: 4.9,
        sales: 4567
    },
    {
        id: 15,
        name: '天然帆布双肩包',
        desc: '有机棉帆布，简约设计，环保染色工艺',
        price: 158.0,
        originalPrice: 198.0,
        image: 'https://picsum.photos/seed/out3/400/400',
        category: 'outdoor',
        badge: 'new',
        rating: 4.7,
        sales: 1234
    },
    {
        id: 16,
        name: '太阳能充电宝10000mAh',
        desc: '太阳能+USB双充电，户外应急必备',
        price: 199.0,
        originalPrice: 259.0,
        image: 'https://picsum.photos/seed/out4/400/400',
        category: 'outdoor',
        badge: '',
        rating: 4.5,
        sales: 2345
    },
    // 办公用品
    {
        id: 17,
        name: '再生纸笔记本套装',
        desc: '100%再生纸制作，环保油墨印刷',
        price: 32.0,
        originalPrice: 45.0,
        image: 'https://picsum.photos/seed/off1/400/400',
        category: 'office',
        badge: '',
        rating: 4.6,
        sales: 3456
    },
    {
        id: 18,
        name: '竹制桌面收纳架',
        desc: '天然竹材，简约设计，多功能收纳',
        price: 68.0,
        originalPrice: 88.0,
        image: 'https://picsum.photos/seed/off2/400/400',
        category: 'office',
        badge: 'new',
        rating: 4.7,
        sales: 1678
    },
    {
        id: 19,
        name: '可重复使用便签纸',
        desc: 'PET材质，可书写擦拭，循环使用500次',
        price: 22.0,
        originalPrice: 32.0,
        image: 'https://picsum.photos/seed/off3/400/400',
        category: 'office',
        badge: '',
        rating: 4.4,
        sales: 4567
    },
    {
        id: 20,
        name: '环保笔筒（回收塑料制作）',
        desc: '海洋回收塑料再造，每个减少0.5kg塑料污染',
        price: 45.0,
        originalPrice: 58.0,
        image: 'https://picsum.photos/seed/off4/400/400',
        category: 'office',
        badge: 'hot',
        rating: 4.8,
        sales: 2890
    }
];

// ===== 购物车数据 =====
let cart = JSON.parse(localStorage.getItem('greenLifeCart')) || [];

// ===== 更新购物车徽标 =====
function updateCartBadge() {
    const badge = document.getElementById('cartBadge');
    if (badge) {
        const total = cart.reduce((sum, item) => sum + item.quantity, 0);
        badge.textContent = total;
        badge.style.display = total > 0 ? 'flex' : 'none';
    }
}

// ===== 保存购物车 =====
function saveCart() {
    localStorage.setItem('greenLifeCart', JSON.stringify(cart));
    updateCartBadge();
}

// ===== 添加到购物车 =====
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;

    const existing = cart.find(item => item.id === productId);
    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({
            id: product.id,
            name: product.name,
            price: product.price,
            image: product.image,
            quantity: 1
        });
    }
    saveCart();
    showToast('✅ 已添加「' + product.name + '」到购物车');
}

// ===== Toast提示 =====
function showToast(message) {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 80px;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(135deg, #2e7d32, #4caf50);
        color: #fff;
        padding: 14px 28px;
        border-radius: 8px;
        font-size: 15px;
        z-index: 9999;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        animation: slideDown 0.3s ease;
        font-family: 'Microsoft YaHei', sans-serif;
    `;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s';
        setTimeout(() => toast.remove(), 300);
    }, 2500);
}

// ===== 生成商品卡片HTML =====
function generateProductCard(product) {
    const badgeMap = {
        'hot': '<span class="product-badge hot">🔥 热销</span>',
        'new': '<span class="product-badge new">🌟 新品</span>',
        '': ''
    };

    const fullStars = Math.floor(product.rating);
    const halfStar = product.rating % 1 >= 0.5 ? '½' : '';
    const stars = '★'.repeat(fullStars) + halfStar;

    return `
        <div class="product-card">
            ${badgeMap[product.badge] || ''}
            <a href="pages/product-detail.html?id=${product.id}">
                <img src="${product.image}" alt="${product.name}" class="product-image" loading="lazy">
            </a>
            <div class="product-info">
                <a href="pages/product-detail.html?id=${product.id}">
                    <div class="product-name">${product.name}</div>
                </a>
                <div class="product-desc">${product.desc}</div>
                <div class="product-price">
                    <span class="current-price">¥${product.price.toFixed(1)}</span>
                    <span class="original-price">¥${product.originalPrice.toFixed(1)}</span>
                </div>
                <div class="product-rating">
                    <span class="stars">${stars}</span>
                    <span>${product.rating}分</span>
                    <span style="margin-left:auto;">已售${product.sales}</span>
                </div>
                <div class="product-actions">
                    <button class="btn-add-cart" onclick="addToCart(${product.id})">加入购物车</button>
                    <button class="btn-favorite" onclick="toggleFavorite(this)">♡</button>
                </div>
            </div>
        </div>
    `;
}

// ===== 渲染商品列表 =====
function renderProducts(containerId, productList) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = productList.map(p => generateProductCard(p)).join('');
}

// ===== 收藏切换 =====
function toggleFavorite(btn) {
    if (btn.textContent === '♡') {
        btn.textContent = '♥';
        btn.style.color = '#e53935';
        btn.style.borderColor = '#e53935';
        showToast('❤️ 已添加至收藏');
    } else {
        btn.textContent = '♡';
        btn.style.color = '';
        btn.style.borderColor = '';
        showToast('已取消收藏');
    }
}

// ===== 轮播图 =====
let currentSlide = 0;
const totalSlides = 3;
let autoPlayInterval;

function goToSlide(index) {
    currentSlide = index;
    const inner = document.getElementById('carouselInner');
    const dots = document.querySelectorAll('.carousel-dot');
    if (inner) {
        inner.style.transform = 'translateX(-' + (index * 100) + '%)';
    }
    dots.forEach((dot, i) => {
        dot.classList.toggle('active', i === index);
    });
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    goToSlide(currentSlide);
}

function prevSlide() {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    goToSlide(currentSlide);
}

function startAutoPlay() {
    autoPlayInterval = setInterval(nextSlide, 4000);
}

function stopAutoPlay() {
    clearInterval(autoPlayInterval);
}

// ===== 搜索功能 =====
function searchProducts() {
    const input = document.getElementById('searchInput');
    if (!input) return;
    const keyword = input.value.trim();
    if (keyword) {
        window.location.href = 'pages/products.html?search=' + encodeURIComponent(keyword);
    } else {
        showToast('请输入搜索关键词');
    }
}

// ===== 日期显示 =====
function displayDate() {
    const dateEl = document.getElementById('currentDate');
    if (!dateEl) return;
    const now = new Date();
    const options = { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' };
    dateEl.textContent = now.toLocaleDateString('zh-CN', options);
}

// ===== 页面加载完成后初始化 =====
document.addEventListener('DOMContentLoaded', function() {
    // 更新购物车徽标
    updateCartBadge();

    // 渲染首页商品
    if (document.getElementById('hotProducts')) {
        const hotProducts = products.filter(p => p.badge === 'hot').slice(0, 4);
        renderProducts('hotProducts', hotProducts);
    }
    if (document.getElementById('newProducts')) {
        const newProducts = products.filter(p => p.badge === 'new').slice(0, 4);
        renderProducts('newProducts', newProducts);
    }

    // 启动轮播自动播放
    startAutoPlay();

    // 鼠标悬停暂停轮播
    const carousel = document.querySelector('.carousel');
    if (carousel) {
        carousel.addEventListener('mouseenter', stopAutoPlay);
        carousel.addEventListener('mouseleave', startAutoPlay);
    }

    // 显示日期
    displayDate();

    // 搜索框回车搜索
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchProducts();
            }
        });
    }
});
