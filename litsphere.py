from math import *

class Sphere:

    def __init__(r):
        self.r = r
        self.lightvalues = None

    def dist(a, b):
        return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


    def z(r, x, y):
        squared = r**2 - x**2 - y**2
        if squared >= 0:
            return sqrt(squared)
        else:
            return 0


    def b(x, x0, y, y0, z, z0, r):
        if z == None:
            return 0
        else:
            return (x*xlight + y*ylight + z*zlight)/(r**2)


    def drawSphere(r, light):
        """Sparar och returnerar belysningsvärde för varje heltalsparskoordinat (x, y) på sfären i self.lightvalues med hjälp av belysningsfunktionen b()"""


def spherecoord(coord):
    """Returnerar konversion av pixelkoordinater till sfärens koordinatssystemet"""


def pixelcoord(coord):
    """Returnerar konversion av koordinater i sfärens koordinatssystemet till pixelkoordinater"""


def changeLight(click):
    """Kallar på drawSphere att beräkna om belysningen med den nya positionen på ljuskällan som angivits genom användarinput och anropar draw()"""


def draw(img, pos, lightvalues):
    """Rita bild på sfären med belysningsvärden lightvalues i positionen pos i bildrutan"""


"""Preamble för att sätta upp canvas etc. för bildritning"""
"""Skapa sfär med radien r och kör drawSphere() på sfären"""
"""Anropa draw()"""
