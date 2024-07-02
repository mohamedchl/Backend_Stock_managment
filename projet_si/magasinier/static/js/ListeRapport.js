function confirmDelete(selected_center, rapport_id) {
    var modal = document.getElementById('confirmationModal');
    modal.style.display = 'block';

    // Handle confirm action
    var confirmButton = document.querySelector('.confirm-button');
    confirmButton.addEventListener('click', function () {
        window.location.href = `/${selected_center}/gerer_employeRes/supprimer_rapport/${rapport_id}/`;
    }); 

    // Handle cancel action and close button
    var cancelButton = document.querySelector('.cancel-button');
    var closeButton = document.querySelector('.close');

    cancelButton.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    closeButton.addEventListener('click', function () {
        modal.style.display = 'none';
    });
}
function printProducts() {
    window.print();
}