// Language translations
const translations = {
    en: {
        'title':'Shree Thaal',
        'subtitle': 'Home-Made Goodness, Straight to Your Door.',
        'tagline': 'Home Sweets, Served with Love ❤️',
        'festival': 'Celebrate the bond of love with every sweet from Shree Thaal this Raksha Bandhan! 💖',
        'menu-title': 'Our Sweet Collection',
        'cart-title': 'Your Sweet Basket 🧺',
        'total': 'Total',
        'place-order': 'Place Order ',
        'order-form-title': 'Complete Your Order 📝',
        'name-label': 'Full Name',
        'phone-label': 'Mobile Number',
        'address-label': 'Delivery Address',
        'submit-order': 'Submit Order 🎉',
        'thank-you-title': 'Thank You!',
        'order-received': 'Your sweet order has been received successfully.',
        'contact-soon': 'We\'ll contact you shortly to confirm your order.',
        'raksha-bandhan-wish': 'Your order is on the way! Happy Raksha Bandhan! ❤️',
        'continue-shopping': 'Continue Shopping',
        'footer-text': 'Celebrate the bond with our sweets 🎉 Happy Raksha Bandhan from Shree Thaal, where love is in every bite 💖',
        'add-to-cart': 'Add to Cart 🛒',
        'empty-cart-text': 'Your sweet basket is empty',
        'empty-cart-subtext': 'Add some delicious sweets!',
        'remove': 'Remove',
        'quantity-label': 'Select Quantity',
        'contact-us-title': 'Contact Us for Orders',
        'contact-us-description': 'Have a sweet tooth or special request? Call or message us for order bookings!',
        'business-contact-number': 'Contact Number: ',
        'order-confirmation': 'Our team will get back to you to confirm your order. We’re happy to serve you!',
        'important-note': 'Important Note:',
        'order-delivery-note': 'All orders will take up to 2-3 days for delivery. The last date for placing orders is <strong>5th August 2025</strong>.'
   
    },
    hi: {
        'title':'श्री थाल',
        'subtitle': 'घरेलू मिठास, सीधे आपके दरवाजे तक।',
        'tagline': 'घर की मिठाई, प्रेम के साथ परोसी गई ❤️',
        'festival': 'श्री थाल के हर मीठे स्वाद के साथ इस रक्षाबंधन पर प्रेम के रिश्ते का उत्सव मनाएं 💖',
        'menu-title': 'हमारा मिठाई संग्रह',
        'cart-title': 'आपकी मिठाई की टोकरी 🧺',
        'total': 'कुल',
        'place-order': 'ऑर्डर दें ',
        'order-form-title': 'अपना ऑर्डर पूरा करें 📝',
        'name-label': 'पूरा नाम',
        'phone-label': 'मोबाइल नंबर',
        'address-label': 'डिलीवरी का पता',
        'submit-order': 'ऑर्डर सबमिट करें 🎉',
        'thank-you-title': 'धन्यवाद!',
        'order-received': 'आपका मिठाई का ऑर्डर सफलतापूर्वक प्राप्त हो गया है।',
        'contact-soon': 'हम जल्द ही आपसे संपर्क करके ऑर्डर की पुष्टि करेंगे।',
        'raksha-bandhan-wish': 'आपका ऑर्डर आ रहा है! रक्षा बंधन की शुभकामनाएं! ❤️',
        'continue-shopping': 'खरीदारी जारी रखें',
        'footer-text': 'हमारी मिठाइयों से रिश्ते की मिठास मनाएं 🎉 श्री थाल की ओर से रक्षाबंधन की शुभकामनाएँ, जहां हर bite में है प्यार 💖',
        'add-to-cart': 'कार्ट में डालें 🛒',
        'empty-cart-text': 'आपकी मिठाई की टोकरी खाली है',
        'empty-cart-subtext': 'कुछ स्वादिष्ट मिठाइयां जोड़ें!',
        'remove': 'हटाएं',
        'quantity-label': 'मात्रा चुनें',
        'contact-us-title': 'ऑर्डर के लिए हमसे संपर्क करें',
        'contact-us-description': 'क्या आपको मीठा पसंद है या विशेष अनुरोध है? ऑर्डर बुकिंग के लिए हमें कॉल या संदेश करें!',
        'business-contact-number': 'संपर्क नंबर: ',
        'order-confirmation': 'हमारी टीम आपके आदेश की पुष्टि करने के लिए जल्दी संपर्क करेगी। हम आपकी सेवा करने के लिए खुश हैं!',"important-note": "महत्वपूर्ण नोट:",
        'important-note': 'महत्वपूर्ण नोट:',
        'order-delivery-note': 'सभी ऑर्डरों की डिलीवरी में 2-3 दिन का समय लगेगा। ऑर्डर करने की आखिरी तारीख <strong>5 अगस्त 2025</strong> है।'
    
    
    }
};


