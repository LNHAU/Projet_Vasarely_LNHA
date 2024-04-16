import turtle
import time
from deformation import deformation  # trop compliquée pour moi...
import projetVasarely

projetVasarely.pavage(turtle, 100, 300, 30, 'pink', 'yellow', 'magenta', projetVasarely.aucune_deformation, (100, 100, 100), 240)
time.sleep(1)  # attend 1 seconde
turtle.title("Exemple Vasarely")
projetVasarely.pavage(turtle, 300, 600, 20, 'pink', 'yellow', 'magenta', projetVasarely.aucune_deformation, (350, 350, 350), 240)
time.sleep(1)  # attend 1 seconde
projetVasarely.pavage(turtle, -100, 300, 30, 'pink', 'yellow', 'magenta', projetVasarely.aucune_deformation, (-50, 250, 200), 240)
time.sleep(1)  # attend 1 seconde
projetVasarely.pavage(turtle, -300, 200, 30, 'pink', 'yellow', 'magenta', projetVasarely.aucune_deformation, (50, -100, 0), 240)
time.sleep(1)  # attend 1 seconde

inf_gauche = -300
sup_droit = 300
longueur = 20
col1 = 'blue'
col2 = 'black'
col3 = 'red'
centre = (-50,  -50,  -50)
r = 200
rayon = 400
turtle.title("Exemple Vasarely 1")
projetVasarely.pavage(turtle, inf_gauche, sup_droit, longueur, col1, col2, col3, deformation, centre, r)

time.sleep(1)  # attend 1 seconde
col1, col2, col3 = 'white', 'black', 'grey'
centre = (-100, -100, 0)
rayon = 300
turtle.title("Exemple Vasarely 2")
projetVasarely.pavage(turtle, inf_gauche, sup_droit, longueur, col1, col2, col3, deformation, centre, rayon)

time.sleep(1)  # attend 1 seconde
col1 = 'blue'
col2 = 'black'
col3 = 'red'
centre = (-50, -50, 0)
r = 240
turtle.title("Exemple Vasarely 3")
projetVasarely.pavage(turtle, inf_gauche, sup_droit, longueur, col1, col2, col3, deformation, centre, r)

turtle.title("Exemple Vasarely 4")
projetVasarely.pavage(turtle, -100, 300, 30, 'pink', 'yellow', 'magenta', projetVasarely.aucune_deformation, (50, 250, 0), 240)
time.sleep(1)  # attend 1 seconde
turtle.title("Exemple Vasarely 5")
projetVasarely.pavage(turtle, 100, -500, 30, 'pink', 'yellow', 'magenta', projetVasarely.aucune_deformation, (-50, 250, 0), 240)
turtle.title("Exemple Vasarely 6")
projetVasarely.pavage(turtle, None, None, 0, '', '', None, projetVasarely.aucune_deformation, (), 0)
# turtle.done()

# Place la fenêtre de visualisation au premier plan
time.sleep(0.5)
turtle.setup(0, 0, 0, 0)
turtle.Canvas.lower
time.sleep(0.5)
turtle.title("Exemple Vasarely 0")
projetVasarely.main()
