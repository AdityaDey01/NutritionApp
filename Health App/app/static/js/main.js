// ── TOAST NOTIFICATIONS ──
function showToast(message, type = 'success') {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  const icon = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
  toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
  container.appendChild(toast);
  setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateX(110%)'; toast.style.transition = 'all 0.3s'; setTimeout(() => toast.remove(), 300); }, 3500);
}

// ── INTERSECTION OBSERVER FOR ANIMATIONS ──
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.style.opacity = '1'; e.target.style.transform = 'translateY(0)'; } });
}, { threshold: 0.1 });

document.addEventListener('DOMContentLoaded', () => {
  // Animate cards
  document.querySelectorAll('.card, .feature-card, .how-step, .impact-stat').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(el);
  });

  // Progress bars animation
  document.querySelectorAll('.progress-fill').forEach(el => {
    const target = el.style.width;
    el.style.width = '0';
    setTimeout(() => { el.style.width = target; }, 200);
  });

  // SVG score ring animation
  document.querySelectorAll('.score-ring .fill').forEach(el => {
    const target = el.getAttribute('stroke-dashoffset');
    el.setAttribute('stroke-dashoffset', '314');
    setTimeout(() => { el.style.transition = 'stroke-dashoffset 1.5s ease'; el.setAttribute('stroke-dashoffset', target); }, 300);
  });

  // Active nav highlighting
  const path = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(a => {
    if (path.startsWith(a.getAttribute('href')) && a.getAttribute('href') !== '/') {
      a.classList.add('active');
    }
  });
});

// ── WATER TRACKER ──
let waterCount = 6;
function addWaterGlass() {
  if (waterCount >= 12) return showToast('🌊 Amazing hydration today!', 'success');
  waterCount++;
  showToast(`💧 ${waterCount} glasses! Keep going!`, 'success');
}

// ── HABIT HELPERS ──
function toggleHabit(el) {
  el.classList.toggle('done');
  const check = el.querySelector('.habit-check');
  if (check) {
    check.classList.toggle('done');
    check.textContent = check.classList.contains('done') ? '✓' : '';
  }
}

// ── SMOOTH SCROLL ──
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    e.preventDefault();
    const target = document.querySelector(a.getAttribute('href'));
    if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});

// ── NAVBAR SCROLL EFFECT ──
window.addEventListener('scroll', () => {
  const nav = document.querySelector('.navbar');
  if (!nav) return;
  if (window.scrollY > 20) {
    nav.style.background = 'rgba(10,15,30,0.97)';
    nav.style.boxShadow = '0 4px 24px rgba(0,0,0,0.4)';
  } else {
    nav.style.background = 'rgba(10,15,30,0.85)';
    nav.style.boxShadow = 'none';
  }
});

// ── NUMBER COUNTER ANIMATION ──
function animateCounter(el, target, duration = 1500) {
  let start = 0;
  const step = target / (duration / 16);
  const timer = setInterval(() => {
    start += step;
    if (start >= target) { el.textContent = target; clearInterval(timer); return; }
    el.textContent = Math.floor(start);
  }, 16);
}
