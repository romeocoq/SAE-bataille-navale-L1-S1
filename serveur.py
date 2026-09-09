import socket
import jeu
import pickle
import copy

host, port = ('', 5566)

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.bind((host, port))
print("Le serveur est démarré.")

serv_socket.listen(2)  # Permet 2 connexions simultanées

clients = []
noms = ["joueur 1", "joueur 2"]

# Acceptation des connexions
while len(clients) < 2:
    connexion, adresse = serv_socket.accept()
    clients.append((connexion, adresse))
    print(f"Connexion acceptée de {adresse}. Assigné à {noms[len(clients) - 1]}.")

# Envoi d'un message de bienvenue aux joueurs
for i, couple in enumerate(clients):
    connexion = couple[0]
    message = f"Bienvenue {noms[i]}, bonne partie !"
    message = message.encode("utf8")
    connexion.sendall(message)

#Initialisation des grilles des joueurs
grille_j1=jeu.init_grille()
grille_j2=jeu.init_grille()

connexion_j1=clients[0][0]
connexion_j2=clients[1][0]
#Envoi des grilles vides
message_j1 = pickle.dumps(grille_j1)
connexion_j1.sendall(message_j1)
print('Grille envoyé au joueur 1')
message_j2 = pickle.dumps(grille_j2)
connexion_j2.sendall(message_j2)
print('Grille envoyé au joueur 2')

#Validation des grilles
for i, couple in enumerate(clients):
    valide = False
    while not valide:
        connexion = couple[0]
        print(f'En attente de la grille de {noms[i]}...')
        grille_recue = pickle.loads(connexion.recv(4096))
        print(f'Grille reçue de {noms[i]} :')
        jeu.print_grille(grille_recue)
        if jeu.verif_grille(grille_recue):
            reponse = 'OK'
            connexion.sendall(reponse.encode("utf8"))
            print(f"Grille de {noms[i]} validée.")
            valide = True
            if i==0:
                grille_j1=grille_recue
            else:
                grille_j2=grille_recue
        else:
            reponse = 'ERREUR : Grille invalide.'
            connexion.sendall(reponse.encode("utf8"))
            print(f"Grille de {noms[i]} invalide.")


# Envoi d'un message de lancement aux joueurs
for i, couple in enumerate(clients):
    connexion = couple[0]
    validation = 'Lancement de la partie !'
    validation = validation.encode("utf8")
    connexion.sendall(validation)
    print(f"Message envoyé au client {noms[i]}: {validation}")


#Gestion des attaques:
terminee = False
while not terminee:
    for i, couple in enumerate(clients):
        if terminee==False:
            jouer=False
            while not jouer: #On demande au joueur de jouer tant qu'il n'a pas fait un coup correct
                connexion = couple[0]
                #On lui dit de jouer
                tour = f"C'est à votre tour {noms[i]}"
                print(tour)
                connexion.sendall(tour.encode("utf8"))
                #On lui montre sa grille et la grille de l'adversaire(avec les bateaux cachés)
                if i==0:
                    sa_grille = pickle.dumps(grille_j1)
                    connexion.sendall(sa_grille)
                    grille_j2_copie = copy.deepcopy(grille_j2)
                    grille_j2_cachee = pickle.dumps(jeu.cache_bateau(grille_j2_copie))
                    print(f"Envoi au joueur 1 : {grille_j2_cachee}")
                    connexion.sendall(grille_j2_cachee)
                else:
                    sa_grille = pickle.dumps(grille_j2)
                    connexion.sendall(sa_grille)
                    grille_j1_copie = copy.deepcopy(grille_j1)
                    grille_j1_cachee = pickle.dumps(jeu.cache_bateau(grille_j1_copie))
                    print(f"Envoi au joueur 2 : {grille_j1_cachee}")
                    connexion.sendall(grille_j1_cachee)
                #On récupère sa commande envoyée
                attaque = connexion.recv(4096).decode()
                if i==0:
                    resultat = jeu.tirer(grille_j2, jeu.ch_to_list(attaque)[1])
                    reponse = resultat[0]
                    grille_j2 = resultat[2]   
                    if resultat[1] == True:
                        jouer = True
                        if resultat[0]!="Raté":
                            bateaux_j2={}
                            for ligne in grille_j2:
                                for case in ligne:
                                    if case!='.' and case!='O' and case!='X':
                                        if case not in bateaux_j2:
                                            bateaux_j2[case]=1
                                        else:
                                            bateaux_j2[case]+=1
                            for bateau, nb in bateaux_j2.items():
                                if nb==0:
                                    del bateaux_j2[bateau]
                            print(f"Les bateaux (en nombre unitaire) restants du joueurs 2 sont {bateaux_j2}")
                            #On regarde si il a gagné
                            if bateaux_j2 == {}:
                                vainqueur = noms[i]
                                terminee=True
                else:
                    resultat = jeu.tirer(grille_j1, jeu.ch_to_list(attaque)[1])
                    print(resultat)
                    reponse = resultat[0]
                    grille_j1 = resultat[2]
                    if resultat[1] == True:
                        jouer = True
                        if resultat[0]!="Raté":
                            bateaux_j1={}
                            for ligne in grille_j1:
                                for case in ligne:
                                    if case!='.' and case!='O' and case!='X':
                                        if case not in bateaux_j1:
                                            bateaux_j1[case]=1
                                        else:
                                            bateaux_j1[case]+=1
                            for bateau, nb in bateaux_j1.items():
                                if nb==0:
                                    del bateaux_j1[bateau]
                            print(f"Les bateaux (en nombre unitaire) restants du joueurs 1 sont {bateaux_j1}")
                            #On regarde si il a gagné
                            if bateaux_j1 == {}:
                                vainqueur = noms[i]
                                terminee = True
                    
                #On envoie la réponse au joueur:
                print(f"La partie est sur {terminee} (False=pas terminéé)")
                print(f"Le retour de l'attaque est: {reponse}")
                connexion.sendall(reponse.encode("utf8"))
                connexion.sendall(str(terminee).encode("utf8"))

message_fin = f"C'était une belle partie, le vainqueur est {vainqueur}"

# Fermeture des connexions
for couple in clients:
    connexion = couple[0]
    connexion.close()

serv_socket.close()