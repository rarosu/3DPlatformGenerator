from math import pi, sin, cos

from direct.directnotify.DirectNotify import DirectNotify
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
#from panda3d.core import Point3, Vec4, Vec3, BitMask32
#from panda3d.core import DirectionalLight, AmbientLight
#from panda3d.core import GeomVertexArrayFormat
from panda3d.core import *
from panda3d.bullet import *

class MyApp(ShowBase):

        def __init__(self):
            ShowBase.__init__(self)

            # Add a debug category for logging.
            self.notify = DirectNotify().newCategory("Logging")

            # Add debug for Bullet
            debugNode = BulletDebugNode("Debug")
            debugNode.showWireframe(True)
            debugNode.showConstraints(True)
            debugNode.showBoundingBoxes(False)
            debugNode.showNormals(True)
            self.debugNP = render.attachNewNode(debugNode)
            self.debugNP.show()

            self.world = BulletWorld()
            self.world.setGravity(Vec3(0, 0, -9.81))
            self.world.setDebugNode(self.debugNP.node())

            # Setup ground plane
            plane = BulletPlaneShape(Vec3(0, 0, 1), 0)
            planeNode = BulletRigidBodyNode("Ground")
            planeNode.addShape(plane)
            planeNP = render.attachNewNode(planeNode)
            planeNP.setPos(0, 0, 0)
            self.world.attachRigidBody(planeNode)

            # Setup dynamic character physics object
            playerHeight = 1.10
            playerRadius = 0.4
            playerStepHeight = 0.15 # NOTE: This is gravity for player controller because Bullet Physics accidentally a bug
            playerJumpHeight = 2.0
            playerJumpSpeed = 4.0

            playerCapsule = BulletCapsuleShape(playerRadius, playerHeight - 2 * playerRadius, ZUp)
            self.playerNode = BulletCharacterControllerNode(playerCapsule, playerStepHeight, "Player")
            self.playerNode.setMaxJumpHeight(playerJumpHeight)
            self.playerNode.setJumpSpeed(playerJumpSpeed)
            self.playerNP = render.attachNewNode(self.playerNode)
            self.playerNP.setPos(0, 0, playerHeight)
            self.playerNP.setCollideMask(BitMask32.allOn())
            self.world.attachCharacter(self.playerNode)

            # Setup non-physical objects
            self.cylinder = self.loader.loadModel("Assets/Models/Cylinder")
            self.cylinder.reparentTo(self.render)
            self.cylinder.setPos(-2, 2, 0)
            self.cylinder.setScale(1, 1, 1)

            cylinderPos = self.cylinder.getPos()
            cylinderGeom = self.cylinder.findAllMatches("**/+GeomNode").getPath(0).node().getGeom(0)
            cylinderShape = BulletConvexHullShape()
            cylinderShape.addGeom(cylinderGeom)
            cylinderNode = BulletRigidBodyNode("Cylinder")
            cylinderNode.addShape(cylinderShape)
            cylinderNP = render.attachNewNode(cylinderNode)
            cylinderNP.setPos(cylinderPos.getX(), cylinderPos.getY(), cylinderPos.getZ() + 1 )
            self.world.attachRigidBody(cylinderNode)

            self.makeCube()
            
            # Load a level
            self.level = Level("Assets/Levels/test.level")

            # Setup tasks
            self.taskMgr.add(self.followCameraTask, "FollowCameraTask")
            self.taskMgr.add(self.physicsUpdate, "PhysicsUpdate")

            self.ralph = Actor("Assets/Models/ralph",
                                    {"walk": "Assets/Models/ralph-walk",
                                    "run": "Assets/Models/ralph-run"})
            self.ralph.setScale(0.2, 0.2, 0.2)
            self.ralph.reparentTo(self.playerNP)
            self.ralph.setPos(0, 0, -playerHeight * 0.5)

            #self.camera.reparentTo(self.ralph)
            #self.camera.setPos(self.ralph.getX(render), self.ralph.getY(render) + 10, 5)
            #self.camera.lookAt(self.ralph)

            ambLight = AmbientLight("ambLight")
            ambLight.setColor(Vec4(0.3, 0.3, 0.3, 1.0))
            ambLightNP = render.attachNewNode(ambLight)
            render.setLight(ambLightNP)

            dirLight = DirectionalLight("dirLight")
            dirLight.setColor(Vec4(0.7, 0.7, 0.7, 1.0))
            dirLightNP = render.attachNewNode(dirLight)
            dirLightNP.setHpr(180, -20, 0)
            render.setLight(dirLightNP)


            self.ralph.loop("run")
            #posInterval1 = self.ralph.posInterval(13, Point3(0, -10, 0), startPos = Point3(0, 10, 0))
            #posInterval2 = self.ralph.posInterval(13, Point3(0, 10, 0), startPos = Point3(0, -10, 0))
            #hprInterval1 = self.ralph.hprInterval(3, Point3(180, 0, 0), startHpr = Point3(0, 0, 0))
            #hprInterval2 = self.ralph.hprInterval(3, Point3(0, 0, 0), startHpr = Point3(180, 0, 0))

            #self.ralphPace = Sequence(posInterval1, hprInterval1, posInterval2, hprInterval2, name = "ralphPace")
            #self.ralphPace.loop()

            # INPUT
            self.keyMap = { "forward" : 0, "left" : 0, "backward" : 0, "right" : 0}

            self.accept("f1", self.toggleDebug)

            self.accept("space", self.jump)

            self.accept("w", self.setKey, ["forward", 1])
            self.accept("a", self.setKey, ["left", 1])
            self.accept("s", self.setKey, ["backward", 1])
            self.accept("d", self.setKey, ["right", 1])
            self.accept("w-up", self.setKey, ["forward", 0])
            self.accept("a-up", self.setKey, ["left", 0])
            self.accept("s-up", self.setKey, ["backward", 0])
            self.accept("d-up", self.setKey, ["right", 0])


        def followCameraTask(self, task):
            radius = 20.0
            position = self.ralph.getPos(render)
            heading = self.ralph.getH(render) * (pi / 180.0) - pi * 0.5
            facing = Vec3(cos(heading), sin(heading), 0.0)
            offset = Vec3(-radius * facing.getX(), -radius * facing.getY(), 5)

            self.camera.setPos(position + offset)
            self.camera.lookAt(self.ralph)

            return task.cont

        def physicsUpdate(self, task):
            dt = globalClock.getDt()
            
            # Update the character movement
            speed = 0
            angularSpeed = 0
            if self.keyMap["forward"] != 0:
                speed = -3.0
            if self.keyMap["backward"] != 0:
                speed = 3.0
            if self.keyMap["left"] != 0:
                angularSpeed = 60
            if self.keyMap["right"] != 0:
                angularSpeed = -60
            self.playerNode.setLinearMovement(Vec3(0, speed, 0), True)
            self.playerNode.setAngularMovement(angularSpeed)

            self.world.doPhysics(dt)
            return task.cont

        def toggleDebug(self):
            if self.debugNP.isHidden():
                self.debugNP.show()
            else:
                self.debugNP.hide()

        def setKey(self, key, value):
            self.keyMap[key] = value

        def jump(self):
            self.playerNode.doJump()

        def makeCube(self):
            array = GeomVertexArrayFormat()
            array.addColumn(InternalName.make('vertex'), 3, Geom.NTFloat32, Geom.CPoint)

            format = GeomVertexFormat()
            format.addArray(array)
            format = GeomVertexFormat.registerFormat(format)

            vdata = GeomVertexData('cube', format, Geom.UHStatic)
            vdata.setNumRows(8)

            vertex = GeomVertexWriter(vdata, 'vertex')

            vertex.addData3f(0, 1, 0) #0
            vertex.addData3f(1, 1, 0) #1
            vertex.addData3f(0, 0, 0) #2
            vertex.addData3f(1, 0, 0) #3

            vertex.addData3f(0, 1, 1) #4
            vertex.addData3f(1, 1, 1) #5
            vertex.addData3f(0, 0, 1) #6
            vertex.addData3f(1, 0, 1) #7

            prim = GeomTriangles(Geom.UHStatic)
            #bottom
            prim.addVertices(1, 2, 0)
            prim.addVertices(1, 3, 2)
            #top
            prim.addVertices(4, 6, 5)
            prim.addVertices(6, 7, 5)
            #front
            prim.addVertices(2, 3, 6)
            prim.addVertices(6, 3, 7)
            #back
            prim.addVertices(4, 1, 0)
            prim.addVertices(5, 1, 4)
            #left
            prim.addVertices(0, 2, 4)
            prim.addVertices(4, 2, 6)
            #right
            prim.addVertices(5, 3, 1)
            prim.addVertices(7, 3, 5)

            geom = Geom(vdata)
            geom.addPrimitive(prim)

            node = GeomNode('gnode')
            node.addGeom(geom)

            nodePath = render.attachNewNode(node)

            #plane = BulletPlaneShape(Vec3(0, 0, 1), 0)
            #planeNode = BulletRigidBodyNode("Ground")
            #planeNode.addShape(plane)
            #planeNP = render.attachNewNode(planeNode)
            #planeNP.setPos(0, 0, 0)
            #self.world.attachRigidBody(planeNode)

            shape = BulletConvexHullShape()
            shape.addGeom(geom)
            shapeNode = BulletRigidBodyNode("Cube")
            shapeNode.addShape(shape)
            shapeNP = render.attachNewNode(shapeNode)
            shapeNP.setPos(0, 0, 0)
            self.world.attachRigidBody(shapeNode)

