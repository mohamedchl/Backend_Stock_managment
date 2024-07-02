from django.shortcuts import render, redirect, get_object_or_404
from .models import Produit,reProduit, Magasinier, Fournisseur, Produit_Fournisseur,Achats_matiereP, Centre, Employe, Responsable,Absence_employe,Achats_client,Rapport_responsable,Client,Stock_centre_primaire,Transfer,paye_credit,Achats_client_centre,Fournisseur, Produit_Fournisseur,Achats_matiereP, Centre, Employe, Responsable,Absence_employe,Rapport_responsable,Client,Payement_sold_fournisseur,Demande_massrouf,Employe_salarie,compteMagazinier,compteResponsable
from django.contrib import messages
from .forms import ProduitForm,FournisseurForm,TransferForm,reProduitForm,ClientForm,Achats_clientform,creditForm,Achats_client_centreform,AchatMPForm,EmployeForm,AbsenceEmployeForm,PaimentSoldForm,FournisseurPForm,AbsenceEmployeDForm,DemandeMassroufForm,RapportForm,compteMagazinierForm,compteResponsableForm
import datetime ,io,base64
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
from django.urls import reverse
import calendar
from collections import defaultdict
import datetime
from django.utils.safestring import mark_safe
import matplotlib.pyplot as plt
import numpy as np
from calendar import monthrange

from django.shortcuts import render
from .forms import compteMagazinierForm

def creerCompteMagazinier(request):
    mssg = ""
    
    if request.method == 'POST':
        form = compteMagazinierForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            
            if compteMagazinier.objects.exists():
                mssg = "Vous avez créé un compte déjà !!"
            else:
                pas1 = form.cleaned_data['password']
                pas2 = form.cleaned_data['confirm_password']
                
                if pas1 != pas2:
                    mssg = "Le mot de passe n'est pas le même !!"
                else:
                    form.save()
                    mssg = "Compte créé avec succès !"
                    return render(request, 'creerCompteMagazinier.html', {"form": form, "message": mssg}) 
    else:
        form = compteMagazinierForm()  # Use compteMagazinierForm here
        mssg = "Veuillez remplir tous les champs!"

    return render(request, 'creerCompteMagazinier.html', {"form": form, "message": mssg})


from django.shortcuts import render
from .forms import compteResponsableForm

def creerCompteResponsable(request):
    mssg = ""
    
    if request.method == 'POST':
        form = compteResponsableForm(request.POST)
        
        if form.is_valid():
            responsable = form.cleaned_data['responsable']
            
            if compteResponsable.objects.filter(responsable=responsable).exists():
                mssg = "Vous avez créé un compte déjà !!"
            else:
                email = form.cleaned_data['email']
                if compteResponsable.objects.filter(email=email).exists():
                    mssg="Ce compte existe déja !!"
                else:
                    pas1 = form.cleaned_data['password']
                    pas2 = form.cleaned_data['confirm_password']
                    
                    if pas1 != pas2:
                        mssg = "Le mot de passe n'est pas le même !!"
                    else:
                        form.save()
                        mssg = "Compte créé avec succès !"
                        return render(request, 'creerCompteResponsable.html', {"form": form, "message": mssg}) 
    else:
        form = compteResponsableForm() 
        mssg = "Veuillez remplir tous les champs!"

    return render(request, 'creerCompteResponsable.html', {"form": form, "message": mssg})

def afficher(request):
    return render(request,"homepage.html")

from django.shortcuts import get_object_or_404

def afficherA(request):
    email = request.GET.get('email')
    password = request.GET.get('password')
    mssg = ""

    try:
        compteM = compteMagazinier.objects.get(email=email)
        
        if compteM.password != password:
            mssg = "Le mot de passe n'est pas correct !!"
        else:
            return redirect('magazinier')
    
    except compteMagazinier.DoesNotExist:
        try:
            compteR = compteResponsable.objects.get(email=email)
            
            if compteR.password != password:
                mssg = "Le mot de passe n'est pas correct !!"
            else:
                return redirect(reverse('gestion_responsable', kwargs={'selected_center': compteR.responsable.id}))
        
        except compteResponsable.DoesNotExist:
            mssg = ""
    return render(request, "Acceuil.html", {"message": mssg})


def gerer_centres(request):
    return render(request, "gerer_centres.html")

def choisirE(request):
    return render(request,"choisirE.html")

def choisir_statistiques(request):
    return render(request,"choisir_statistiques.html")

def choisir_option_achat(request):
    return render(request,"choisir_option_achat.html")

def gerer_employeRes(request,selected_center):
    return render(request,'gerer_employeRes.html',{"selected_center":selected_center})

def afficher_produits(request):
    cherch = request.GET.get('chercher')
    produits = Produit.objects.all() 
    if cherch:
        produits = produits.filter(nomP__startswith=cherch)
    total_cout = sum(produit.prix_total for produit in produits)
    return render(request,"stock_magasin.html",{"produits":produits,"total_cout":total_cout})

def supprimer_produit(request, produit_id):
    product = get_object_or_404(Produit, pk=produit_id)
    product.delete()
    return redirect('stock_magasin')


def modifier_produit(request,produit_id):
    produit=Produit.objects.get(id=produit_id) 
    if request.method=='POST':
        form =ProduitForm(request.POST, instance=produit)
        
        if form.is_valid():
            produit.nomP = form.cleaned_data['nomP']
            produit.designation = form.cleaned_data['designation']
            produit.qte = form.cleaned_data['qte']
            produit.prix_unitaire = form.cleaned_data['prix_unitaire']
            produit.prix_total = produit.qte*produit.prix_unitaire
            produit.save()
            return redirect('stock_magasin') 
    else:
        form=ProduitForm(instance=produit) 
        return render(request,'modifier_produit.html',{"form":form, "produit": produit})
    
   

def ajouter_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST) 

        if form.is_valid():
            nomP = form.cleaned_data['nomP']
            if Produit.objects.filter(nomP=nomP).exists():
                mssg="Ce produit existe déja ! vous pouvez le modifier dans une autre page"
            else:
                des = form.cleaned_data['designation']
                qte = form.cleaned_data['qte']
                prix_unitaire = form.cleaned_data['prix_unitaire']
                prix_total = qte*prix_unitaire
                produit = Produit(nomP=nomP,designation=des,qte=qte,prix_unitaire=prix_unitaire,prix_total=prix_total)
                produit.save()
                form = ProduitForm()
                mssg="Produit successivement créé !"
        else:
            mssg ="veuillez remplir tous les champs!"
    else:
         form = ProduitForm() #créer une instance de formulaire vierge
         mssg ="veuillez remplir tous les champs!"
    return render(request,"ajouter_produit.html",{"form":form,"message":mssg})
    

def supprimer_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)
    fournisseur.delete()
    return redirect('gerer_fournisseur')

def modifier_fournisseur(request,fournisseur_id):
    fournisseur=Fournisseur.objects.get(id=fournisseur_id) 
    if request.method=='POST':
        form =FournisseurForm(request.POST, instance=fournisseur)
        
        if form.is_valid():
            form.save()
            return redirect('gerer_fournisseur') 
    else:
        form=FournisseurForm(instance=fournisseur) 
        return render(request,'modifier_fournisseur.html',{"form":form, "produit": fournisseur})
    
def ajouter_fournisseur(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST) 

        if form.is_valid():
            form.save()
            form = FournisseurForm()
            mssg="Fournisseur successivement créé !"
        else:
            mssg ="veuillez remplir tous les champs!"
    else:
         form = FournisseurForm() #créer une instance de formulaire vierge
         mssg ="veuillez remplir tous les champs!"
    return render(request,"ajouter_fournisseur.html",{"form":form,"message":mssg})


def supprimer_fournisseurP(request, fournisseur_id, fournisseurP_id):
    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)
    produit = get_object_or_404(Produit_Fournisseur, pk=fournisseurP_id)
    fournisseur.produits_fournisseur.remove(produit)
    
    return redirect(reverse('listeProduit_fournisseur', kwargs={'fournisseur_id': fournisseur_id}))


def modifier_fournisseurP(request,fournisseur_id,fournisseurP_id):
    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)
    produit = get_object_or_404(Produit_Fournisseur, pk=fournisseurP_id)
    if request.method=='POST':
        form =FournisseurPForm(request.POST, instance=produit)
        
        if form.is_valid():
            form.save()
            return redirect(reverse('listeProduit_fournisseur', kwargs={'fournisseur_id': fournisseur_id}))
    else:
        form=FournisseurPForm(instance=produit) 
        return render(request,'modifier_produitF.html',{"form":form, "produit": produit,"fournisseur":fournisseur})



def ajouter_fournisseurP(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)

    if request.method == 'POST':
        form = FournisseurPForm(request.POST)

        if form.is_valid():
            produit = form.save(commit=False)
            produit.save()
            fournisseur.produits_fournisseur.add(produit)
            fournisseur.save()
            form = FournisseurPForm()
            mssg = "Produit successivement créé !"
        else:
            mssg = "veuillez remplir tous les champs!"
    else:
        form = FournisseurPForm()
        mssg = ""

    return render(request, "ajouter_produitF.html", {"form": form, "message": mssg, "fournisseur": fournisseur})


