const fileInput = document.getElementById("fileInput");
const fileList = document.getElementById("fileList");
const dropArea = document.getElementById("dropArea");

let files = [];

/* =========================
   FILE SELECT
========================= */
fileInput.addEventListener("change", (e) => {
  files = Array.from(e.target.files);
  renderFiles();
});

/* =========================
   DRAG OVER
========================= */
dropArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropArea.style.borderColor = "#06B6D4";
});

/* =========================
   DRAG LEAVE
========================= */
dropArea.addEventListener("dragleave", () => {
  dropArea.style.borderColor = "#334155";
});

/* =========================
   DROP FILES
========================= */
dropArea.addEventListener("drop", (e) => {
  e.preventDefault();
  files = Array.from(e.dataTransfer.files);
  dropArea.style.borderColor = "#334155";
  renderFiles();
});

/* =========================
   RENDER FILE LIST
========================= */
function renderFiles() {
  fileList.innerHTML = "";

  if (files.length === 0) {
    fileList.innerHTML = `<p style="color:#64748b;">No files added</p>`;
    return;
  }

  files.forEach((file) => {
    const div = document.createElement("div");
    div.style.padding = "8px 0";
    div.style.borderBottom = "1px solid rgba(255,255,255,0.05)";

    div.innerHTML = `
      📄 ${file.name}
      <span style="color:#64748b;font-size:12px;">
        (${(file.size / 1024).toFixed(1)} KB)
      </span>
    `;

    fileList.appendChild(div);
  });
}

/* =========================
   UPLOAD ENGINE (FIXED)
========================= */
async function uploadFiles() {

  if (files.length === 0) {
    alert("No files selected");
    return;
  }

  const uploadBtn = document.querySelector(".upload-btn");

  uploadBtn.innerText = "Uploading...";
  uploadBtn.disabled = true;

  try {

    const formData = new FormData();

    files.forEach(file => {
      formData.append("files", file);
    });

    const response = await fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData
    });

    const data = await response.json();
    console.log("Upload response:", data);

    if (!data.success) {
      throw new Error(data.message || "Upload failed");
    }

    uploadBtn.innerText = "Upload Complete ✔";

    setTimeout(() => {
      uploadBtn.innerText = "Execute Upload";
      uploadBtn.disabled = false;
      files = [];
      renderFiles();
    }, 1200);

  } catch (err) {

    console.error("Upload error:", err);

    uploadBtn.innerText = "Upload Failed ✖";

    setTimeout(() => {
      uploadBtn.innerText = "Execute Upload";
      uploadBtn.disabled = false;
    }, 1200);
  }
}