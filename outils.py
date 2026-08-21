import time
import pandas as pd
import tkinter
import driver
import subprocess

class output:

    def __init__(self,mes_1,mes_2,mes_3) ->None:
        self.mes_1 = mes_1
        self.mes_2 = mes_2
        self.mes_3 = mes_3




def mesure_multi(nom_multi,demande,moyennage):
    Val=0
    value_multi = nom_multi.query_ascii_values(demande) 
    time.sleep(0.5)
    for k in range(moyennage):      #moyennage sur 10 valeurs 
        value_multi = nom_multi.query_ascii_values(demande) 
        Val+=value_multi[0]
        time.sleep(1)
    return (Val)

def changement_de_channel(channel):
    fenetre = tkinter.Tk()
    fenetre.configure(background="#56dcf1")

    # label
    lbl =tkinter.Label(fenetre, text=f"branchez sur le channel {channel} de l'alimentation")
    lbl.pack()
    
    # bouton de sortie
    bouton_ok=tkinter.Button(fenetre, text="OK", command=fenetre.destroy)
    bouton_ok.pack()

    fenetre.mainloop()

def lien_driver_alim(nom_alim):
    if nom_alim == "TTI":
        return(driver.TTI_QL355TP_STANDART_POWER_SUPPLY_DRIVER)
    if nom_alim == "KEYSIGHT N8700":
        return(driver.KEYSIGHT_8700_STANDART_POWER_SUPPLY_DRIVER)
    if nom_alim == "KEYSIGHT E3632A":
        return(driver.KEYSIGHT_E3632A_STANDART_POWER_SUPPLY_DRIVER)
    if nom_alim == "EA-PS 2084-10B":
        return(driver.KEYSIGHT_E3632A_STANDART_POWER_SUPPLY_DRIVER)
    if nom_alim == "KEYSIGHT E3634A":
        return(driver.TDK_LAMBDA_GENH_STANDART_POWER_SUPPLY_DRIVER)
    if nom_alim == "TDK LAMBDA GENH 12.5-60":
        return(driver.TDK_LAMBDA_GENH_STANDART_POWER_SUPPLY_DRIVER)
    if nom_alim == "ROHDE & SCHWARZ HMP SERIE":
        return(driver.ROHDE_AND_SCHWARZ_HMP_MULTICHANNEL_POWER_SUPPLY_DRIVER)
    if nom_alim == "R-S NGP800":
        return(driver.ROHDE_AND_SCHWARZ_HMP_MULTICHANNEL_POWER_SUPPLY_DRIVER)
    if nom_alim == "KEYSIGHT E3644A":
        return(driver.ROHDE_AND_SCHWARZ_HMP_MULTICHANNEL_POWER_SUPPLY_DRIVER)
    if nom_alim == "AGILENT N6705A":
        return(driver.AGILENT_N6705A_STANDART_POWER_SUPPLY_DRIVER)
    
        

    
    
