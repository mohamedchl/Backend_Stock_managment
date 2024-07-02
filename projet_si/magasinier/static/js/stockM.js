function confirmDelete(produitId) {
    var modal = document.getElementById('confirmationModal');
    modal.style.display = 'block';

    // Handle confirm action
    document.querySelector('.confirm-button').addEventListener('click', function() {
        window.location.href = `/stock_magasin/supprimer_produit/${produitId}/`;
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