// Motif Image Modal for Desktop
(function() {
  'use strict';

  // Create modal HTML structure
  function createImageModal() {
    const modal = document.createElement('div');
    modal.id = 'image-modal';
    modal.className = 'fixed inset-0 z-50 hidden';
    modal.innerHTML = `
      <!-- Backdrop -->
      <div class="fixed inset-0 bg-black bg-opacity-75 transition-opacity" id="image-modal-backdrop"></div>
      
      <!-- Modal Content -->
      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4">
          <div class="relative bg-white rounded-lg shadow-xl max-w-4xl w-full">
            <!-- Close Button -->
            <button 
              id="close-image-modal-btn"
              class="absolute top-3 right-3 z-10 w-10 h-10 flex items-center justify-center rounded-full bg-white hover:bg-slate-100 text-slate-600 hover:text-slate-900 transition-colors shadow-md"
              aria-label="Fermer"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
            
            <!-- Image Container -->
            <div class="p-6">
              <h3 id="image-modal-title" class="text-xl font-semibold mb-4 text-slate-900"></h3>
              <img 
                id="image-modal-img"
                src="" 
                alt="" 
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

  // Show image modal
  function showImageModal(imageSrc, imageName) {
    const modal = document.getElementById('image-modal');
    const img = document.getElementById('image-modal-img');
    const title = document.getElementById('image-modal-title');
    
    if (modal && img && title) {
      img.src = imageSrc;
      img.alt = imageName;
      title.textContent = imageName;
      modal.classList.remove('hidden');
      document.body.style.overflow = 'hidden'; // Prevent scrolling
    }
  }

  // Hide image modal
  function hideImageModal() {
    const modal = document.getElementById('image-modal');
    if (modal) {
      modal.classList.add('hidden');
      document.body.style.overflow = ''; // Restore scrolling
    }
  }

  // Match heights function
  function matchHeights() {
    const filtersSection = document.getElementById('filters-section');
    const motifGuideSection = document.getElementById('motif-guide-section');
    
    if (filtersSection && motifGuideSection && window.innerWidth >= 768) {
      // Reset height first
      motifGuideSection.style.height = 'auto';
      
      // Get the height of filters section
      const filtersHeight = filtersSection.offsetHeight;
      
      // Set the motif guide section to match
      motifGuideSection.style.height = filtersHeight + 'px';
    } else if (motifGuideSection) {
      motifGuideSection.style.height = 'auto';
    }
  }

  // Initialize
  function init() {
    // Create modal
    createImageModal();

    // Add click listeners to all motif images
    const imageItems = document.querySelectorAll('.motif-image-item');
    imageItems.forEach(item => {
      item.addEventListener('click', function() {
        const imageSrc = this.getAttribute('data-src');
        const imageName = this.getAttribute('data-name');
        showImageModal(imageSrc, imageName);
      });
    });

    // Close button click
    const closeBtn = document.getElementById('close-image-modal-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', hideImageModal);
    }

    // Backdrop click
    const backdrop = document.getElementById('image-modal-backdrop');
    if (backdrop) {
      backdrop.addEventListener('click', hideImageModal);
    }

    // ESC key to close
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        hideImageModal();
      }
    });

    // Match heights on load and resize
    matchHeights();
    window.addEventListener('resize', matchHeights);
    
    // Also match heights after a short delay to ensure all content is loaded
    setTimeout(matchHeights, 100);
    setTimeout(matchHeights, 500);
  }

  // Run init when DOM is loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
