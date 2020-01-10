from tkinter import*
#from tkinter.messagebox import*
from recherche_creation_ports import*
#from search_create_ports_MFC import*
from trames_fonctions import*

numeroDeSerie=''

class instrument:
    def __init__(self):
        self.nom="INSTRUMENT"

    def liste_port(self):
        port_disponible=listing_ports()
        return(port_disponible)

    def cree_port(self):
        monPort=cree_port_unique()
        return(monPort)

    def Control_mode(self,monPort,modeControle):
        Control_mode_12('E',modeControle,monPort)

    def laCapacite(self,monPort):
        capacite=Capacity_21('L',0,monPort)
        return(capacite)

    def fluideNom(self,monPort):
        fluide=Fluid_name_25('L',0,monPort)
        return(fluide)
    
    def modelType(self,monPort):
        modele=BHT_Model_number_91('L',0,monPort)
        return(modele)

    def numeroSerie(self,monPort):
        numeroDeSerie=Serial_number_92('L',0,monPort)
        return(numeroDeSerie)

    def capaciteUnit(self,monPort):
        uniteCapacite=Capacity_unit_129('L',0,monPort)
        return(uniteCapacite)

    def laMesure(self,monPort):
        maMesure=fMeasure_205('L',0,monPort)
        return(maMesure)

    def laConsigne(self,monPort,consigne):
        fSetpoint_206('E',consigne,monPort)

canal1=instrument()
portDisponible=canal1.liste_port()
nbrePort=len(portDisponible)
monPort=canal1.cree_port()

lesCOMs=[""]*20
for bla in range(0,nbrePort):
    lesCOMs[bla]=str(portDisponible[bla])

if monPort=="":
    port_actif="Pas d'instrument en ligne"
    instruction="Pour sortir fermer cette fenêtre"
else:
    port_actif="Un instrument en ligne"
    instruction="Pour poursuivre : fermer cette fenêtre"

fenCom=Tk()
fenCom.geometry("400x400+150+50")
fenCom.title("CONFIGURATION")
fenCom['bg']='white'

etiquette_port_actif=Label(fenCom,text=port_actif,bg='white',font="ARIAL 15",fg='red')
etiquette_port_actif.pack()
for bla in range(0,nbrePort):
    etiquette_port_present=Label(fenCom,text=lesCOMs[bla],bg='white',font="ARIAL 12",fg='blue')
    etiquette_port_present.pack()
etiquette_instruction=Label(fenCom,text=instruction,bg='white',font="ARIAL 15",fg='red')
etiquette_instruction.pack()
fenCom.mainloop()

if monPort !="":
    while numeroDeSerie=='':
        numeroDeSerie=canal1.numeroSerie(monPort)
    canal1.Control_mode(monPort,0)
    modele=canal1.modelType(monPort)
    nom_de_fluide=canal1.fluideNom(monPort)
    unite=canal1.capaciteUnit(monPort)
    pleine_echelle=canal1.laCapacite(monPort)
    mesure=canal1.laMesure(monPort)

    def admission_consigne(valeur):
        valeur=float(valeur)
        canal1.laConsigne(monPort,valeur)

    counter=0
    def inc_label():
        def count():
            global counter
            counter += 1
            graph_mesure.delete(ALL)
            mesure=canal1.laMesure(monPort)
            mesure_graph=290-(((mesure)/pleine_echelle)*290)
            mesure_graph=str(mesure_graph)
            graph_mesure.create_rectangle("10",mesure_graph,"85","290",fill="green")
            graph_mesure.after(100, count)
        count()

    counter_mesure=0
    def inc_label_mesure(label_mesure):
        def count_mesure():
            global counter_mesure
            counter_mesure += 1
            label_mesure.config(text=str(canal1.laMesure(monPort))+" "+unite)
            label_mesure.after(100, count_mesure)
        count_mesure()
            

    fen=Tk()
    fen.title("Bargraphe du flux")
    fen.geometry("300x500+50+50")
    fen['bg']="AliceBlue"

    label_modele=Label(fen,text=modele,bg="Azure",fg="blue",font="ARIAL 18")
    label_modele.pack()
    label_numeroDeSerie=Label(fen,text=numeroDeSerie,bg="Cornsilk",fg="red",font="ARIAL 20")
    label_numeroDeSerie.pack()
    label_nom_de_fluide=Label(fen,text=nom_de_fluide,bg="Azure",fg="blue",font="ARIAL 18")
    label_nom_de_fluide.pack()
    label_capacite=Label(fen,text=str(pleine_echelle)+" "+unite,bg="Azure",fg="Blue",font="ARIAL 18")
    label_capacite.pack()

    label_mesure=Label(fen,bg="Azure",fg="ForestGreen",font="ARIAL 20")
    label_mesure.place(x='10',y='460')
    inc_label_mesure(label_mesure)

    graph_mesure=Canvas(fen,width="90",height="300",bg="white")
    ruban_mesure=graph_mesure.create_rectangle("10",str(canal1.laMesure(monPort)),"40","0",fill="green")
    inc_label()
    graph_mesure.place(x='40',y='150')

    consigne=DoubleVar()
    resolution_echelle=pleine_echelle/100
    rouleur=Scale(fen,variable=consigne,bg="white",troughcolor="red",from_=pleine_echelle, to =0,orient=VERTICAL,width=90,length=298,resolution=resolution_echelle,command=admission_consigne)
    rouleur.place(x='140',y='150')
    fen.mainloop()
