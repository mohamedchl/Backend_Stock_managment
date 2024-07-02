from django.db import models
from datetime import datetime
from calendar import monthrange

class Produit(models.Model):
    nomP = models.CharField(max_length=50, default = 'Produit')
    designation = models.CharField(max_length=100, null=True)
    qte = models.IntegerField(default=0)
    prix_unitaire = models.FloatField(max_length=10, default=0)
    prix_total = models.FloatField(max_length=10, default=0)
    def __str__(self):
        return self.nomP
    
class Centre(models.Model):
    id = models.AutoField(primary_key=True)
    numC = models.IntegerField(default=0)
    designation = models.CharField(max_length=100, null=True)
    def __str__(self):
        return f"Centre {self.numC}"


class Stock_centre_primaire(models.Model):#cette classe contient stock centre des produit primaire
    Centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    nomP = models.CharField(max_length=50, default = 'Produit')
    designation = models.CharField(max_length=100, null=True)
    qte = models.IntegerField(default=1)
    prix_unitaire = models.FloatField(max_length=10, default=0)
    def __str__(self):
        return self.nomP

class reProduit(models.Model):#cette classe contient stock des produit reproduit
    nomP = models.CharField(max_length=50, default = 'Produit')
    Centre = models.ForeignKey(Centre, on_delete=models.CASCADE, default=0)
    Produit_primaire = models.ForeignKey(Stock_centre_primaire,on_delete=models.CASCADE)
    qte_Produit_primaire=models.IntegerField(default=1)
    designation = models.CharField(max_length=100, null=True)
    qte_reProduit= models.IntegerField(default=1)
    prix_unitaire = models.FloatField(max_length=10, default=0)
    def __str__(self):
        return self.nomP
        

class Transfer(models.Model):
    produit_transfer = models.ForeignKey(Produit, on_delete=models.CASCADE)
    Date_transfer= models.DateField(default=datetime.now)
    Centre_transfer = models.ForeignKey(Centre, on_delete=models.CASCADE)
    Qte = models.IntegerField()
    @property
    def designation(self):
        return self.produit_transfer.designation
    @property
    def prix_unitaire(self):
        return self.produit_transfer.prix_unitaire
    @property
    def cout(self):
        return self.prix_unitaire * self.Qte

class Client(models.Model):
    nomCl = models.CharField(max_length=50,unique=True)
    prenomCl = models.CharField(max_length=50)
    adrCl = models.CharField(max_length=50)
    telephone = models.BigIntegerField()
    credit = models.FloatField(max_length=10, default=0)
    somme_paye= models.FloatField(max_length=10, default=0)
    def __str__(self):
        return self.nomCl
    
class paye_credit(models.Model):
    nom = models.ForeignKey(Client, on_delete = models.CASCADE)
    date_modification= models.DateField(default=datetime.now)
    @property
    def credit(self):
        return self.nom.credit
    
class Achats_client(models.Model):
     Date_achat = models.DateField(default=datetime.now)
     Client = models.ForeignKey(Client, on_delete = models.CASCADE)
     Produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
     qte = models.IntegerField(default=1)
     prix_unitaire= models.FloatField(max_length=10, default=0)
     somme_paye =models.FloatField(max_length=10, default=0)
     @property
     def cout(self):
        return self.prix_unitaire * self.qte

class Achats_client_centre(models.Model):
     Date_achat = models.DateField(default=datetime.now)
     Client = models.ForeignKey(Client, on_delete = models.CASCADE)
     produit_primaire=models.ForeignKey(Stock_centre_primaire, on_delete=models.CASCADE,null=True, default=None)
     reproduit=models.ForeignKey(reProduit, on_delete=models.CASCADE, null=True, default=None)
     Centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
     qte = models.IntegerField(default=1)
     prix_unitaire= models.FloatField(max_length=10, default=0)
     somme_paye =models.FloatField(max_length=10, default=0)
     @property
     def cout(self):
        return self.prix_unitaire * self.qte

