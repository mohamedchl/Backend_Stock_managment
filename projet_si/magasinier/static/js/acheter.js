function calculerMontant(prixProduit){
    document.getElementById('qte').addEventListener('input', function () {
        var qte = document.getElementById('qte').value;
        var montant = qte*prixProduit;
        document.getElementById('message').innerHTML="la montant de cette achat est"+montant;
    });
    document.getElementById('section2').style.display='block';
}
function printProducts() {
    window.print();
}