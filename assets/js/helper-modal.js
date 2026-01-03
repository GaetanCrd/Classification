// Helper Modal for Mobile
(function() {
  'use strict';

  // Create modal HTML structure
  function createModal() {
    const modal = document.createElement('div');
    modal.id = 'helper-modal';
    modal.className = 'fixed inset-0 z-50 hidden';
    modal.innerHTML = `
      <!-- Backdrop -->
      <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity" id="modal-backdrop"></div>
      
      <!-- Modal Content -->
      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <div class="relative bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-hidden">
            <!-- Close Button -->
            <button 
              id="close-modal-btn"
              class="absolute top-3 right-3 z-10 w-8 h-8 flex items-center justify-center rounded-full bg-white hover:bg-slate-100 text-slate-600 hover:text-slate-900 transition-colors shadow-md"
              aria-label="Fermer"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            
            <!-- Image Container -->
            <div class="p-4 overflow-auto max-h-[90vh]">
              <h3 class="text-lg font-semibold mb-3 text-slate-900">Guide des motifs</h3>
              <img 
                src="assets/images/exemple motif.jpg" 
                alt="Guide des motifs de plumes" 
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

  // Show modal
  function showModal() {
    const modal = document.getElementById('helper-modal');
    if (modal) {
      modal.classList.remove('hidden');
      document.body.style.overflow = 'hidden'; // Prevent scrolling
    }
  }

  // Hide modal
  function hideModal() {
    const modal = document.getElementById('helper-modal');
    if (modal) {
      modal.classList.add('hidden');
      document.body.style.overflow = ''; // Restore scrolling
    }
  }

  // Initialize modal when DOM is ready
  function init() {
    // Create modal
    const modal = createModal();

    // Get helper button
    const helperBtn = document.getElementById('helper-btn');
    
    if (helperBtn) {
      helperBtn.addEventListener('click', showModal);
    }

    // Close button click
    const closeBtn = document.getElementById('close-modal-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', hideModal);
    }

    // Backdrop click
    const backdrop = document.getElementById('modal-backdrop');
    if (backdrop) {
      backdrop.addEventListener('click', hideModal);
    }

    // ESC key to close
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        hideModal();
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
