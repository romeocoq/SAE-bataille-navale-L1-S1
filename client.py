import socket
import jeu
import pickle

host, port = ('localhost', 5566)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((host, port))
    print('Client connecté')
    
     # Attente d'un message du serveur
    message = client_socket.recv(1024)  # Réception d'un message de 1024 octets maximum
    print(message.decode('utf8'))
    
    #Mise en place de la grille de jeu
    liste_bateau={'carrier':(5,'C'),'battleship':(4,'B'),'destroyer':(3,'D'),'submarine':(3,'S'),'patrol boat':(2,'P')}
    grille_validee = False
    grille = client_socket.recv(1024)  # Réception d'un message de 1024 octets maximum
    grille = pickle.loads(grille)
    jeu.print_grille(grille)
    nb_bateau=0
    bateaux_places=[]
    while not grille_validee:
        action = input("Placez un bateau (ex: PLACE carrier B2 F2) ou envoyez votre grille(GRILLE): ")
        if jeu.quelle_commande(action)=='PLACE':
            if nb_bateau<5:
                liste_action = jeu.ch_to_list(action)
                if len(liste_action)==4:
                    if liste_action[1] not in bateaux_places:
                        placement=jeu.place_bat(grille, liste_action[1], liste_bateau, liste_action[2], liste_action[3])
                        print(placement[0])
                        if placement[1]==True:
                            jeu.print_grille(grille)
                            nb_bateau+=1
                            bateaux_places.append(liste_action[1])
                    else:
                        print('Erreur: Bateau déjà placé')
                elif len(liste_action)==5 and (liste_action[1]+' '+liste_action[2]== 'patrol boat'):
                    if 'patrol boat' not in bateaux_places:
                        placement=jeu.place_bat(grille, 'patrol boat', liste_bateau, liste_action[3], liste_action[4])
                        print(placement[0])
                        if placement[1]==True:
                            jeu.print_grille(grille)
                            nb_bateau+=1
                            bateaux_places.append('patrol boat')
                    else:
                        print('Erreur: Bateau déjà placé')
                else:
                    print("Erreur: Il y a trop ou pas assez d'arguments")
            else:
                print('Erreur: Vous avez déjà placé 5 bateaux')
        elif action=='GRILLE':
            #Envoi de la grille au serveur
            grille_envoi = pickle.dumps(grille)
            client_socket.sendall(grille_envoi)
            # Réception de la réponse
            reponse = client_socket.recv(1024).decode()
            print(reponse)
            if reponse == "OK":
                grille_validee = True 
        else:
            print('Erreur: Mauvaise commande')
            
    validation = client_socket.recv(1024).decode()
    print(validation)
    
    #Partie:
    terminee = False
    while not terminee:
        coup_valide = False
        while not coup_valide:
            tour = client_socket.recv(1024).decode()
            print(tour)
            ma_grille = client_socket.recv(1024)
            ma_grille = pickle.loads(ma_grille)
            print('Voici votre grille :')
            jeu.print_grille(ma_grille)
            data = client_socket.recv(1024)
            grille_adv = pickle.loads(data)
            print("Voici la grille de l'adversaire :")
            jeu.print_grille(grille_adv)
            jouer=True
            while jouer:  # Boucle infinie pour valider la commande
                action = input("Où voulez-vous tirer ? (ex: TIR A1) : ")
                # Vérifier si la commande est valide
                if jeu.quelle_commande(action) == "TIR" and len(jeu.ch_to_list(action)) == 2:
                    # Si la commande est correcte, l'envoyer au serveur
                    client_socket.sendall(action.encode("utf8"))
                    jouer=False
                else:
                    # Si la commande est incorrecte, afficher un message d'erreur
                    print("Erreur : commande invalide. Essayez à nouveau (format attendu : TIR A1).")
            reponse = client_socket.recv(1024)
            print(reponse.decode('utf8'))
            if len(reponse)==4 or len(reponse)==5 or len(reponse)==6:
                coup_valide = True
            fin = client_socket.recv(1024)
            fin = fin.decode('utf8')
            if fin=='True':
                terminee=True
        print('Au joueur suivant de jouer.')
    
    message_fin = client_socket.recv(1024)
    print(message_fin.decode('utf8'))
                               
except ConnectionRefusedError:
    print('Connexion au serveur échouée !')
finally:
    client_socket.close()