// Catégorie Helper Modal
(function() {
  'use strict';

  // Create modal HTML structure
  function createModal() {
    const modal = document.createElement('div');
    modal.id = 'categorie-helper-modal';
    modal.className = 'fixed inset-0 z-50 hidden';
    modal.innerHTML = `
      <!-- Backdrop -->
      <div class="fixed inset-0 bg-black bg-opacity-50 transition-opacity categorie-modal-backdrop"></div>
      
      <!-- Modal Content -->
      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <div class="relative bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-hidden">
            <!-- Close Button -->
            <button 
              class="close-categorie-modal-btn absolute top-3 right-3 z-10 w-8 h-8 flex items-center justify-center rounded-full bg-white hover:bg-slate-100 text-slate-600 hover:text-slate-900 transition-colors shadow-md"
              aria-label="Fermer"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            
            <!-- Content Container -->
            <div class="p-6 overflow-auto max-h-[90vh]">
              <h3 class="text-xl font-bold mb-4 text-slate-900">Catégories de plumes</h3>
              <div class="text-sm md:text-base text-slate-700 leading-relaxed space-y-3">
                <p>Les plumes figurant dans cet atlas sont de 3 catégories différentes, selon la zone anatomique où elles sont implantées.</p>
                <p>Les <strong>rémiges primaires (P)</strong> prennent appui sur les os des phalanges et du métacarpe et les <strong>rémiges secondaires (S)</strong> sont insérées au niveau du radius-ulna.</p>
                <p>Les <strong>rectrices (R)</strong> sont issues du croupion et constituent la base de la queue.</p>
                <p>Au sein de chaque catégorie, les plumes sont numérotées.</p>
              </div>
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
    const modal = document.getElementById('categorie-helper-modal');
    if (modal) {
      modal.classList.remove('hidden');
      document.body.style.overflow = 'hidden'; // Prevent scrolling
    }
  }

  // Hide modal
  function hideModal() {
    const modal = document.getElementById('categorie-helper-modal');
    if (modal) {
      modal.classList.add('hidden');
      document.body.style.overflow = ''; // Restore scrolling
    }
  }

  // Initialize modal when DOM is ready
  function init() {
    // Create modal
    const modal = createModal();

    // Use event delegation for both desktop and mobile buttons (since they're created dynamically)
    document.addEventListener('click', function(e) {
      // Check for desktop button
      if (e.target.closest('#categorie-helper-btn-desktop')) {
        e.stopPropagation();
        showModal();
        return;
      }
      
      // Check for mobile buttons
      if (e.target.closest('.categorie-helper-btn-mobile')) {
        e.stopPropagation();
        showModal();
        return;
      }
    });

    // Close button click
    const closeBtn = modal.querySelector('.close-categorie-modal-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', hideModal);
    }

    // Backdrop click
    const backdrop = modal.querySelector('.categorie-modal-backdrop');
    if (backdrop) {
      backdrop.addEventListener('click', hideModal);
    }

    // ESC key to close
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
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