class Magasinier(models.Model):
    nomM = models.CharField(max_length=50)
    prenomM = models.CharField(max_length=50)

class Produit_Fournisseur(models.Model):
    nomP = models.CharField(max_length=50, default = 'Produit')
    designation = models.CharField(max_length=100,default='des')
    qte = models.IntegerField(default=0)
    prix_unitaire = models.FloatField(max_length=10, default=0)

class Fournisseur(models.Model):
    nomF = models.CharField(max_length=50)
    prenomF = models.CharField(max_length=50)
    adrF = models.CharField(max_length=50)
    telephone = models.BigIntegerField()
    solde = models.FloatField(max_length=10, default=0)
    produits_fournisseur = models.ManyToManyField(Produit_Fournisseur, related_name='Fournisseurs')

class Payement_sold_fournisseur(models.Model):
    Date_payement = models.DateField(default=datetime.now)
    fournisseur = models.ForeignKey(Fournisseur,on_delete=models.CASCADE)
    montant_payé = models.FloatField(max_length=10, default=0)

#class Date_achat(models.Model):
#   Date_achat = models.DateField(default=datetime.now)

class Achats_matiereP(models.Model):
       Date_achat = models.DateTimeField(default=datetime.now)
       Fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
       Produit_Fournisseur = models.ForeignKey(Produit_Fournisseur, on_delete=models.CASCADE)
       qte = models.IntegerField(default=1)
       Montant_achat = models.FloatField(max_length=10, default=0)
       Montant_payé = models.FloatField(max_length=10, default=0) 
       sold_achat = models.FloatField(max_length=10, default=0)
       Produit = models.ForeignKey(Produit,on_delete=models.CASCADE,default=None)

class Employe(models.Model):
    nomE = models.CharField(max_length=50)
    prenomE = models.CharField(max_length=50)
    adrE = models.CharField(max_length=50)
    telephone = models.BigIntegerField()
    Salarie_jour = models.FloatField(default=0)  # 'max_length' isn't needed for FloatField
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)

    def monthly_salary(self, year, month):
        days_in_month = monthrange(year, month)[1]
        return self.Salarie_jour * days_in_month

    def __str__(self):
        return self.nomE

class Absence_employe(models.Model):
    Date_absence = models.DateField(default=datetime.now, unique = True)
    Employe_absente = models.ManyToManyField(Employe,related_name='date_absence')

class Responsable(models.Model):
     nomR = models.CharField(max_length=50)
     prenomR = models.CharField(max_length=50)
     adrR = models.CharField(max_length=50)
     telephone = models.BigIntegerField()
     centre = models.ForeignKey(Centre, on_delete = models.CASCADE)
     def __str__(self):
        return self.nomR

class Demande_massrouf(models.Model):
    Date_dem = models.DateField(default=datetime.now)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    responsable = models.ForeignKey(Responsable, on_delete=models.CASCADE)
    massrouf = models.FloatField(max_length=10, default=0)

class Rapport_responsable(models.Model):
    Date_R = models.DateField(default=datetime.now)
    Rapport = models.FileField(upload_to='pdfs/', default=None)
    responsable = models.ForeignKey(Responsable, on_delete=models.CASCADE, default=1)
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE, default=1)
    demandes_massrouf = models.ManyToManyField(Demande_massrouf, related_name='rapports')

class Employe_salarie(models.Model):
    année = models.BigIntegerField(default = 1)
    mois = models.CharField(max_length=10)
    employe = models.ForeignKey(Employe,on_delete=models.CASCADE)
    massrouf_total = models.FloatField(max_length=10, default=0)
    absences_count = models.IntegerField(default=0)
    Salarie = models.FloatField(max_length=10, default=0)


class compteMagazinier(models.Model):
    username = models.CharField(max_length=20,default=None)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    confirm_password = models.CharField(max_length=20,default = None)

class compteResponsable(models.Model):
    username = models.CharField(max_length=20,default=None)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    confirm_password = models.CharField(max_length=20 ,default = None)
    responsable = models.ForeignKey(Responsable,on_delete = models.CASCADE)