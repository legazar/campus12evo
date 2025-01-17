from django.shortcuts import render,get_object_or_404
from .models import Logo_Ecole, Epreuve, Correction,Acheter,AcheterCorrect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from campay.sdk import Client as CamPayClient
import requests
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,permission_required
# pages principales

def accueil(request):
    return render(request,"index.html")

#pages secondaires

def epreuve(request):
    logos_ecoles=Logo_Ecole.objects.all()
    conteneur={"liste_logos":logos_ecoles}
    return render(request,"epreuve-correction.html",conteneur)



def cours(request):
    return render(request,"cours.html")
def cours_m(request):
    return render(request,"Cours/cours_maths.html")
def cours_p(request):
    return render(request,"Cours/cours_phy.html")
def cours_c(request):
    return render(request,"Cours/cours_ch.html")
def cours_if(request):
    return render(request,"Cours/cours_info.html")
def cours_mec(request):
    return render(request,"Cours/cours_mec.html")
def cours_bl(request):
    return render(request,"Cours/cours_bio.html")

def politique(request):
    return render(request,"politique.html")

def soutien(request):
    return render(request,"soutien.html")
def bord(request):
    return render(request,"bord.html")

def traitement(request):
    return render(request,"traitement.html")




def contact (request):
    return render (request, "contact.html")


    
def correction(request):
    list_correction = Correction.objects.all()
    context = {'list_correction':list_correction}
    return render(request,"correction.html",context)




def detail(request, id_logo_ecole): # renvoie une liste d'epreuve en fonction de l'ecole selectionnee
    logo_ecole = Logo_Ecole.objects.get(id=id_logo_ecole)
    list_epreuve = Epreuve.objects.filter(ecole=logo_ecole)
    context = {'logo_ecole': logo_ecole, 'list_epreuve': list_epreuve}
    return render(request, 'detail.html', context)

def message ( request):
    return render ( request,"message.html" )


########################  les apercus ############################################
@login_required
def apercu ( request, id_selection_epreuve): # apercu des epreuves + boutton d'achat
    epreuve = get_object_or_404(Epreuve, pk=id_selection_epreuve)
    
    # Enregistrer la consultation de l'épreuve par l'utilisateur actuel
    if not Epreuve.objects.filter(id=id_selection_epreuve, utilisateur=request.user).exists():
        epreuve.utilisateur = request.user
        epreuve.save()
    
    context = {'epreuve': epreuve,}
    return render (request, "apercu.html", context)

@login_required
def apercu_correction(request, correction_id): # renvoie l'apercu de corrections + bouttton d'achat 
    correction = get_object_or_404(Correction, pk=correction_id)
    if not Correction.objects.filter(id=correction_id, utilisateur=request.user).exists():
        correction.utilisateur = request.user
        correction.save()
    
    context = {'correction': correction,}
    return render (request, "apercu_correction.html", context)




########################  dashboard : cette partie gere les tableaux de bors #############################
@login_required
def dashboard(request): # tableau de bord principale affichant 'epreuves' et 'coorection' non achetees
    # retourne les epreuves et les corrections en fontions des consultation srecentes de l'utilisateur 
    epreuves_recentes = Epreuve.objects.filter(utilisateur=request.user).order_by('-date_consultation')[:5]
    corrections_recentes = Correction.objects.filter(utilisateur = request.user).order_by('-date_consultation')[:5]
    
    context = {
        'epreuves_recentes': epreuves_recentes,
        'corrections_recentes': corrections_recentes
        
    }
    return render(request, 'dashboard.html', context)

@login_required
def dashboard_achat(request):
    
    utilisateur = request.user
    achat_recents = Acheter.objects.filter(acheteur=utilisateur)
    achat_recents_correct = AcheterCorrect.objects.filter(acheteur=utilisateur)
    context = {
        'achat_recents_correct':achat_recents_correct,
        'achat_recents': achat_recents
    }
    return render(request, 'dashboard_achat.html', context)
@login_required
def dashboard_stat(request):
    epreuves_recentes = Epreuve.objects.filter(utilisateur=request.user).order_by('-date_consultation')[:5]
    corrections_recentes = Correction.objects.filter(utilisateur = request.user).order_by('-date_consultation')[:5]
    
    context = {
        'epreuves_recentes': epreuves_recentes,
        'corrections_recentes': corrections_recentes
        
    }
    return render(request, 'dashboard.html', context)



########################  initialisation de paiement avec l'api de CAMPAY #############################
@login_required
def paiement(request,epreuve_id):
    try:# gere les ereure au cas ou l'epreuve selectionnee n'existerai pas
        epreuve = Epreuve.objects.get(pk=epreuve_id)
    except Epreuve.DoesNotExist:
        return HttpResponse('Cette épreuve n\'existe pas.')
    
    # Récupération des informations de l'utilisateur connecté
    user = request.user
    last_name = user.username
    email = user.email
    # Initialisez le client Campay avec vos clés d'API
    
    campay = CamPayClient({
    "app_username" : "NP54kSL91mpOVJqYDNSpMHudPsUprQ68h5RBb79XFfI61nhnErBktg750Iv4SIS-54LoAlX1c4An26MgU0gywg",
    "app_password" : "POino7zaXCTR03kcLXAITxpnYu4Yd0ZFi4vF8xWE2mtLvYXjZgVSX113Zbuufv-q58_sVzWXUyytkBLbhVjOJA",
    "environment" : "DEV" #use "DEV" for demo mode or "PROD" for live mode
    })

    # Créez le lien de paiement avec les paramètres requis
    ep = str(epreuve_id)
    lien = 'http://127.0.0.1:8000/apercu/' + ep
    lien2 = 'http://127.0.0.1:8000/epreuve/telechargement/UIQBGG8SF46ASF466F4S56F4S6FSFNASGS6+565654654654/5465465GSGSAGSA6GAS4SF5454544'+ep+'56DG16ASSJKFNSKF/'
    
    payment_link = campay.get_payment_link({
        "amount": "5",
        "currency": "XAF",
        "description": "some description",
        "external_reference": "",
        "from": "",
        "first_name": "",
        "last_name": last_name,
        "email": email,
        "redirect_url": lien2,  # URL de redirection après paiement réussi
        "failure_redirect_url": lien,  # URL de redirection en cas d'échec de paiement
        "payment_options": "MOMO,CARD"
    })

        # Redirigez l'utilisateur vers le lien de paiement recuprerer
    print(payment_link['link']) 
    
    return redirect(payment_link['link'])

