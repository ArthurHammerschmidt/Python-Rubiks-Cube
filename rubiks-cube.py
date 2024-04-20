import sys
import random
import wx
import time
import numpy
from lib_rubiks import  *
from interactionMatrix import InteractionMatrix

import wx.glcanvas as glcanvas
from math import *

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print( ''' Error: PyOpenGL not installed properly !!''')
  sys.exit(  )

(faceList, bodyList, cubeList)= (1,2,3)
(turn,angle,axis,tick_obj) = (0,0,0,0)
moving = False


class MyCanvas(glcanvas.GLCanvas):

    def __init__(self, parent):
        global interactor
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.init = False
        self.context = glcanvas.GLContext(self)

        size = self.size = self.GetClientSize()
        self.SetCurrent(self.context)
        glViewport(0, 0, size.width, size.height)

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        interactor = InteractionMatrix()

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def draw_string(self,x, y, z, p, s, scale=0.006):
        glPushMatrix()
        glTranslatef(x, y, z)
        if p == "xy":
            pass
        elif p == "yz":
            glRotatef(90, 0, 1, 0)
        elif p == "xz":
            glRotatef(-90, 1, 0, 0)
            glRotatef(90, 0, 0, 1)
        glScalef(scale, scale, scale)
        for c in str(s):
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
        glPopMatrix()

    def build_cube(self):
        global cubeList
        # cubeList = glGenLists(1)
        # if cubeList == 0:
        #     print( 'error : glGenLists failed')
        #     quit()
#        print( 'cubeList',cubeList)
        glNewList(cubeList,GL_COMPILE)
        glBegin(GL_QUADS)
        for ic in range(8):
            for k in [0,1,2]:
                coli = Ccif[ic][k]
                glColor3fv(colors[coli])
                f = Cfp[ic][k][0]
                p = Cfp[ic][k][1]
                for j in range(4):
                    glVertex3fv(patch[f][p][j])
        glEnd()

        glBegin(GL_QUADS)
        for ie in range(12):
            for k in [0,1]:
                coli = Ecif[ie][k]
                glColor3fv(colors[coli])
                f = Efp[ie][k][0]
                p = Efp[ie][k][1]
                for j in range(4):
                    glVertex3fv(patch[f][p][j])
        glEnd()
        glColor3f(0.1,0.1,0.1) # black lines
        for fac in range(6):
            for i in range(9):
                glBegin(GL_LINE_LOOP)
                for j in range(4):
                    glVertex3fv(patch[fac][i][j])
                glEnd()

        for fac in face_order:
            glColor3fv(colors[fac])
            glBegin(GL_QUADS)
            for j in range(4):
                glVertex3fv(centers[fac][j])
            glEnd()

        glEndList()


# remaining list of corners and edges
# by removing corner 'num' or edge 'num'
    def remaining_list(self,num, alist):
        blist = list(range(num))
        for i in alist:
            blist.remove(i)
        return blist

    def build_glLists(self,facei):
#        global faceList, bodyList

        # faceList = glGenLists(1)
        # bodyList = glGenLists(1)
        # if faceList == 0  or bodyList == 0 :
        #     print( 'error : glGenLists failed')
        #     quit()
