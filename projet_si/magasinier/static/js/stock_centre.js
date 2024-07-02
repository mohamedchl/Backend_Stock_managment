function confirmDelete(selected_center, reproduit_id) {
    var modal = document.getElementById('confirmationModal');
    modal.style.display = 'block';

    // Handle confirm action
    document.querySelector('.confirm-button').addEventListener('click', function() {
        var url = `/${selected_center}/supprimer_reProduit/${reproduit_id}/`;
        window.location.href = url;
    });

    // Handle cancel action
    document.querySelector('.cancel-button').addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Handle close button
    document.querySelector('.close').addEventListener('click', function() {
        modal.style.display = 'none';
    });
}
function printProducts() {
    window.print();
}