class Sphere:

    def __init__(r):
        self.r = r
        self.lightvalues = None #Sparar belysningsvärde för heltalparskoordinater (x, y) på sfären
        """Initialiserar sphere objektet med en radie r"""

    def dist(a, b):
        """Hjälpfunktion som returnerar distansen mellan punkterna a och b i planet"""


    def z(r, x, y):
        """Returnerar z koordinat motsvarande till (x, y) koordinater på framsidan av sfären"""


    def b(x, x0, y, y0, z, z0, r):
        """"Returnerar ett belysningsvärde mellan -1 och 1 för en punkt på sfären beroende på belysningen position och vinkel"""


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
