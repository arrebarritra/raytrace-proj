# Specifikation
## Inledning
Jag har tänkt programmera en belyst sfär. Programmet ska beräkna ljusstyrkan av varje punkt av ytan av en sfär som är belyst av en ljuskälla från en viss vinkel. Sedan ska programmet rita sfären i ett grafikfönster med hjälp av belysningsvärdena.

En utmaning är att konvertera sfären som är centrerad i origo i sitt koordinatsystem till pixelkoordinatsystemet som bilden i grafikfönstret ska ritas i. En annan utmaning jag kan stöta på är att felkolla z funktionen när termen inuti roten är negativt.

## Användarscenarier
### Månen
Johannes Kepler undrar hur månen ser ut från jorden när solen ligger vid en viss vinkel till månen. Kepler matar in solens vinkel och får en simulerad bild på månen. Kepler blir glad.

### Bowlingklot
Walter är i ett mörkt rum och kan inte hitta sitt bowlingklot. För att hitta den behöver han veta hur den ser ut i mörkret när han lyser en ficklampa på den. Han kör klotbelysninsprogrammet vilket hjälper honom att hitta sit klot. Walter blir glad.

## Kodskelett
```python
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
```

## Programflöde
Programmet börjar med att skapa ett sfärobjekt med en defaultradie r som är belyst av en ljuskälla som är parallel till linjen mellan (0, 0, r) och sfärens mittpunkt i origo. Metoden draw() ritar sfären i ett grafikfönster. Därefter kan användaren välja att klicka på sfären och ändra positionen på ljuskällan. Då anropas changeLight() som i sin tur anropar drawSphere() med en ny light parameter beroende på klickpositionen, och därefter ritas sfären i bildrutan med draw().