// Global state
let cart = [];
let currentLanguage = 'en';

// DOM elements
// const sweetsGrid = document.getElementById('sweetsGrid');
const cartFloat = document.getElementById('cartFloat');
const cartCount = document.getElementById('cartCount');
const cartSidebar = document.getElementById('cartSidebar');
const closeCart = document.getElementById('closeCart');
const cartItems = document.getElementById('cartItems');
const cartTotal = document.getElementById('cartTotal');
const placeOrderBtn = document.getElementById('placeOrderBtn');
const orderModal = document.getElementById('orderModal');
const closeModal = document.getElementById('closeModal');
const orderForm = document.getElementById('orderForm');
const thankYouModal = document.getElementById('thankYouModal');
const continueShoppingBtn = document.getElementById('continueShoppingBtn');
const overlay = document.getElementById('overlay');
const langButtons = document.querySelectorAll('.lang-btn');

// Initialize the app
function init() {
    // renderSweets();
    updateCartUI();
    setupEventListeners();
    setupLanguageToggle();
}

// Language toggle functionality
function setupLanguageToggle() {
    langButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const lang = btn.dataset.lang;
            if (lang !== currentLanguage) {
                switchLanguage(lang);
            }
        });
    });
}

function switchLanguage(lang) {
    currentLanguage = lang;

    // Update active button
    langButtons.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });

    // Update the content of the translated sections
    updateTranslations();
    updateCartUI();
}

// Update translations for all sections with data-translate attributes
function updateTranslations() {
    // For all elements with a data-translate attribute
    document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.getAttribute('data-translate');
        
        if (translations[currentLanguage][key]) {
            if (element.tagName === 'SPAN' || element.tagName === 'P' || element.tagName === 'H2' || element.tagName === 'H1' || element.tagName === 'H3') {
                element.innerHTML = translations[currentLanguage][key];
            } else if (element.tagName === 'BUTTON') {
                // Special handling for buttons
                element.innerHTML = translations[currentLanguage][key];
            } else if (element.tagName === 'LABEL') {
                // Special handling for form labels
                element.innerHTML = translations[currentLanguage][key];
            }
        }
    });

    // Update the sweet names dynamically (for sweet cards)
    document.querySelectorAll('.sweet-name').forEach(element => {
        const nameEn = element.getAttribute('data-name-en');
        const nameHi = element.getAttribute('data-name-hi');
        
        // Switch between English and Hindi based on currentLanguage
        if (currentLanguage === 'hi') {
            element.innerHTML = nameHi;  // Use Hindi name
        } else {
            element.innerHTML = nameEn;  // Use English name
        }
    });

    // Update dynamic content such as "Your Sweet Basket 🧺" and "Complete Your Order 📝"
    document.querySelectorAll('.cart-title[data-translate]').forEach(element => {
        element.innerHTML = translations[currentLanguage]['cart-title'];
    });

    document.querySelectorAll('.order-form-title[data-translate]').forEach(element => {
        element.innerHTML = translations[currentLanguage]['order-form-title'];
    });
    
    // Repeat the above for any additional dynamic content in your modal or other sections
}


    


// Cart related functions (addToCart, removeFromCart, updateQuantity, updateCartUI) remain mostly same
// Just ensure cart items use currentLanguage for showing sweet names