#        print( 'faceList ',faceList)
#        print( 'bodyList ',bodyList)

        glNewList(faceList,GL_COMPILE)
        #corner patches
        glBegin(GL_QUADS)
        for ic in Cbp[facei]:
            for k in [0,1,2]:
                coli = Ccif[ic][k]
                glColor3fv(colors[coli])
                f = Cfp[ic][k][0]
                p = Cfp[ic][k][1]
                for j in range(4):
                    glVertex3fv(patch[f][p][j])
        glEnd()
        # edge patches
        glBegin(GL_QUADS)
        for ie in Ebp[facei]:
            for k in [0,1]:
                coli = Ecif[ie][k]
                glColor3fv(colors[coli])
                f = Efp[ie][k][0]
                p = Efp[ie][k][1]
                for j in range(4):
                    glVertex3fv(patch[f][p][j])
        glEnd()
        #center patch
        glColor3fv(colors[facei])
        glBegin(GL_QUADS)
        for j in range(4):
            glVertex3fv(centers[facei][j])
        glEnd()
        # under plane
        glColor3f(0.4,0.4,0.4) # grey
        for f in [facei]:
            glBegin(GL_QUADS)
            for j in range(4):
                glVertex3fv(op[f][j])
            glEnd()



        # lines
        glColor3f(0.1,0.1,0.1) # black lines
        for ic in Cbp[facei]:
            for k in [0,1,2]:
                glBegin(GL_LINE_LOOP)
                for j in range(4):
                    glVertex3fv(patch[ Cfp[ic][k][0] ] [ Cfp[ic][k][1] ] [j])
                glEnd()
        for ie in Ebp[facei]:
            for k in [0,1]:
                glBegin(GL_LINE_LOOP)
                for j in range(4):
                    glVertex3fv(patch[ Efp[ie][k][0] ] [ Efp[ie][k][1] ] [j])
                glEnd()

        glEndList()

        corn = self.remaining_list(8,Cbp[facei])
        edge = self.remaining_list(12,Ebp[facei])
        glNewList(bodyList,GL_COMPILE)
        glBegin(GL_QUADS)
        for ic in corn:
            for k in [0,1,2]:
                coli = Ccif[ic][k]
                glColor3fv(colors[coli])
                f = Cfp[ic][k][0]
                p = Cfp[ic][k][1]
                for j in range(4):
                    glVertex3fv(patch[f][p][j])
        glEnd()

        glBegin(GL_QUADS)
        for ie in edge:
            for k in [0,1]:
                coli = Ecif[ie][k]
                glColor3fv(colors[coli])
                f = Efp[ie][k][0]
                p = Efp[ie][k][1]
                for j in range(4):
                    glVertex3fv(patch[f][p][j])
        glEnd()

        #center patch
        centps = self.remaining_list(6,[facei])
        for f in centps:
            glColor3fv(colors[f])
            glBegin(GL_QUADS)
            for j in range(4):
                glVertex3fv(centers[f][j])
            glEnd()
        # cover plane
        glColor3f(0.4,0.4,0.4) # grey
        for f in [facei]:
            glBegin(GL_QUADS)
            for j in range(4):
                glVertex3fv(op[f][j])
            glEnd()



        # lines
        glColor3f(0.1,0.1,0.1) # black lines
        for ic in corn:
            for k in [0,1,2]:
                glBegin(GL_LINE_LOOP)
                for j in range(4):
                    glVertex3fv(patch[ Cfp[ic][k][0] ] [ Cfp[ic][k][1] ] [j])
                glEnd()
        for ie in edge:
            for k in [0,1]:
                glBegin(GL_LINE_LOOP)
                for j in range(4):
                    glVertex3fv(patch[ Efp[ie][k][0] ] [ Efp[ie][k][1] ] [j])
                glEnd()
        glEndList()



    def InitGL(self):
        # setup OpenGL state
        glClearDepth(1.0)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        x,y,width,height = glGetDoublev(GL_VIEWPORT)
#        print( 'InitGL ',width,height)
        gluPerspective(
            45, # field of view in degrees
            width/float(height or 1), # aspect ratio
            .25, # near clipping plane
            200, # far clipping plane
            )
        #
        #        glOrtho(-5,5,-5,5,-30,30)
        # and then the model view matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(
            0,1,15, # eyepoint
            0,0,0, #2,1,-8, # center-of-view
            0,1,0, # up-vector
        )
        self.build_cube()

    def OnDraw(self):
    #    global angle,axis,tick_obj,interactor

        glClear(GL_DEPTH_BUFFER_BIT)
        glDisable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        #glMatrixMode (GL_MODELVIEW)
        glLineWidth(5)

        glBegin(GL_POLYGON);
        glColor3f(0.0, 0.0, 0.0);
        glVertex3f(-20.0, 20.0, -19.0)
        glVertex3f( 20.0, 20.0, -19.0)
        glColor3f(0.5, 0.5, 0.5)
        glVertex3f( 20.0, -20.0, -19.0)
        glVertex3f(-20.0, -20.0, -19.0)
        glEnd()
        # paint planes
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_FLAT)

        glPushMatrix()
        glTranslatef(0,0,-5)
        glRotatef(25.0,1.0,0.0,0.0);
        glRotatef(-50.0,0.0,1.0,0.0);

        glColor3f(0.1,0.1,0.1) # black lines
        self.draw_string(3.3,0.0,0.4,"yz",'F')
        self.draw_string(0.8,3.3,0.7,"xz",'U')
        self.draw_string(0.2,0,3.3,"xy",'L')

        #print( 'draw tick_obj',tick_obj)
        glLineWidth(8)
        if tick_obj == 0 :
            glMultMatrixf(interactor.getCurrentMatrix()) # apply all cube rotations so far
            glCallList(cubeList)
        elif tick_obj == 1: #rotating face layer

            glPushMatrix()
            if axis == 0 :
                glRotatef(angle,1.0,0.0,0.0)
            if axis == 1 :
                glRotatef(angle,0.0,1.0,0.0)
            if axis == 2 :
                glRotatef(angle,0.0,0.0,1.0)
            glMultMatrixf(interactor.getCurrentMatrix()) # apply all cube rotations so far
            glCallList(faceList)
            glPopMatrix()

            glMultMatrixf(interactor.getCurrentMatrix()) # apply all cube rotations so far
            glCallList(bodyList)
        elif tick_obj == 2: # rotating whole cube

            glPushMatrix()
            if axis == 0 :
                glRotatef(angle,1.0,0.0,0.0)
            if axis == 1 :
                glRotatef(angle,0.0,1.0,0.0)
            if axis == 2 :
                glRotatef(angle,0.0,0.0,1.0)
            glMultMatrixf(interactor.getCurrentMatrix()) # apply all cube rotations so far
            glCallList(cubeList)
            glPopMatrix()

    ################################################
        glPopMatrix()

        self.SwapBuffers()


