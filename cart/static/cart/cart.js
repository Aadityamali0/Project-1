const cartItems = document.getElementById('cartItems');
const cartEmpty = document.getElementById('cartEmpty');
const cartCountLabel = document.getElementById('cartCountLabel');
const summarySubtotal = document.getElementById('summarySubtotal');
const summaryTotal = document.getElementById('summaryTotal');

function money(n) { return '$' + n.toFixed(2); }

function recalc() {
  const rows = cartItems.querySelectorAll('.cart-item');
  let subtotal = 0;

  rows.forEach(row => {
    const price = parseFloat(row.dataset.price);
    const qtyInput = row.querySelector('.qty-input');
    const qty = Math.max(1, parseInt(qtyInput.value, 10) || 1);
    qtyInput.value = qty;
    const lineTotal = price * qty;
    row.querySelector('.line-total').textContent = money(lineTotal);
    subtotal += lineTotal;
  });

  const productCount = rows.length;
  summarySubtotal.textContent = money(subtotal);
  summaryTotal.textContent = money(subtotal);
  cartCountLabel.textContent = productCount === 1 ? '1 item' : productCount + ' items';

  const hasItems = rows.length > 0;
  cartEmpty.classList.toggle('show', !hasItems);
}

cartItems.addEventListener('click', e => {
  const qtyBtn = e.target.closest('.qty-btn');
  if (qtyBtn) {
    const input = qtyBtn.parentElement.querySelector('.qty-input');
    let val = parseInt(input.value, 10) || 1;
    val = qtyBtn.dataset.action === 'increase' ? val + 1 : Math.max(1, val - 1);
    input.value = val;
    recalc();
    return;
  }

  const editBtn = e.target.closest('.edit-btn');
  if (editBtn) {
    const row = editBtn.closest('.cart-item');
    row.classList.add('editing');
    row.querySelector('.qty-input').readOnly = false;
    return;
  }

  const doneBtn = e.target.closest('.done-btn');
  if (doneBtn) {
    const row = doneBtn.closest('.cart-item');
    row.classList.remove('editing');
    row.querySelector('.qty-input').readOnly = true;
    return;
  }

  const deleteBtn = e.target.closest('.delete-btn');

  if (deleteBtn) {
    const row = deleteBtn.closest('.cart-item');

    row.classList.add('removing');

    row.addEventListener('transitionend', () => {
        row.remove();
        recalc();
    }, { once: true });
  }
});

cartItems.addEventListener('input', e => {
  if (e.target.classList.contains('qty-input')) recalc();
});

recalc();