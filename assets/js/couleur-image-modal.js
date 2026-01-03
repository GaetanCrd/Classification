// Couleur Image Modal for Mobile and Desktop
(function() {
  'use strict';

  // Create modal HTML structure
  function createCouleurModal() {
    const modal = document.createElement('div');
    modal.id = 'couleur-modal';
    modal.className = 'fixed inset-0 z-50 hidden';
    modal.innerHTML = `
      <!-- Backdrop -->
      <div class="fixed inset-0 bg-black bg-opacity-75 transition-opacity" id="couleur-modal-backdrop"></div>
      
      <!-- Modal Content -->
      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <div class="relative bg-white rounded-lg shadow-xl max-w-4xl w-full">
            <!-- Close Button -->
            <button 
              id="close-couleur-modal-btn"
              class="absolute top-3 right-3 z-10 w-10 h-10 flex items-center justify-center rounded-full bg-white hover:bg-slate-100 text-slate-600 hover:text-slate-900 transition-colors shadow-md"
              aria-label="Fermer"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            
            <!-- Image Container -->
            <div class="p-6">
              <h3 id="couleur-modal-title" class="text-xl font-semibold mb-4 text-slate-900">Guide des nuances de couleurs</h3>
              <img 
                id="couleur-modal-img"
                src="assets/images/nuance.jpg" 
                alt="Guide des nuances de couleurs" 
                class="w-full h-auto rounded-lg"
              />
            </div>
          </div>
        </div>
      </div>
    `;
    
    document.body.appendChild(modal);
    return modal;
  }

  // Show couleur modal
  function showCouleurModal() {
    const modal = document.getElementById('couleur-modal');
    if (modal) {
      modal.classList.remove('hidden');
      document.body.style.overflow = 'hidden'; // Prevent scrolling
    }
  }

  // Hide couleur modal
  function hideCouleurModal() {
    const modal = document.getElementById('couleur-modal');
    if (modal) {
      modal.classList.add('hidden');
      document.body.style.overflow = ''; // Restore scrolling
    }
  }

  // Initialize
  function init() {
    // Create modal
    createCouleurModal();

    // Mobile helper button
    const mobileHelperBtn = document.getElementById('couleur-helper-btn-mobile');
    if (mobileHelperBtn) {
      mobileHelperBtn.addEventListener('click', showCouleurModal);
    }

    // Desktop helper button
    const desktopHelperBtn = document.getElementById('couleur-helper-btn-desktop');
    if (desktopHelperBtn) {
      desktopHelperBtn.addEventListener('click', showCouleurModal);
    }

    // Close button click
    const closeBtn = document.getElementById('close-couleur-modal-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', hideCouleurModal);
    }

    // Backdrop click
    const backdrop = document.getElementById('couleur-modal-backdrop');
    if (backdrop) {
      backdrop.addEventListener('click', hideCouleurModal);
    }

    // ESC key to close
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        hideCouleurModal();
      }
    });
  }

  // Run init when DOM is loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