def acheter_matiereP(request, fournisseur_id, fournisseurP_id):
    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)
    produitF = get_object_or_404(Produit_Fournisseur, pk=fournisseurP_id)

    if request.method == 'POST':
        form = AchatMPForm(request.POST)
        if form.is_valid():
            date_achat = form.cleaned_data['Date_achat']
            qte = form.cleaned_data['qte']
            montant_payé = form.cleaned_data['Montant_payé']

            if qte > produitF.qte:
                mssg="la quantité de ce produit est trés grand !!"
            elif qte<=0 :
                mssg="la quantité doit etre sup a 0 !!"

            else:
                montant_achat = qte * produitF.prix_unitaire
                if montant_achat<montant_payé :
                    mssg="la montant payé est plus grand que la montant total d'achat !!"
                else:
                    sold_achat = (montant_achat - montant_payé)
                      
                    form = AchatMPForm()

                    fournisseur.solde = fournisseur.solde +sold_achat
                    produitF.qte = produitF.qte -qte
                    fournisseur.save()
                    produitF.save()
                    produit, created = Produit.objects.get_or_create(nomP=produitF.nomP, defaults={
                    'designation': produitF.designation,
                    'prix_unitaire': produitF.prix_unitaire
                      })
                    produit.qte += qte
                    produit.prix_total=produit.qte*produit.prix_unitaire
                    produit.save()
                    achat = Achats_matiereP(Date_achat=date_achat,Fournisseur =fournisseur,Produit_Fournisseur = produitF, qte=qte,Montant_achat=montant_achat, Montant_payé=montant_payé,sold_achat=sold_achat,Produit=produit)
                    achat.save()
                    return redirect(reverse('voirAchat', kwargs={'achat_id': achat.id}))
           
        else:
            mssg = "Veuillez remplir tous les champs!"
    else:
        form = AchatMPForm()
        mssg = ""

    return render(request, "acheter_matiereP.html", {"form": form, "message": mssg, "fournisseur": fournisseur, "produitF": produitF})



def afficher_achat(request,achat_id):
    achat = get_object_or_404(Achats_matiereP,pk=achat_id)
    fournisseur = get_object_or_404(Fournisseur,pk=achat.Fournisseur.id)
    produit = get_object_or_404(Produit_Fournisseur,pk=achat.Produit_Fournisseur.id)
    return render(request, "voirAchat.html", {"achat": achat,"fournisseur":fournisseur,"produit":produit})

from datetime import datetime as dt

def afficher_listeAchat(request):
    filter_type = request.GET.get('filter_type')
    cherch = request.GET.get('chercher')
    achat = Achats_matiereP.objects.all()

    if filter_type == 'date' and cherch:
        try:
            cherch_date = dt.strptime(cherch, '%Y-%m-%d').date()
            achat = Achats_matiereP.objects.filter(Date_achat=cherch_date)
        except ValueError:
            # Handle the case where the date format is incorrect
            # You might want to add a message or log the error
            pass
    elif filter_type == 'fournisseur' and cherch:
        achat = Achats_matiereP.objects.filter(Fournisseur__nomF__startswith=cherch)
    elif filter_type == 'produit' and cherch:
        achat = Achats_matiereP.objects.filter(Produit_Fournisseur__nomP__startswith=cherch)

    return render(request, "listeAchatsMP.html", {"achat": achat})





def supprimer_achat(request,achat_id):
    achat = get_object_or_404(Achats_matiereP, pk=achat_id)

    produitF = achat.Produit_Fournisseur
    produit = Produit.objects.get(nomP=produitF.nomP)
    fournisseur = achat.Fournisseur

    qtePF = produitF.qte+achat.qte
    produitF.qte=qtePF
    produitF.save()

    qteP = produit.qte-achat.qte
    if qteP <= 0 :
        produit.delete()
    else:
        produit.qte=qteP
        produit.prix_total=produit.prix_unitaire*produit.qte
        produit.save()

    fournisseur.solde = fournisseur.solde - achat.sold_achat
    fournisseur.save()
    achat.delete()
    return redirect('listeAchatsMP')


def afficher_employés(request):
    filter_type = request.GET.get('filter_type')
    cherch = request.GET.get('chercher')
    employe = Employe.objects.all()

    if filter_type == 'employe' and cherch:
        employe = employe.filter(nomE__startswith=cherch)
    
    if filter_type == 'centre' and cherch:
        employe = employe.filter(centre__numC__startswith=cherch)
    return render(request, "gerer_employe.html", {"employees": employe})


def ajouter_employé(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST) 

        if form.is_valid():
            form.save()
            form = EmployeForm()
            mssg="Employé successivement créé !"
    else:
         form = EmployeForm() #créer une instance de formulaire vierge
         mssg ="veuillez remplir tous les champs!"
    return render(request,"ajouter_employe.html",{"form":form,"message":mssg})

def modifier_employe(request,employe_id):
    employe=Employe.objects.get(id=employe_id) 
    if request.method=='POST':
        form =EmployeForm(request.POST, instance=employe)
        
        if form.is_valid():
            form.save()
            return redirect('liste_employé') 
    else:
        form=EmployeForm(instance=employe) 
        return render(request,'modifier_employe.html',{"form":form, "employe": employe})
    

def supprimer_employe(request,employe_id):
    employe = get_object_or_404(Employe, pk=employe_id)
    employe.delete()
    return redirect('liste_employé')

def afficher_listeAbsence(request):
    cherch = request.GET.get('chercher')
    absence = Absence_employe.objects.all()
    if cherch :
        absence = absence.filter(Date_absence=cherch)
    return render(request, "gerer_absenceE.html", {"absences": absence})

def ajouter_absenceE(request):
    mssg = ""  # Initializing the message variable outside the conditions
    if request.method == 'POST':
        form = AbsenceEmployeForm(request.POST)
        if form.is_valid():
            dateA = form.cleaned_data['Date_absence']
            existing_absence = Absence_employe.objects.filter(Date_absence=dateA)
            if existing_absence.exists():
                mssg = "Cette date existe déjà, vous ne pouvez pas l'ajouter !!"
            else:
                form.save()
                form = AbsenceEmployeForm()
                mssg = "Liste des employés absences successivement créé !"
        else:
            mssg = "Veuillez remplir tous les champs correctement!"
    else:
        form = AbsenceEmployeForm()
        mssg = "Veuillez remplir tous les champs!"

    return render(request, "ajouter_absenceE.html", {"form": form, "message": mssg})


def supprimer_absence(request,absence_id):
    absence = get_object_or_404(Absence_employe, pk=absence_id)
    absence.delete()
    return redirect('gerer_absenceE')



def supprimer_EmployeAbsent(request, absence_id, employeA_id):
    absence = get_object_or_404(Absence_employe, pk=absence_id)
    employeA = get_object_or_404(Employe, pk=employeA_id)
    absence.Employe_absente.remove(employeA)
    if absence.Employe_absente.count() == 0:
        absence.delete()
        return redirect('gerer_absenceE')
    else:
        return redirect('gerer_absenceE')

from django.shortcuts import redirect  # Import redirect

def ajouter_EmployeAbsent(request, absence_id):
    absence = get_object_or_404(Absence_employe, pk=absence_id)
    if request.method == 'POST':
        form = AbsenceEmployeDForm(request.POST)
        if form.is_valid():
            employeA_queryset = form.cleaned_data['Employe_absente']
            employeA = employeA_queryset.first()
            if employeA in absence.Employe_absente.all():  # Ensure only one result
                mssg = "Cette employé est déjà enregistré comme absent à cette date !"
            else:
                absence.Employe_absente.add(employeA)
                absence.save()
                mssg = "employe ajouté comme un absent, vous pouvez saisir un autre"
                  # Redirect to a success page or another view
        else:
            mssg = "Veuillez remplir tous les champs correctement !"
    else:
        form = AbsenceEmployeDForm()
        mssg = "Veuillez remplir tous les champs !"
    
    return render(request, "ajouter_employeAbsent.html", {"absence": absence, "message": mssg, "form": form})



def ajouter_paiment_soldF(request,fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)
    if request.method == 'POST':
        form = PaimentSoldForm(request.POST)

        if form.is_valid():
            date_achat= form.cleaned_data['Date_payement']
            montant_payé = form.cleaned_data['montant_payé']
            paiment = Payement_sold_fournisseur(Date_payement=date_achat,fournisseur =fournisseur,montant_payé = montant_payé)
            paiment.save()
            sold = fournisseur.solde-montant_payé
            if sold<0:
                mssg = "cette montant est plus que le sold!!"
            else :
                fournisseur.solde = sold
                fournisseur.save()
                form = PaimentSoldForm()
                mssg = "Paiment successivement fait !"
        else:
            mssg = "veuillez remplir tous les champs!"
    else:
        form = PaimentSoldForm()
        mssg = ""

    return render(request, "ajouter_paiment_soldF.html", {"form": form, "message": mssg, "fournisseur": fournisseur})

