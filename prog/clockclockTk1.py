#
from tkinter import *
import math
import random


class Aiguille:
    def __init__(
        self,
        zoneAffichage,
        thetaDep=0,
        hChangement=None,
        duréeChangement=None,
        thetaArrivée=None,
        xAxe=0,
        yAxe=0,
        longueur=0,
        épaisseur=1,
        couleur="#000000",
    ):
        self.zoneAffichage = zoneAffichage
        self.thetaActuel = thetaDep
        self.hChangement = hChangement
        self.duréeChangement = duréeChangement
        self.thetaDépart = thetaDep
        self.thetaArrivée = thetaArrivée
        self.xAxe = xAxe
        self.yAxe = yAxe
        self.longueur = longueur
        self.épaisseur = épaisseur
        self.couleur = couleur
        self.trace()

    def trace(self):
        self.aig = self.zoneAffichage.create_line(
            self.xAxe,
            self.yAxe,
            self.xAxe + self.longueur * math.cos(self.thetaActuel),
            self.yAxe + self.longueur * math.sin(self.thetaActuel),
            fill=self.couleur,
            width=self.épaisseur,
            capstyle="round",
        )

    def augmente(self):
        self.thetaActuel += 2 * math.pi / 360
        if self.thetaActuel > 2 * math.pi:
            self.thetaActuel -= 2 * math.pi
        self.deplace()

    def diminue(self):
        self.thetaActuel -= 2 * math.pi / 360
        if self.thetaActuel < 0:
            self.thetaActuel += 2 * math.pi
        self.deplace()

    def deplace(self):
        canvas.coords(
            self.aig,
            self.xAxe,
            self.yAxe,
            self.xAxe + self.longueur * math.cos(self.thetaActuel),
            self.yAxe + self.longueur * math.sin(self.thetaActuel),
        )

    def affiche(self, angle, duréeChangement=None):
        self.duréeChangement = duréeChangement
        self.thetaActuel = self.listePosition[angle]
        if duréeChangement == None:
            self.thetaActuel = self.listePosition[angle]
            self.deplace()
        else:
            self.thetaArrivée = self.listePosition[angle]
            pass  # régler le deplacement


def creeMonAiguille(
    listePositions,
    xAxe,
    yAxe,
    longueur,
    épaisseur,
    couleur,
    positionHorizontaleBouton,
    positionVerticaleBouton,
    largeurBouton,
    hauteurBouton,
):
    aiguille = Aiguille(
        canvas,
        thetaDep=0,
        xAxe=xAxe,
        yAxe=yAxe,
        longueur=longueur,
        épaisseur=épaisseur,
        couleur=couleur,
    )
    """
    aiguille.boutonPlus=Button(canvas,text="+",bg="#888888", fg="white",command=aiguille.augmente)
    aiguille.boutonPlus.place(x=positionHorizontaleBouton,y=positionVerticaleBouton,width=largeurBouton,height=hauteurBouton)
    aiguille.boutonMoins=Button(canvas,text="-",bg="#888888", fg="white",command=aiguille.diminue)
    aiguille.boutonMoins.place(x=positionHorizontaleBouton+largeurBouton,y=positionVerticaleBouton,width=largeurBouton,height=hauteurBouton)
    """
    aiguille.listePosition = listePositions
    return aiguille


def rendPosition(a, i, j):
    chiffres = {
        0: (
            ((0, 6, 6), (2, 2, 0)),
            ((4, 6, 6), (2, 2, 4)),
        ),  # chiffres[numero][colonne][aiguille][positionV]
        1: (((3, 3, 3), (3, 3, 3)), ((6, 6, 6), (2, 2, 2))),  #
        2: (((0, 0, 6), (0, 2, 0)), ((4, 6, 4), (2, 4, 4))),  #    5  6  7
        3: (((0, 0, 0), (0, 0, 0)), ((4, 6, 4), (2, 4, 6))),  #     \ | /
        4: (((2, 6, 3), (2, 0, 3)), ((2, 6, 6), (2, 2, 6))),  #    4-- --0
        5: (((0, 6, 0), (2, 0, 0)), ((4, 4, 6), (4, 2, 4))),  #     / | \
        6: (((0, 6, 6), (2, 2, 0)), ((4, 4, 6), (4, 2, 4))),  #    3  2  1
        7: (((0, 3, 3), (0, 3, 3)), ((4, 6, 6), (2, 2, 6))),  #
        8: (((0, 6, 6), (2, 0, 0)), ((4, 6, 6), (2, 4, 4))),  #
        9: (((0, 6, 0), (2, 0, 0)), ((4, 6, 6), (2, 2, 4))),  #
    }
    rep = []
    for v in range(10):
        rep.append(chiffres[v][i % 2][a][j] * 2 * math.pi / 8)
    return rep


monTk = Tk()
nombreHorlogesHorizontales = 8
nombreHorlogesVerticales = 3
tailleHorloge = 150
espacementHorloge = 1
tailleBouton = 20
largeurAiguille = 20
longueurAiguille = int(tailleHorloge - largeurAiguille) / 2
couleurAiguille = "#000000"
couleurFond = "#888888"
couleurFondHorloge = "#888888"
largeurFenetre = nombreHorlogesHorizontales * (tailleHorloge + 2 * espacementHorloge)
hauteurFenetre = nombreHorlogesVerticales * (tailleHorloge + 2 * espacementHorloge)
canvas = Canvas(
    monTk, width=largeurFenetre, height=hauteurFenetre, background=couleurFond
)
listeHorloges = [
    [0] * nombreHorlogesVerticales for j in range(nombreHorlogesHorizontales)
]
#
# Initialisation de horloges
#
for i in range(nombreHorlogesHorizontales):
    positionHorizontale = (
        espacementHorloge + (tailleHorloge + 2 * espacementHorloge) * i
    )
    valeur = int(i / 2) + 6
    for j in range(nombreHorlogesVerticales):
        positionVerticale = (
            espacementHorloge + (tailleHorloge + 2 * espacementHorloge) * j
        )
        # Tracé du cercle
        canvas.create_oval(
            positionHorizontale,
            positionVerticale,
            positionHorizontale + tailleHorloge,
            positionVerticale + tailleHorloge,
            fill=couleurFondHorloge,
        )
        # Création et tracé des aiguilles
        aiguilles = [0 for j in range(2)]
        for numeroAiguille in range(2):
            listePositions = rendPosition(numeroAiguille, i, j)
            positionHorizontaleBouton = (
                positionHorizontale + numeroAiguille * tailleHorloge - 2 * tailleBouton
            )
            positionVerticaleBouton = positionVerticale + tailleHorloge
            aiguilles[numeroAiguille] = creeMonAiguille(
                listePositions,
                xAxe=int(positionHorizontale + tailleHorloge / 2),
                yAxe=int(positionVerticale + tailleHorloge / 2),
                longueur=longueurAiguille,
                épaisseur=largeurAiguille,
                couleur=couleurAiguille,
                positionHorizontaleBouton=positionHorizontaleBouton,
                positionVerticaleBouton=positionVerticale + tailleHorloge,
                largeurBouton=tailleBouton,
                hauteurBouton=tailleBouton,
            )
            aiguilles[numeroAiguille].affiche(valeur)
        listeHorloges[i][j] = aiguilles

canvas.pack()
canvas.mainloop()
