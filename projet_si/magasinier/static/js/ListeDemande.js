function confirmDelete(selected_center,demande_id){
    var modal = document.getElementById('confirmationModal');
    modal.style.display = 'block';

    // Handle confirm action
    document.querySelector('.confirm-button').addEventListener('click', function() {
        window.location.href = `/${selected_center}/gerer_employeRes/supprmier_demande/${demande_id}/`;
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