def afficher_listePaiment_soldF(request):
    filter_type = request.GET.get('filter_type')
    cherch = request.GET.get('chercher')
    paiment = Payement_sold_fournisseur.objects.all()

    if filter_type == 'date' and cherch:
       paiment = paiment.filter(Date_payement=cherch)
              
    if filter_type == 'fournisseur' and cherch:
        paiment = paiment.filter(fournisseur__nomF__startswith=cherch)

    return render(request, 'listePaimentsSold.html', {"paiment": paiment})

def supprimer_paimentSoldF(request,paiment_id):
    paiment = get_object_or_404(Payement_sold_fournisseur, pk=paiment_id)
    fournisseur = paiment.fournisseur
    fournisseur.solde = fournisseur.solde + paiment.montant_payé
    fournisseur.save()
    paiment.delete()
    return redirect('listePaimentF')

def Transfer_produit(request):
    if request.method == 'POST':
        form = TransferForm(request.POST) 
        if form.is_valid():
            produit = form.cleaned_data['produit_transfer']
            centre = form.cleaned_data['Centre_transfer']
            qtee = form.cleaned_data['Qte']
            if  qtee <= produit.qte:
             produit.qte -=qtee
             produit.save()
             stock_verify = Stock_centre_primaire.objects.filter(Centre__numC=centre.numC)
             exist = stock_verify.filter(nomP=produit.nomP).last()
             if exist :
              exist.qte += qtee
              exist.save()
             else:
                stock_centre_primaire = Stock_centre_primaire(
                Centre=centre,
                nomP=produit.nomP,
                qte=qtee,
                designation= produit.designation,
                prix_unitaire= produit.prix_unitaire )
                stock_centre_primaire.save()
            
             form.save()
             mssg = "Produits envoyés, vous pouvez saisir une autre"
            else:
             mssg = "quantite stock unsufisant"
            form = TransferForm()
            
        else:
            # Handle form validation errors
            mssg = "Veuillez corriger les erreurs dans le formulaire."
    else:
         form = TransferForm()
         mssg ="Veuillez remplir tous les champs."

    return render(request, "Transfer.html", {"form": form, "message": mssg})
def annuler_transfer(request,transfer_id):
     cmd=Transfer.objects.get(id=transfer_id)
     cmd2 = Stock_centre_primaire.objects.get(nomP=cmd.produit_transfer, Centre_id=cmd.Centre_transfer)
     if cmd.Qte>cmd2.qte :
      messages.error(request, "Vous ne pouvez pas annuler le transfert car le centre a déjà utilisé ce produit")
      return redirect('list_transfer')
     cmd.delete()
     cmd2.delete()
     return redirect('list_transfer')

def list_transfer(request):
    filter_type = request.GET.get('filter_type')
    cherch = request.GET.get('chercher')

    trnasf = Transfer.objects.all()

    if filter_type == 'date':
        date_debut = request.GET.get('date_debut')
        date_fin = request.GET.get('date_fin')

        if date_debut and date_fin:
                start_date = datetime.datetime.strptime(date_debut, '%Y-%m-%d').date()
                end_date = datetime.datetime.strptime(date_fin, '%Y-%m-%d').date()
                trnasf = trnasf.filter(Date_transfer__range=(start_date, end_date))

    elif filter_type == 'centre' and cherch:
        trnasf = trnasf.filter(Centre_transfer__numC__startswith=int(cherch))

    elif filter_type == 'produit' and cherch:
        trnasf = trnasf.filter(produit_transfer__nomP__startswith=cherch)

    return render(request, "list_transfer.html", {"trnasf": trnasf})

def list_vente_centre(request):
    filter_type = request.GET.get('filter_type')
    cherch = request.GET.get('chercher')

    vente = Achats_client_centre.objects.all()

    if filter_type == 'date':
        date_debut = request.GET.get('date_debut')
        date_fin = request.GET.get('date_fin')

        if date_debut and date_fin:
                start_date = datetime.datetime.strptime(date_debut, '%Y-%m-%d').date()
                end_date = datetime.datetime.strptime(date_fin, '%Y-%m-%d').date()
                vente = vente.filter(Date_achat__range=(start_date, end_date))
    

    if filter_type == 'produit' and cherch:
        vente = vente.filter(Q(reproduit__nomP__startswith=cherch) | Q(produit_primaire__nomP__startswith=cherch))
    if filter_type == 'centre' and cherch: 
        vente = vente.filter(Centre__numC=cherch)  
    return render(request, "list_vente_centre.html", {"vente":vente})

def gestion_responsable(request,selected_center):
    return render(request, "gestion_responsable.html", {'selected_center': selected_center})


def afficher_stock_centre(request, selected_center):
    cherch = request.GET.get('chercher_primaire')
    cherch2 = request.GET.get('chercher_reproduit')

    stock = Stock_centre_primaire.objects.filter(Centre=selected_center)
    rep = reProduit.objects.filter(Centre=selected_center)


    if cherch:
        stock = stock.filter(nomP__startswith=cherch)

    if cherch2:
        rep = rep.filter(nomP__startswith=cherch2)
    
    return render(request, "stock_centre.html", {"stock": stock,"rep":rep,'selected_center': selected_center})


def choisir_centre(request):
    return render(request,"choisire_centre.html")

def ajouter_reproduit(request, selected_center):
    centre = get_object_or_404(Centre, id=selected_center)
    mssg = ""
    if request.method == 'POST':
        form = reProduitForm(request.POST, selected_center=selected_center)
        if form.is_valid():
            reproduit = form.save(commit=False)
            stock = reproduit.Produit_primaire
            qte_reproduit = reproduit.qte_Produit_primaire
            if stock.qte - qte_reproduit < 0:
                messages.error(request, "La quantité du produit primaire est insuffisante")
                return redirect ('ajouter_reproduit',selected_center)
            stock.qte -= qte_reproduit
            stock.save()
            reproduitnom = reproduit.nomP

            exist = reProduit.objects.filter(nomP=reproduitnom).last()
            if exist:
              mssg="produit exist deja"
            else:
             form.save()
            
            form = reProduitForm(selected_center=selected_center)
        else:
            mssg = "Veuillez remplir tous les champs!"
    else:
        form = reProduitForm(selected_center=selected_center)
        form.fields["Centre"].initial = centre
        
        mssg = ""

    return render(request, "ajouter_reproduit.html", {"form": form, "message": mssg,'selected_center': selected_center})

def modifier_reproduit(request,selected_center, reproduit_id):
    reproduit = reProduit.objects.get(id=reproduit_id)
    mssg=""
    if request.method == 'POST':
        form = reProduitForm(request.POST, instance=reproduit,selected_center=selected_center)
        form.fields.pop('qte_reProduit')
        form.fields.pop('Centre')  
        form.fields.pop('Produit_primaire')
        form.fields.pop('qte_Produit_primaire')
        if form.is_valid():
            reproduit = form.save(commit=False)
            reproduit.save()
            return redirect('afficher_stock_centre',selected_center)
    else:
        mssg=""
        form = reProduitForm(instance=reproduit,selected_center=selected_center)
        form.fields.pop('Centre')  
        form.fields.pop('Produit_primaire')
        form.fields.pop('qte_Produit_primaire')
        form.fields.pop('qte_reProduit')
    return render(request, 'modifier_reProduit.html', {"form": form,'selected_center': selected_center, "reproduit_id": reproduit_id,"message": mssg})

def supprimer_reProduit(request,selected_center, reproduit_id):
     cmd=reProduit.objects.get(id=reproduit_id)
     cmd.delete()
     return redirect('afficher_stock_centre',selected_center)

def gerer_client(request):
    return render(request,'gestion_clients.html')

def gerer_client_centre(request,selected_center):
    return render(request,'gerer_client_centre.html',{"selected_center":selected_center})

def choose_client(request):

    if request.method == "GET":
        query = request.GET.get('search')
        if query:
            client = Client.objects.filter(nomCl__contains=query).first()
            if not client:
                mssg = "Aucun résultat trouvé"
                return render(request, 'choose_client.html', {'message': mssg})
            nom_client = client.nomCl
            return render(request, 'choose_client.html', {'client': client,'nom_client' :nom_client})

    return render(request, 'choose_client.html')

def choose_client_centre(request,selected_center):

    if request.method == "GET":
        query = request.GET.get('search')
        if query:
            client = Client.objects.filter(nomCl__contains=query).first()
            if not client:
                mssg = "Aucun résultat trouvé"
                return render(request, 'choose_client_centre.html', {'message': mssg,'selected_center': selected_center})
            nom_client = client.nomCl
            return render(request, 'choose_client_centre.html', {'client': client,'nom_client' :nom_client,'selected_center': selected_center})

    return render(request, 'choose_client_centre.html',{'selected_center': selected_center})

