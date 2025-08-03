const form = document.getElementById('upload-form');
const resultDiv = document.getElementById('scan-result');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById('imageInput');
    if (!fileInput.files.length) {
        alert("Please select an image file.");
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    // Clear previous results
    resultDiv.innerHTML += "Processing...";

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.text();
            resultDiv.textContent = `Error: ${error}`;
            return;
        }

        // Get image blob from response
        const blob = await response.blob();

        // Create local URL and show image
        const imgUrl = URL.createObjectURL(blob);
        resultDiv.innerHTML = `<img src="${imgUrl}" style="max-width:100%; height:auto;" />`;

    } catch (err) {
        resultDiv.textContent = `Error: ${err.message}`;
    }
});
