from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import ImageUploadForm
from django.contrib import messages
import re
import pytesseract
from PIL import Image
import os


# Create your views here.


def home(request):
    all_facture, _ = extract_data()
    
        
    data = {
        'facture':all_facture
    }
    return render(request, 'app/index.html', data)

def welcome(request):
    return render(request, 'app/welcome.html')

def charts(request):
    return render(request, 'app/charts.html')

def tables(request):
    return render(request, 'app/tables.html')

def tables2(request):

    _, all_produit = extract_data()
    data = {
        'produit':all_produit,
    }

    return render(request, 'app/tables2.html', data)

def tables3(request):
    all_facture, _ = extract_data()
    
        
    data = {
        'facture':all_facture
    }


    return render(request, 'app/tables3.html', data)

def extract_data():

    chemin=r"C:\Program Files\Tesseract-OCR\tesseract"
    pytesseract.tesseract_cmd=chemin


    folder_path_image = os.path.join('media', 'imgs')
    folder_path_data = os.path.join('media', 'data_treat')

    image_names = [file for file in os.listdir(folder_path_image) if os.path.isfile(os.path.join(folder_path_image, file))]
    full_images_paths = [os.path.join(folder_path_image, image_name) for image_name in image_names]


    all_facture = []
    all_produit = []

    for image in full_images_paths:
        img=Image.open(image)
        text=pytesseract.image_to_string(img)


        fichier = open(f'{os.path.join(folder_path_data, "data_treatment_file.txt")}', 'w')
        fichier = fichier.write(text)
        with open(f'{os.path.join(folder_path_data, "data_treatment_file.txt")}', 'r') as fichier :
            ligne = fichier.readlines()

        with open(f'{os.path.join(folder_path_data, "data_treatment_file.txt")}', 'r') as fichier :    
            chaine=fichier.read()
        if ligne[0]=='HUBERT ET DURAND\n':
            fournisseur=ligne[0].split('\n')[0]
            numero=int(ligne[4].split('\n')[0])
            date=ligne[5].split('\n')[0]
            liste_des_produits={}

                
            pattern = r"DESCRIPTION DE L'ARTICLE PRIX UNITAIRE QUANTITE TOTAL(.*?)TOTAL TTC"
            resultats = re.search(pattern,chaine, re.DOTALL)
            info_produits=resultats.group(1).strip().split('\n')
            TVA=0.1
            s=0
            for i in range(0,len(info_produits)):
                L=info_produits[i].split()
                L = [elem for elem in L if elem != '€' and elem != "de" and elem != "l'entreprise"]
                nom,prix_unitaire,quantité=L[0],L[1],L[2]
                prix_unitaire=prix_unitaire.replace(',', '.')
                quantité=quantité.replace(',', '.')
                liste_des_produits[nom]=(float(prix_unitaire),float(quantité))
                Total=float(prix_unitaire)*float(quantité)
                
                s=s+Total
            v=s*(1+TVA)
            liste_des_factures=[numero,fournisseur,date,s,TVA,v]
        else:     

            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"
            img = Image.open(image)
            text = pytesseract.image_to_string(img)



            def extraction(texte, mot):

                indice = text.find(mot)
                if indice != -1:

                    debut = indice + len(mot)                      

                    fin = text.find('\n', debut)

            

                    if fin == -1:

                        extrait = text[debut:]

                    else:

                        extrait = text[debut:fin]

            

                    return extrait.strip()

            

                return None

            lignes = text.splitlines()

            text1 = [ligne for ligne in lignes if len(ligne)!=0]

            nvtext=""

            for ligne in text1:

                if ligne != text1[-1]:

                    nvtext += ligne + "\n"

                else: nvtext += ligne



            noms=[]
            quantites=[]
            prix_unitaire=[]
            liste_des_produits={}

            noms.append(nvtext[nvtext.find("Total:")+7:nvtext.find("Eau")+3])
            noms.append(nvtext[nvtext.find("395,00€")+8:nvtext.find("Café")+4])
            noms.append(nvtext[nvtext.find("702,00€")+8:nvtext.find("Huile")+5])

            quantites.append(nvtext[nvtext.find("Eau ")+4:nvtext.find(" 30,00€")])
            quantites.append(nvtext[nvtext.find("Café ")+5:nvtext.find(" 50,00€")])
            quantites.append(nvtext[nvtext.find("Huile ")+6:nvtext.find(" 400,00€")])

            prix_unitaire.append(nvtext[nvtext.find("19,00 ")+6:nvtext.find(" 395,00€")])
            prix_unitaire.append(nvtext[nvtext.find("70,00 ")+6:nvtext.find(" 702,00€")])
            prix_unitaire.append(nvtext[nvtext.find("60,00 ")+6:nvtext.find(" 40,00€")])
            liste_des_produits[noms[0]]=(prix_unitaire[0],quantites[0])
            liste_des_produits[noms[1]]=(prix_unitaire[1],quantites[1])
            liste_des_produits[noms[2]]=(prix_unitaire[2],quantites[2])
            prix_unitaire1=nvtext[nvtext.find("19,00 ")+6:nvtext.find(" 395,00€")-1].replace(",",".")
            prix_unitaire2=nvtext[nvtext.find("70,00 ")+6:nvtext.find(" 702,00€")-1].replace(",",".")
            prix_unitaire3=nvtext[nvtext.find("60,00 ")+6:nvtext.find(" 40,00€")-1].replace(",",".")

            quantite1= float(nvtext[nvtext.find("Eau ")+4:nvtext.find(" 30,00€")].replace(",","."))
            quantite2= float(nvtext[nvtext.find("Café ")+5:nvtext.find(" 50,00€")].replace(",","."))
            quantite3= float(nvtext[nvtext.find("Huile ")+6:nvtext.find(" 400,00€")].replace(",","."))

            calcultotal = float(prix_unitaire1)+float(prix_unitaire2)+float(prix_unitaire3)
            calcultotal = format(calcultotal, '.2f')
            CALCULTOTAL = float(prix_unitaire1)*quantite1+float(prix_unitaire2)*quantite2+float(prix_unitaire3)*quantite3
            CALCULTOTAL = format(CALCULTOTAL, '.2f')

            #n=len(bloc.splitlines())


            liste_des_factures=[]

            liste_des_factures.append(int(extraction(text, "FACTURE N:")))
            liste_des_factures.append("Food Alumni")
            liste_des_factures.append(extraction(text, "Date:"))
            liste_des_factures.append("{}€".format(calcultotal))
            liste_des_factures.append(extraction(text, "TVA:"))
            liste_des_factures.append("{}€".format(CALCULTOTAL))



        
        all_facture.append(liste_des_factures)
        all_produit.append(liste_des_produits)

    
    return all_facture, all_produit

    
        
   
    
    


    



def charger(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Le chemin de l'image est accessible via form.cleaned_data['image']
            image_path = handle_uploaded_file(form.cleaned_data['image'])
            # Ajoutez ici votre logique de traitement avec le chemin de l'image
            # Par exemple, rediriger vers une autre page avec le chemin de l'image
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"
            # Open the image file
            image = Image.open(image_path)
            # Perform OCR using PyTesseract
            text = pytesseract.image_to_string(image)
            # Print the extracted text
            #print(text)
            extract_data(image_path)


            return render(request, 'app/charts.html', {})
    else:
        form = ImageUploadForm()
    return render(request, 'app/charger1.html', {'form': form})


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['image'])
            return redirect('home')
    else:
        form = ImageUploadForm()
    return render(request, 'app/upload_image.html', {'form': form})

def handle_uploaded_file(file):
    # Create the 'media/imgs' folder if it doesn't exist
    folder_path = os.path.join('media', 'imgs')
    os.makedirs(folder_path, exist_ok=True)

    
    # Saving
    file_path = os.path.join(folder_path, file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)




def logIn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        

        if user is not None:
            login(request, user)
            username = user.username
            return render(request, 'app/index.html')
        
        else:
            return render(request,'app/login.html')

    return render(request, 'app/login.html')   