def vendre_produit(request, nom_client):
    mssg=""
    if request.method == 'POST':
        form = Achats_clientform(request.POST)
        form.fields.pop('Client')
        if form.is_valid():
            instance = form.save(commit=False)
            produit = form.cleaned_data['Produit']
            qtee = form.cleaned_data['qte']
            pro = get_object_or_404(Produit, nomP=produit)
            if pro.qte<qtee:
                messages.error(request, "La quantité du stock est insuffisante")
                return redirect ('vendre_produit',nom_client)
            pro.qte -= qtee
            pro.save()
            client_objj = get_object_or_404(Client, nomCl=nom_client)
            instance.Client = client_objj
            instance.save()
            form = Achats_clientform()
            return redirect('paye_achat',nom_client)
    else:
        form = Achats_clientform()
        client_obj = get_object_or_404(Client, nomCl=nom_client)
        form.fields["Client"].initial = client_obj  
        form.fields["Client"].widget.attrs["disabled"] = True  
        mssg = "Veuillez remplir tous les champs!"
    return render(request, "vendre_produit.html", {"form": form, "message": mssg})

def select_product_type(request, selected_center, nom_client):
     return render(request, "select_product_type.html", {"selected_center": selected_center , "nom_client":nom_client})
    

def vendre_produit_centre(request, selected_center, nom_client, category_vent):
    mssg = ""
    if request.method == 'POST':
        form = Achats_client_centreform(request.POST, selected_center=selected_center, category_vent=category_vent)
        form.fields.pop('Client')
        form.fields.pop('Centre')
     
        if form.is_valid():
            instance = form.save(commit=False)
            qtee = form.cleaned_data['qte']
            prix_unit = form.cleaned_data['prix_unitaire']
            
            if category_vent == 'produit_primaire':
                 produit = form.cleaned_data['produit_primaire']
                 produit_primaire = Stock_centre_primaire.objects.filter(
                    Centre__numC=selected_center,
                    nomP=produit.nomP
                ).first()
                 if produit_primaire:
                    if produit_primaire.qte < qtee:
                        print("Form submitted")
                        messages.error(request, "La quantité du stock est insuffisante")
                        return redirect('vendre_produit_centre', selected_center=selected_center, nom_client=nom_client, category_vent=category_vent)
                    if prix_unit < produit_primaire.prix_unitaire :
                        error_message = "le prix du vent {} est moin que le prix du produit {}"
                        messages.error(request, error_message.format(prix_unit, produit_primaire.prix_unitaire))
                        return redirect('vendre_produit_centre', selected_center=selected_center, nom_client=nom_client, category_vent=category_vent)
                    produit_primaire.qte -= qtee
                    produit_primaire.save()
            if category_vent == 'reproduit':
                produit = form.cleaned_data['reproduit']
                re_produit = reProduit.objects.filter(
                    Centre__numC=selected_center,
                    nomP=produit.nomP
                ).first()
                if re_produit:
                    if re_produit.qte_reProduit < qtee:
                        messages.error(request, "La quantité du stock est insuffisante")
                        return redirect('vendre_produit_centre', selected_center=selected_center, nom_client=nom_client, category_vent=category_vent)
                    if prix_unit < re_produit.prix_unitaire :
                        error_message = "le prix du vent {} est moin que le prix du produit {}"
                        messages.error(request, error_message.format(prix_unit, re_produit.prix_unitaire))
                        return redirect('vendre_produit_centre', selected_center=selected_center, nom_client=nom_client, category_vent=category_vent)
                    re_produit.qte_reProduit -= qtee
                    re_produit.save()

            client_obj = get_object_or_404(Client, nomCl=nom_client)
            instance.Client = client_obj
            centre_obj = get_object_or_404(Centre, numC=selected_center)
            instance.Centre = centre_obj
            instance.save()

            
            return redirect('paye_achat_centre', selected_center, nom_client)
    else:
        form = Achats_client_centreform(selected_center=selected_center, category_vent=category_vent)
        client_obj = get_object_or_404(Client, nomCl=nom_client)
        centre_obj = get_object_or_404(Centre, numC=selected_center)
        form.fields["Client"].initial = client_obj
        form.fields["Client"].widget.attrs["disabled"] = True
        form.fields["Centre"].initial = centre_obj
        form.fields["Centre"].widget.attrs["disabled"] = True
        mssg = "Veuillez remplir tous les champs!"

    return render(request, "vendre_Produit_centre.html", {"form": form, "message": mssg, "selected_center": selected_center})

def paye_achat(request, nom_client):
    achats_client = Achats_client.objects.filter(Client__nomCl=nom_client).last()
    cout = achats_client.cout 
    client_obj = get_object_or_404(Client, nomCl=nom_client)
    if request.method == 'POST':
        if 'annuler' in request.POST:
            achats_client.delete()
            return redirect('choose_client')
        prix_paye = float(request.POST.get('prix_paye'))
        if prix_paye > cout:
            messages.error(request, "Le prix paye est plus que la cout")
            return redirect('paye_achat', nom_client )
        

        achats_client.somme_paye =prix_paye
        client_obj.credit += cout - prix_paye
        client_obj.somme_paye +=prix_paye
        if cout - prix_paye > 0:
            exist = paye_credit.objects.filter(nom=client_obj).last()
            if not exist:
                paye_credit_obj = paye_credit.objects.create(nom=client_obj,date_modification=timezone.now().date())
                paye_credit_obj.save()
        achats_client.save()
        client_obj.save()   
        return redirect('choose_client')

    return render(request, 'paye_achat.html', {'cout': cout})
    
def paye_achat_centre(request,selected_center, nom_client):
    achats_client = Achats_client_centre.objects.filter(Client__nomCl=nom_client).last()
    cout = achats_client.cout 
    client_obj = get_object_or_404(Client, nomCl=nom_client)
    if request.method == 'POST':
        if 'annuler' in request.POST:
            achats_client.delete()
            return redirect('choose_client')
        prix_paye = float(request.POST.get('prix_paye'))
        if prix_paye > cout:
            messages.error(request, "Le prix paye est plus que la cout")
            return redirect('paye_achat_centre',selected_center, nom_client )

        achats_client.somme_paye =prix_paye
        client_obj.credit += cout - prix_paye
        client_obj.somme_paye +=prix_paye
        if cout - prix_paye > 0:
            exist = paye_credit.objects.filter(nom=client_obj).last()
            if not exist:
                paye_credit_obj = paye_credit.objects.create(nom=client_obj)
                paye_credit_obj.save()
        achats_client.save()
        client_obj.save()  
        return redirect('choose_client_centre',selected_center)

    return render(request, 'paye_achat_centre.html', {'cout': cout ,'selected_center':selected_center})
    
def ajouter_client(request):
    mssg = ""

    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            nom = form.cleaned_data['nomCl']

            if Client.objects.filter(nomCl=nom).exists():
                mssg = f"Le client avec le nom {nom} existe déjà."
            else:
                form.save()
                form = ClientForm()
                mssg = "Client successivement créé !"

    else:
        form = ClientForm()  
        mssg = "Veuillez remplir tous les champs!"

    return render(request, "ajouter_client.html", {"form": form, "message": mssg})

def list_client(request):
    cherch = request.GET.get('chercher')
    client = Client.objects.all()
    if cherch:
        client = client.filter(nomCl__startswith=cherch)

    return render(request, "list_client.html", {"client": client})

def modifier_client(request, client_id):
    mssg=""
    cmd=Client.objects.get(id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=cmd) 
        form.fields.pop('credit')  
        if form.is_valid():
            form.save()
            return redirect('list_client')  
        else:
            mssg = "Veuillez corriger les erreurs dans le formulaire."
    else:
         form = ClientForm(instance=cmd)
         
         form.fields['credit'].widget.attrs['disabled'] = 'disabled'
         mssg = "Veuillez remplir tous les champs."


    return render(request, "modifier_client.html", {"form": form, "message": mssg})

def supprimer_client(request,client_id):
   cmd=Client.objects.get(id=client_id)
   if cmd.credit>0 :
       messages.error(request, "vous ne pouvez pas supprimer ce client car il a un credit")
       return redirect('list_client')
   cmd.delete()
   return redirect('list_client')

def ajouter_client_centre(request,selected_center):
    mssg = ""

    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            nom = form.cleaned_data['nomCl']

            if Client.objects.filter(nomCl=nom).exists():
                mssg = "ce client existe déjà."
            else:
                form.save()
                form = ClientForm()
                mssg = "client ajoute, vous pouvez ajoute un autre"

    else:
        form = ClientForm()  
        mssg = "Veuillez remplir tous les champs!"

    return render(request, "ajouter_client_centre.html", {"form": form, "message": mssg ,"selected_center":selected_center})

def list_vente(request):
    filter_type = request.GET.get('filter_type')
    cherch = request.GET.get('chercher')

    ventes = Achats_client.objects.all()

    if filter_type == 'date':
        date_debut = request.GET.get('date_debut')
        date_fin = request.GET.get('date_fin')

        if date_debut and date_fin:
                start_date = datetime.datetime.strptime(date_debut, '%Y-%m-%d').date()
                end_date = datetime.datetime.strptime(date_fin, '%Y-%m-%d').date()
                ventes = ventes.filter(Date_achat__range=(start_date, end_date))
        

    if filter_type == 'client' and cherch:
        ventes = ventes.filter(Client__nomCl__startswith=cherch)

    if filter_type == 'produit' and cherch:
        ventes = ventes.filter(Produit__nomP__startswith=cherch)
    total_cout = sum(vente.cout for vente in ventes)
    return render(request, "list_vente.html", {"ventes": ventes, "total_cout": total_cout})

