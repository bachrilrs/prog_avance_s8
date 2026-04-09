#!/usr/bin/env python3
def notes():     
    nb_coeff = input("Entrer le nombre de partiels: ")


    coeff = {'graphes' : {'cc': 0.5 , 'ct' : 0.5},
    'prog' : {'cc' : 0.4 , 'ct' : 0.6},
    'bg' : {'cc': 0.5 , 'ct' : 0.5},
    'anglais' : {'cc1' : 0.2,'cc2' : 0.3,'cc3' : 0.5},
    'maths' : {'cc': 0.5 , 'ct' : 0.5},
    'tdb' : {'cc': 0.3 , 'ct' : 0.7},
    'bioseq' : {'cc': 0.5 , 'ct' : 0.5},
    'bd' : {'cc': 0.3 , 'ct' : 0.7},
    'geq' : {'cc': 0.3 , 'ct' : 0.7},
    'algo' : {'cc': 0.3 , 'ct' : 0.7}}

            
    
    matieres = ['graphes','bg','algo','tdb','bd','anglais','bioseq','genetique','maths','prog']
      
    notes = []

    for elem in coeff:
        note_1 = float(input(f'Note de CC : '))
        note_2 = float(input(f'Note de CT : '))
        notes.append(note_1*coeff[elem]['cc']+note_2*coeff[elem]['ct'])
    
    return notes
    # total = 0 
    # for i, key in enumerate(coeff.keys()): 
    #     total += coeff[key][0] * notes[i] 
    # return total



# notes_finales = {}
# for matiere in matieres: 
#     print(f"Calcul des notes pour la matière {matiere} : ")
#     notes_finales[matiere] = notes() 

# print("Notes finales : ") 
# for matiere, note in notes_finales.items(): 
#     print(f"{matiere} : {note}")

# print("Moyenne générale : ", sum(notes_finales.values())/len(notes_finales))

# with open('notes.txt' , 'r') as fh:
#     fh.write(notes_finales)
#     a = f'Moyenne générale{sum(notes_finales.values())/len(notes_finales)}'
#     fh.write(a)

print(notes())