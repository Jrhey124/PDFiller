document.addEventListener('DOMContentLoaded', function () {
  const dataScript = document.getElementById('addressee-data');
  const addresseeOptionsContainer = document.getElementById('addressee-options');
  const addresseeDetails = document.getElementById('addressee-details');
  const addresseeHiddenInput = document.getElementById('addressee');
  const addresseeSelect = document.getElementById('addressee-select');

  if (!dataScript || !addresseeOptionsContainer) return;

  const names = JSON.parse(dataScript.textContent);

  // Populate addressee options
  names.forEach(name => {
    const option = document.createElement('div');
    option.className = 'custom-option';
    option.setAttribute('data-value', name);
    option.textContent = name;
    addresseeOptionsContainer.appendChild(option);
    
    // Add click handler
    option.addEventListener('click', function(e) {
      e.stopPropagation();
      const value = this.getAttribute('data-value');
      const text = this.textContent;
      
      // Update UI
      const allOptions = addresseeOptionsContainer.querySelectorAll('.custom-option');
      allOptions.forEach(opt => opt.classList.remove('selected'));
      this.classList.add('selected');
      
      const trigger = addresseeSelect.querySelector('.custom-select-trigger');
      const selectedValue = trigger.querySelector('.selected-value');
      selectedValue.textContent = text;
      selectedValue.classList.remove('text-gray-400');
      
      // Update hidden input
      addresseeHiddenInput.value = value;
      
      // Show details
      if (addresseeDetails) {
        addresseeDetails.textContent = value;
        addresseeDetails.classList.remove('hidden');
      }
      
      // Close dropdown
      addresseeSelect.classList.remove('open');
    });
  });
});