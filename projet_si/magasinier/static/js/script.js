function goToStockMagasin(){
    var currentPath = window.location.pathname;
    var newPath = currentPath.replace('gestion_magasin', 'stock_magasin');  
    window.location.href = newPath;
}

function goToGererAchat(){
    var currentPath = window.location.pathname;
    var newPath = currentPath.replace('gestion_magasin', 'gerer_achat');  
    window.location.href = newPath;
}
function goToGererEmploye(){
    var currentPath = window.location.pathname;
    var newPath = currentPath.replace('gestion_magasin', 'gerer_employe');  
    window.location.href = newPath;
}
function goToStat() {
    window.location.href = "{% url 'statistiques' %}";
}
function printProducts() {
    window.print();
}