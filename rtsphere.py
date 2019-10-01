class Vec3(object):
  """Metoder för 3D-vektor operationer"""
  def __init__(self, x, y, z):
      self.x, self.y, self.z = x, y, z


  def __str__(self):
      return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"


  def __add__(self, v):
      return Vec3(self.x + v.x, self.y + v.y, self.z + v.z)


  def __sub__(self, v):
      return Vec3(self.x - v.x, self.y - v.y, self.z - v.z)


  def __mul__(self, v):
      return Vec3(v * self.x, v * self.y, v * self.z)


  def __truediv__(self, v):
      return self * (1 / float(v))


  def len(self):
      return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)


  def dot(self, v):
      return self.x * v.x + self.y * v.y + self.z * v.z


  def cross(self, v):
      return Vec3(self.y * v.z - self.z * v.y, self.z * v.x - self.x * v.z, self.x * v.y - self.y * v.z)


  def norm(self):
      return Vec3(self.x, self.y, self.z) / self.len()


class Colour(object):
  """Innehåller RGB färg med värden mellan 0 och 1, samt färgoperationer för blandning av färger"""
  min = 0
  max = 1
  scale = 255

  def __init__(self, r, g, b):
      self.r, self.g, self.b = r, g, b


  def __add__(self, c):
      return Colour(self.r + c.r, self.g + c.g, self.b + c.b)


  def __mul__(self, c):
      if type(c) == Colour:
          return Colour(self.r * c.r, self.g * c.g, self.b * c.b)
      elif type(c) == float:
          return Colour(self.r * c, self.g * c, self.b * c)


  def gammaCorrection(self, exposure, gamma):
      self.r = (self.r * exposure) ** gamma
      self.g = (self.g * exposure) ** gamma
      self.b = (self.b * exposure) ** gamma

  def clamp(self):
      self.r = max(self.min, min(self.max, self.r))
      self.g = max(self.min, min(self.max, self.g))
      self.b = max(self.min, min(self.max, self.b))


  def scaleRGB(self):
      return (int(self.scale * self.r), int(self.scale * self.g), int(self.scale * self.b))


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


class Material(object):
  """Innehåller information om färg, reflektivitet och specular highlight värden för ett material"""


class GUI(object):
  """Skapa ett GUI där användaren kan specificera kamera och upplösning och displaya den raytracade bilden"""


"""Sätt upp kamera, läs och sätt upp geometriska objekt i scenen, skicka Ray för varje pixel och raytracea, skicka visa en bild"""