function addToCart(buttonEl) {
    const sweetCard = buttonEl.closest('.sweet-card');
    if (!sweetCard) {
        console.error("Could not find sweet-card element.");
        return;
    }

    const sweetId = buttonEl.dataset.id;
    const nameEn = buttonEl.dataset.nameEn; // Corrected data access
    const nameHi = buttonEl.dataset.nameHi; // Corrected data access
    const pricePerKg = parseFloat(buttonEl.dataset.pricePerKg);
    const image = buttonEl.dataset.image;

    // Ensure quantity selector exists for the sweet card
    const quantitySelect = sweetCard.querySelector(`#quantity-${sweetId}`);
    if (!quantitySelect) {
        console.error("Could not find quantity selector.");
        return;
    }

    const selectedMultiplier = parseFloat(quantitySelect.value);
    const selectedOption = quantitySelect.options[quantitySelect.selectedIndex];
    const selectedWeight = selectedOption.textContent.split(' - ')[0]; // Handle weight selection

    const calculatedPrice = Math.round(pricePerKg * selectedMultiplier);
    const cartItemId = `${sweetId}-${selectedMultiplier}`;

    const existingItem = cart.find(item => item.cartItemId === cartItemId);
    if (existingItem) {
        existingItem.quantity += 1; // Increase quantity if item already exists
    } else {
        // Add the new item to cart
        cart.push({
            cartItemId,
            id: sweetId,
            nameEn,
            nameHi,
            selectedWeight,
            selectedMultiplier,
            calculatedPrice,
            quantity: 1,
            image
        });
    }

    // Update cart UI
    updateCartUI();
    showCartSidebar(); // Show cart sidebar if item is added
}




// Remove from cart
function removeFromCart(cartItemId) {
    cart = cart.filter(item => item.cartItemId !== cartItemId);
    updateCartUI();
}

// Update quantity
function updateQuantity(cartItemId, change) {
    const item = cart.find(item => item.cartItemId === cartItemId);
    if (item) {
        item.quantity += change;
        if (item.quantity <= 0) {
            removeFromCart(cartItemId);
        } else {
            updateCartUI();
        }
    }
}

// Update cart UI
function updateCartUI() {
    // Update cart count (total quantity of items)
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
    cartCount.style.display = totalItems > 0 ? 'flex' : 'none';
    
    // If cart is empty, show empty message
    if (cart.length === 0) {
        cartItems.innerHTML = `
            <div class="empty-cart">
                <div class="empty-cart-icon">🧺</div>
                <p>${translations[currentLanguage]['empty-cart-text']}</p>
                <p style="font-size: 0.9rem; opacity: 0.7;">${translations[currentLanguage]['empty-cart-subtext']}</p>
            </div>
        `;
        placeOrderBtn.disabled = true;
    } else {
        // Render cart items with correct product names by language
        cartItems.innerHTML = cart.map(item => `
            <div class="cart-item">
                <img src="${item.image}" alt="${currentLanguage === 'en' ? item.nameEn : item.nameHi}" class="cart-item-image">
                <div class="cart-item-info">
                    <div class="cart-item-name">${currentLanguage === 'en' ? item.nameEn : item.nameHi}</div>
                    <div class="cart-item-quantity">${item.selectedWeight}</div>
                    <div class="cart-item-price">₹ ${item.calculatedPrice} </div>
                    <div class="cart-item-controls">
                        <button class="quantity-btn" onclick="updateQuantity('${item.cartItemId}', -1)">−</button>
                        <span class="quantity-display">${item.quantity}</span>
                        <button class="quantity-btn" onclick="updateQuantity('${item.cartItemId}', 1)">+</button>
                        <button class="remove-item" onclick="removeFromCart('${item.cartItemId}')">${translations[currentLanguage]['remove']}</button>
                    </div>
                </div>
            </div>
        `).join('');
        placeOrderBtn.disabled = false;
    }
    
    // Update total price display
    const total = cart.reduce((sum, item) => sum + (item.calculatedPrice * item.quantity), 0);
    cartTotal.textContent = total;

      // Call updateTranslations after updating the cart UI to ensure all text is translated
    updateTranslations();
}


// Show cart sidebar
function showCartSidebar() {
    cartSidebar.classList.add('open');
    overlay.classList.add('active');
}

// Hide cart sidebar
function hideCartSidebar() {
    cartSidebar.classList.remove('open');
    overlay.classList.remove('active');
}