def supprimer_vente(request, achat_id):
     achats_client = get_object_or_404(Achats_client, id=achat_id)
     produit = achats_client.Produit
     produit.qte += achats_client.qte
     achats_client.Client.credit -= (achats_client.cout-achats_client.somme_paye)
     achats_client.Client.somme_paye -= achats_client.somme_paye
     produit.save()
     achats_client.Client.save() 
     achats_client.save()
     cmd=Achats_client.objects.get(id=achat_id)
     cmd.delete()
     return redirect('list_vente')

def supprimer_vente_centre(request,selected_center, achat_id):
     achats_client = get_object_or_404(Achats_client_centre, id=achat_id,Centre_id=selected_center)
     if achats_client.reproduit:
      produit = achats_client.reproduit
      produit.qte_reProduit += achats_client.qte
     if achats_client.produit_primaire:
      produit = achats_client.produit_primaire
      produit.qte += achats_client.qte
     achats_client.Client.credit -= (achats_client.cout-achats_client.somme_paye)
     achats_client.Client.somme_paye -= achats_client.somme_paye
     produit.save()
     achats_client.Client.save() 
     achats_client.save()
     cmd=Achats_client_centre.objects.get(id=achat_id)
     cmd.delete()
     return redirect('journal_vente_centre',selected_center)


def regle_credit(request):
    cherch = request.GET.get('chercher')
    client = paye_credit.objects.all()
    if cherch:
        client = client.filter(nom__nomCl__startswith=cherch)
    return render(request, "regle_credit.html", {"credit": client})

def afficher_fournisseur(request):
    cherch = request.GET.get('chercher')
    fournisseurs = Fournisseur.objects.all()
    if cherch:
        fournisseurs = fournisseurs.filter(nomF__startswith=cherch)
    return render(request,"gerer_achat.html",{"fournisseurs":fournisseurs})

def afficher_listeP_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)
    cherch = request.GET.get('chercher')
    produits_fournisseur = fournisseur.produits_fournisseur.all()
    if cherch:
        produits_fournisseur = produits_fournisseur.filter(nomP__startswith=cherch)
    return render(request,"listeProduits_fournisseur.html",{"produits_fournisseur":produits_fournisseur,"fournisseur":fournisseur})


def modifier_credit(request, credit_id):
    credit = get_object_or_404(paye_credit, pk=credit_id)
    crd = credit.credit
    if request.method == 'POST':
        form = creditForm(request.POST, instance=credit) 
        form.fields.pop('nom')  
        form.fields.pop('date_modification')
        if form.is_valid():
            prix_paye = request.POST.get('prix_paye')  
            client = credit.nom
            client.somme_paye = client.somme_paye + float(prix_paye) 
            client.credit = client.credit - float(prix_paye)
            if client.credit<0 : 
                messages.error(request, "Le prix paye est plus que le credit")
                return redirect('modifier_credit',credit_id )
            credit.date_modification=timezone.now().date()
            form.save()
            client.save()
            return redirect('regle_credit')  
        else:
            mssg = "Veuillez corriger les erreurs dans le formulaire."
    else:
         form = creditForm(instance=credit)
         for field in form.fields.values():
            field.widget.attrs['disabled'] = 'disabled'
         form.fields['date_modification'].initial = timezone.now().date()
         mssg = "Veuillez remplir tous les champs."


    return render(request, "modifier_credit.html", {"form": form, "message": mssg, "credit":crd})


def supprimer_credit(request, credit_id):
     cmd=paye_credit.objects.get(id=credit_id)
     cmd.delete()
     return redirect('regle_credit')

def regle_credit_centre(request,selected_center):
    cherch = request.GET.get('chercher')
    client = paye_credit.objects.all()
    if cherch:
        client = client.filter(nom__nomCl__startswith=cherch)
    return render(request, "regle_credit_centre.html", {"credit": client,"selected_center":selected_center})

def modifier_credit_centre(request, credit_id,selected_center):
    credit = get_object_or_404(paye_credit, pk=credit_id)
    crd = credit.credit
    if request.method == 'POST':
        form = creditForm(request.POST, instance=credit) 
        form.fields.pop('nom')  
        form.fields.pop('date_modification')
        if form.is_valid():
            prix_paye = request.POST.get('prix_paye')  
            client = credit.nom
            client.somme_paye = client.somme_paye + float(prix_paye) 
            client.credit = client.credit - float(prix_paye)
            if client.credit<0 : 
                messages.error(request, "Le prix paye est plus que le credit")
                return redirect('modifier_credit_centre',selected_center,credit_id )
            credit.date_modification=timezone.now().date()
            form.save()
            client.save()
            return redirect('regle_credit_centre',selected_center)
            
        else:
            mssg = "Veuillez corriger les erreurs dans le formulaire."
    else:
         form = creditForm(instance=credit)
         form.fields['date_modification'].initial = timezone.now().date()
         for field in form.fields.values():
            field.widget.attrs['disabled'] = 'disabled'
         mssg = "Veuillez remplir tous les champs."

    return render(request, "modifier_credit_centre.html", {"form": form, "message": mssg, "credit":crd,"selected_center":selected_center})

def supprimer_credit_centre(request, credit_id,selected_center):
     cmd=paye_credit.objects.get(id=credit_id)
     cmd.delete()
     return redirect('regle_credit_centre',selected_center)

def les_journale_centre(request,selected_center):
      tranf = Transfer.objects.filter(Centre_transfer__numC=selected_center)
      total_transf_cout = sum(tr.cout for tr in tranf)
      vente = Achats_client_centre.objects.filter(Centre__numC=selected_center)
      somme_vent = sum(float(vent.cout) for vent in vente)
      Benefice = somme_vent-total_transf_cout
      return render(request, "les_journale_centre.html", {"selected_center":selected_center,"Benefice":Benefice,"total_transf_cout":total_transf_cout,"somme_vent":somme_vent})

def journal_transfer_centre(request,selected_center):
    filter_type = request.GET.get('filter_type')
    cherch = request.GET.get('chercher')
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')

    trnasf = Transfer.objects.filter(Centre_transfer__numC=selected_center)


    if filter_type == 'date' and date_debut and date_fin :
            trnasf = trnasf.filter(Date_transfer__range=[date_debut, date_fin])

    if filter_type == 'produit' and cherch:
        trnasf = trnasf.filter(produit_transfer__nomP__startswith=cherch)
    return render(request, "journal_transfer_centre.html", {"trnasf": trnasf,"selected_center":selected_center})

def journal_vente_centre(request,selected_center):
    filter_type = request.GET.get('filter_type')
    cherch = request.GET.get('chercher')
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    vente = Achats_client_centre.objects.filter(Centre__numC=selected_center)

    if filter_type == 'date' and date_debut and date_fin :
            vente = vente.filter(Date_achat__range=[date_debut, date_fin])

    if filter_type == 'produit' and cherch:
        vente = vente.filter(Q(reproduit__nomP__startswith=cherch) | Q(produit_primaire__nomP__startswith=cherch))
    return render(request, "journal_vente_centre.html", {"vente":vente,"selected_center":selected_center})

def ajouter_qte_reproduit(request,selected_center,reproduit_id):
    reproduit = reProduit.objects.get(id=reproduit_id)
    mssg=""
    if request.method == 'POST':
        form = reProduitForm(request.POST, instance=reproduit,selected_center=selected_center)
        form.fields.pop('Centre')  
        form.fields.pop('Produit_primaire')
        form.fields.pop('nomP')
        form.fields.pop('designation')
        form.fields.pop('prix_unitaire')
        if form.is_valid():
            reproduit1 = form.save(commit=False)
            stock = reproduit1.Produit_primaire
            qte_reproduit = reproduit1.qte_Produit_primaire
            if stock.qte < qte_reproduit:
                messages.error(request, "La quantité du stock est insuffisante")
                return redirect('ajouter_qte_reproduit', selected_center,reproduit_id)
            stock.qte -= qte_reproduit
            stock.save()
            reproduit.qte_reProduit+=reproduit1.qte_reProduit
            reproduit.save()
            return redirect('afficher_stock_centre',selected_center)
    else:
        mssg=""
        form = reProduitForm(instance=reproduit,selected_center=selected_center)
        form.fields.pop('designation')
        form.fields.pop('prix_unitaire')
        form.fields['Centre'].disabled = True
        form.fields['qte_Produit_primaire'].initial = 0
        form.fields['Produit_primaire'].disabled = True
        form.fields['nomP'].disabled = True
    return render(request, 'ajouter_qte_reproduit.html', {"form": form,'selected_center': selected_center, "reproduit_id": reproduit_id,"message": mssg})


def afficher_liste_demMassrouf(request,selected_center):
    filter_type = request.GET.get('filter_type')
    cherch = request.GET.get('chercher')
    demande_massrouf = Demande_massrouf.objects.filter(responsable_id = selected_center)
 
    if filter_type == 'date' and cherch:
        demande_massrouf = demande_massrouf.filter(Date_dem=cherch)
              
    if filter_type == 'employe' and cherch:
        demande_massrouf = demande_massrouf.filter(employe__nomE__startswith=cherch)
    
    return render(request, "liste_demandeMassrouf.html", {"demande": demande_massrouf,"selected_center":selected_center})

