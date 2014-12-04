from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, Vec4, Vec3
from panda3d.core import DirectionalLight, AmbientLight
from panda3d.bullet import *

class MyApp(ShowBase):

        def __init__(self):
            ShowBase.__init__(self)

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
            plane = BulletPlaneShape(Vec3(0, 0, 1), -1)
            planeNode = BulletRigidBodyNode("Ground")
            planeNode.addShape(plane)
            planeNP = render.attachNewNode(planeNode)
            planeNP.setPos(0, 0, 0)
            self.world.attachRigidBody(planeNode)

            # Setup dynamic physics object
            capsule = BulletCapsuleShape(1, 1, ZUp)
            capsuleNode = BulletRigidBodyNode("Capsule")
            capsuleNode.setMass(1.0)
            capsuleNode.addShape(capsule)
            capsuleNP = render.attachNewNode(capsuleNode)
            capsuleNP.setPos(0, 0, 200)
            self.world.attachRigidBody(capsuleNode)

            self.cylinder = self.loader.loadModel("Assets/Models/Cylinder")
            self.cylinder.reparentTo(self.render)
            self.cylinder.setPos(-2, 2, 0)
            self.cylinder.setScale(1, 1, 1)

            self.taskMgr.add(self.followCameraTask, "FollowCameraTask")
            self.taskMgr.add(self.update, "Update")

            self.ralph = Actor("Assets/Models/ralph",
                                    {"walk": "Assets/Models/ralph-walk",
                                    "run": "Assets/Models/ralph-run"})
            self.ralph.setScale(0.2, 0.2, 0.2)
            self.ralph.reparentTo(capsuleNP)

            #self.camera.reparentTo(self.ralph)
            #self.camera.setPos(self.ralph.getX(render), self.ralph.getY(render) + 10, 5)
            #self.camera.lookAt(self.ralph)

            ambLight = AmbientLight("ambLight")
            ambLight.setColor(Vec4(0.3, 0.3, 0.3, 1))
            ambLightNP = render.attachNewNode(ambLight)
            render.setLight(ambLightNP)

            dirLight = DirectionalLight("dirLight")
            dirLight.setColor(Vec4(1.0, 0.0, 0.0, 1.0))
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
            self.accept("f1", self.toggleDebug)


        def followCameraTask(self, task):
            #hpr = self.ralph.getHpr()
            #facing = Vec3(cos(hpr.x))
            #self.camera.setPos(self.ralph.getPos() - )
            #self.camera.setHpr(hpr)
            pos = self.ralph.getPos(render)
            self.camera.setPos(pos.getX(), pos.getY() + 10, 5)
            self.camera.lookAt(self.ralph)
            return Task.cont

        def update(self, task):
            dt = globalClock.getDt()
            self.world.doPhysics(dt)
            return task.cont

        def toggleDebug(self):
            if self.debugNP.isHidden():
                self.debugNP.show()
            else:
                self.debugNP.hide()


app = MyApp()
app.run()
