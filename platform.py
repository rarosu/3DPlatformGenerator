from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, Vec4, Vec3, BitMask32
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

            # Setup dynamic character physics object
            playerHeight = 1.10
            playerRadius = 0.4
            playerStepHeight = 0.4
            playerJumpHeight = 5.0
            playerJumpSpeed = 8.0
            
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
            #hpr = self.ralph.getHpr()
            #facing = Vec3(cos(hpr.x))
            #self.camera.setPos(self.ralph.getPos() - )
            #self.camera.setHpr(hpr)
            pos = self.ralph.getPos(render)
            self.camera.setPos(pos.getX(), pos.getY() + 10, pos.getZ() + 5)
            self.camera.lookAt(self.ralph)
            return Task.cont

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


app = MyApp()
app.run()
