const fileInput = document.getElementById("fileInput");
const fileList = document.getElementById("fileList");
const dropArea = document.getElementById("dropArea");

let files = [];

fileInput.addEventListener("change", (e) => {
  files = [...e.target.files];
  renderFiles();
});

dropArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropArea.style.borderColor = "#38bdf8";
});

dropArea.addEventListener("drop", (e) => {
  e.preventDefault();
  files = [...e.dataTransfer.files];
  renderFiles();
});

function renderFiles() {
  if (files.length === 0) {
    fileList.innerHTML = "No files added";
    return;
  }

  fileList.innerHTML = "";

  files.forEach((f, i) => {
    const div = document.createElement("div");
    div.textContent = `📄 ${f.name}`;
    fileList.appendChild(div);
  });
}

function uploadFiles() {
  if (files.length === 0) {
    alert("No files selected");
    return;
  }

  alert(`Uploading ${files.length} file(s) to TwinThink pipeline...`);

  // later: Flask + RAG pipeline here
}