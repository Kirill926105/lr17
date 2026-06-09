function showToast(message, type) {
  type = type || 'success';
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = 'toast align-items-center text-bg-' + (type === 'danger' ? 'danger' : 'success') + ' border-0';
  toast.setAttribute('role', 'alert');
  toast.setAttribute('aria-live', 'assertive');
  toast.setAttribute('aria-atomic', 'true');
  const body = document.createElement('div');
  body.className = 'd-flex align-items-center p-2';
  body.innerHTML = '<span style="flex:1;padding:2px 12px">' + message + '</span>' +
    '<button type="button" class="btn-close btn-close-white me-1" data-bs-dismiss="toast" aria-label="Закрыть"></button>';
  toast.appendChild(body);
  container.appendChild(toast);
  var bsToast = new bootstrap.Toast(toast, { delay: 3500 });
  bsToast.show();
  toast.addEventListener('hidden.bs.toast', function() { toast.remove(); });
}

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

function getToken() {
  return localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
}

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>"']/g, (char) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;',
  }[char]));
}

function productVector(product) {
  const text = `${product.name || ''} ${product.category_name || ''}`.toLowerCase();
  if (/(sleeve|card|кар|протектор|протек|чех|рукав)/.test(text)) return '/static/img/products/cards.svg';
  if (/(dice|die|куб|дайс|d20|d6)/.test(text)) return '/static/img/products/dice.svg';
  if (/(organizer|insert|box|органайзер|встав|короб)/.test(text)) return '/static/img/products/organizer.svg';
  if (/(token|coin|marker|жетон|маркер|монет)/.test(text)) return '/static/img/products/tokens.svg';
  if (/(mat|playmat|ковр|поле|плеймат)/.test(text)) return '/static/img/products/mat.svg';
  return '/static/img/products/accessory.svg';
}

async function apiFetch(url, options = {}) {
  const token = getToken();
  const headers = options.headers || {};
  if (token) headers['Authorization'] = `Bearer ${token}`;
  headers['Content-Type'] = 'application/json';
  const csrf = getCookie('csrftoken');
  if (csrf) headers['X-CSRFToken'] = csrf;
  return fetch(url, { ...options, headers, credentials: 'same-origin' });
}

function renderProducts(products) {
  const container = document.getElementById('product-list');
  if (!container) return;
  container.innerHTML = '';

  if (products.length === 0) {
    container.innerHTML = '<div class="empty-state">Товары не найдены. Попробуйте изменить поиск или фильтры.</div>';
    return;
  }

  products.forEach((p) => {
    const imageUrl = p.image || productVector(p);
    const stock = Number(p.stock || 0);
    const stockLabel = stock > 0 ? `${stock} шт.` : 'нет в наличии';
    const cartControl = stock > 0
      ? `<button class="btn btn-success" onclick="addToCart(${p.id})">В корзину</button>`
      : '<button class="btn btn-secondary" disabled>Нет в наличии</button>';

    container.innerHTML += `
      <div class="col-12 col-sm-6 col-xl-4">
        <article class="product-card">
          <img src="${imageUrl}" class="product-image" alt="${escapeHtml(p.name)}" loading="lazy" onerror="this.src='${productVector(p)}'">
          <div class="product-body">
            <div class="product-meta">${escapeHtml(p.category_name || '')} · ${escapeHtml(p.producer_name || '')}</div>
            <h2>${escapeHtml(p.name)}</h2>
            <div class="product-card-footer">
              <span class="product-price">${escapeHtml(p.price)} руб.</span>
              <span class="stock-pill ${stock > 0 ? '' : 'is-empty'}">${stockLabel}</span>
            </div>
          </div>
          <div class="product-actions">
            <a class="btn btn-outline-primary" href="/product/${p.id}/">Подробнее</a>
            ${cartControl}
          </div>
        </article>
      </div>
    `;
  });
}

async function loadProductsFromApi() {
  setVisible('loading', true);

  try {
    const params = new URLSearchParams(window.location.search);
    const resp = await fetch(`/api/products/?${params.toString()}`, { credentials: 'same-origin' });
    if (!resp.ok) throw new Error(resp.status);

    const data = await resp.json();
    renderProducts(data.results ? data.results : data);
  } catch {
    showToast('Не удалось загрузить товары из API.', 'danger');
  } finally {
    setVisible('loading', false);
  }
}

async function addToCart(productId) {
  try {
    const resp = await apiFetch('/api/cart/add/', {
      method: 'POST',
      body: JSON.stringify({ product_id: productId, quantity: 1 })
    });

    if (!resp.ok) {
      const data = await resp.json().catch(() => ({}));
      if (data.error === 'Not enough stock') {
        throw new Error('Товара недостаточно на складе.');
      }
      throw new Error('Не удалось добавить товар.');
    }

    showToast('Товар добавлен в корзину.', 'success');
  } catch (error) {
    showToast(error.message || 'Не удалось добавить товар в корзину. Возможно, нужно войти.', 'danger');
  }
}
