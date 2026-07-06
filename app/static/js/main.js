(function() {
  'use strict';

  // --- Auto-dismiss alerts after 5s ---
  document.querySelectorAll('.alert-dismissible').forEach(function(alert) {
    setTimeout(function() {
      var bsAlert = bootstrap.Alert.getInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

  // --- Animate elements on scroll (Intersection Observer) ---
  var revealElements = document.querySelectorAll('.animate-on-scroll');
  if (revealElements.length > 0 && 'IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    revealElements.forEach(function(el) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(24px)';
      el.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
      observer.observe(el);
    });
  }

  // --- Animate stat cards with counter ---
  var statValues = document.querySelectorAll('.stat-value[data-count]');
  statValues.forEach(function(el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    if (isNaN(target)) return;
    var duration = 1000;
    var startTime = null;

    function animateCounter(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      var current = Math.round(eased * target);
      el.textContent = current;
      if (progress < 1) {
        requestAnimationFrame(animateCounter);
      } else {
        el.textContent = target;
      }
    }
    requestAnimationFrame(animateCounter);
  });

  // --- Add staggered animation to lists with stagger-children class ---
  var staggerLists = document.querySelectorAll('.stagger-children');
  staggerLists.forEach(function(list) {
    Array.from(list.children).forEach(function(child, index) {
      child.style.opacity = '0';
      child.style.animation = 'fadeInUp 0.5s ease forwards';
      child.style.animationDelay = (index * 0.07) + 's';
    });
  });

  // --- Confirm delete with a nicer dialog (Bootstrap modal) ---
  document.querySelectorAll('form[onsubmit*="confirm"]').forEach(function(form) {
    form.removeAttribute('onsubmit');
    form.addEventListener('submit', function(e) {
      if (!confirm('Tem a certeza que deseja eliminar? Esta ação não pode ser desfeita.')) {
        e.preventDefault();
      }
    });
  });

  // --- Highlight tasks nearing deadline ---
  document.querySelectorAll('[data-deadline]').forEach(function(el) {
    var deadline = new Date(el.getAttribute('data-deadline'));
    var hoje = new Date();
    hoje.setHours(0, 0, 0, 0);
    var diffDays = Math.ceil((deadline - hoje) / (1000 * 60 * 60 * 24));
    if (diffDays <= 0) {
      el.classList.add('text-danger', 'fw-bold');
      el.innerHTML += ' <span class="badge bg-danger">Atrasado</span>';
    } else if (diffDays <= 2) {
      el.classList.add('text-warning', 'fw-bold');
    }
  });

  // --- Card entrance stagger for dashboard tasks/events lists ---
  var cardLists = document.querySelectorAll('.card-list-animate');
  cardLists.forEach(function(list) {
    Array.from(list.children).forEach(function(item, idx) {
      item.style.animationDelay = (idx * 0.08) + 's';
    });
  });

  // --- Progress bar animation on goals page ---
  var progressBars = document.querySelectorAll('.goal-progress .progress-bar');
  progressBars.forEach(function(bar) {
    var width = bar.style.width;
    bar.style.width = '0%';
    setTimeout(function() {
      bar.style.transition = 'width 1s cubic-bezier(0.4, 0, 0.2, 1)';
      bar.style.width = width;
    }, 300);
  });

  // --- Kanban card drag visual feedback ---
  document.querySelectorAll('.kanban-column .card').forEach(function(card) {
    card.addEventListener('mouseenter', function() {
      this.style.transition = 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)';
    });
  });

})();
