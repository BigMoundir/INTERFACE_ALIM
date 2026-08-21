import tkinter as tk 
from tksheet import Sheet 
from tkinter import ttk
import procedure
import pyvisa
import outils
import driver 
import time
import threading 
import tkinter.messagebox as messagebox


rm= pyvisa.ResourceManager()

#décla des variables globales (qui permet d'avoir des thermes valables pour tout les fichiers)

alim = None
multi=None
load=None
alimentation_driver = None
multimetre_driver = None
dynamic_load_driver = None
data = None
utilisation_shunt = None
valeur_shunt = None

start = time.time()

#fonctions qu'on appel en activant les bouttons de l'interface

def valider_configuration():
    global alim,multi,load,alimentation_driver,multimetre_driver,dynamic_load_driver
    try:
        modele = model_combo.get()
        print (modele)

        alimentation_driver = outils.lien_driver_alim(modele)
        multimetre_driver = driver.STANDART_MULTIMETER_DRIVER
        dynamic_load_driver =driver.EA_EL_DYNAMIC_LOAD_DRIVER
        
        visa_alim = gpib_alim.get()
        visa_multi = gpib_multimetre.get()
        visa_load = gpib_charge.get()

        connection_alim = proto_alim.get()
        connection_load = proto_load.get()
        connection_multi = proto_multi.get()

        if connection_alim == "GPIB":
            alim_name = f"GPIB0::{visa_alim}::INSTR"           #attention ici c'est uniquement sur "GPIB0" à voir pour plus tard 
        else:
            alim_name = f"ASRL{visa_alim}::INSTR"

        if connection_multi == "GPIB":
            multi_name = f"GPIB0::{visa_multi}::INSTR"
        else:
            multi_name = f"ASRL{visa_multi}::INSTR"

        if connection_load == "GPIB":
            load_name = f"GPIB0::{visa_load}::INSTR"
        else:
            load_name = f"ASRL{visa_load}::INSTR"

        #=============================================================
        #               INITIALISATION DES VARIABLES
        #=============================================================

        #initialisation de l'alim
        alim=rm.open_resource(alim_name)
        alim.write('*RST; *CLS')

        #initialisation du multi
        multi=rm.open_resource(multi_name)
        multi.write('*RST; *CLS')

        #initialisation de la charge 
        load=rm.open_resource(load_name)
        load.write('*RST; *CLS')

        open_image_window()

    except Exception as e:
        tk.messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")



# Fonctions qui font le lien entre le bouton et le programme "procedure"
def simu_tension_sortie():
    try:
        print("Lancer test de tension de sortie...")
        sortie.clear()
        messagebox.showinfo(
                    title="simu_tension_sortie",
                    message=f'Veuillez configurer le multimètre en mode "INPUT FRONT" .\nPuis cliquez sur OK pour continuer'
                )
        IVS_1_a=procedure.tension_sortie_2(data,alim,multi,alimentation_driver,multimetre_driver)
        for i in range(len(IVS_1_a[0])):
            sortie.set_cell_data(r= i, c=0, value = "{:.3f}".format(IVS_1_a[0][i]).replace('.', ','))
            sortie.set_cell_data(r= i, c=1, value = "{}".format(IVS_1_a[1][i]).replace('.', ','))     #pour les R-S il faut rajouter un [0] a la fin de IVS_1_a[1][i] car la sortie est en forme de liste 
        sortie.set_header_data(value="V mesuré",c=0)
        sortie.set_header_data(value="V affiché",c=1)
        sortie.set_header_data(value="/",c=2)
    except Exception as e:
        tk.messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")
    

def simu_regulation_de_tension():
    try:
        print("Lancer test de régulation de tension...")
        sortie.clear()
        messagebox.showinfo(
                    title="simu_tension_sortie",
                    message=f'Veuillez configurer le multimètre en mode "INPUT FRONT" .\nPuis cliquez sur OK pour continuer'
                )
        IVS_1_b=procedure.regulation_tension_avec_charge_et_bruit(data,alim,multi,load,alimentation_driver,multimetre_driver,dynamic_load_driver)
        for i in range(0,len(IVS_1_b[0]),2):
            sortie.set_cell_data(r= int(i/2), c=0, value = "{:.3f}".format(IVS_1_b[0][i]).replace('.', ','))
        for i in range(1,len(IVS_1_b[0]),2):
            sortie.set_cell_data(r= int((i-1)/2), c=1, value = "{:.3f}".format(IVS_1_b[0][i]).replace('.', ','))

        for i in range(len(IVS_1_b[1])):
            sortie.set_cell_data(r= i, c=2, value ="{:.3f}".format(IVS_1_b[1][i]).replace('.', ','))

        sortie.set_header_data(value="V mesuré (I=0A)",c=0)
        sortie.set_header_data(value="V mesuré (I=Io)",c=1)
        sortie.set_header_data(value="Bruit",c=2)
    except Exception as e:
        tk.messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")