// Show modal
function showModal(modal) {
    modal.classList.add('active');
}

// Hide modal
function hideModal(modal) {
    modal.classList.remove('active');
}

// Validate phone number
function validatePhone(phone) {
    const phoneRegex = /^[0-9]{10}$/;
    return phoneRegex.test(phone);
}

// Setup event listeners
function setupEventListeners() {
    // Cart float button
    cartFloat.addEventListener('click', showCartSidebar);
    
    // Close cart
    closeCart.addEventListener('click', hideCartSidebar);
    
    // Place order button
    placeOrderBtn.addEventListener('click', () => {
        hideCartSidebar();
        showModal(orderModal);
    });
    
    // Close modal
    closeModal.addEventListener('click', () => hideModal(orderModal));
    
    // Order form submission
document.getElementById('orderForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const name = document.getElementById("customerName")?.value.trim();
    const phone = document.getElementById("customerPhone")?.value.trim();
    const address = document.getElementById("deliveryAddress")?.value.trim();
    const paymentMode = document.querySelector('input[name="paymentMode"]:checked')?.value || "COD";

    
    if (!name || !phone || !address) {
        alert("Please fill all required fields");
        return;
    }

   const orderData = {
    name: name,
    contact_number: phone,
    address: address,
    payment_method: paymentMode.toLowerCase(),  // convert to "cod" or "upi"
    items: cart.map(item => ({
        product_id: item.id,
        quantity: item.quantity,
        weight_selected: item.selectedWeight.trim(),
            price: item.calculatedPrice
        }))
    };

    // // **Add these lines here, just before you send the data**
    // console.log("Current cart array:", cart);
    // console.log("Order data JSON string:", JSON.stringify(orderData));

    try {
        const response = await fetch('/customer/order', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(orderData)
        });

        const result = await response.json();

        if (response.ok) {
            alert("Order placed successfully!");
            cart = [];
            updateCartUI();
            hideModal(orderModal);
            showModal(thankYouModal);
        } else {
            alert("Failed to place order: " + result.detail);
        }
    } catch (err) {
        console.error("Error placing order:", err);
        alert("An error occurred while placing the order.");
    }
});
    
    // Continue shopping button
    continueShoppingBtn.addEventListener('click', () => {
        hideModal(thankYouModal);
    });
    
    // Overlay click to close
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            hideCartSidebar();
        }
    });
    
    // Close modals on outside click
    orderModal.addEventListener('click', (e) => {
        if (e.target === orderModal) {
            hideModal(orderModal);
        }
    });
    
    thankYouModal.addEventListener('click', (e) => {
        if (e.target === thankYouModal) {
            hideModal(thankYouModal);
        }
    });
    
    // Close modals on escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            hideCartSidebar();
            hideModal(orderModal);
            hideModal(thankYouModal);
        }
    });
    
    // Add interactive feedback for buttons
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('add-to-cart-btn')) {
            // Create floating animation
            const rect = e.target.getBoundingClientRect();
            const floatingText = document.createElement('div');
            floatingText.textContent = currentLanguage === 'en' ? 'Added! 🍬' : 'जोड़ा गया! 🍬';
            floatingText.style.cssText = `
                position: fixed;
                left: ${rect.left + rect.width/2}px;
                top: ${rect.top}px;
                transform: translateX(-50%);
                background: #059669;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 20px;
                font-size: 0.9rem;
                font-weight: 600;
                z-index: 10000;
                pointer-events: none;
                animation: floatUp 2s ease-out forwards;
            `;
            
            // Add keyframes for animation
            if (!document.getElementById('floatUpStyle')) {
                const style = document.createElement('style');
                style.id = 'floatUpStyle';
                style.textContent = `
                    @keyframes floatUp {
                        0% { opacity: 1; transform: translateX(-50%) translateY(0); }
                        100% { opacity: 0; transform: translateX(-50%) translateY(-50px); }
                    }
                `;
                document.head.appendChild(style);
            }
            
            document.body.appendChild(floatingText);
            setTimeout(() => {
                if (document.body.contains(floatingText)) {
                    document.body.removeChild(floatingText);
                }
            }, 2000);
        }
    });
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', init);

