/**
 * Range Slider Component
 * Manages a range slider with 5 positions (0-4) representing 4 size categories
 * Positions: 0cm(0), 10cm(1), 20cm(2), 35cm(3), 60cm(4)
 * Categories: <10cm, 10-20cm, 20-35cm, 35-60cm
 */

let tailleRange = [0, 4]; // Default: all sizes selected

// Configuration
const STEP_POSITIONS = [0, 25, 50, 75, 100]; // Position percentages
const SCALE_MARKS = [
  { value: '0 cm', position: 0 },
  { value: '10 cm', position: 25 },
  { value: '20 cm', position: 50 },
  { value: '35 cm', position: 75 },
  { value: '60 cm', position: 100 }
];

/**
 * Build the taille range slider with draggable handles
 * @param {Array} taillesOrder - Ordered array of taille category values
 * @param {HTMLElement} tailleSliderContainer - Container element for the slider
 * @param {Function} onRangeChange - Callback function when range changes
 * @returns {Object} API with updateRangeVisuals and reset methods
 */
function buildTailleSlider(taillesOrder, tailleSliderContainer, onRangeChange) {
  // State
  let isDragging = false;
  let dragHandle = null;
  
  // DOM elements
  const elements = createSliderElements(taillesOrder);
  tailleSliderContainer.appendChild(elements.wrapper);
  
  // Event handlers
  setupEventListeners();
  
  // Initialize
  setTimeout(updateRangeVisuals, 100);
  
  // Public API
  return {
    updateRangeVisuals,
    reset: () => {
      tailleRange = [0, 4];
      updateRangeVisuals();
      if (onRangeChange) onRangeChange();
    }
  };
  
  // --- Helper Functions ---
  
  /**
   * Create all DOM elements for the slider
   */
  function createSliderElements(taillesOrder) {
    const wrapper = document.createElement('div');
    wrapper.className = 'relative py-14 md:py-12 px-2 md:px-4 overflow-visible';
    
    // Track elements
    const track = createTrack();
    const activeTrack = createActiveTrack();
    
    // Scale and labels
    const { container: scaleContainer, ticks } = createScaleMarks();
    
    // Clickable areas for each category
    const clickableAreas = createClickableAreas(taillesOrder);
    
    // Draggable handles
    const startHandle = createHandle('start');
    const endHandle = createHandle('end');
    
    // Append all elements
    wrapper.appendChild(track);
    wrapper.appendChild(activeTrack);
    wrapper.appendChild(scaleContainer);
    clickableAreas.forEach(area => wrapper.appendChild(area));
    wrapper.appendChild(startHandle);
    wrapper.appendChild(endHandle);
    
    return {
      wrapper,
      track,
      activeTrack,
      scaleContainer,
      ticks,
      clickableAreas,
      startHandle,
      endHandle
    };
  }
  
  function createTrack() {
    const track = document.createElement('div');
    track.className = 'absolute top-1/2 left-2 md:left-4 right-2 md:right-4 h-2 md:h-2.5 bg-slate-300 -translate-y-1/2 rounded-full cursor-pointer overflow-visible';
    return track;
  }
  
  function createActiveTrack() {
    const activeTrack = document.createElement('div');
    activeTrack.id = 'active-track';
    activeTrack.className = 'absolute top-1/2 h-2 md:h-2.5 bg-slate-900 -translate-y-1/2 rounded-full pointer-events-none overflow-visible';
    return activeTrack;
  }
  
  function createScaleMarks() {
    const container = document.createElement('div');
    container.className = 'absolute top-1/2 left-2 md:left-4 right-2 md:right-4 -translate-y-1/2 pointer-events-none';
    
    const ticks = [];
    
    SCALE_MARKS.forEach((mark, index) => {
      const labelWrapper = document.createElement('div');
      labelWrapper.className = 'flex flex-col items-center absolute';
      labelWrapper.style.left = `${mark.position}%`;
      labelWrapper.style.transform = 'translateX(-50%)';
      
      const tick = document.createElement('div');
      tick.className = 'w-0.5 h-3 md:h-4 bg-slate-400 mb-2 transition-colors';
      tick.dataset.position = index;
      ticks.push(tick);
      
      const label = document.createElement('span');
      label.className = 'text-xs md:text-sm text-slate-700 font-medium whitespace-nowrap mt-1';
      label.textContent = mark.value;
      
      labelWrapper.appendChild(tick);
      labelWrapper.appendChild(label);
      container.appendChild(labelWrapper);
    });
    
    return { container, ticks };
  }
  
  function createClickableAreas(taillesOrder) {
    const areas = [];
    
    // Create clickable areas for each category (0-3)
    // Category 0: 0% to 25% (positions 0-1)
    // Category 1: 25% to 50% (positions 1-2)
    // Category 2: 50% to 75% (positions 2-3)
    // Category 3: 75% to 100% (positions 3-4)
    for (let categoryIndex = 0; categoryIndex < taillesOrder.length; categoryIndex++) {
      const area = document.createElement('div');
      area.className = 'absolute top-1/2 h-10 md:h-8 -translate-y-1/2 cursor-pointer hover:bg-slate-100 hover:bg-opacity-30 transition-colors rounded';
      area.dataset.categoryIndex = categoryIndex;
      
      const startPercent = STEP_POSITIONS[categoryIndex];
      const endPercent = STEP_POSITIONS[categoryIndex + 1];
      
      area.style.left = `calc(${startPercent}% + ${categoryIndex === 0 ? '0.5rem' : '0px'})`;
      area.style.width = `calc(${endPercent - startPercent}% - ${categoryIndex === 0 ? '0.5rem' : '0px'} - ${categoryIndex === taillesOrder.length - 1 ? '0.5rem' : '0px'})`;
      
      area.addEventListener('click', () => handleCategoryClick(categoryIndex));
      areas.push(area);
    }
    
    return areas;
  }
  
  function createHandle(type) {
    const handle = document.createElement('div');
    handle.className = 'absolute top-1/2 w-7 h-7 md:w-6 md:h-6 rounded-full bg-slate-900 -translate-x-1/2 -translate-y-1/2 cursor-grab active:cursor-grabbing hover:scale-110 transition-transform shadow-lg border-2 md:border-3 border-white';
    handle.dataset.handle = type;
    handle.style.zIndex = '20';
    return handle;
  }
  
  // --- Event Handling Functions ---
  
  /**
   * Handle click on a category area (0-3)
   * Maps category to position range (category N = positions N to N+1)
   */
  function handleCategoryClick(categoryIndex) {
    const [start, end] = tailleRange;
    const positionStart = categoryIndex; // Start position of this category
    const positionEnd = categoryIndex + 1; // End position of this category
    
    // Determine which handle to move
    if (positionEnd <= start) {
      // Category is entirely before current range - move start handle
      tailleRange[0] = positionStart;
    } else if (positionStart >= end) {
      // Category is entirely after current range - move end handle
      tailleRange[1] = positionEnd;
    } else if (positionStart >= start && positionEnd <= end) {
      // Category is inside current range - contract to just this category
      tailleRange[0] = positionStart;
      tailleRange[1] = positionEnd;
    } else {
      // Category overlaps - expand to include it
      tailleRange[0] = Math.min(start, positionStart);
      tailleRange[1] = Math.max(end, positionEnd);
    }
    
    updateRangeVisuals();
    if (onRangeChange) onRangeChange();
  }
  
  /**
   * Handle click on track - snap to nearest position
   */
  function handleTrackClick(e) {
    const trackRect = elements.track.getBoundingClientRect();
    const clickX = e.clientX - trackRect.left;
    const clickPercent = (clickX / trackRect.width) * 100;
    
    const closestIndex = findClosestPosition(clickPercent);
    handlePositionClick(closestIndex);
  }
  
  /**
   * Handle click on a specific position (0-4)
   */
  function handlePositionClick(positionIndex) {
    const [start, end] = tailleRange;
    
    if (positionIndex < start) {
      tailleRange[0] = positionIndex;
    } else if (positionIndex > end) {
      tailleRange[1] = positionIndex;
    } else if (positionIndex === start && positionIndex === end) {
      return; // Both handles at same position
    } else if (positionIndex === start) {
      if (positionIndex < end) {
        tailleRange[0] = Math.min(positionIndex + 1, end);
      }
    } else if (positionIndex === end) {
      if (positionIndex > start) {
        tailleRange[1] = Math.max(positionIndex - 1, start);
      }
    } else {
      // Inside range - move closest handle
      const distToStart = positionIndex - start;
      const distToEnd = end - positionIndex;
      if (distToStart <= distToEnd) {
        tailleRange[0] = positionIndex;
      } else {
        tailleRange[1] = positionIndex;
      }
    }
    
    updateRangeVisuals();
    if (onRangeChange) onRangeChange();
  }
  
  /**
   * Find closest position index for a given percentage
   */
  function findClosestPosition(percent) {
    let closestIndex = 0;
    let minDist = Math.abs(percent - STEP_POSITIONS[0]);
    
    for (let i = 1; i < STEP_POSITIONS.length; i++) {
      const dist = Math.abs(percent - STEP_POSITIONS[i]);
      if (dist < minDist) {
        minDist = dist;
        closestIndex = i;
      }
    }
    
    return closestIndex;
  }
  
  // --- Drag Functions ---
  
  function getClientX(e) {
    return e.type.includes('touch') ? e.touches[0].clientX : e.clientX;
  }
  
  function startDrag(handle, e) {
    isDragging = true;
    dragHandle = handle;
    handle.classList.remove('hover:scale-110');
    handle.style.transform = 'translate(-50%, -50%) scale(1.1)';
    e.preventDefault();
    e.stopPropagation();
  }
  
  function onDrag(e) {
    if (!isDragging || !dragHandle) return;
    
    e.preventDefault();
    
    const trackRect = elements.track.getBoundingClientRect();
    const mouseX = getClientX(e) - trackRect.left;
    const mousePercent = Math.max(0, Math.min(100, (mouseX / trackRect.width) * 100));
    
    const closestIndex = findClosestPosition(mousePercent);
    const [currentStart, currentEnd] = tailleRange;
    
    if (dragHandle.dataset.handle === 'start') {
      if (closestIndex <= currentEnd) {
        tailleRange[0] = closestIndex;
        updateRangeVisuals();
      }
    } else if (dragHandle.dataset.handle === 'end') {
      if (closestIndex >= currentStart) {
        tailleRange[1] = closestIndex;
        updateRangeVisuals();
      }
    }
  }
  
  function endDrag() {
    if (isDragging) {
      if (dragHandle) {
        dragHandle.classList.add('hover:scale-110');
        dragHandle.style.transform = '';
      }
      if (onRangeChange) onRangeChange();
    }
    isDragging = false;
    dragHandle = null;
  }
  
  // --- Visual Update ---
  
  function updateRangeVisuals() {
    const [start, end] = tailleRange;
    const startPos = STEP_POSITIONS[start];
    const endPos = STEP_POSITIONS[end];
    
    // Update handle positions
    elements.startHandle.style.left = `${startPos}%`;
    elements.endHandle.style.left = `${endPos}%`;
    
    // Update active track
    elements.activeTrack.style.left = `${startPos}%`;
    elements.activeTrack.style.width = `${endPos - startPos}%`;
    
    // Update tick colors
    elements.ticks.forEach((tick, index) => {
      if (index >= start && index <= end) {
        tick.classList.remove('bg-slate-400');
        tick.classList.add('bg-slate-900');
      } else {
        tick.classList.remove('bg-slate-900');
        tick.classList.add('bg-slate-400');
      }
    });
  }
  
  // --- Event Listeners Setup ---
  
  function setupEventListeners() {
    // Track click
    elements.track.addEventListener('click', handleTrackClick);
    
    // Handle drag (mouse)
    elements.startHandle.addEventListener('mousedown', (e) => startDrag(elements.startHandle, e));
    elements.endHandle.addEventListener('mousedown', (e) => startDrag(elements.endHandle, e));
    
    // Handle drag (touch)
    elements.startHandle.addEventListener('touchstart', (e) => startDrag(elements.startHandle, e), { passive: false });
    elements.endHandle.addEventListener('touchstart', (e) => startDrag(elements.endHandle, e), { passive: false });
    
    // Global drag listeners
    document.addEventListener('mousemove', onDrag);
    document.addEventListener('touchmove', onDrag, { passive: false });
    document.addEventListener('mouseup', endDrag);
    document.addEventListener('touchend', endDrag);
    
    // Window resize
    let resizeTimeout;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(updateRangeVisuals, 100);
    });
  }
}

/**
 * Get the current selected taille range
 * @returns {Array} Current range [start, end]
 */
function getSelectedTailleRange() {
  return tailleRange;
}
