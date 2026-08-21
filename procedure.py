import time
import driver
import outils
import pandas as pd
from tksheet import Sheet 
import tkinter.messagebox as messagebox


def tension_sortie_2(data,alim,multi,alimentation,multimetre):
    print("===Test : Tension de sortie ===")

    dernier_channel = None
    liste_valeur_sortie = []
    liste_valeur_affiche = []

    for i, row in enumerate(data): #pour capter le nombre de ligne dans le tableau
        if not row or all(cell.strip() == "" for cell in row): #pour passer à la suite si un ligne est vide 
            time.sleep(1)
            continue

        try: 
            channel = row[0].strip()
            calibre = row[1].strip()
            tension_tab = str(row[2].strip())
            tension = float(tension_tab.replace(',','.'))


            if channel != dernier_channel:
                messagebox.showinfo(
                    title="changement de channel",
                    message=f"Veuillez connecter l'alimentation sur le canal {channel}.\nPuis cliquez sur OK pour continuer"
                )
                dernier_channel = channel
            
            alim.write(alimentation.channel_selection(channel))
            alim.write(alimentation.power_range(channel,calibre))
            alim.write(alimentation.channelContextualise(alimentation.dc_voltage,channel,tension))
            alim.write(alimentation.channelContextualise(alimentation.dc_current,channel,1))
            alim.write(alimentation.output(channel,alimentation.on))
            time.sleep(0.5)

            valeur_affiche = alim.query(alimentation.internal_multimeter(channel,alimentation.dc_voltage))
            time.sleep(0.5)

            valeur_mesure = outils.mesure_multi(multi,multimetre.dc_voltage,moyennage=1)#(multi,demande,moyennage)
            print(f" Tension mesuré : {valeur_mesure:.5f} V")
            liste_valeur_sortie.append(valeur_mesure)
            liste_valeur_affiche.append(valeur_affiche)

            alim.write(alimentation.output(channel,alimentation.off))
            time.sleep(0.5)

        except Exception as e:
            print(f"Error --- LIGNE{i} : {e}")
    return(liste_valeur_sortie,liste_valeur_affiche)
 



def regulation_tension_avec_charge_et_bruit(data,alim,multi,charge,alimentation, multimetre,dynamic_load):
    print("===Test de la régulation de tension avec charge + bruit===")

    dernier_channel=None
    liste_valeur_tension= []
    liste_valeur_bruit= []

    for i, row in enumerate(data):
        if not row or all(cell.strip() == "" for cell in row):
            time.sleep(1)
            continue

        try: 
            channel = row[0].strip()
            calibre = row[1].strip()
            tension_tab = str(row[2].strip())
            tension = float(tension_tab.replace(',','.'))
            courant_tab = str(row[3].strip())
            courant = float(courant_tab.replace(',','.'))


            if channel != dernier_channel:
                messagebox.showinfo(
                    title="changement de channel",
                    message=f"Veuillez connecter l'alimentation sur le canal {channel}.\nPuis cliquez sur OK pour continuer"
                )
                dernier_channel = channel

            alim.write(alimentation.channel_selection(channel))
            alim.write(alimentation.gestion_sense(channel))
            alim.write(alimentation.power_range(channel,calibre))
            alim.write(alimentation.channelContextualise(alimentation.dc_voltage,channel,tension))
            alim.write(alimentation.channelContextualise(alimentation.dc_current,channel,courant+0.1))
            
            
            charge.write(dynamic_load.dc_current(courant))
            time.sleep(0.5)

            alim.write(alimentation.output(channel,alimentation.on))
            charge.write(dynamic_load.output("1"))
            time.sleep(1)

            tension_mesure = outils.mesure_multi(multi,multimetre.dc_voltage,moyennage=1)#(multi,demande,moyennage)
            bruit_mesure = outils.mesure_multi(multi,multimetre.ac_voltage,moyennage=1)
            print(f" Tension mesuré : {tension_mesure:.5f}V\n Bruit mesuré : {bruit_mesure:.5f}V")
            liste_valeur_tension.append(tension_mesure)
            liste_valeur_bruit.append(bruit_mesure*1000)

            alim.write(alimentation.output(channel,alimentation.off))
            charge.write(dynamic_load.output("0"))
            time.sleep(0.5)

        except Exception as e:
            print(f"Error --- LIGNE{i} : {e}")

    return(liste_valeur_tension,liste_valeur_bruit)



def courant_sortie_2(data,alim,multi,charge,alimentation, multimetre,dynamic_load,utilisation_shunt,shunt):
    print("===Test du courant de sortie===")

    dernier_channel=None
    liste_valeur_sortie = []
    liste_tension_sortie = []
    liste_affichage = []

    for i, row in enumerate(data):
        if not row or all(cell.strip() == "" for cell in row):
            time.sleep(1)
            continue

        try: 
            channel = row[0].strip()
            calibre = row[1].strip()
            tension = 5
            courant_tab = str(row[3].strip())
            courant = float(courant_tab.replace(',','.'))

            if channel != dernier_channel:
                messagebox.showinfo(
                    title="changement de channel",
                    message=f"Veuillez connecter l'alimentation sur le canal {channel}.\nPuis cliquez sur OK pour continuer"
                )
                dernier_channel = channel

            alim.write(alimentation.channel_selection(channel))
            alim.write(alimentation.power_range(channel,calibre))
            alim.write(alimentation.channelContextualise(alimentation.dc_voltage,channel,tension))
            alim.write(alimentation.channelContextualise(alimentation.dc_current,channel,courant))
            
            charge.write(dynamic_load.dc_current(courant+0.5))
            

            alim.write(alimentation.output(channel,alimentation.on))
            charge.write(dynamic_load.output("1"))
            time.sleep(1)

            valeur_affiche = alim.query(alimentation.internal_multimeter(channel,alimentation.dc_current))

            liste_affichage.append(valeur_affiche)

            time.sleep(0.5)

            if utilisation_shunt.get() == True:
                tension_mesure = float(outils.mesure_multi(multi,multimetre.dc_voltage,moyennage=1))#(multi,demande,moyennage)
                courant_deduit=tension_mesure/(float(shunt)/1000)
                print(f" Tension mesuré : {tension_mesure:.5f}V\n Courrant deduit:{courant_deduit:.5f}A")
                liste_valeur_sortie.append(courant_deduit)
                liste_tension_sortie.append(tension_mesure)

            if utilisation_shunt.get() == False:
                courant_mesure = outils.mesure_multi(multi,multimetre.dc_current,moyennage=1)#(multi,demande,moyennage)
                print(f" Courant mesuré : {courant_mesure:.5f}A")
                liste_valeur_sortie.append(courant_mesure)

            alim.write(alimentation.output(channel,alimentation.off))
            charge.write(dynamic_load.output("0"))
            time.sleep(0.5)

        except Exception as e:
            print(f"Error --- LIGNE{i} : {e}")

    return(liste_valeur_sortie,liste_tension_sortie,liste_affichage)

