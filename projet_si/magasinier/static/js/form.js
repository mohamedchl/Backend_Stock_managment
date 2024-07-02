document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.querySelector('.file-input');
    const fileLabel = document.querySelector('.file-label');

    fileLabel.addEventListener('click', function () {
        fileInput.click();
    });

    fileInput.addEventListener('change', function () {
        fileLabel.textContent = this.files[0].name;
    });
});
