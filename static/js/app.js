// Application client scripts
document.addEventListener("DOMContentLoaded", function () {
  // Initialize Lucide icons if available
  if (window.lucide) {
    window.lucide.createIcons();
  }

  // Mobile sidebar toggle
  const mobileMenuBtn = document.getElementById("mobile-menu-btn");
  const sidebar = document.getElementById("sidebar");
  const sidebarOverlay = document.getElementById("sidebar-overlay");

  if (mobileMenuBtn && sidebar) {
    mobileMenuBtn.addEventListener("click", function () {
      sidebar.classList.toggle("-translate-x-full");
      if (sidebarOverlay) {
        sidebarOverlay.classList.toggle("hidden");
      }
    });
  }

  if (sidebarOverlay) {
    sidebarOverlay.addEventListener("click", function () {
      sidebar.classList.add("-translate-x-full");
      sidebarOverlay.classList.add("hidden");
    });
  }

  // Auto dismiss flash alerts after 4 seconds
  const flashAlerts = document.querySelectorAll(".flash-alert");
  flashAlerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = "opacity 0.4s ease-out";
      alert.style.opacity = "0";
      setTimeout(function () {
        alert.remove();
      }, 400);
    }, 4000);
  });
});

// Modal helpers
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove("hidden");
    modal.classList.add("flex");
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
  }
}