def ajouter_demMassrouf(request, selected_center):
    centre = get_object_or_404(Centre, pk=selected_center)
    mssg = ""
    
    if request.method == 'POST':
        form = DemandeMassroufForm(request.POST)
        if form.is_valid():
            employe = form.cleaned_data['employe']
            date_dem = form.cleaned_data['Date_dem']
            massrouf = form.cleaned_data['massrouf']
            responsable = get_object_or_404(Responsable, pk=selected_center)
            if massrouf <=0:
                mssg = "La demande massrouf doit etre superieur a 0 !!"
            else:
                
                month = date_dem.month
                year = date_dem.year
                
                demandes = Demande_massrouf.objects.filter(Date_dem__month=month, Date_dem__year=year, employe=employe)
                massroufT = sum(demande.massrouf for demande in demandes)
                
                # Print to check the values
                print(f"Massrouf total: {massroufT}")
                
                
                Total_M = massroufT + massrouf
                total_absences = Absence_employe.objects.filter(Date_absence__year = year,Date_absence__month = month,Employe_absente=employe).aggregate(absences=Count('id'))['absences'] or 0
                monthly_salary = employe.monthly_salary(year, month) - (total_absences * employe.Salarie_jour) - massroufT

                print(f"absences total  :{total_absences}")
                print(f"Monthly salary: {monthly_salary}")

                if massrouf > monthly_salary:
                    mssg = f"Ce employé a demandé un montant de massrouf supérieur à son salaire ce mois-ci. Le massrouf maximum qu'il peut demander est {monthly_salary} DA."
                else:
                    dem_massrouf = Demande_massrouf(Date_dem=date_dem, employe=employe, responsable=responsable, massrouf=massrouf)
                    dem_massrouf.save()
                    mssg = "Demande enregistrée. Vous pouvez en saisir une autre."
                    form = DemandeMassroufForm(employe=Employe.objects.filter(centre=centre))
        else:
            mssg = "Veuillez remplir tous les champs!"
    else:
        form = DemandeMassroufForm(employe=Employe.objects.filter(centre=centre))
    
    return render(request, "ajouter_demandeMassrouf.html", {"form": form, "message": mssg, "selected_center": selected_center})


def modifier_demMassrouf(request, demande_id, selected_center):
    demande = get_object_or_404(Demande_massrouf, id=demande_id)

    if request.method == 'POST':
        form = DemandeMassroufForm(request.POST, instance=demande)

        if form.is_valid():
            form.save()
            return redirect(reverse('liste_demandeMassrouf', kwargs={'selected_center': selected_center}))
    else:
        form = DemandeMassroufForm(instance=demande, employe=demande.employe.centre.employe_set.all())
        return render(request, 'modifier_demandeMassrouf.html', {"form": form, "demande": demande, "selected_center": selected_center})


def supprmier_demMassrouf(request,demande_id,selected_center):
    demande = get_object_or_404(Demande_massrouf, pk=demande_id)
    demande.delete()
    return redirect(reverse('liste_demandeMassrouf', kwargs={'selected_center': selected_center}))

def afficher_listePV(request, selected_center):
    cherch = request.GET.get('chercher')
    PV = Rapport_responsable.objects.filter(responsable__id = selected_center)
    if cherch :
        PV = PV.filter(Date_R=cherch)
                
    return render(request, "liste_rapport.html", {"PV": PV,"selected_center":selected_center})

def ajouter_rapport(request, selected_center):
    mssg = ""
    if request.method == 'POST':
        form = RapportForm(request.POST, request.FILES)  # Pass request.FILES for file upload handling

        if form.is_valid():
            date_R = form.cleaned_data['Date_R']
            existedRapport = Rapport_responsable.objects.filter(Date_R=date_R,responsable__id=selected_center)
            if existedRapport:
                mssg = "Le rapport de cette date est enregistré. Veuillez saisir une autre date."
            else:
                rapport_file = form.cleaned_data['Rapport']  # Access the file using the correct field name
                responsable = get_object_or_404(Responsable, pk=selected_center)
                centre = get_object_or_404(Centre, pk=selected_center)
                demandes = Demande_massrouf.objects.filter(Date_dem=date_R,responsable__id=selected_center)
                
                PV = Rapport_responsable(Date_R=date_R, responsable=responsable,centre=centre, Rapport=rapport_file)
                PV.save()
                PV.demandes_massrouf.set(demandes)
                mssg = "Rapport enregistrée."
                form = RapportForm()
        else:
            mssg = "Veuillez remplir tous les champs!"
    else:
        form = RapportForm()

    return render(request, "ajouter_rapport.html", {"form": form, "message": mssg, "selected_center": selected_center})


def supprimer_rapport(request,rapport_id,selected_center):
    rapport = get_object_or_404(Rapport_responsable, pk=rapport_id)
    rapport.delete()
    return redirect(reverse('liste_PV', kwargs={'selected_center': selected_center}))

def afficher_listePVM(request):
    filter_type = request.GET.get('filter_type')
    cherch = request.GET.get('chercher')
    PV = Rapport_responsable.objects.all()

    if filter_type == 'date' and cherch:
        PV = Rapport_responsable.objects.filter(Date_R=cherch)

    if filter_type == 'centre' and cherch:
        PV = PV.filter(centre__numC__startswith=cherch)

    return render(request, "liste_PVM.html", {"PV": PV})

from django.db.models import Sum
from datetime import datetime
from django.db.models import Count




def gerer_salariePM(request):
    PV = Rapport_responsable.objects.all()
    salaries_dict = defaultdict(lambda: defaultdict(dict))

    years = {p.Date_R.year for p in PV}
    for year in years :
        PV_yearly = Rapport_responsable.objects.filter(Date_R__year=year)
        months = {p.Date_R.month for p in PV_yearly}
        for month in months:
            demandes = Demande_massrouf.objects.filter(Date_dem__year = year,Date_dem__month = month)
            absences = Absence_employe.objects.filter(Date_absence__year = year,Date_absence__month = month)
            mois_name = calendar.month_name[month]
            employes = Employe.objects.all()

            for employe in employes:
                existing_salarie = Employe_salarie.objects.filter(année=year, mois=mois_name, employe=employe).first()

                employee_absence_counts = absences.filter(Employe_absente=employe).count()
                employee_massrouf_total = demandes.filter(employe=employe).aggregate(total_price=Sum('massrouf'))['total_price'] or 0
                Salarie_mois = employe.monthly_salary(year,month) - employee_absence_counts * employe.Salarie_jour - employee_massrouf_total
                if Salarie_mois <0:
                    Salarie_mois = 0
                if existing_salarie:
                    existing_salarie.massrouf_total = employee_massrouf_total
                    existing_salarie.absences_count = employee_absence_counts
                    existing_salarie.Salarie = Salarie_mois
                    existing_salarie.save()
                else:
                    salarie = Employe_salarie(année=year,mois=mois_name,employe=employe,massrouf_total=employee_massrouf_total,absences_count=employee_absence_counts,Salarie=Salarie_mois)
                    salarie.save()

    salaries = Employe_salarie.objects.all()  
    salaries_dict = {}
    for salary in salaries:
        year = salary.année
        month = salary.mois
        if year not in salaries_dict:
            salaries_dict[year] = {}
        if month not in salaries_dict[year]:
            salaries_dict[year][month] = []
        salaries_dict[year][month].append({
            'employee': {
                'name': f"{salary.employe.nomE} {salary.employe.prenomE}",
                'centre': salary.employe.centre.numC,  # Assuming centre information is in numC
            },
            'total_massrouf': salary.massrouf_total,
            'absences_count': salary.absences_count,
            'salary_per_day': salary.employe.Salarie_jour,
            'salary': salary.Salarie,
        })

    filter_type = request.GET.get('filter_type')
    cherch = request.GET.get('chercher')

    if filter_type == 'mois' and cherch:
        year, cherch = map(int, cherch.split('-')) 
        cherch_month_name = calendar.month_name[cherch]
        filtered_salaries = {}
        
        for yr, months in salaries_dict.items():
            if yr == year:
                filtered_salaries[yr] = {}
                for month, employees in months.items():
                    if month == cherch_month_name:
                        filtered_salaries[yr][month] = employees

        salaries_dict = filtered_salaries

    if filter_type == 'employe' and cherch:
        filtered_salaries = {}
        
        for year, months in salaries_dict.items():
            filtered_salaries[year] = {}
            for month, employees in months.items():
                filtered_employees = [emp for emp in employees if emp['employee']['name'].lower().startswith(cherch.lower())]
                if filtered_employees:
                    filtered_salaries[year][month] = filtered_employees

        salaries_dict = filtered_salaries

    if filter_type == 'centre' and cherch:
        filtered_salaries = {}
        cherch = int(cherch)  # Assuming 'cherch' contains the center ID as an integer

        for year, months in salaries_dict.items():
            filtered_salaries[year] = {}
            for month, employees in months.items():
                filtered_employees = [emp for emp in employees if emp['employee']['centre'] == cherch]
                if filtered_employees:
                    filtered_salaries[year][month] = filtered_employees

        salaries_dict = filtered_salaries
    return render(request, 'gerer_salariePM.html', {'salaries_dict': salaries_dict})
                