def simu_courant_de_sortie():
    try:
        global utilisation_shunt,valeur_shunt
        print("Lancer test de courant de sortie...")
        valeur_shunt = entry_shunt.get()
        print(utilisation_shunt.get(),valeur_shunt)
        sortie.clear()
        messagebox.showinfo(
                    title="simu_tension_sortie",
                    message=f'Veuillez configurer le multimètre en mode "INPUT REAR" .\nPuis cliquez sur OK pour continuer'
                )
        IVS_1_C=procedure.courant_sortie_2(data,alim,multi,load,alimentation_driver,multimetre_driver,dynamic_load_driver,utilisation_shunt,valeur_shunt)
        for i in range(len(IVS_1_C[0])):
            if len(IVS_1_C) == 3:
                sortie.set_header_data(value="V mesuré",c=0)
                sortie.set_header_data(value="I déduit",c=1)
                sortie.set_header_data(value="I affiché",c=2)
                sortie.set_cell_data(r= i, c=1, value = "{:.3f}".format(IVS_1_C[0][i]).replace('.', ','))
                sortie.set_cell_data(r= i, c=0, value = "{:.3f}".format(IVS_1_C[1][i]).replace('.', ','))
                sortie.set_cell_data(r= i, c=2, value = "{}".format(IVS_1_C[2][i]).replace('.', ','))  #ici y a un probele parce que le dernier [0] c'est pour mettre la vaeur en float parce qu'elle sort n liste pour les HMP, or ca diffère en fonction de la marque de l alim (ex: TTI sort en str et pas en liste)
            if len(IVS_1_C) == 2:
                sortie.set_header_data(value="I mesuré",c=0)
                sortie.set_header_data(value="I affiché",c=1)
                sortie.set_header_data(value="/",c=2)
                sortie.set_cell_data(r= i, c=0, value = "{:.3f}".format(IVS_1_C[0][i]).replace('.', ','))
                sortie.set_cell_data(r= i, c=1, value = "{}".format(IVS_1_C[2][i]).replace('.', ','))
    except Exception as e:
        tk.messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")


def open_image_window():
    window = tk.Toplevel()
    window.title("MONTAGE")

    # Charger une image PNG ou GIF (remplace par ton chemin)
    photo = tk.PhotoImage(file=r"C:\Users\gaspard.friteau\Desktop\projet_alim\.venv\Montage.png")

    label_image = tk.Label(window, image=photo)
    label_image.image = photo  # garder la référence
    label_image.pack(padx=10, pady=10)

    btn_ok = tk.Button(window, text="OK", command=window.destroy)
    btn_ok.pack(pady=10)


def valide_tableur():
    global data

    data = sheet.get_sheet_data()

def toogle_shunt_entry():
    print(utilisation_shunt)
    print(type(utilisation_shunt))
    
    if utilisation_shunt.get()==1:
        entry_shunt.config(state="normal")
    else:
        entry_shunt.config(state="disabled")
        






#Creation de la fenetre principale 
root = tk.Tk()
root.title("Allimentation DC - programme automatique")
root.geometry("1070x750")
root.resizable(False,False)
root.configure(background="#cbcbcb")
root.grid_rowconfigure(1, weight=5)
root.grid_columnconfigure(0, weight=5)

style = ttk.Style()
style.configure("RedBold.TLabelframe.Label", foreground="red", font=("TkDefaultFont", 10, "bold"))

#===========================================================================
#                   ESPACE CONFIGURATION
#===========================================================================
frame_config = ttk.LabelFrame(root, text="1/ Configuration", padding=10, style="RedBold.TLabelframe")
frame_config.grid(row=0,column=0, padx=10, pady=10)

