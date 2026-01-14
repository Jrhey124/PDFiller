// student_fields.js

function addStudentField() {
  const container = document.getElementById('student-fields');
  const entry = document.createElement('div');
  entry.className = 'student-entry flex gap-2';

  const input = document.createElement('input');
  input.type = 'text';
  input.name = 'students';
  input.required = true;
  input.placeholder = 'Enter student name';
  input.className = 'flex-1 px-3 py-2.5 border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#ffd60a] focus:border-[#ffd60a] text-sm bg-white';

  const removeBtn = document.createElement('button');
  removeBtn.type = 'button';
  removeBtn.textContent = 'Remove';
  removeBtn.className = 'remove-btn px-3 py-2.5 border-2 border-gray-300 text-gray-700 rounded-md text-sm font-medium hover:bg-[#ffd60a] hover:text-black hover:border-[#ffd60a] transition-all duration-200';
  removeBtn.onclick = function () {
    removeStudentField(removeBtn);
  };

  entry.appendChild(input);
  entry.appendChild(removeBtn);
  container.appendChild(entry);
  
  // Add animation
  entry.style.opacity = '0';
  entry.style.transform = 'translateY(-10px)';
  setTimeout(() => {
    entry.style.transition = 'all 0.3s ease-out';
    entry.style.opacity = '1';
    entry.style.transform = 'translateY(0)';
  }, 10);
}

function removeStudentField(button) {
  const entry = button.parentNode;
  entry.style.opacity = '0';
  entry.style.transform = 'translateX(-10px)';
  entry.style.transition = 'all 0.2s ease';
  setTimeout(() => {
    entry.remove();
  }, 200);
}