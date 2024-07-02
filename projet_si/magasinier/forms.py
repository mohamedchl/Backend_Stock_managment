from django.db.models import fields,Q
from django import forms
from .models import Produit,Transfer, reProduit,Stock_centre_primaire,Centre,Client,Achats_client,paye_credit,Achats_client_centre, Fournisseur, Produit_Fournisseur,Achats_matiereP,Employe,Absence_employe,Payement_sold_fournisseur,Demande_massrouf,Rapport_responsable,compteMagazinier,compteResponsable

class compteMagazinierForm(forms.ModelForm):
    class Meta:
        model = compteMagazinier
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }
class compteResponsableForm(forms.ModelForm):
    class Meta:
        model = compteResponsable
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password': forms.PasswordInput(),
            'confirm_password': forms.PasswordInput(),
        }

class ProduitForm(forms.ModelForm): 
    class Meta:
        model = Produit
        exclude = ['prix_total']

class reProduitForm(forms.ModelForm):
    class Meta:
        model = reProduit
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        selected_center = kwargs.pop('selected_center', None)
        super().__init__(*args, **kwargs)
        if selected_center:
            self.fields['Centre'].queryset = Centre.objects.filter(id=selected_center)
        else:
            self.fields['Centre'].queryset = Centre.objects.none()

        if selected_center:
            self.fields['Produit_primaire'].queryset = Stock_centre_primaire.objects.filter(Centre__id=selected_center)
        else:
            self.fields['Produit_primaire'].queryset = Stock_centre_primaire.objects.none()

class FournisseurForm(forms.ModelForm): 
    class Meta:
        model = Fournisseur
        exclude = ['solde']

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        exclude = ['cout','Date_transfer']
 
class ClientForm(forms.ModelForm):
    class Meta :
        model = Client
        exclude = ['somme_paye','Centre']

class Client_centreForm(forms.ModelForm):
    class Meta :
        model = Client
        exclude = ['somme_paye']


class Achats_clientform(forms.ModelForm):
    class Meta:
        model = Achats_client
        exclude = ['somme_paye']

class Achats_client_centreform(forms.ModelForm):
    class Meta:
        model = Achats_client_centre
        exclude = ['somme_paye']

    def __init__(self, *args, **kwargs):
        selected_center = kwargs.pop('selected_center', None)
        category_vent = kwargs.pop('category_vent', None)
        super().__init__(*args, **kwargs)
        if category_vent=="reproduit":
            self.fields.pop('produit_primaire')
            self.fields['Centre'].queryset = Centre.objects.filter(id=selected_center)
            self.fields['reproduit'].queryset = reProduit.objects.filter(
                Centre__id=selected_center
            )
        if category_vent=="produit_primaire":
            self.fields.pop('reproduit')
            self.fields['Centre'].queryset = Centre.objects.filter(id=selected_center)
            self.fields['produit_primaire'].queryset = Stock_centre_primaire.objects.filter(
                Centre__id=selected_center
            )



class creditForm(forms.ModelForm):
    class Meta:
        model = paye_credit
        fields = "__all__"

class FournisseurForm(forms.ModelForm): 
    class Meta:
        model = Fournisseur
        exclude = ['solde','produits_fournisseur']
 
class FournisseurPForm(forms.ModelForm): 
    class Meta:
        model = Produit_Fournisseur
        fields="__all__"

class AchatMPForm(forms.ModelForm):
    class Meta:
        model = Achats_matiereP
        fields = ['Date_achat','qte','Montant_payé']

class EmployeForm(forms.ModelForm): 
    class Meta:
        model = Employe
        exclude=['Salarie_mois']

class AbsenceEmployeForm(forms.ModelForm): 
    class Meta:
        model = Absence_employe
        fields="__all__"

class AbsenceEmployeDForm(forms.ModelForm): 
    class Meta:
        model = Absence_employe
        fields=['Employe_absente']

class PaimentSoldForm(forms.ModelForm):
    class Meta:
        model = Payement_sold_fournisseur
        fields=['Date_payement','montant_payé']

class DemandeMassroufForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        employe_choices = kwargs.pop('employe', None)
        super(DemandeMassroufForm, self).__init__(*args, **kwargs)
        if employe_choices:
            self.fields['employe'].queryset = employe_choices
        # Set Date_dem field as non-editable and keep its initial value
        self.fields['Date_dem'].widget.attrs['readonly'] = True

    class Meta:
        model = Demande_massrouf
        fields = ['employe', 'Date_dem', 'massrouf']

from django.forms import ClearableFileInput

class RapportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RapportForm, self).__init__(*args, **kwargs)
        self.fields['Date_R'].widget.attrs['readonly'] = True

    class Meta:
        model = Rapport_responsable
        fields = ['Date_R', 'Rapport']
        widgets = {
            'Rapport': ClearableFileInput(attrs={'multiple': False}),
        }