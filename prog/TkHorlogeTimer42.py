#
# -*- coding: cp1252 -*-
import threading
import time
import tkinter as Tk
import math

__version__ = (0, 1, 0)
__build__ = (0, 0)
__date__ = (2023, 2, 12)
__author__ = ("Guy", "Tittelein")


## Classe permettant de gÃ©rer un Timer
class MyTimer:
    def __init__(self, tempo, target, args=[], kwargs={}):
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._tempo = tempo

    def _run(self):
        self._timer = threading.Timer(self._tempo, self._run)
        self._timer.start()
        self._target(*self._args, **self._kwargs)

    def start(self):
        self._timer = threading.Timer(self._tempo, self._run)
        self._timer.start()

    def stop(self):
        self._timer.cancel()


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
        self.zoneAffichage.coords(
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
            self.thetaDépart = self.thetaActuel
            self.deplace()
        else:
            self.thetaArrivée = self.listePosition[angle]
            pass  # rÃ©gler le deplacement

    def glisse(self, theta):
        self.zoneAffichage.coords(
            self.aig,
            self.xAxe,
            self.yAxe,
            self.xAxe + self.longueur * math.cos(theta),
            self.yAxe + self.longueur * math.sin(theta),
        )
        self.thetaActuel = theta


def creeMonAiguille(
    cnv,
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
        cnv,
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
        1: (((3, 3, 3), (3, 3, 3)), ((2, 6, 6), (2, 2, 6))),  #
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


class Horloge(Tk.Canvas):
    def __init__(self, parent, colonne, ligne):
        #        MyTimer.__init__(self, 1.0, self.turn)
        Tk.Canvas.__init__(
            self,
            parent,
            width=tailleHorloge + espacementHorloge,
            height=tailleHorloge + espacementHorloge,
        )

        self.create_oval(
            espacementHorloge,
            espacementHorloge,
            tailleHorloge + espacementHorloge,
            tailleHorloge + espacementHorloge,
            width=2,
            fill="#888888",
        )
        #        for i in range(60):
        #            self.create_line(100 + math.cos(i*math.pi/30-math.pi/2)*(80+(i%5 != 0)*5),
        #                                100 + math.sin(i*math.pi/30-math.pi/2)*(80+(i%5 != 0)*5),
        #                                100 + math.cos(i*math.pi/30-math.pi/2)*90, 100 + math.sin(i*math.pi/30-math.pi/2)*90, width = 2)
        #        self._second = self.create_line(0, 0, 0, 0, fill = "red")
        #        self._minute = self.create_line(0, 0, 0, 0, width = 2, fill = "blue")
        self.colonne = colonne
        self.ligne = ligne
        self._minute = creeMonAiguille(
            self,
            rendPosition(0, colonne, ligne),
            int(tailleHorloge / 2) + espacementHorloge,
            int(tailleHorloge / 2) + espacementHorloge,
            longueurAiguille,
            largeurAiguille,
            couleurAiguille[0],
            espacementHorloge,
            espacementHorloge + tailleHorloge - tailleBouton,
            tailleBouton,
            tailleBouton,
        )
        self._hour = creeMonAiguille(
            self,
            rendPosition(1, colonne, ligne),
            int(tailleHorloge / 2) + espacementHorloge,
            int(tailleHorloge / 2) + espacementHorloge,
            longueurAiguille,
            largeurAiguille,
            couleurAiguille[1],
            espacementHorloge,
            espacementHorloge + tailleHorloge - tailleBouton,
            tailleBouton,
            tailleBouton,
        )

    def affiche(self, valeur):
        self._hour.affiche(valeur, None)
        self._minute.affiche(valeur, None)

    #    def turn(self):


#        gmtime = time.gmtime()
#        self.coords(self._hour, 100, 100, 100 + math.cos(gmtime[3]*math.pi/12+gmtime[4]*math.pi/360-math.pi/2)*45,
#                       100 + math.sin(gmtime[3]*math.pi/12+gmtime[4]*math.pi/360-math.pi/2)*45)
#        self.coords(self._minute, 100, 100, 100 + math.cos(gmtime[4]*math.pi/30+gmtime[5]*math.pi/1800-math.pi/2)*70,
#                       100 + math.sin(gmtime[4]*math.pi/30+gmtime[5]*math.pi/1800-math.pi/2)*70),
#        self.coords(self._second, 100, 100, 100 + math.cos(gmtime[5]*math.pi/30-math.pi/2)*85,
#                       100 + math.sin(gmtime[5]*math.pi/30-math.pi/2)*85)
#        self.update()
def start(lh):
    for h in lh:
        h.start()


def deplace(actu, nouv, duréeDéplacement, echantillon, echantillonnage):
    k = echantillon / echantillonnage / duréeDéplacement
    for hor in listeHorloge:
        nouvellepositionAiguille = rendPosition(1, hor.colonne, hor.ligne)[
            nouv[int(hor.colonne / 2)]
        ]
        #        if hor.colonne==7 and hor.ligne==0:
        #            print (f"DÃ©placement de {hor._hour.thetaActuel} [{hor._hour.thetaActuel}] vers {nouvellepositionAiguille}",end=" et ")
        if hor._hour.thetaDépart != nouvellepositionAiguille:
            hor._hour.glisse(
                hor._hour.thetaDépart
                + (nouvellepositionAiguille - hor._hour.thetaDépart) * k
            )
        nouvellepositionAiguille = rendPosition(0, hor.colonne, hor.ligne)[
            nouv[int(hor.colonne / 2)]
        ]
        #        if hor.colonne==7 and hor.ligne==0:
        #            print (f"de {hor._minute.thetaActuel}  [{hor._minute.thetaActuel}] vers {nouvellepositionAiguille}")
        if hor._minute.thetaDépart != nouvellepositionAiguille:
            hor._minute.glisse(
                hor._minute.thetaDépart
                + (nouvellepositionAiguille - hor._minute.thetaDépart) * k
            )


def maj():
    global positionsActuelle, échantillon, échantillonnage
    maintenant = time.localtime()
    heure = int(maintenant[3])
    dh, h = int(heure / 10), heure % 10
    minute = int(maintenant[4])
    dm, m = int(minute / 10), minute % 10
    seconde = int(maintenant[5])
    ds, s = int(seconde / 10), seconde % 10
    #    print(f"{dh}{h}:{dm}{m}:{ds}{s}")
    if int(maintenant[5]) > debutDéplacement:
        échantillon = (maintenant[5] - debutDéplacement) * échantillonnage
        m += 1
        if m == 10:
            dm += 1
            m = 0
            if dm == 6:
                h += 1
                dm = 0
                if h == 9:
                    dh += 1
                    h = 0
        if dh == 2 and h == 4:
            dh = 0
            h = 0
        positionsDemandées = [dh, h, dm, m]
        #        print(f"{échantillon=}/{int((60-debutDéplacement)/échantillonnage)} déplacement :{positionsActuelle} -> {positionsDemandées}")
        deplace(
            positionsActuelle,
            positionsDemandées,
            60 - debutDéplacement,
            échantillon,
            échantillonnage,
        )
    else:
        for hor in listeHorloge:
            if hor.colonne in (0, 1):
                hor.affiche(dh)
            if hor.colonne in (2, 3):
                hor.affiche(h)
            if hor.colonne in (4, 5):
                hor.affiche(dm)
            if hor.colonne in (6, 7):
                hor.affiche(m)
        positionsActuelle = [dh, h, dm, m]
    root.update()


nombreHorlogesHorizontales = 8
nombreHorlogesVerticales = 3
tailleHorloge = 150
espacementHorloge = 10
tailleBouton = 20
largeurAiguille = 20
longueurAiguille = int(tailleHorloge - largeurAiguille) / 2
couleurAiguille = ("#880000", "#008800")
couleurFond = "#888888"
couleurFondHorloge = "#888888"
largeurFenetre = nombreHorlogesHorizontales * (tailleHorloge + 2 * espacementHorloge)
hauteurFenetre = nombreHorlogesVerticales * (tailleHorloge + 2 * espacementHorloge)
debutDéplacement = 60 - 7
échantillonnage = 0.005
root = Tk.Tk()
root.title("Horloge")
listeHorloge = []
for colonne in range(nombreHorlogesHorizontales):
    #    valeur = int(colonne /2)#+6
    for ligne in range(nombreHorlogesVerticales):
        h = Horloge(root, colonne, ligne)
        h.grid(row=ligne, column=colonne)
        listeHorloge.append(h)
#        h._minute.affiche(valeur)
#        h._hour.affiche(valeur)
positionsActuelle = [0, 0, 0, 0]
MyTimer(échantillonnage, maj).start()
root.mainloop()