import matplotlib
matplotlib.use('agg')  # Set non-interactive backend

import matplotlib.pyplot as plt
from io import BytesIO
import base64
import datetime

def generate_produit_quantites_graph(year):
    products_quantities = (
        Achats_matiereP.objects.filter(Date_achat__year=year)
        .values('Produit_Fournisseur__nomP')
        .annotate(total_quantity=Sum('qte'))
    )

    product_names = []
    quantities = []
    for item in products_quantities:
        product_names.append(item['Produit_Fournisseur__nomP'])
        quantities.append(item['total_quantity'])

    plt.figure(figsize=(10, 6))
    plt.bar(product_names, quantities, color='skyblue')
    plt.xlabel('Noms des produits achetés')
    plt.ylabel('Les quantités')
    plt.title('Les quantités des produits')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graph = base64.b64encode(image_png).decode('utf-8')

    return f'data:image/png;base64,{graph}'

def generate_fournisseur_achats_graph(year):
    fournisseurs = (
        Achats_matiereP.objects.filter(Date_achat__year=year)
        .values('Fournisseur__nomF')
        .annotate(total_montant_achat=Sum('Montant_achat'))
    )

    fournisseur_names = []
    achats = []
    for item in fournisseurs:
        fournisseur_names.append(item['Fournisseur__nomF'])
        achats.append(item['total_montant_achat'])

    plt.figure(figsize=(10, 6))
    plt.bar(fournisseur_names, achats, color='skyblue')
    plt.xlabel('Noms des employés')
    plt.ylabel('Le total absences')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graph = base64.b64encode(image_png).decode('utf-8')

    return f'data:image/png;base64,{graph}'



def afficherStatistiques(request):
    fournisseurs_purchase = []
    fournisseurs = Fournisseur.objects.all()
    cherch = request.GET.get('chercher')

    if not cherch:
        cherch=datetime.datetime.now().year


    for fournisseur in fournisseurs:
        # Aggregate total purchase amount for each supplier
        montant_achat_total = Achats_matiereP.objects.filter(Fournisseur=fournisseur,Date_achat__year=cherch).aggregate(total_purchase=Sum('Montant_achat'))

        # Store the total purchase amount and supplier details in a dictionary
        fournisseurs_purchase.append({
            'nom': fournisseur.nomF,
            'prenom': fournisseur.prenomF,
            'montant_achat_total': montant_achat_total['total_purchase'] if montant_achat_total['total_purchase'] else 0
        })

    # Find the supplier with the highest total purchase amount
    Top_fournisseur = max(fournisseurs_purchase, key=lambda x: x['montant_achat_total'])
    Top_fournisseur_montant = Top_fournisseur['montant_achat_total']
    montant_achat_T = Achats_matiereP.objects.filter(Date_achat__year=cherch).aggregate(total_montant=Sum('Montant_achat'))

    produit_quantités_graph = generate_produit_quantites_graph(cherch)
    fournisseur_achats_graph = generate_fournisseur_achats_graph(cherch)
    

    return render(request, 'statistiques.html', {
        "Top_fournisseur": f"{Top_fournisseur['nom']} {Top_fournisseur['prenom']}",
        "Top_fournisseur_montant": Top_fournisseur_montant,
        "montant_total": montant_achat_T['total_montant'],
        "produit_quantités_graph": produit_quantités_graph,
        "fournisseur_achats_graph":fournisseur_achats_graph,
        
    })


def generate_ventes_centre_circle(centres, date_debut,date_fin):
    centre_labels = []
    sales_values = []
    achat_exist = False

    for centre in centres:
        achats_centre = Achats_client_centre.objects.filter(Centre=centre)
        if date_debut and date_fin:
            achats_centre = achats_centre.filter(Date_achat__range=[date_debut, date_fin])
            if achats_centre:
                achat_exist = True
        else:
            achat_exist = True
        total_sales = sum(achat.prix_unitaire * achat.qte for achat in achats_centre)
        centre_labels.append(f"Centre {centre.numC}")
        sales_values.append(total_sales)

    if achat_exist:
        fig, ax = plt.subplots(figsize=(5, 4.8))  
        
        wedges, labels, autopct = ax.pie(sales_values, labels=centre_labels, autopct='%1.1f%%')
        wedges[1].set_facecolor((0.4, 0.8, 0.8, 1))
        wedges[0].set_facecolor('lightblue')
        wedges[2].set_facecolor((0.4, 0.6, 0.8, 1))
        ax.set_title("évolution de la valeur des ventes des centres", weight='bold', color='white')

        for label in labels:
            label.set_fontweight('bold')
            label.set_color('white')

        for pct in autopct:
            pct.set_fontweight('bold')
            pct.set_color('white')

    else:
        sales_values = [1]
        centre_labels = ['pas du data']
        colors = ['lightgray']

        fig, ax = plt.subplots(figsize=(5, 4.8))  

        wedges, labels = ax.pie(sales_values, labels=centre_labels, colors=colors)
        ax.set_title("pas du data", weight='bold', color='white')

        for label in labels:
            label.set_fontweight('bold')
            label.set_color('white')

    buffer = BytesIO()
    plt.savefig(buffer, format='png', transparent=True)
    buffer.seek(0)
    plt.clf()

    image_png = buffer.getvalue()
    buffer.close()
    graph = base64.b64encode(image_png).decode('utf-8')
    client_graph = f'data:image/png;base64,{graph}'

    return client_graph