#GPIB/USB
proto_alim = tk.StringVar(value="GPIB")
proto_multi = tk.StringVar(value="GPIB")
proto_load = tk.StringVar(value="GPIB")

#label theme colonne
ttk.Label (frame_config, text="MODELE").grid(row=0, column=1, sticky="w", pady=2)     # row et column pour le positionnement/ sticky pour le style/ pady pour ?
ttk.Label (frame_config, text="Adresse GPIB/USB").grid(row=0, column=2, sticky="w", pady=2)

#choix modele allimentation 
model_var = tk.StringVar()    #voir à quoi ca sert 
model_combo = ttk.Combobox(frame_config, textvariable=model_var, width=30)
model_combo["values"] = ("TTI",
                          "KEYSIGHT N8700",
                          "KEYSIGHT E3632A",
                          "KEYSIGHT E3634A",
                          "KEYSIGHT E3644A",
                          "AGILENT N6705A",
                          "ROHDE & SCHWARZ HMP SERIE",
                          "ROHDE & SCHWARZ NGP800",
                          "TDK LAMBDA GENH 12.5-60",
                          "EA-PS 2084-10B"
                          )
model_combo.current(0)
model_combo.grid(row=1, column=1,padx=0.1 ,pady=0.1 ,sticky="ew")

#choix modele charge 
model_charge_var = tk.StringVar()
model_charge_combo = ttk.Combobox(frame_config, textvariable=model_charge_var)
model_charge_combo["values"] = ("HP6060B", "EA-EL_9080-340B")
model_charge_combo.current(0)       #si rien de choisi, objet 0 par defaut 
model_charge_combo.grid(row=3, column=1,padx=5, pady=2, sticky="ew")

#choix modele multimètre
model_multi_var = tk.StringVar()
model_multi_combo = ttk.Combobox(frame_config, textvariable=model_multi_var)
model_multi_combo["values"] = ("AGILENT-34401A","KEITHLEY 2000")
model_multi_combo.current(0)
model_multi_combo.grid(row=2, column=1,padx=5, pady=2, sticky="ew")

#adresse GPIB
#multi title 
ttk.Label (frame_config, text="Multimètre :").grid(row=2, column=0, sticky="w", pady=2)
gpib_multimetre = ttk.Entry(frame_config)
gpib_multimetre.grid(row=2, column=2, sticky="ew", pady=2)
proto_multi_cb = ttk.Combobox(frame_config, textvariable=proto_multi, values=("GPIB","USB"),width=8)
proto_multi_cb.grid(row=2, column=3, sticky="w", pady=5)

#charge title 
ttk.Label (frame_config, text="Charge :").grid(row=3, column=0, sticky="w", pady=2)
gpib_charge = ttk.Entry(frame_config)
gpib_charge.grid(row=3, column=2, sticky="ew", pady=2)
proto_load_cb = ttk.Combobox(frame_config, textvariable=proto_load, values=("GPIB","USB"),width=8)
proto_load_cb.grid(row=3, column=3, sticky="w", pady=5)

#alim title
ttk.Label (frame_config, text="Allimentation DC :").grid(row=1, column=0, sticky="w", pady=2)
gpib_alim = ttk.Entry(frame_config)
gpib_alim.grid(row=1, column=2, sticky="ew", pady=2)
proto_alim_cb = ttk.Combobox(frame_config, textvariable=proto_alim, values=("GPIB","USB"),width=8)
proto_alim_cb.grid(row=1, column=3, sticky="w", pady=5)


#bouton valider configuration
btn_valider = ttk.Button(frame_config, text="valider la configuration", command=valider_configuration)
btn_valider.grid(row=4, column=0, pady=10)

#partie timer 
label_time=ttk.Label (frame_config, text="Temps écoulé : 00:00")
label_time.grid(row=4, column=2, sticky="w", pady=2)

def timer_indefini(seconds=0):
    mins = seconds // 60
    secs = seconds % 60
    label_time.config(text=f"Temps écoulé : {mins:02d}:{secs:02d}")
    # Relancer la fonction dans 1 seconde avec seconds+1
    threading.Timer(1, timer_indefini, [seconds + 1]).start()

timer_indefini()


frame_config.columnconfigure(1, weight=1) #--- pour éditer la taille de la zone de texte 




