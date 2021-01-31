# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 17:46:36 2020

@author: jad
"""

import os
import numpy as np
import cv2 
from matplotlib.image import imread
import shutil
import PIL

#Définition des constante de base de la vidéo

nomVideo = "test2.mp4"
cap = cv2.VideoCapture(nomVideo)
nombreImage = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))   



def separationImages(fichier):
    if os.path.exists("video2.mp4"):
        os.remove("video2.mp4")
    if os.path.exists("videofin2.mp4"):
        os.remove("videofin2.mp4")
    if(len(os.listdir('ImageCompresse')) !=0):
        for f in os.listdir('ImageCompresse'):
            os.remove(os.path.join('ImageCompresse', f))
    cap = cv2.VideoCapture(fichier)
    try :
        if not os.path.exists('dossierImage'):
            os.makedirs("dossierImage")
    except OSError:
        print("Error: Creation du fichier de récuperation des images")
        
    imageActuelle = 0
    while(imageActuelle < cap.get(cv2.CAP_PROP_FRAME_COUNT)):
        #récuperation des images
        ret, image = cap.read()
        # Sauvegarde des images en format jpg
        nom = './dossierImage/image' + str(imageActuelle) + '.jpg'
        print ("Creation..." + nom )
        cv2.imwrite(nom, image)
        imageActuelle += 1
    cap.release()
    cv2.destroyAllWindows()




def compression():
    if len(os.listdir('./ImageCompresse')) == 0:
        listImage = []
        listComp = []
        colorList = []
        arrayImage = 0
        for i in range(0, nombreImage):
            frame = imread('./dossierImage/image' +str(i)+ ".jpg")
            height,width,layers = frame.shape
            listImage.append(frame)
            b,g,r = cv2.split(frame)  # Séparation des matrices de couleurs
            colorList.append(b)
            colorList.append(g)
            colorList.append(r)
            for j in range(0, 3):
                Bt = np.fft.fft2(colorList[j]) # calcul de la fft
                BtSort = np.sort(np.abs(Bt.reshape(-1))) #triage des coefficient de Fourier
                keep = 0.05 # determination du pourcentage de données conservé
                thresh = BtSort[int(np.floor((1-keep)*len(BtSort)))] # calcul du seuil
                ind  = np.abs(Bt) > thresh # Determination des coefficient à enlever
                atLow = Bt*ind # On enlève des coefficients
                aLow = np.fft.ifft2(atLow).real # transformee inverse
                colorList[j] = aLow;
            arrayImage = np.dstack((colorList[2],colorList[1],colorList[0])) # Fusion des matrices couleurs pour reconstituer l'image
            arrayImage = cv2.resize(arrayImage, (width, height), interpolation = cv2.INTER_NEAREST)
            cv2.imwrite("ImageCompresse"+ str(i)+ ".jpg", arrayImage) # création de l'image
            shutil.move("ImageCompresse"+ str(i)+ ".jpg","./ImageCompresse")
            colorList.clear()
            arrayImage = 0;
       # height,width,layers = listImage[1].shape
        video = cv2.VideoWriter('video2.mp4',cv2.VideoWriter_fourcc(*'MP4V'),25,(width, height))
        for j in range(nombreImage):
            image = cv2.imread('./ImageCompresse/ImageCompresse' +str(j)+ ".jpg")
            listComp.append(image)
        for j in range(nombreImage):
            video.write(listComp[j])
        video.release()
        cv2.destroyAllWindows()
        os.system("ffmpeg -i video2.mp4 -vcodec  h264 -crf 28 videofin2.mp4") # encodage de la video
 
    # Il faut telehrger la bibliothèque ffmpeg pour lancer cette dernière commande, la bibliothèque existe sur tous les systèmes d'éxploitation



separationImages(nomVideo)        
compression() 
 
    
    
            
            
        