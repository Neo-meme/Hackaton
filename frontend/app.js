document.addEventListener('DOMContentLoaded', () => {
  let currentUserRole = 'client';
  let cart = [];
  const COMBO_EXTRA = 5000;

  // Catálogo dinámico de productos
  let products = [
    {
      id: 1,
      name: 'Hamburguesa Artisan',
      description: 'Carne 100% de res, queso cheddar y salsa especial.',
      price: 18000,
      image: 'hamburguesa.webp'
    },
    {
      id: 2,
      name: 'Sushi Roll Roll',
      description: '10 bocados de salmón, aguacate y queso crema.',
      price: 24000,
      image: 'sushi.webp'
    },
    {
      id: 3,
      name: 'Pizza Pepperoni',
      description: 'Masa artesanal, mozzarella y abundante pepperoni.',
      price: 22000,
      image: 'pizza.webp'
    }
  ];

  // Elementos DOM
  const loginView = document.getElementById('loginView');
  const appView = document.getElementById('appView');
  const loginForm = document.getElementById('loginForm');
  const userDisplay = document.getElementById('userDisplay');
  const roleBadge = document.getElementById('roleBadge');
  const logoutBtn = document.getElementById('logoutBtn');
  const productsGrid = document.getElementById('productsGrid');
  const addProductBtn = document.getElementById('addProductBtn');
  const cartList = document.getElementById('cartList');
  const cartTotal = document.getElementById('cartTotal');
  const payBtn = document.getElementById('payBtn');

  // Modal DOM
  const productModal = document.getElementById('productModal');
  const productForm = document.getElementById('productForm');
  const closeModalBtn = document.getElementById('closeModalBtn');
  const modalTitle = document.getElementById('modalTitle');

  // Login y selección de rol
  loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const usernameInput = document.getElementById('username').value;
    currentUserRole = document.getElementById('userRole').value;

    // Dentro del evento loginForm.addEventListener('submit', ...)
    if (usernameInput.trim() !== '') {
      const displayName = usernameInput.includes('@') ? usernameInput.split('@')[0] : usernameInput;
      userDisplay.textContent = displayName;
      roleBadge.textContent = currentUserRole === 'admin' ? 'ADMIN' : 'CLIENTE';
      
      addProductBtn.style.display = currentUserRole === 'admin' ? 'block' : 'none';

      // Transición limpia de pantallas
      loginView.style.setProperty('display', 'none', 'important');
      appView.style.setProperty('display', 'block', 'important');

      renderProducts();
    }
  });

  // Logout
  logoutBtn.addEventListener('click', () => {
    appView.style.display = 'none';
    loginView.style.display = 'flex';
    cart = [];
    updateCartUI();
    resetQR();
  });

  // Renderizar catálogo según rol
  function renderProducts() {
    productsGrid.innerHTML = '';

    products.forEach(product => {
      const card = document.createElement('article');
      card.className = 'product-card';
      card.dataset.id = product.id;

      card.innerHTML = `
        <div class="product-image">
          <img src="imagenes/${product.image}" alt="${product.name}">
        </div>
        <div class="product-info">
          <h3>${product.name}</h3>
          <p class="description">${product.description}</p>
          
          <div class="combo-selector">
            <label class="switch-label">
              <span>¿Hacerlo Combo? (+ $5.000)</span>
              <input type="checkbox" class="combo-checkbox" data-base-price="${product.price}">
              <span class="slider"></span>
            </label>
          </div>

          <div class="card-footer">
            <span class="price">$${product.price.toLocaleString('es-CO')}</span>
            
            <div class="action-buttons">
              ${
                currentUserRole === 'admin'
                  ? `<button class="btn btn-edit" onclick="editProduct(${product.id})">Editar</button>
                     <button class="btn btn-delete" onclick="deleteProduct(${product.id})">Eliminar</button>`
                  : ''
              }
              <button class="btn btn-secondary add-to-cart">Agregar</button>
            </div>
          </div>
        </div>
      `;

      // Evento del toggle combo para actualizar el precio visible
      const comboCheckbox = card.querySelector('.combo-checkbox');
      const priceDisplay = card.querySelector('.price');

      comboCheckbox.addEventListener('change', (e) => {
        const isChecked = e.target.checked;
        const base = product.price;
        const final = isChecked ? base + COMBO_EXTRA : base;
        priceDisplay.textContent = `$${final.toLocaleString('es-CO')}`;
      });

      // Evento de agregar al carrito (Disponible para Cliente y Admin)
      const addBtn = card.querySelector('.add-to-cart');
      addBtn.addEventListener('click', () => {
        const isCombo = comboCheckbox.checked;
        const finalPrice = isCombo ? product.price + COMBO_EXTRA : product.price;
        const title = isCombo ? `${product.name} (Combo)` : product.name;

        cart.push({ id: Date.now(), title: title, price: finalPrice });
        updateCartUI();
      });

      productsGrid.appendChild(card);
    });
  }

  // ACCIONES ADMINISTRADOR: Eliminar
  window.deleteProduct = function(id) {
    if (confirm('¿Estás seguro de eliminar este producto?')) {
      products = products.filter(p => p.id !== id);
      renderProducts();
    }
  };

  // ACCIONES ADMINISTRADOR: Abrir Modal Editar
  window.editProduct = function(id) {
    const prod = products.find(p => p.id === id);
    if (!prod) return;

    document.getElementById('prodId').value = prod.id;
    document.getElementById('prodName').value = prod.name;
    document.getElementById('prodDesc').value = prod.description;
    document.getElementById('prodPrice').value = prod.price;
    document.getElementById('prodImage').value = prod.image;

    modalTitle.textContent = 'Editar Producto';
    productModal.style.display = 'flex';
  };

  // Abrir Modal Crear
  addProductBtn.addEventListener('click', () => {
    productForm.reset();
    document.getElementById('prodId').value = '';
    modalTitle.textContent = 'Nuevo Producto';
    productModal.style.display = 'flex';
  });

  closeModalBtn.addEventListener('click', () => {
    productModal.style.display = 'none';
  });

  // Guardar/Crear Producto
  productForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const id = document.getElementById('prodId').value;
    const name = document.getElementById('prodName').value;
    const description = document.getElementById('prodDesc').value;
    const price = parseInt(document.getElementById('prodPrice').value);
    const image = document.getElementById('prodImage').value;

    if (id) {
      const prod = products.find(p => p.id === parseInt(id));
      if (prod) {
        prod.name = name;
        prod.description = description;
        prod.price = price;
        prod.image = image;
      }
    } else {
      products.push({
        id: Date.now(),
        name,
        description,
        price,
        image
      });
    }

    productModal.style.display = 'none';
    renderProducts();
  });

  // Renderizar Carrito
  function updateCartUI() {
    cartList.innerHTML = '';

    if (cart.length === 0) {
      cartList.innerHTML = '<li class="empty-msg">Tu carrito está vacío</li>';
      cartTotal.textContent = '$0';
      payBtn.disabled = true;
      resetQR();
      return;
    }

    let total = 0;
    cart.forEach(item => {
      total += item.price;
      const li = document.createElement('li');
      li.className = 'cart-item';
      li.innerHTML = `
        <span>${item.title}</span>
        <strong>$${item.price.toLocaleString('es-CO')}</strong>
      `;
      cartList.appendChild(li);
    });

    cartTotal.textContent = `$${total.toLocaleString('es-CO')}`;
    payBtn.disabled = false;
  }

  function resetQR() {
    const qrImage = document.getElementById('qrImage');
    const qrPlaceholder = document.querySelector('.qr-placeholder');
    const qrStatus = document.getElementById('qrStatus');

    if (qrImage && qrPlaceholder && qrStatus) {
      qrImage.style.display = 'none';
      qrImage.src = '';
      qrPlaceholder.style.display = 'block';
      qrStatus.textContent = 'Esperando orden...';
      payBtn.textContent = 'Pagar con Factus Pay';
    }
  }

  // Generar QR de pago
  payBtn.addEventListener('click', () => {
    if (cart.length === 0) return;

    const qrImage = document.getElementById('qrImage');
    const qrPlaceholder = document.querySelector('.qr-placeholder');
    const qrStatus = document.getElementById('qrStatus');

    payBtn.disabled = true;
    payBtn.textContent = 'Procesando...';
    qrStatus.textContent = 'Generando QR con Factus Pay...';

    setTimeout(() => {
      qrPlaceholder.style.display = 'none';
      qrImage.src = 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=FactusPay_Pago_Exitoso';
      qrImage.style.display = 'block';

      qrStatus.textContent = 'Escanea para pagar con tu app';
      payBtn.textContent = 'QR Generado';
    }, 1200);
  });
});