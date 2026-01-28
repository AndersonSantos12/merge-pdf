document.addEventListener("DOMContentLoaded", function () {
  const input = document.querySelector('input[type="file"][name="pdfs"]');
  const list = document.getElementById("pdf-list");
  const instructions = document.getElementById("order-instructions");
  if (!input) return;

  input.addEventListener("change", function (e) {
    const fileList = Array.from(input.files);
    list.innerHTML = "";
    if (fileList.length > 1 && instructions)
      instructions.style.display = "block";
    else if (instructions) instructions.style.display = "none";
    fileList.forEach((file, idx) => {
      const li = document.createElement("li");
      li.innerHTML = '<span class="drag-icon">&#x2630;</span> ' + file.name;
      li.draggable = true;
      li.dataset.index = idx;
      list.appendChild(li);
    });
    makeListSortable(list, input);
  });

  function makeListSortable(list, input) {
    let dragSrcEl = null;
    list.addEventListener("dragstart", function (e) {
      if (e.target.tagName !== "LI") return;
      dragSrcEl = e.target;
      e.target.classList.add("dragging");
      e.dataTransfer.effectAllowed = "move";
    });
    list.addEventListener("dragend", function (e) {
      if (e.target.tagName !== "LI") return;
      e.target.classList.remove("dragging");
    });
    list.addEventListener("dragover", function (e) {
      e.preventDefault();
      const afterElement = getDragAfterElement(list, e.clientY);
      const dragging = list.querySelector(".dragging");
      if (afterElement == null) {
        list.appendChild(dragging);
      } else {
        list.insertBefore(dragging, afterElement);
      }
    });
    list.addEventListener("drop", function (e) {
      e.preventDefault();
      reorderFiles(input, list);
    });
  }
  function getDragAfterElement(list, y) {
    const draggableElements = [...list.querySelectorAll("li:not(.dragging)")];
    return draggableElements.reduce(
      (closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
          return { offset: offset, element: child };
        } else {
          return closest;
        }
      },
      { offset: -Infinity },
    ).element;
  }
  function reorderFiles(input, list) {
    const order = Array.from(list.children).map((li) =>
      li.textContent.trim().replace(/^\u2630\s*/, ""),
    );
    const files = Array.from(input.files);
    const newFiles = order.map((name) => files.find((f) => f.name === name));
    const dt = new DataTransfer();
    newFiles.forEach((f) => dt.items.add(f));
    input.files = dt.files;
  }
});
