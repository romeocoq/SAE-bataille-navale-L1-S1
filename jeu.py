def init_grille():
    '''On crée une grille vide de 10x10 cases
    '''
    res=[]
    for i in range(10):
        ligne=[]
        for j in range(10):
            ligne.append('.')
        res.append(ligne)
    return res

def print_grille(grille:list):
    '''On affiche au joueur la grille
    '''
    ligne=''
    lettres=['  ','A','B','C','D','E','F','G','H','I','J']
    chiffres=['1','2','3','4','5','6','7','8','9','10']
    for i in range(len(lettres)):
        if i!=10:
            ligne+=lettres[i]+'|'
        else:
            ligne+=lettres[i]
    print(ligne)
    for j in range(len(chiffres)):
        ligne=''
        if chiffres[j]!='10':
            ligne+=chiffres[j]+' |'
        else:
            ligne+=chiffres[j]+'|'
        for k in range(10):
            if k!=9:
                ligne+=grille[j][k]+'|'
            else:
                ligne+=grille[j][k]
        print(ligne)
        
def test_coord(coord:'str'):
    '''On teste si les coordonnées sont valides
    '''
    if len(coord)<2 or len(coord)>3:
        return ((0,0),False)
    if len(coord)==2:
        x=coord[0]
        y=coord[1]
        if y=='0':
            return ((0,0),False)
    else:
        x=coord[0]
        y=coord[1]+coord[2]
    if (len(y)==2 and y!='10') or (x<'A' or x>'J'):
        return ((0,0),False)
    return ((x,y),True)

def lettre_to_coord(lettre:str):
    '''condition: len(lettre)=1
    '''
    return ord(lettre)-65
    
def place_bat(grille:list,nom:str,list_bat:dict[str,tuple[int,str]],deb:str,fin:str):
    '''On place un bateau sur la grille:
       -nom: nom du bateau
       -list_bat: la liste des bateaux avec en clé le nom du bateau et en valeur un couple (taille,symbole)
       -deb: les coordonnées 1
       -fin: les coordonnées 2
       '''
    message=''
    erreur=False
    if nom not in list_bat:
        #On teste si le bateau fait bien parti de la liste des bateaux
        message='Erreur: Nom de bateau incorrect.'
    elif not(test_coord(deb)[1]) or not(test_coord(fin)[1]):
        #On teste si les coordonnées entrées sont bien dans la grille
        message='Erreur: Au moins une coordonnée est incorrecte.'
    else:
        x1=lettre_to_coord(test_coord(deb)[0][0])
        y1=int(test_coord(deb)[0][1])-1
        x2=lettre_to_coord(test_coord(fin)[0][0])
        y2=int(test_coord(fin)[0][1])-1
        if x1>x2 or y1>y2:
            message='Erreur: La coordonnée 1 est pus grande que la 2'
        elif x1!=x2 and y1!=y2:
            #On teste si le bateau est bien sur une ligne ou une colonne
            message='Erreur: Le bateau ne peut pas être en diagonale'
        elif x1==x2:
            #Si il est sur une même colonne...
            if ((y2-y1)+1)!=list_bat[nom][0]:
                #On teste si la taille est correcte
                message='Erreur: La taille du bateau est incorrecte.'
            else:
                #La taille est correcte alors...
                test=True
                for i in range(y1,y2+1):
                    #On teste si un bateau est déjà présent
                    if grille[i][x1]!='.':
                        message='Erreur: Chevauchement de bateau.'
                        test=False
                if test:
                    for i in range(y1,y2+1):
                        grille[i][x1]=list_bat[nom][1]
                    message='OK'
                    erreur=True
        else:
            #Si il est sur une même ligne...
            if ((x2-x1)+1)!=list_bat[nom][0]:
                #On teste si la taille est correcte
                message='Erreur: La taille du bateau est incorrecte.'
            else:
                #La taille est correcte alors...
                test=True
                for i in range(x1,x2+1):
                    #On teste si un bateau est déjà présent
                    if grille[y1][i]!='.':
                        message='Erreur: Chevauchement de bateau.'
                        test=False
                if test:
                    #Le test est validé, on place le bateau
                    for i in range(x1,x2+1):
                        grille[y1][i]=list_bat[nom][1]
                    message='OK'
                    erreur=True
    return (message, erreur)

def quelle_commande(ch:str)->str:
    '''On regarde la commande utilisée
    '''
    res=''
    for car in ch:
        if car!=' ':
            res+=car
        else:
            return res
        
def ch_to_list(ch:str)->list[str]:
    '''On fait de chaque mot de la chaine de caractère un élément d'une liste
    '''
    res=[]
    mot_act=''
    for car in ch:
        if car!=' ':
            mot_act+=car
        else:
            res.append(mot_act)
            mot_act=''
    res.append(mot_act)
    return res

def verif_grille(grille)->bool:
    '''On vérifie la validité de la grille
    '''
    attendu={'C':5,'S':3,'B':4,'P':2,'D':3}
    res={}
    for ligne in grille:
        for case in ligne:
            if case!='.':
                if case not in res:
                    res[case]=1
                else:
                    res[case]+=1
    return res==attendu

def tirer(grille, case):
    """permet de tirer
        - case: coordonnée (tuple) où le joueur veut tirer
        retourne 3 informations: le message, la validité du coup et la grille
    """
    valide=True
    message = ''
    if test_coord(case)[1]==False:
        message= 'Erreur: Coordonnées incorrectes'
        valide = False
    else:
        x=int(test_coord(case)[0][1])-1
        y=lettre_to_coord(test_coord(case)[0][0])
        if grille[x][y]=='X' or grille[x][y]=='O':
            message = 'Erreur: Case déjà attaquée'
            valide = False
        else:
            if grille[x][y]=='.':
                 # Si il n'y a pas de bateau sur la case où l'on tire
                 message = "Raté"
                 grille[x][y] = "O"
            elif grille[x][y] == "C" or grille[x][y] == "D" or grille[x][y] == "B" or grille[x][y] == "P" or grille[x][y] == "S":
                # Si il y a un bateau sur la case où l'on tire
                message = "Touché"
                bateau_touché = grille[x][y]
                grille[x][y] = "X"
                nb_case=0
                #On regarde si il y a encore un case avec le symbole du bateau
                for ligne in grille:
                    for unitee in ligne:
                        if unitee == bateau_touché:
                            nb_case+=1
                #Si il y en a pas, c'est coulé
                if nb_case==0:
                    message = "Coulé"
    return (message, valide, grille)

def cache_bateau(grille:dict)->dict:
    '''On cache le bateau sur la grille
    '''
    for i in range (len(grille)):
        for j in range (len(grille)):
            if grille[i][j]!='.' and grille[i][j]!='X' and grille[i][j]!='O':
                grille[i][j]='.'
    return grille
                        
    