document.addEventListener("DOMContentLoaded", function () {
  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("file-input");
  const fileName = document.getElementById("file-name");

  // Open file picker on click
  dropZone.addEventListener("click", function () {
    fileInput.click();
  });

  // Highlight while dragging
  dropZone.addEventListener("dragover", function (e) {
    e.preventDefault();
    dropZone.classList.add("dragover");
  });

  // Remove highlight
  dropZone.addEventListener("dragleave", function () {
    dropZone.classList.remove("dragover");
  });

  // Handle file drop
  dropZone.addEventListener("drop", function (e) {
    e.preventDefault();

    dropZone.classList.remove("dragover");

    const files = e.dataTransfer.files;

    if (files.length > 0) {
      fileName.textContent = files[0].name;

      // Put dropped file into input
      const dataTransfer = new DataTransfer();

      for (let i = 0; i < files.length; i++) {
        dataTransfer.items.add(files[i]);
      }

      fileInput.files = dataTransfer.files;
    }
  });

  // Handle browse selection
  fileInput.addEventListener("change", function () {
    if (fileInput.files.length > 0) {
      fileName.textContent = fileInput.files[0].name;
    }
  });
});