class ToolPanel(wx.Panel):
    def __init__(self, parent):
        super(ToolPanel,self).__init__(parent)

        box = wx.StaticBox(self, -1, "FACE ROTATION :   plain = CW ,   prime = CCW")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)

        hsizer = wx.BoxSizer()
        st = wx.StaticText(self, label="Front    Back      Up     Down    Left     Right  ")
        hsizer.Add(st, 0, wx.ALL | wx.CENTER, 2)
        vsizer.Add(hsizer)

        hsizer = wx.BoxSizer()
        st = wx.StaticText(self, label="                                      ")
        hsizer.Add(st, 0, wx.ALL | wx.CENTER, 2)
        vsizer.Add(hsizer)

        hsizer = wx.BoxSizer()
        btn = wx.Button(self, size=(40,20),label='F ')
        btn.Bind(wx.EVT_BUTTON, self.on_rotate_face)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 2)
        btn = wx.Button(self, size=(40,20), label='B ')
        btn.Bind(wx.EVT_BUTTON, self.on_rotate_face)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 2)
        btn = wx.Button(self,  size=(40,20),label='U ')
        btn.Bind(wx.EVT_BUTTON, self.on_rotate_face)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 2)
        btn = wx.Button(self,  size=(40,20),label='D ')
        btn.Bind(wx.EVT_BUTTON, self.on_rotate_face)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 2)
        btn = wx.Button(self, size=(40,20), label='L ')
        btn.Bind(wx.EVT_BUTTON, self.on_rotate_face)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 2)
        btn = wx.Button(self, size=(40,20), label='R ')
        btn.Bind(wx.EVT_BUTTON, self.on_rotate_face)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 2)
        vsizer.Add(hsizer)

        hsizer = wx.BoxSizer()
        btn = wx.Button(self, size=(40,20),label="F'")
        btn.Bind(wx.EVT_BUTTON, self.on_rotate_face)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 2)
        btn = wx.Button(self, size=(40,20), label="B'")
        btn.Bind(wx.EVT_BUTTON, self.on_rotate_face)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 2)
        btn = wx.Button(self,  size=(40,20),label="U'")
        btn.Bind(wx.EVT_BUTTON, self.on_rotate_face)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 2)
        btn = wx.Button(self,  size=(40,20),label="D'")
        btn.Bind(wx.EVT_BUTTON, self.on_rotate_face)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 2)
        btn = wx.Button(self, size=(40,20), label="L'")
        btn.Bind(wx.EVT_BUTTON, self.on_rotate_face)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 2)
        btn = wx.Button(self, size=(40,20), label="R'")
        btn.Bind(wx.EVT_BUTTON, self.on_rotate_face)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 2)
        vsizer.Add(hsizer)

        bsizer.Add(vsizer, 0, wx.CENTER)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(bsizer, 1, wx.EXPAND | wx.ALL, 10)

        # next box
        box = wx.StaticBox(self, -1, "WHOLE CUBE ROTATION ")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        hsizer = wx.BoxSizer()
        vsizer = wx.BoxSizer(wx.VERTICAL)

        btn = wx.Button(self, size=(60,20),label="L ")
        btn.Bind(wx.EVT_BUTTON, self.on_rotate_cube)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        btn = wx.Button(self,size=(60,20), label="U ")
        btn.Bind(wx.EVT_BUTTON, self.on_rotate_cube)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        btn = wx.Button(self, size=(60,20),label="F ")
        btn.Bind(wx.EVT_BUTTON, self.on_rotate_cube)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        vsizer.Add(hsizer)

        hsizer = wx.BoxSizer()

        btn = wx.Button(self, size=(60,20),label="L'")
        btn.Bind(wx.EVT_BUTTON, self.on_rotate_cube)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        btn = wx.Button(self,size=(60,20), label="U'")
        btn.Bind(wx.EVT_BUTTON, self.on_rotate_cube)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        btn = wx.Button(self, size=(60,20),label="F'")
        btn.Bind(wx.EVT_BUTTON, self.on_rotate_cube)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        vsizer.Add(hsizer)

        bsizer.Add(vsizer, 0, wx.CENTER)
        main_sizer.Add(bsizer, 1, wx.EXPAND | wx.ALL, 10)

        # next box
        box = wx.StaticBox(self, -1, "GENERAL")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        hsizer = wx.BoxSizer()
        vsizer = wx.BoxSizer(wx.VERTICAL)

        btn = wx.Button(self,label="Reset")
        btn.Bind(wx.EVT_BUTTON, self.on_reset)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        btn = wx.Button(self, label="Jumble")
        btn.Bind(wx.EVT_BUTTON, self.on_jumble)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        vsizer.Add(hsizer)

        hsizer = wx.BoxSizer()
        btn = wx.Button(self, label="Exit")
        btn.Bind(wx.EVT_BUTTON, self.on_exit)
        hsizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        vsizer.Add(hsizer)

        bsizer.Add(vsizer, 0, wx.CENTER)

        main_sizer.Add(bsizer, 1, wx.EXPAND | wx.ALL, 10)


        self.SetSizer(main_sizer)

    def do_motion(self,tick):
        global angle,tick_obj
        for i in range(1,31):
            angle = angle+cw*3
            time.sleep(0.006)
            frame.canvas.OnDraw()
        # done rotating
        frame.canvas.build_cube()
        if tick_obj == 2: # keep cube rotations
            if axis == 0 :
                interactor.addRotation(angle,1.0,0.0,0.0)
            if axis == 1 :
                interactor.addRotation(angle,0.0,1.0,0.0)
            if axis == 2 :
                interactor.addRotation(angle,0.0,0.0,1.0)

        angle = 0
        tick_obj = 0
        frame.canvas.OnDraw()



    def on_rotate_face(self, event):
        global cw,facei,axis,tick_obj,angle
        btn = event.GetEventObject().GetLabel()