@login_required
def paiement_correction(request,correction_id):
    try: # gere les ereure au cas ou l'epreuve selectionnee n'existerai pas
        correction = Correction.objects.get(pk=correction_id)
    except Epreuve.DoesNotExist:
        return HttpResponse('Cette épreuve n\'existe pas.')
    
    # Récupération des informations de l'utilisateur connecté
    user = request.user
    last_name = user.username
    
    email = user.email
    # Initialisez le client Campay avec les clés d'API
    
    campay = CamPayClient({
    "app_username" : "NP54kSL91mpOVJqYDNSpMHudPsUprQ68h5RBb79XFfI61nhnErBktg750Iv4SIS-54LoAlX1c4An26MgU0gywg",
    "app_password" : "POino7zaXCTR03kcLXAITxpnYu4Yd0ZFi4vF8xWE2mtLvYXjZgVSX113Zbuufv-q58_sVzWXUyytkBLbhVjOJA",
    "environment" : "DEV" #use "DEV" for demo mode or "PROD" for live mode
    })

    # Créez le lien de paiement avec les paramètres requis
    ep = str(correction_id)
    lien = 'http://127.0.0.1:8000/apercu_correction/' + ep
    lien2 = 'http://127.0.0.1:8000/correction/telechargement_correction/osgkmodngosangoasngonasognos1 11o313 1o1614wgwg4g/wtw5tw5t6w54w'+ ep +'564 +5dgwwwgGKOMWFWF5F5W5FS5SF/'
    
    payment_link = campay.get_payment_link({
        "amount": "5",
        "currency": "XAF",
        "description": "some description",
        "external_reference": "",
        "from": "",
        "first_name": "",
        "last_name": last_name,
        "email": email,
        "redirect_url": lien2,  # URL de redirection après paiement réussi
        "failure_redirect_url": lien,  # URL de redirection en cas d'échec de paiement
        "payment_options": "MOMO,CARD"
    })

        # Redirigez l'utilisateur vers le lien de paiement
    print(payment_link['link']) 
    #print('>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<',payment_link['status'])# recuperer le status 
    return redirect(payment_link['link'])





########################  gestion du telecgargement #############################
@login_required
def telechargement(request, epreuve_id): # telechargement des epreuves avec sauvegarde de l'epreuve et de l'utilisateur a l'origine du telechargement
    user = request.user # recupere les information de l'utilisateur 
    
    try: # verifi si l'epreuve existe
        telecharge = Epreuve.objects.get(pk=epreuve_id)
    except Epreuve.DoesNotExist:
        return HttpResponse('Cette épreuve n\'existe pas.')
    
    context = { 'telecharge' : telecharge}

    acheteur = Acheter.objects.create(user=user,epreuve=telecharge)
    acheteur.save() # sauvegarde les identifiant de l'utilisateur et de l'epreuve qu'il a achetee
    return render ( request, 'telechargement.html', context)

@login_required
def telechargement_correction(request, correction_id):
    
    try:# verifi si la correction existe
        telecharge = Correction.objects.get(pk=correction_id)
    except Correction.DoesNotExist:
        return HttpResponse('Cette épreuve n\'existe pas.')
    context = { 'telecharge' : telecharge}
    return render ( request, 'telechargement_correction.html', context)




########################  gestion des recherhes #############################
@login_required
def recherche_dashboard(request): # recherche des epreuves dans le tableau de bord
    query = request.GET['article']
    liste_epreuve = Epreuve.objects.filter(nom__icontains =query)
    liste_correction = Correction.objects.filter(nom__icontains =query)
    #liste_epreuve_acheter = Acheter.objects.filter(epreuve.nom__icontains=query)
    #liste_correction_acheter = AcheterCorrect.objects.filter(correction =query)
    return render(request,'recherche_dasboard.html',{'liste_epreuve':liste_epreuve ,'liste_correction':liste_correction,''''liste_epreuve_acheter':liste_epreuve_acheter,'liste_correction_acheter':liste_correction_acheter,''' 'query':query})
@login_required
def recherche_correction(request):# recherhe des corrections
    query = request.GET['correction']
    liste_correction = Correction.objects.filter(nom__icontains =query)
    return render(request,'recherche_correction.html',{'liste_correction':liste_correction, 'query':query})
@login_required
def recherche_epreuve(request):# recherche des epreuves 
    query2 = request.GET['epreuve']
    liste_epreuve = Epreuve.objects.filter(nom__icontains =query2)
    return render(request,'recherche_epreuve.html',{'liste_epreuve':liste_epreuve, 'query2':query2})
@login_required
def recherche_epreuve_acheter(request):# recherche des epreuves acheters 
    query = request.GET['article']
    
    return render(request,'recherche_dasboard.html',{ 'query':query})
