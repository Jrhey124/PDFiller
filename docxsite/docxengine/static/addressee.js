document.addEventListener('DOMContentLoaded', function () {
  const dataScript = document.getElementById('addressee-data');
  const addresseeSelect = document.getElementById('addressee');

  if (!dataScript || !addresseeSelect) return;

  const names = JSON.parse(dataScript.textContent);

  names.forEach(name => {
    const option = document.createElement('option');
    option.value = name;
    option.textContent = name;
    addresseeSelect.appendChild(option);
  });
});