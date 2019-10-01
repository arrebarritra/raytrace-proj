## Inledning
Jag kommer att implementera "Belysning av klot" P-uppgiften med hjälp av en raytracer. Den ska kunna rendera en scen med oändliga planer och sfärer med godtyckligt många ljuskällor. Utöver diffuse shading och skuggor som förekommer i den originella uppgiften kommer jag att implementera ambient och specular shading, och reflektion. Att beräkna reflektionen kommer troligtvis vara den svåraste delen av projektet då man måste beräkna och skicka rays rekursivt och kombinera färgen av reflektionsrays med färgen av den originella objektet. Dataflödet är också en svår aspekt av projektet då jag måste göra beslut om jag t.ex. ska returna färgen av en Ray i funktionen som beräknar om en Ray intersekterar ett objekt, eller om jag ska ha en metod som ändrar färgen i Ray objektet direkt.

## Användarscenarier
### Klot i ett rum
Användaren vill simulera hur två reflektiva klot i ett kubiskt rum med två ljuskällor. Användaren kodar scenen i en JSON fil där objekten, dess färger och optiska egenskaper specificeras. Denna fil läses in av programmet. Användaren inputtar kamerans koordinater och riktning via användargränssnittet. En bild av scenen outputtas i användargränssnittet.

## Kodskelett
```python
class Vec3(object):
  """Metoder för 3D-vektor operationer"""
  pass


class Ray(object):
  """Ljusstråle"""

  def intersect(self, scene):
    """Returnerar True om Ray korsar något objekt i scenen, och uppdaterar Intersection objektet om detta är fallet"""
    pass

  def doesintersect(self, scene):
    """Returnerar True om Ray korsar något objekt i scenen"""
    pass


class Camera(object):
  def makeray(self, x, y):
    """Skickar Ray baserat på (x, y) koordinater och kamerans position och riktning"""
    pass


class Shape(object):
  """Superklass för geometriska objekt, alla geometriska figurer implementerar nedanstående metoder. Innehåller position-, storlek- och materialinformation"""

  def intersect():
    """Returnerar True om Ray korsar detta objekt, och uppdaterar Intersection objektet om detta är fallet"""
    pass

  def doesintersect(self, scene):
    """Returnerar True om Ray korsar detta objekt"""
    pass

  def light(self, ray, scene):
    """Färgar ray intersektionen. Implementerar ambient, diffuse och specular lighting för varje ljus i scenen samt skickar reflection rays"""
    pass


class Plane(Shape):
  """Oändligt plan, implementerar Sphere metoder"""


class Sphere(Shape):
  """Sfär, implementerar Sphere metoder"""


class Light(object):
  """Innehåller positionen och intensiteten av et ljusobjekt"""


class Scene(object):
  """Innehåller alla Shape och Light objekt"""

  def importscene():
    """Läser in en scen från en JSON fil"""


class Intersection(object):
  """Innehåller information om intersektionen av en Ray och objektet som den intersekterar"""

  def setintersect(self, t, shape):
    """Uppdaterar intersektionspunkten t och intersektionsobjektet shape"""


class Colour(object):
  """Innehåller RGB färg med värden mellan 0 och 1, samt färgoperationer för blandning av färger"""


class Material(object):
  """Innehåller information om färg, reflektivitet och specular highlight värden för ett material"""


class GUI(object):
  """Skapa ett GUI där användaren kan specificera kamera och upplösning och displaya den raytracade bilden"""


"""Sätt upp kamera, läs och sätt upp geometriska objekt i scenen, skicka Ray för varje pixel och raytracea, skicka visa en bild"""
```

## Programflöde och dataflöde
Programmet börjar med att sätta upp kameran och läsa in scenen. Därefter börjar den raytracea. Dataflödet sker när en ray interekterar ett objekt i scenen. Rayens färg uppdateras med diffuse och specular komponenter. Om det är en icke-primary ray (alltså en reflektionsray) skickas dess färg tillbaks till ray:en högre upp i rekursionen.