def generate_ventes_centre_graph(centres, date_debut,date_fin):
    centre_labels = []
    sales_values = []

    for centre in centres:
        achats_centre = Achats_client_centre.objects.filter(Centre=centre)
        if date_debut and date_fin:
            achats_centre = achats_centre.filter(Date_achat__range=[date_debut, date_fin])
        total_sales = sum(achat.prix_unitaire * achat.qte for achat in achats_centre)

        centre_labels.append(f"Centre {centre.numC}")
        sales_values.append(total_sales)

    fig, ax = plt.subplots()
    bars = ax.bar(centre_labels, sales_values)
    for bar in bars:
        bar.set_facecolor('lightblue')
    ax.set_facecolor('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.set_xlabel("Centres", weight='bold')  # Set x-axis label font weight to bold
    ax.set_ylabel("Sales Value", weight='bold')  # Set y-axis label font weight to bold
    ax.set_title("Evolution of Sales Value for Centers", weight='bold')
    for tick in ax.get_xticklabels() + ax.get_yticklabels():
        tick.set_fontweight('bold')
    plt.xlabel("Centres")
    plt.ylabel("Sales Value")
    plt.title("Evolution of Sales Value for Centers")

    buffer = BytesIO()
    plt.savefig(buffer, format='png', transparent=True)
    buffer.seek(0)
    plt.clf()  # Clear the figure

    image_png = buffer.getvalue()
    buffer.close()
    graph = base64.b64encode(image_png).decode('utf-8')
    client_graph = f'data:image/png;base64,{graph}'

    return client_graph

def generate_client_graph(clients, date_debut,date_fin):
    client_names = []
    client_payments = []

    for client in clients:
        total_payment_qs = Achats_client_centre.objects.filter(Client=client)
        if date_debut and date_fin:
            total_payment_qs = total_payment_qs.filter(Date_achat__range=[date_debut, date_fin])
        total_payment = total_payment_qs.aggregate(total_payment=Sum('somme_paye'))
        payment_amount = total_payment['total_payment'] if total_payment['total_payment'] else 0

        client_names.append(f"{client.nomCl} {client.prenomCl}")
        client_payments.append(payment_amount)

    fig, ax = plt.subplots()
    ax.bar(client_names, client_payments, color='lightblue')
    ax.set_xlabel("Clients", fontweight='bold', color='white')
    ax.set_ylabel("Payment Amount", fontweight='bold', color='white')
    ax.set_title("Clients by Payment Amount", fontweight='bold', color='white')

    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.setp(ax.get_xticklabels(), fontweight='bold')
    plt.setp(ax.get_yticklabels(), fontweight='bold')

    buffer = BytesIO()
    plt.savefig(buffer, format='png', transparent=True)
    buffer.seek(0)
    plt.clf()

    image_png = buffer.getvalue()
    buffer.close()
    graph = base64.b64encode(image_png).decode('utf-8')
    client_graph = f'data:image/png;base64,{graph}'

    return client_graph

def generate_benefits_table(centres, date_debut,date_fin):
    table_html = '<table ><thead><tr><th>Centres</th><th>Benefits</th></tr></thead><tbody>'

    for centre in centres:
        demandes = Demande_massrouf.objects.filter(responsable__centre=centre)
        salaires = Employe_salarie.objects.filter(employe__centre=centre)
        vente = Achats_client_centre.objects.filter(Centre=centre)
        transfer = Transfer.objects.filter(Centre_transfer=centre)

        if date_debut and date_fin:
            date_debut_salaire = datetime.datetime.strptime(date_debut, '%Y-%m-%d').date()
            date_fin_salaire = datetime.datetime.strptime(date_fin, '%Y-%m-%d').date()

            year_range = [date_debut_salaire.year, date_fin_salaire.year]
            month_range = [date_debut_salaire.month, date_fin_salaire.month]
            salaires = salaires.filter(année__range=year_range, mois__range=month_range)
            demandes = demandes.filter(Date_dem__range=[date_debut, date_fin])
            vente = vente.filter(Date_achat__range=[date_debut, date_fin])
            transfer = transfer.filter(Date_transfer__range=[date_debut, date_fin])

        total_massrouf = demandes.aggregate(total_messrouf=Sum('massrouf'))['total_messrouf'] or 0
        total_salarie = salaires.aggregate(total_salaires=Sum('Salarie'))['total_salaires'] or 0
        try:
             total_vente = sum(item.cout for item in vente)
        except TypeError:
             total_vente = 0

        try:
            total_transfer = sum(item.cout for item in transfer)
        except TypeError:
            total_transfer = 0

        benefits = total_vente - (total_massrouf + total_salarie + total_transfer)
        centre_label = f"Centre {centre.numC}"

        table_html += f'<tr><td>{centre_label}</td><td>{benefits}</td></tr>'

    table_html += '</tbody></table>'

    return mark_safe(table_html)
def generate_benefits_graph(centres, date_debut,date_fin):
    centre_labels = []
    benefits = []

    for centre in centres:
        demandes = Demande_massrouf.objects.filter(responsable__centre=centre)
        salaires = Employe_salarie.objects.filter(employe__centre=centre)
        vente = Achats_client_centre.objects.filter(Centre=centre)
        transfer = Transfer.objects.filter(Centre_transfer=centre)

        if date_debut and date_fin:
            date_debut_salaire = datetime.datetime.strptime(date_debut, '%Y-%m-%d').date()
            date_fin_salaire = datetime.datetime.strptime(date_fin, '%Y-%m-%d').date()

            year_range = [date_debut_salaire.year, date_fin_salaire.year]
            month_range = [date_debut_salaire.month, date_fin_salaire.month]
            salaires = salaires.filter(année__range=year_range, mois__range=month_range)
            demandes = demandes.filter(Date_dem__range=[date_debut, date_fin])
            vente = vente.filter(Date_achat__range=[date_debut, date_fin])
            transfer = transfer.filter(Date_transfer__range=[date_debut, date_fin])

        total_massrouf = demandes.aggregate(total_messrouf=Sum('massrouf'))['total_messrouf'] or 0
        total_salarie = salaires.aggregate(total_salaires=Sum('Salarie'))['total_salaires'] or 0

        try:
            total_vente = sum(item.cout for item in vente)
        except TypeError:
            total_vente = 0

        try:
            total_transfer = sum(item.cout for item in transfer)
        except TypeError:
            total_transfer = 0

        benefits.append(total_vente - (total_massrouf + total_salarie + total_transfer))
        centre_labels.append(f"Centre {centre.numC}")

    fig, ax = plt.subplots()
    ax.bar(centre_labels, benefits, color='lightblue')
    ax.set_xlabel("Centres", fontweight='bold', color='white')
    ax.set_ylabel("Benefits", fontweight='bold', color='white')
    ax.set_title("Benefits for Centers", fontweight='bold', color='white')
    ax.axhline(0, color='white', linewidth=1)

    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    plt.xticks(fontweight='bold', color='white')
    plt.yticks(fontweight='bold', color='white')

    buffer = BytesIO()
    plt.savefig(buffer, format='png', transparent=True)
    buffer.seek(0)
    plt.clf()

    image_png = buffer.getvalue()
    buffer.close()
    graph = base64.b64encode(image_png).decode('utf-8')
    client_graph = f'data:image/png;base64,{graph}'

    return client_graph

def generate_best_product_graph(date_debut,date_fin):
    if date_debut and date_fin:
        achats_client = Achats_client.objects.filter(Date_achat__range=[date_debut, date_fin]).values('Produit__nomP').annotate(total_quantity=Sum('qte')).order_by('-total_quantity')[:5]
        achats_client_centre = Achats_client_centre.objects.filter(Date_achat__range=[date_debut, date_fin]).values('reproduit__nomP').annotate(total_quantity=Sum('qte')).order_by('-total_quantity')[:5]
        achats_client_centre_primaire = Achats_client_centre.objects.filter(Date_achat__range=[date_debut, date_fin]).values('produit_primaire__nomP').annotate(total_quantity=Sum('qte')).order_by('-total_quantity')[:5]
    else:
        achats_client = Achats_client.objects.values('Produit__nomP').annotate(total_quantity=Sum('qte')).order_by('-total_quantity')[:5]
        achats_client_centre = Achats_client_centre.objects.values('reproduit__nomP').annotate(total_quantity=Sum('qte')).order_by('-total_quantity')[:5]
        achats_client_centre_primaire = Achats_client_centre.objects.values('produit_primaire__nomP').annotate(total_quantity=Sum('qte')).order_by('-total_quantity')[:5]

    products = []

    for achats in achats_client:
        products.append((achats['Produit__nomP'], achats['total_quantity']))

    for achats in achats_client_centre:
        if achats['reproduit__nomP']:
            products.append((achats['reproduit__nomP'], achats['total_quantity']))

    for achats in achats_client_centre_primaire:
        if achats['produit_primaire__nomP']:
            product_name = achats['produit_primaire__nomP']
            total_quantity = achats['total_quantity']
            if product_name in [product[0] for product in products]:
                index = [product[0] for product in products].index(product_name)
                products[index] = (product_name, products[index][1] + total_quantity)
            else:
                products.append((product_name, total_quantity))

    products.sort(key=lambda x: x[1], reverse=True)
    top_products = products[:5]

    product_names, quantities = zip(*top_products) if top_products else ([], [])

    quantities = list(map(int, quantities))
    product_names = list(map(str, product_names))

    fig, ax = plt.subplots(facecolor='none')
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.bar(product_names, quantities, color='lightblue')

    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['top'].set_color('white')

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    ax.set_xlabel("Produit", color='white')
    ax.set_ylabel("Quantity Sold", color='white')
    ax.set_title("Best-selling Products", color='white')

    if not top_products:
        ax.text(0.5, 0.5, "No data available", ha='center', va='center', fontsize=12, color='gray')
        ax.set_xticks([])

    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png', transparent=True)
    buffer.seek(0)
    plt.clf()

    image_png = buffer.getvalue()
    buffer.close()
    graph = base64.b64encode(image_png).decode('utf-8')
    client_graph = f'data:image/png;base64,{graph}'

    return client_graph


def ventes_statistiques(request):

    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    centres = Centre.objects.all()
    centre_graph = generate_ventes_centre_graph(centres,date_debut,date_fin)
    clients = Client.objects.all()
    client_graph = generate_client_graph(clients,date_debut,date_fin)
    benifits_graph = generate_benefits_graph(centres,date_debut,date_fin)
    benifits_table=generate_benefits_table(centres,date_debut,date_fin)
    best_product_table = generate_best_product_graph(date_debut,date_fin)
    circle_centre_vent = generate_ventes_centre_circle(centres,date_debut,date_fin)

    return render(request, 'ventes_statistiques.html', {'circle_centre_vent':circle_centre_vent,'centre_graph': centre_graph, 'client_graph': client_graph, 'benifits_table': benifits_table, 'benifits_graph': benifits_graph, 'best_product_table': best_product_table})
    
def afficherCentreStatistiques(request):
    return render(request, "statistiques_centre.html")

def afficherbenifices_centre(request):
    numCentre = request.GET.get('centre')
    month = request.GET.get('mois')
    centre = get_object_or_404(Centre, numC=numCentre)
    year, month_number = map(int, month.split('-'))

    demandes = Demande_massrouf.objects.filter(
        responsable__centre=centre,
        Date_dem__year=year,
        Date_dem__month=month_number
    )
    
    salaires = Employe_salarie.objects.filter(
        employe__centre=centre,
        année=year,
        mois=calendar.month_name[month_number]
    )
    vente = Achats_client_centre.objects.filter(
        Centre=centre,
        Date_achat__year=year,
        Date_achat__month=month_number
    )
    transfer = Transfer.objects.filter(
        Centre_transfer=centre,
        Date_transfer__year=year,
        Date_transfer__month=month_number
    )
    total_massrouf = (demandes.aggregate(total_messrouf=Sum('massrouf'))['total_messrouf'] or 0)
    total_salarie = (salaires.aggregate(total_salaires=Sum('Salarie'))['total_salaires'] or 0)
    total_vente = 0  
    for item in vente:
        total_vente += item.cout
    total_transfer = 0  
    for item in transfer:
        total_transfer += item.cout
    benifices =  total_vente - (total_massrouf + total_salarie+total_transfer)

    return render(request, "benifices_centre.html", {"benifices": benifices,"numC":numCentre,"month":month,"massrouf":total_massrouf
                                                     ,"ventes":total_vente,"salaire":total_salarie,"transfers":total_transfer})

# views.py

# views.py