#===========================================================================
#                   FRAME ACTION DE TEST
#===========================================================================
frame_actions = ttk.LabelFrame(root, text="3/ Tests disponibles", padding=10, style="RedBold.TLabelframe")
frame_actions.grid(row=0,column=1, padx=10, pady=10)

#boutons qui appelent les fonction d'en haut
bouton_tension = ttk.Button(frame_actions, text="Test de la tension de sortie", command=simu_tension_sortie)
bouton_tension.grid(row=0, column=0, padx=2, pady=5)

bouton_regulation = ttk.Button(frame_actions, text="Test de la régulation en tension", command=simu_regulation_de_tension)
bouton_regulation.grid(row=1, column=0, padx=2, pady=5)

bouton_courant = ttk.Button(frame_actions, text="Test du courant de sortie", command=simu_courant_de_sortie)
bouton_courant.grid(row=2, column=0, padx=2, pady=5)

#variables à utiliser dans les fonctions
utilisation_shunt = tk.IntVar()
valeur_shunt = tk.StringVar(value="0.000")

check_shunt = ttk.Checkbutton(frame_actions, text="Utiliser un shunt",variable=utilisation_shunt,command=toogle_shunt_entry)#case a cocher 
check_shunt.grid(row=2, column=1, padx=2, pady=5)

ttk.Label(frame_actions,text="Shunt [mΩ]:").grid(row=2, column=2, padx=(10,2), pady=5,sticky="e")
entry_shunt = ttk.Entry(frame_actions, textvariable=valeur_shunt, width= 10,state="disabled") #grisé si la case n'est pas coché 
entry_shunt.grid(row=2, column=3, padx=2, pady=5)



#===========================================================================
#                   ESPACE TABLEUR
#===========================================================================

frame_tab = ttk.LabelFrame(root, text="2/ Entrer les mesures demandées dans la procédure de test", padding=10, style="RedBold.TLabelframe")
frame_tab.grid(row=1,column=0, padx=10, pady=10)

btn_tab_valide = ttk.Button(frame_tab, text="Valider les valeurs entrées", padding=10 ,command=valide_tableur)
btn_tab_valide.grid(row = 0, column = 0, sticky = "nsew")

#tableur
sheet = Sheet(
    frame_tab,
    data=[["","","",""],["","","",""],["","","",""],["","","",""],["","","",""],["","","",""],["","","",""],["","","",""],
          ["","","",""],["","","",""],["","","",""],["","","",""],["","","",""],["","","",""],["","","",""],["","","",""],
          ["","","",""],["","","",""],["","","",""],["","","",""],["","","",""],["","","",""],["","","",""],["","","",""],],
    headers=["Channel", "Calibre",  "Tension","Courant"],
    width = 545,
    height = 500
)

sheet.enable_bindings((
    "single_select",
    "edit_cell",
    "arrowkeys",
    "row_select",
    "column_select",
    "copy",
    "paste",
    "delete",
    "undo",
    "redo",
    "drag_select",
    "ctrl_a",
    "right_click_popup_menu"
))

sheet.grid(row = 1, column = 0, sticky = "nsew")





#===========================================================================
#                   ESPACE SORTIE  
#===========================================================================

frame_sortie = ttk.LabelFrame(root, text="4/ Sortie: Copier-coller dans la procédure de test", padding=10, style="RedBold.TLabelframe")
frame_sortie.grid(row=1,column=1, padx=10, pady=10)


#tableau sorti
sortie = Sheet(
    frame_sortie,
    data=[["","",""],["","",""],["","",""],["","",""],["","",""],["","",""],["","",""],["","",""],["","",""],["","",""],["","",""],["","",""],
          ["","",""],["","",""],["","",""],["","",""],["","",""],["","",""],["","",""],["","",""],["","",""],["","",""],["","",""],["","",""],],
    headers=["/","/","/"],
    height = 500,
    width= 450
)

sortie.enable_bindings((
    "single_select",
    "edit_cell",
    "arrowkeys",
    "row_select",
    "column_select",
    "copy",
    "paste",
    "delete",
    "undo",
    "redo",
    "drag_select",
    "ctrl_a",
    "right_click_popup_menu"
))

sortie.pack(fill="x",expand=True)



#Lancement de l'interface 
root.mainloop()


