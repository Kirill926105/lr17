function setVisible(id, visible) {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.toggle('d-none', !visible);
  }
  
  function setText(id, text) {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = text;
  }
  
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }
  
  function renderProducts(products) {
    const container = document.getElementById('product-list');
    if (!container) return;
    container.innerHTML = '';
  
    products.forEach(p => {
      const img = p.image ? `<img src="${p.image}" class="card-img-top" alt="${p.name}">` : '';
      container.innerHTML += `
        <div class="col-12 col-sm-6 col-lg-4">
          <div class="card h-100">
            ${img}
            <div class="card-body">
              <div class="fw-bold mb-1">${p.name}</div>
              <div class="price">${p.price} руб.</div>
            </div>
            <div class="card-footer bg-white border-0 d-grid gap-2">
              <a class="btn btn-outline-primary" href="/product/${p.id}/">Подробнее</a>
              <button class="btn btn-success" onclick="addToCart(${p.id})">В корзину</button>
            </div>
          </div>
        </div>
      `;
    });
  }
  
  async function loadProductsFromApi() {
    setVisible('api-error', false);
    setVisible('api-success', false);
    setVisible('loading', true);
  
    try {
      const params = new URLSearchParams(window.location.search);
      const url = `/api/products/?${params.toString()}`;
  
      const resp = await fetch(url, { credentials: 'same-origin' });
      if (!resp.ok) throw new Error(resp.status);
  
      const data = await resp.json();
      const products = data.results ? data.results : data;
  
      renderProducts(products);
    } catch (e) {
      setText('api-error', 'Ошибка загрузки товаров из API (возможно, нужно войти в аккаунт).');
      setVisible('api-error', true);
    } finally {
      setVisible('loading', false);
    }
  }
  
  async function addToCart(productId) {
    try {
      const csrftoken = getCookie('csrftoken');
  
      const resp = await fetch('/api/cart/add/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ product_id: productId, quantity: 1 })
      });
  
      if (!resp.ok) throw new Error(resp.status);
  
      setText('api-success', 'Товар добавлен в корзину');
      setVisible('api-success', true);
      setTimeout(() => setVisible('api-success', false), 2000);
    } catch (e) {
      setText('api-error', 'Не удалось добавить в корзину (возможно, нужно войти).');
      setVisible('api-error', true);
    }
  }