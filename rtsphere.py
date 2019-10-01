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


class Shape(Shape):
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
