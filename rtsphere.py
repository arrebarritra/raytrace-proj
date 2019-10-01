from math import *
from PIL import Image
import json


class Vec3(object):
    """Metoder för 3D-vektor operationer"""

    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def __str__(self):
        return str(self.x), str(self.y), str(self.z)

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
        return Vec3(self.y * v.z - self.z * v.y, self.z * v.x - self.x * v.z,
                    self.x * v.y - self.y * v.z)

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
        return (int(self.scale * self.r), int(self.scale * self.g),
                int(self.scale * self.b))


class Material(object):
    """Innehåller information om färg, reflektivitet och specular highlight-egenskaper"""

    def __init__(self, colour, mirror, specularcolour, shininess):
        self.colour = colour
        self.mirror = mirror
        self.specularcolour = specularcolour
        self.shininess = shininess


class Intersection(object):
    """Innehåller information om intersektionen av en Ray och objektet som den intersekterar"""

    def __init__(self, ray):
        self.t = ray.tmax
        self.shape = None
        self.c = Colour(0, 0, 0)

    def setintersect(self, t, shape):
        """Uppdaterar intersektionspunkten t och intersektionsobjektet shape"""
        if t < self.t:
            self.t = t
            self.shape = shape


class Ray(object):
    """Ljusstråle"""

    def __init__(self, origin, direction, distmin=0.0001, distmax=1e30,
                 maxbounce=3, bounce=0):
        self.o = origin
        self.d = direction.norm()
        self.tmin = distmin
        self.tmax = distmax
        self.maxbounce = maxbounce
        self.bounce = bounce
        self.intersection = Intersection(self)

    def intersect(self, scene):
        intersect = self.doesintersect(scene)

        if intersect:
            intersection = self.intersection
            self.shade(intersection.shape, intersection.t, scene)

        return intersect

    def doesintersect(self, scene):
        for shape in scene.shapes:
            if shape.doesintersect(self):
                return True
        return False

    def shade(self, shape, t, scene):
        intersection = self.intersection
        intersectpoint = self.point(intersection.t)
        normal = shape.normal(intersectpoint)
        nudge = intersectpoint + normal * self.tmin
        intersectioncolour = intersection.c

        # Ambient
        intersectioncolour += shape.m.colour * scene.ambient

        for light in self.scene.lights:
            lightray = Ray(nudge, light.p - nudge,
                           distmax=(light.p - nudge).len())

            if not(lightray.doesintersect(scene)):
                # Diffuse
                diffuse = max(0, normal.dot(lightray.d))
                intersectioncolour += shape.m.colour * light.colour * diffuse

                # Specular
                specular = max(0, normal.dot(
                    (lightray.o - intersectpoint + self.o - intersectpoint)
                    .norm()))
                intersection.c += shape.m.specularcolour * \
                    light.colour * (specular ** shape.m.shininess)

        if self.bounce < self.maxbounce and shape.m.mirror > 0:
            # Reflection
            refd = (self.d - normal * 2 * self.d.dot(normal)).norm()
            refray = Ray(nudge, refd, bounce=self.bounce + 1)
            if refray.intersect(scene):
                intersectioncolour += refray.intersection.c * shape.m.mirror

    def point(self, t):
        return self.o + self.d * t


class Camera(object):
    def __init__(self, o, fwd, upguide, w, h, fovh):
        self.o = o
        self.fwd = fwd.norm()
        self.right = self.fwd.cross(upguide).norm()
        self.up = self.right.cross(self.fwd)
        self.h = tan(radians(fovh))
        self.w = self.h * (w / h)

    def makeray(self, x, y):
        """Skickar Ray baserat på (x, y) koordinater och kamerans position och riktning"""
        rayd = self.fwd + (self.right * x * self.w) + (self.up * y * self.h)
        return Ray(self.o, rayd.norm())


class Plane(object):
    """Oändligt plan, implementerar Sphere metoder"""

    def __init__(self, origin, normal, material):
        self.o = origin
        self.n = normal.norm()
        self.m = material

    def intersect(self, ray, doesintersectmethod=False):
        if self.n.dot(ray.d) == 0:
            return False
        else:
            t = self.n.dot(self.o - ray.o) / self.n.dot(ray.d)

        if t > ray.tmin and t < ray.tmax:
            if not doesintersectmethod:
                ray.intersection.setintersect(t, self)
            return True
        else:
            return False

    def doesintersect(self, ray):
        self.intersect(ray, doesintersectmethod=True)

    def normal(self, point):
        return self.n


class Sphere(object):
    """Sfär, implementerar Sphere metoder"""

    def __init__(self, origin, radius, material):
        self.o = origin
        self.r = radius
        self.m = material

    def intersect(self, ray, doesintersectmethod=False):
        sphererayo = ray.o - self.o
        # Solve quadratic for t, a = 1
        b = 2 * ray.d.dot(sphererayo)
        c = sphererayo.len() ** 2 - self.r ** 2
        disc = b ** 2 - (4 * c)

        if disc < 0:
            return False

        t1 = (-b - sqrt(disc)) / 2
        t2 = (-b + sqrt(disc)) / 2
        t = min(t1, t2)

        if t > ray.tmin and t < ray.tmax:
            if not doesintersectmethod:
                ray.intersection.setintersect(t, self)
            return True
        else:
            return False

    def doesintersect(self, ray):
        return self.intersect(ray, doesintersectmethod=True)

    def normal(self, point):
        return (point - self.o).norm()


class Light(object):
    """Innehåller positionen och intensiteten av et ljusobjekt"""

    def __init__(self, position, colour):
        self.p = position
        self.colour = colour


class Scene(object):
    """Innehåller alla Shape och Light objekt, importeras från en JSON fil"""

    def __init__(self, filescene, filematerials):
        scenedata = json.load(filescene)
        materials = json.load(filematerials)
        self.ambient = scenedata["ambient"]
        self.shapes = []
        self.lights = []

        for shape in scenedata["Shapes"]:
            origin = Vec3(shape["origin"][0], shape["origin"][1],
                          shape["origin"][2])
            materialname = shape["material"]
            material = Material(materials[materialname]["colour"],
                                materials[materialname]["mirror"],
                                materials[materialname]["specularcolour"],
                                materials[materialname]["shininess"])

            if shape["type"] == "Plane":
                normal = Vec3(shape["normal"][0], shape["normal"][1],
                              shape["normal"][2])
                self.shapes += Plane(origin, normal, material)
            elif shape["type"] == "Sphere":
                radius = shape["radius"]
                self.shapes += Plane(origin, radius, material)

        for light in scenedata["Lights"]:
            position = Vec3(light["position"][0], light["position"][1],
                            light["position"][2])
            colour = light["colour"]
            self.lights += Light(position, colour)


class GUI(object):
    """Skapa ett GUI där användaren kan specificera kamera och upplösning och displaya den raytracade bilden"""


"""Sätt upp kamera, läs och sätt upp geometriska objekt i scenen, skicka Ray för varje pixel och raytracea, skicka visa en bild"""
