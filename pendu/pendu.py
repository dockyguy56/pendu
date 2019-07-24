""" LE jeu du pendu """
import os
import pickle

print("Welcome in the jeu du pendu \n")
name = input("Qui est tu?")
life = 8
score = {}
word_to_search = "ThisIsAmerica"
current_findings = ""
previous_findings = ""
for let in word_to_search:
    previous_findings += "*"

try:
    with open('score','rb') as fichier_score:
        depickler = pickle.Unpickler(fichier_score)
        score = depickler.load()
        #existing/returning players
        if name in score.keys():
            (life, word_to_search, previous_findings) = score[name]
        #new player
        else:
            score[name] = (life, word_to_search, previous_findings)

    #update file for new player
    with open('score','wb') as fichier_score:
        pickler = pickle.Pickler(fichier_score)
        pickler.dump(score)
except: 
    print("No score file. Creating it...")
    score[name] = (life, word_to_search, previous_findings)
    fichier_score = open('score', 'wb')
    pickler = pickle.Pickler(fichier_score)
    pickler.dump(score)
    fichier_score.close()

#setup
print ("""Mr/Mrs {}, you have {} live to start.
        You are looking for {}.
        You have found {}.""".format(name, life, word_to_search,
                                     previous_findings))

done = False
quit = False

#game iteration
while (not done) and life > 0 and (not quit): 
    done = True

    #Validation scheme
    valid = False
    while not valid:
        entry = input ("Enter one letter only: ")
        valid = True

        if len(entry) > 1:
            print ("I said ONE LETTER!")
            valid = False

        if valid and not entry.isalpha():
            print("I said A letter")
            valid = False

    #Existence scheme
    current_findings = ""
    found = False
    for i, let in enumerate(word_to_search):
        if  let.lower() == entry.lower():
            found = True
            current_findings += let
            done &= True
        else:
            if previous_findings[i] == "*":
                current_findings += "*"
                done = False
            else:
                current_findings+= previous_findings[i]

    #result and display
    if found:
        print("A Letter was found")
    else:
        print ("Missed. life lost")
        life -= 1
    print(current_findings)
    print("Life that rest:{} ".format(life))
    previous_findings = str(current_findings)

    if life <= 0:
        done = True

    if not done:
        q = input ("Do you want to quit? (y/n)")
        if q.lower() == "y":
            quit = True

#game quit scheme
if quit:
    print ("Mr/Mrs {}, you have {} left".format(name,life))
    with open('score','rb') as fichier_score:
        depickler = pickle.Unpickler(fichier_score)
        score = depickler.load()
        score[name] = (life, word_to_search, previous_findings)
    with open('score','wb') as fichier_score:
        pickler = pickle.Pickler(fichier_score)
        pickler.dump(score)

#done scheme
if done:
    #if won, remove from the registry
    if life > 0:
        print ("Mr/Mrs {}, you won".format(name))
        with open('score','rb') as fichier_score:
            depickler = pickle.Unpickler(fichier_score)
            score = depickler.load()
            del score[name]
        with open('score','wb') as fichier_score:
            pickler = pickle.Pickler(fichier_score)
            pickler.dump(score)

    #reset lives
    else:
        life = 8
        print ("Mr/Mrs {}, you lives are reset to {}".format(name,life))
        with open('score','rb') as fichier_score:
            depickler = pickle.Unpickler(fichier_score)
            score = depickler.load()
            score[name] = (life, word_to_search, previous_findings)
        with open('score','wb') as fichier_score:
            pickler = pickle.Pickler(fichier_score)
            pickler.dump(score)