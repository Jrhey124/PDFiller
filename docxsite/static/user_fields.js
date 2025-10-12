// student_fields.js

function addStudentField() {
  const container = document.getElementById('student-fields');
  const entry = document.createElement('div');
  entry.className = 'student-entry';

  const input = document.createElement('input');
  input.type = 'text';
  input.name = 'students';
  input.required = true;

  const removeBtn = document.createElement('button');
  removeBtn.type = 'button';
  removeBtn.textContent = '–';
  removeBtn.onclick = function () {
    removeStudentField(removeBtn);
  };

  entry.appendChild(input);
  entry.appendChild(removeBtn);
  container.appendChild(entry);
}

function removeStudentField(button) {
  const entry = button.parentNode;
  entry.remove();
}