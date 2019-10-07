from math import *
import tkinter
from PIL import Image
import json
import numpy as np


class Vec3(object):
    """Metoder för 3D-vektor operationer"""

    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def __str__(self):
        return str(self.x) + ", " + str(self.y) + ", " + str(self.z)

    def __add__(self, v):
        return Vec3(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        return Vec3(self.x - v.x, self.y - v.y, self.z - v.z)

    def __mul__(self, v):
        return Vec3(v * self.x, v * self.y, v * self.z)

    def __truediv__(self, v):
        return self * (1 / float(v))

    def len(self):
        """Returnerar denna Vec3:s längd"""
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def dot(self, v):
        """Returnerar skalärprodukten av denna Vec3 och Vec3:n v"""
        return self.x * v.x + self.y * v.y + self.z * v.z

    def cross(self, v):
        """Returnerar kryssprodukten av denna Vec3 och Vec3:n v"""
        return Vec3(self.y * v.z - self.z * v.y, self.z * v.x - self.x * v.z,
                    self.x * v.y - self.y * v.x)

    def norm(self):
        """Returnerar denna Vec3 normaliserad"""
        return Vec3(self.x, self.y, self.z) / self.len()

    def listtovec(vec):
        """Konverterar en lista till Vec3"""
        return Vec3(vec[0], vec[1], vec[2])


class Colour(object):
    """Innehåller RGB färg med värden mellan 0 och 1, samt färgoperationer för blandning av färger"""

    min = 0
    max = 1
    scale = 255

    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b

    def __str__(self):
        return str(self.r) + ", " + str(self.g) + ", " + str(self.b)

    def __add__(self, c):
        return Colour(self.r + c.r, self.g + c.g, self.b + c.b)

    def __mul__(self, c):
        if type(c) == Colour:
            return Colour(self.r * c.r, self.g * c.g, self.b * c.b)
        elif type(c) == float or type(c) == int:
            return Colour(self.r * c, self.g * c, self.b * c)

    def gammaCorrection(self, exposure, gamma):
        """Justerar pixelfärgen till en gammakurva"""
        self.r = (self.r * exposure) ** gamma
        self.g = (self.g * exposure) ** gamma
        self.b = (self.b * exposure) ** gamma

    def clamp(self):
        """Clampar RGB värden mellan 0 och 1"""
        self.r = max(self.min, min(self.max, self.r))
        self.g = max(self.min, min(self.max, self.g))
        self.b = max(self.min, min(self.max, self.b))

    def scaleRGB(self):
        """Returnerar RGB värde på skala 0 till 255"""
        return (int(self.scale * self.r), int(self.scale * self.g),
                int(self.scale * self.b))

    def listtocolour(c):
        """Konverterar en lista till Colour"""
        return Colour(c[0], c[1], c[2])


class Material(object):
    """Innehåller information om färg, reflektivitet och specular highlight-egenskaper"""

    def __init__(self, ambient, diffuse, specular, shininess, mirror):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.mirror = mirror


class Intersection(object):
    """Innehåller information om intersektionen av en Ray och objektet som den intersect:ar"""

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
    """Hanterar en rays position, riktning och intersektion, innehåller metoder för att beräkna intersektionen shade:a rayen"""

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
        """Returnerar om detta objekt intersect:ar scenen, uppdaterar intersection objektet"""
        intersect = False
        for shape in scene.shapes:
            if shape.intersect(self):
                intersect = True

        if intersect:
            self.shade(scene)
        return intersect

    def doesintersect(self, scene):
        """Returnerar om detta objekt intersect:ar scenen"""
        for shape in scene.shapes:
            if shape.doesintersect(self):
                return True
        return False

    def shade(self, scene):
        """Shadear scenen med ambient, diffuse och specular shading och beräknar reflektion, uppdaterar intersektionsfärgen"""
        intersection = self.intersection
        t = intersection.t
        shape = intersection.shape
        intersectpoint = self.point(t)
        normal = shape.normal(intersectpoint)
        nudge = intersectpoint + normal * self.tmin

        # Ambient
        intersection.c += shape.m.ambient * scene.ambient

        for light in scene.lights:
            lightray = Ray(nudge, light.p - nudge,
                           distmax=(light.p - nudge).len())

            if not(lightray.doesintersect(scene)):
                # Diffuse
                diffuse = max(0, normal.dot(lightray.d))
                intersection.c += shape.m.diffuse * light.diffuse * diffuse

                # Specular
                specular = max(0, normal.dot(
                    (lightray.o - intersectpoint + self.o - intersectpoint)
                    .norm()))
                intersection.c += shape.m.specular * \
                    light.specular * (specular ** shape.m.shininess)

        # Reflection
        if self.bounce < self.maxbounce and shape.m.mirror > 0:
            refd = (self.d - normal * 2 * self.d.dot(normal)).norm()
            refray = Ray(nudge, refd, bounce=self.bounce + 1)
            if refray.intersect(scene):
                intersection.c += refray.intersection.c * shape.m.mirror

    def point(self, t):
        """Returnerar punkten på denna Ray t enheter ifrån origo"""
        return self.o + self.d * t


class Camera(object):
    """Skapar en kamera med position och riktning, skickar Rays baserat på pixeln som ska färgas"""

    def __init__(self, origin, fwd, upguide, aspectratio, fovv, maxbounce):
        self.o = origin
        self.fwd = fwd.norm()
        self.right = self.fwd.cross(upguide).norm() * -1
        self.up = self.right.cross(self.fwd) * -1
        self.h = tan(radians(fovv))
        self.w = self.h * aspectratio
        self.maxbounce = maxbounce

    def makeray(self, x, y):
        """Skickar en Ray som färgar pixeln (x, y) baserat kamerans position och riktning, returnerar Ray med intersection objektet som innehåller dess färg"""
        rayd = self.fwd + (self.right * x * self.w) + (self.up * y * self.h)
        return Ray(self.o, rayd.norm(), maxbounce=self.maxbounce)


class Plane(object):
    """Hanterar ett plan i rymden och beräknar dess intersektioner med Rays"""

    def __init__(self, origin, normal, material):
        self.o = origin
        self.n = normal.norm()
        self.m = material

    def intersect(self, ray, updateintersect=True):
        """Returnerar om ray intersect:ar detta plan, uppdaterar intersection objektet"""
        if self.n.dot(ray.d) == 0:
            return False
        else:
            t = self.n.dot(self.o - ray.o) / self.n.dot(ray.d)

        if t > ray.tmin and t < ray.tmax:
            if updateintersect:
                ray.intersection.setintersect(t, self)
            return True
        else:
            return False

    def doesintersect(self, ray):
        """Returnerar om Ray intersect:ar detta Plan"""
        self.intersect(ray, updateintersect=False)

    def normal(self, point):
        """Returnerar planets normalvektor"""
        return self.n


class Sphere(object):
    """Hanterar en sfär i rymden och beräknar dess intersektioner med Rays"""

    def __init__(self, origin, radius, material):
        self.o = origin
        self.r = radius
        self.m = material

    def intersect(self, ray, updateintersect=True):
        """Returnerar om ray intersect:ar denna sfär, uppdaterar intersection objektet"""
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
            if updateintersect:
                ray.intersection.setintersect(t, self)
            return True
        else:
            return False

    def doesintersect(self, ray):
        """Returnerar om ray intersect:ar denna sfär"""
        return self.intersect(ray, updateintersect=False)

    def normal(self, point):
        """Returnerar sfärens normalvektor vid point"""
        return (point - self.o).norm()


class Light(object):
    """Innehåller positionen och egenskaper av en point light"""

    def __init__(self, position, diffuse, specular):
        self.p = position
        self.diffuse = diffuse
        self.specular = specular


class Scene(object):
    """Innehåller alla Shape och Light objekt, importeras från en JSON fil"""

    def __init__(self, filescene, filematerials):
        scenedata = json.load(filescene)
        materials = json.load(filematerials)
        self.ambient = Colour.listtocolour(scenedata["ambient"])
        self.shapes = []
        self.lights = []

        for shape in scenedata["Shapes"]:
            origin = Vec3.listtovec(shape["origin"])
            materialname = shape["material"]
            material = Material(Colour.listtocolour(
                                materials[materialname]["ambient"]),
                                Colour.listtocolour(
                                materials[materialname]["diffuse"]),
                                Colour.listtocolour(
                                materials[materialname]["specular"]),
                                materials[materialname]["shininess"],
                                materials[materialname]["mirror"])

            if shape["type"] == "Plane":
                normal = Vec3.listtovec(shape["normal"])
                self.shapes += [Plane(origin, normal, material)]
            elif shape["type"] == "Sphere":
                radius = shape["radius"]
                self.shapes += [Sphere(origin, radius, material)]

        for light in scenedata["Lights"]:
            position = Vec3.listtovec(light["position"])
            diffuse = Colour.listtocolour(light["diffuse"])
            specular = Colour.listtocolour(light["specular"])
            self.lights += [Light(position, diffuse, specular)]


class optionsWindow(object):
    """Fönster med render settings"""

    def __init__(self):
        window = tkinter.Tk()
        window.title("Cam")
        tkinter.Label(window, text="Origin vector").grid(row=0)
        tkinter.Label(window, text="Forward vector").grid(row=1)
        tkinter.Label(window, text="Up vector").grid(row=2)
        tkinter.Label(window, text="Image width").grid(row=3)
        tkinter.Label(window, text="Image height").grid(row=4)
        tkinter.Label(window, text="Vertical FOV").grid(row=5)
        tkinter.Label(window, text="Ray max bounce").grid(row=6)
        tkinter.Label(window, text="Exposure").grid(row=7)
        self.fields = [tkinter.Entry(window) for i in range(8)]
        fields = self.fields
        fields[0].insert(0, '0,0,0')
        fields[1].insert(0, '0,0,1')
        fields[2].insert(0, '0,1,0')
        fields[3].insert(0, '300')
        fields[4].insert(0, '200')
        fields[5].insert(0, '60')
        fields[6].insert(0, '3')
        fields[7].insert(0, '1')
        for i in range(len(fields)):
            fields[i].grid(row=i, column=1)
        button = tkinter.Button(window, text="Render", command=self.render)
        button.grid(row=len(fields)+1, column=1)
        window.mainloop()

    def render(self):
        """Skickar användarinmatade parametrar till render funktionen"""
        fields = self.fields
        vec = []
        for field in fields[:-3]:
            vec += [strtolist(field.get())]
        width = int(fields[3].get())
        height = int(fields[4].get())
        fovv = float(fields[5].get())
        maxbounce = int(fields[6].get())
        exposure = float(fields[7].get())
        cam = Camera(Vec3.listtovec(vec[0]), Vec3.listtovec(vec[1]),
                     Vec3.listtovec(vec[2]), width / height, fovv, maxbounce)
        scene = Scene(open("scenedata.json"), open("materials.json"))
        img = render(cam, scene, width, height, exposure)
        img.show()


def render(cam, scene, width, height, exposure, gamma=2.2):
    """Renderar (färgar pixlar) och returnar bild av scenen"""
    img = Image.new('RGB', (width, height), 'black')
    pixels = img.load()
    for x, xspace in zip(range(width), np.linspace(-1, 1, width)):
        for y, yspace in zip(range(height), np.linspace(1, -1, height)):
            ray = cam.makeray(float(xspace), float(yspace))
            if ray.intersect(scene):
                ray.intersection.c.gammaCorrection(exposure, gamma)
                ray.intersection.c.clamp()
                pixels[x, y] = ray.intersection.c.scaleRGB()
    return img


def strtolist(cstr):
    """Konverterar en kommaseparerad sträng till en lista av floats, ex. "0,1,2"->[0.0,1.0,2.0]"""
    convlist = cstr.split(",")
    for i in range(len(convlist)):
        convlist[i] = float(convlist[i])
    return convlist


def main():
    optionsWindow()


if __name__ == '__main__':
    main()