#        print( "Label of pressed button =",btn)
        if btn[1] == "'": key = btn[0].lower()
        else: key = btn[0]
#        print( key)
        facei, cw ,axis = rot_parms(key) # using only facei for build
        # get original face index
        tick_obj = 1
        angle = 0
        frame.canvas.build_glLists(facei) # genrate list with current colors
        face_rotate(key)  # rotate colors
#        build_cube()      # generate cube list with final colors
        facei, cw ,axis = rot_parms_request(key)
        if facei%2 == 1  : cw = cw*(-1) # flip if odd faces  ie. negative axis
        frame.canvas.Refresh(True)
        self.do_motion(1)

    def on_rotate_cube(self, event):
        global cw,facei,axis,tick_obj,angle
        btn = event.GetEventObject().GetLabel()
#        print( "Label of pressed button =",btn)
        if btn[1] == "'": key = btn[0].lower()
        else: key = btn[0]
#        print( key)
        facei, cw ,axis = rot_parms(key) # using only facei for build
        # get original face index
        tick_obj = 2
        angle = 0
        frame.canvas.build_glLists(facei) # genrate list with current colors
        rotate_cube(key)  # rotate colors
#        build_cube()      # generate cube list with final colors
        facei, cw ,axis = rot_parms_request(key)
        if facei%2 == 1  : cw = cw*(-1) # flip if odd faces  ie. negative axis
        frame.canvas.Refresh(True)
        self.do_motion(2)

    def on_reset(self,event):
        global tick_obj
        reset_colors()
        interactor.reset()
        for i in face_order: ofi_cfi[i] = i
        frame.canvas.build_cube()
        tick_obj = 0
        frame.canvas.OnDraw()

    def on_jumble(self,event):
        global tick_obj
        n = random.randrange(100,1201)
        print( 'random rotations = ',n)
        prvrot = None
        for i in range(n):
            rot = random.choice('FBLRUDfblrud')
            srot = rot.swapcase()
            if srot == prvrot:
                continue
            face_rotate(rot)
            prvrot = rot
        tick_obj = 0
        frame.canvas.build_cube()
        frame.canvas.OnDraw()

    def on_exit(self,event):
        exit()

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MyFrame,self).__init__(None, title='Rubiks')
        self.SetSize((800, 550))
        self.canvas = MyCanvas(self)
        self.panel2 =  ToolPanel(self)

        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.canvas, 1, wx.EXPAND|wx.LEFT)
        self.sizer.Add(self.panel2, 0, wx.EXPAND|wx.RIGHT)
        self.SetSizer(self.sizer)

        self.Show()


if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