class Level:
    def __init__(self, filepath):
        file = open(filepath)
        
        s = file.readline().strip()
        while s != "[Curve]":
            s = file.readline().strip()
        
        curveString = ""
        while s != "[Genotype]":
            s = file.readline().strip()
            if s != "[Genotype]":
                curveString += s
        
        # Process the curve data now in curveString.
        self.ProcessCurve(curveString)
        
        genotypeString = ""
        while s != "":
            s = file.readline().strip()
            genotypeString += s
            
        # Process the genotype data now in genotypeString.
        self.ProcessGenotype(genotypeString)
    
    def ProcessCurve(self, curveString):
        comp = curveString.split(",")
        cp = []
        
        for i in range(0, len(comp) - 3, 3):
            #print("(%s, %s, %s)" % (comp[i], comp[i + 1], comp[i + 2]))
            cp.append(Vec3(float(comp[i]), float(comp[i + 1]), float(comp[i + 2])))
            
        assert((len(cp) - 1) % 3 == 0)
        self.curve = BezierCurve(cp)
        
    def ProcessGenotype(self, genotypeString):
        pass
            
class BezierSpline:
    # start, cp1, cp2 and end are type: panda3d.core.Vec3
    def __init__(self, start, cp1, cp2, end):
        self.start = start
        self.cp1 = cp1
        self.cp2 = cp2
        self.end = end
    
    def getPoint(self, t):
        it = 1 - t
        
        return (self.start * it * it * it +
               self.cp1 * 3 * it * it * t +
               self.cp2 * 3 * it * t * t +
               self.end * t * t * t)
    
    def getTangent(self, t):
        it = 1 - t
        tangent = ((self.cp1 - self.start) * 3 * it * it +
                  (self.cp2 - self.cp1) * 6 * it * t +
                  (self.end - self.cp2) * 3 * t * t)
        tangent.normalize()
        return tangent
        
class BezierCurve:
    def __init__(self, cp):
        self.splines = []
        
        for i in range(0, len(cp) - 3, 3):
            self.splines.append(BezierSpline(cp[i], cp[i + 1], cp[i + 2], cp[i + 3]))

    def getPoint(self, t):
        i = int(t)
        i = max(min(i, len(self.splines) - 1), 0)
        
        if t > 0 and t < len(self.splines):
            return self.splines[i].getPoint(t - i)
        elif t < 0:
            point = self.splines[0].getPoint(0)
            tangent = self.splines[0].getTangent(0)
            
            return point + tangent * t
        elif t > len(self.splines):
            point = self.splines[-1].getPoint(1)
            tangent = self.splines[-1].getTangent(1)
            
            return point + tangent * (t - i)

    def getTangent(self, t):
        i = int(t)
        return self.splines[i].getTangent(t - i)


app = MyApp()
app.run()
