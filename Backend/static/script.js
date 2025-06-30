const imageUpload = document.getElementById('imageUpload');
const imagePreview = document.getElementById('imagePreview');
const submitBtn = document.getElementById('submitBtn');
const resultBox = document.getElementById('result');
const loading = document.getElementById('loading');

imageUpload.addEventListener('change', () => {
    const file = imageUpload.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreview.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
});

submitBtn.addEventListener('click', async () => {
    const file = imageUpload.files[0];
    if (!file) {
        resultBox.textContent = "Please select an image first.";
        return;
    }

    loading.classList.remove('hidden');
    resultBox.textContent = "";

    const formData = new FormData();
    formData.append("image", file);

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.annotated_image) {
            imagePreview.src = data.annotated_image;
            imagePreview.classList.remove('hidden');
        }

        if (data.explanation) {
            resultBox.textContent = data.explanation;
        } else if (data.error) {
            resultBox.textContent = "Error: " + data.error;
        } else {
            resultBox.textContent = "Something went wrong.";
        }
    } catch (error) {
        resultBox.textContent = "Error: " + error.message;
    } finally {
        loading.classList.add('hidden');
    }
});
