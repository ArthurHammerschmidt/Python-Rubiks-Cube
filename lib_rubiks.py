# this version ignores cubie tracking and only tracks colors
# on the base positions of the colors.


import numpy

# array of  base position indices for each face in ccw order
# positions don't change (fix for entire cube)
# corners move into positions.
# In the beginning ( or reset) all corner indices match postion indices
cbpF = [0,4,5,1]
cbpB = [2,6,7,3]
cbpL = [0,3,7,4]
cbpR = [1,5,6,2] # positions 1,5,6,2 are the corners for right face
cbpU = [0,1,2,3]
cbpD = [7,6,5,4]

ebpF = [0,4,8,5]
ebpB = [2,6,10,7]
ebpL = [3,7,11,4]
ebpR = [1,5,9,6]
ebpU = [0,1,2,3]
ebpD = [8,11,10,9]

face_rotations = 'FBUDLRfbudlr' #
Cbp = [cbpF,cbpB,cbpU,cbpD,cbpL,cbpR]
Ebp = [ebpF,ebpB,ebpU,ebpD,ebpL,ebpR]

# axis defintion FUL is XYZ , F or X or thumb pointing to your face.
# colr placement:
# F,B : X, -X : Red, Orange
# U,D : Y, -Y : Yellow, White
# L,R : Z, -Z : Green, Blue
#
face_order = [0,1,2,3,4,5]  #  [F,B,U,D,L,R] = [0,1,2,3,4,5] at start
ofi_cfi = [0,1,2,3,4,5]  #  original face_i at current face index
# eg.  ofi_cfi[2]= 5  means original face_i 5 is at current face_i 2
# [ F   B   U  D  L  R]
# [ x  -x  y  -y  z  -z] # axis direction and order
# [0   1   2   3  4   5] # index of axis direction
# each 'corner color axis' is in order in face_rotations-uppercase
# color axis direction indices match color indices originally ( in reset)
# Corner color axis (a,b,c ) keeps current locations for each corner-i : [[a,b,c]ith]
# Corner color definition keeps original orientation of corner-i and colors

# cif = color indexes of order faces (x,y,z) for the ith box
# bfc = base face colors are array of color indexes that are kept in (xyz) order
#      [  0        1        2        3        4        5        6        7   ]
Ccif = [[0,2,4], [0,2,5], [1,2,5], [1,2,4], [0,3,4], [0,3,5], [1,3,5], [1,3,4] ]
Cbfc = [[0,2,4], [0,2,5], [1,2,5], [1,2,4], [0,3,4], [0,3,5], [1,3,5], [1,3,4] ]
# Edge  color axis direction (a,b) for each edge-i : [[a,b]ith]
#     [   0     1     2     3     4     5     6     7     8     9    10    11   ]
Ecif = [ [0,2],[2,5],[1,2],[2,4],[0,4],[0,5],[1,5],[1,4],[0,3],[3,5],[1,3],[3,4] ]
Ebfc = [ [0,2],[2,5],[1,2],[2,4],[0,4],[0,5],[1,5],[1,4],[0,3],[3,5],[1,3],[3,4] ]

colors= numpy.zeros((6,3),'f')
colors[0] = 1,0,0 # red
colors[1] = 0.98,0.45,0.1  # orange
colors[2] = 0,1,0  # green
colors[3] = 0,0.3,1  # blue
colors[4] = 1,1,0  # yellow
colors[5] = 1,1,1  # white

patch = numpy.zeros((6,9,4,3),'f')
centers = numpy.zeros((6,4,3),'f')
  # 6 faces 9 patches on each face
  # 6 centers one on each face : centers[facei]

# define vertices of a patch: patch[facei][patchi][vertexi][coordinatei]
# right                        left
patch[5][0][0] = -3,-3,-3;     patch[4][0][0] = -3,-3,3
patch[5][0][1] = -1,-3,-3;     patch[4][0][1] = -1,-3,3
patch[5][0][2] = -1,-1,-3;     patch[4][0][2] = -1,-1,3
patch[5][0][3] = -3,-1,-3;     patch[4][0][3] = -3,-1,3

patch[5][1][0] = -1,-3,-3;     patch[4][1][0] = -1,-3,3;
patch[5][1][1] = 1,-3,-3;     patch[4][1][1] = 1,-3,3;
patch[5][1][2] = 1,-1,-3;     patch[4][1][2] = 1,-1,3;
patch[5][1][3] = -1,-1,-3;     patch[4][1][3] = -1,-1,3;

patch[5][2][0] = 1,-3,-3;     patch[4][2][0] = 1,-3,3;
patch[5][2][1] = 3,-3,-3;     patch[4][2][1] = 3,-3,3;
patch[5][2][2] = 3,-1,-3;     patch[4][2][2] = 3,-1,3;
patch[5][2][3] = 1,-1,-3;     patch[4][2][3] = 1,-1,3;
#
patch[5][3][0] = -3,-1,-3;     patch[4][3][0] = -3,-1,3;
patch[5][3][1] = -1,-1,-3;     patch[4][3][1] = -1,-1,3;
patch[5][3][2] = -1,1,-3;     patch[4][3][2] = -1,1,3;
patch[5][3][3] = -3,1,-3;     patch[4][3][3] = -3,1,3;

patch[5][4][0] = -1,-1,-3;     patch[4][4][0] = -1,-1,3;
patch[5][4][1] = 1,-1,-3;     patch[4][4][1] = 1,-1,3;
patch[5][4][2] = 1,1,-3;     patch[4][4][2] = 1,1,3;
patch[5][4][3] = -1,1,-3;     patch[4][4][3] = -1,1,3;

patch[5][5][0] = 1,-1,-3;     patch[4][5][0] = 1,-1,3;
patch[5][5][1] = 3,-1,-3;     patch[4][5][1] = 3,-1,3;
patch[5][5][2] = 3,1,-3;     patch[4][5][2] = 3,1,3;
patch[5][5][3] = 1,1,-3;     patch[4][5][3] = 1,1,3;
#
patch[5][6][0] = -3,1,-3;     patch[4][6][0] = -3,1,3;
patch[5][6][1] = -1,1,-3;     patch[4][6][1] = -1,1,3;
patch[5][6][2] = -1,3,-3;     patch[4][6][2] = -1,3,3;
patch[5][6][3] = -3,3,-3;     patch[4][6][3] = -3,3,3;

patch[5][7][0] = -1,1,-3;     patch[4][7][0] = -1,1,3;
patch[5][7][1] = 1,1,-3;     patch[4][7][1] = 1,1,3;
patch[5][7][2] = 1,3,-3;     patch[4][7][2] = 1,3,3;
patch[5][7][3] = -1,3,-3;     patch[4][7][3] = -1,3,3;

patch[5][8][0] = 1,1,-3;     patch[4][8][0] = 1,1,3;
patch[5][8][1] = 3,1,-3;     patch[4][8][1] = 3,1,3;
patch[5][8][2] = 3,3,-3;     patch[4][8][2] = 3,3,3;
patch[5][8][3] = 1,3,-3;     patch[4][8][3] = 1,3,3;
#
#   back                             front
patch[1][0][0] = -3,-3,-3;     patch[0][0][0] = 3,-3,-3
patch[1][0][1] = -3,-1,-3;     patch[0][0][1] = 3,-1,-3
patch[1][0][2] = -3,-1,-1;     patch[0][0][2] = 3,-1,-1
patch[1][0][3] = -3,-3,-1;     patch[0][0][3] = 3,-3,-1

patch[1][1][0] = -3,-1,-3;     patch[0][1][0] = 3,-1,-3;
patch[1][1][1] = -3,1,-3;     patch[0][1][1] = 3,1,-3;
patch[1][1][2] = -3,1,-1;     patch[0][1][2] = 3,1,-1;
patch[1][1][3] = -3,-1,-1;     patch[0][1][3] = 3,-1,-1;

patch[1][2][0] = -3,1,-3;     patch[0][2][0] = 3,1,-3;
patch[1][2][1] = -3,3,-3;     patch[0][2][1] = 3,3,-3;
patch[1][2][2] = -3,3,-1;     patch[0][2][2] = 3,3,-1;
patch[1][2][3] = -3,1,-1;     patch[0][2][3] = 3,1,-1;
#
patch[1][3][0] = -3,-3,-1;     patch[0][3][0] = 3,-3,-1;
patch[1][3][1] = -3,-1,-1;     patch[0][3][1] = 3,-1,-1;
patch[1][3][2] = -3,-1,1;     patch[0][3][2] = 3,-1,1;
patch[1][3][3] = -3,-3,1;     patch[0][3][3] = 3,-3,1;

patch[1][4][0] = -3,-1,-1;     patch[0][4][0] = 3,-1,-1;
patch[1][4][1] = -3,1,-1;     patch[0][4][1] = 3,1,-1;
patch[1][4][2] = -3,1,1;     patch[0][4][2] = 3,1,1;
patch[1][4][3] = -3,-1,1;     patch[0][4][3] = 3,-1,1;

patch[1][5][0] = -3,1,-1;     patch[0][5][0] = 3,1,-1;
patch[1][5][1] = -3,3,-1;     patch[0][5][1] = 3,3,-1;
patch[1][5][2] = -3,3,1;     patch[0][5][2] = 3,3,1;
patch[1][5][3] = -3,1,1;     patch[0][5][3] = 3,1,1;
#
patch[1][6][0] = -3,-3,1;     patch[0][6][0] = 3,-3,1;
patch[1][6][1] = -3,-1,1;     patch[0][6][1] = 3,-1,1;
patch[1][6][2] = -3,-1,3;     patch[0][6][2] = 3,-1,3;
patch[1][6][3] = -3,-3,3;     patch[0][6][3] = 3,-3,3;

patch[1][7][0] = -3,-1,1;     patch[0][7][0] = 3,-1,1;
patch[1][7][1] = -3,1,1;     patch[0][7][1] = 3,1,1;
patch[1][7][2] = -3,1,3;     patch[0][7][2] = 3,1,3;
patch[1][7][3] = -3,-1,3;     patch[0][7][3] = 3,-1,3;

patch[1][8][0] = -3,1,1;     patch[0][8][0] = 3,1,1;
patch[1][8][1] = -3,3,1;     patch[0][8][1] = 3,3,1;
patch[1][8][2] = -3,3,3;     patch[0][8][2] = 3,3,3;
patch[1][8][3] = -3,1,3;     patch[0][8][3] = 3,1,3;
#
#
#  down                               up
patch[3][0][0] = -3,-3,-3;     patch[2][0][0] = -3,3,-3
patch[3][0][1] = -3,-3,-1;     patch[2][0][1] = -3,3,-1
patch[3][0][2] = -1,-3,-1;     patch[2][0][2] = -1,3,-1
patch[3][0][3] = -1,-3,-3;     patch[2][0][3] = -1,3,-3

patch[3][1][0] = -1,-3,-3;     patch[2][1][0] = -1,3,-3;
patch[3][1][1] = -1,-3,-1;     patch[2][1][1] = -1,3,-1;
patch[3][1][2] = 1,-3,-1;     patch[2][1][2] = 1,3,-1;
patch[3][1][3] = 1,-3,-3;     patch[2][1][3] = 1,3,-3;

patch[3][2][0] = 1,-3,-3;     patch[2][2][0] = 1,3,-3;
patch[3][2][1] = 1,-3,-1;     patch[2][2][1] = 1,3,-1;
patch[3][2][2] = 3,-3,-1;     patch[2][2][2] = 3,3,-1;
patch[3][2][3] = 3,-3,-3;     patch[2][2][3] = 3,3,-3;
#
patch[3][3][0] = -3,-3,-1;     patch[2][3][0] = -3,3,-1;
patch[3][3][1] = -3,-3,1;     patch[2][3][1] = -3,3,1;
patch[3][3][2] = -1,-3,1;     patch[2][3][2] = -1,3,1;
patch[3][3][3] = -1,-3,-1;     patch[2][3][3] = -1,3,-1;

patch[3][4][0] = -1,-3,-1;     patch[2][4][0] = -1,3,-1;
patch[3][4][1] = -1,-3,1;     patch[2][4][1] = -1,3,1;
patch[3][4][2] = 1,-3,1;     patch[2][4][2] = 1,3,1;
patch[3][4][3] = 1,-3,-1;     patch[2][4][3] = 1,3,-1;

patch[3][5][0] = 1,-3,-1;     patch[2][5][0] = 1,3,-1;
patch[3][5][1] = 1,-3,1;     patch[2][5][1] = 1,3,1;
patch[3][5][2] = 3,-3,1;     patch[2][5][2] = 3,3,1;
patch[3][5][3] = 3,-3,-1;     patch[2][5][3] = 3,3,-1;
#
patch[3][6][0] = -3,-3,1;     patch[2][6][0] = -3,3,1;
patch[3][6][1] = -3,-3,3;     patch[2][6][1] = -3,3,3;
patch[3][6][2] = -1,-3,3;     patch[2][6][2] = -1,3,3;
patch[3][6][3] = -1,-3,1;     patch[2][6][3] = -1,3,1;

patch[3][7][0] = -1,-3,1;     patch[2][7][0] = -1,3,1;
patch[3][7][1] = -1,-3,3;     patch[2][7][1] = -1,3,3;
patch[3][7][2] = 1,-3,3;     patch[2][7][2] = 1,3,3;
patch[3][7][3] = 1,-3,1;     patch[2][7][3] = 1,3,1;

patch[3][8][0] = 1,-3,1;     patch[2][8][0] = 1,3,1;
patch[3][8][1] = 1,-3,3;     patch[2][8][1] = 1,3,3;
patch[3][8][2] = 3,-3,3;     patch[2][8][2] = 3,3,3;
patch[3][8][3] = 3,-3,1;     patch[2][8][3] = 3,3,1;

 # F                     #B
centers[0][0] =  3,-1,-1; centers[1][0] =  -3,-1,-1
centers[0][1] =  3,1,-1; centers[1][1] =  -3,1,-1
centers[0][2] =  3,1,1; centers[1][2] =  -3,1,1
centers[0][3] =  3,-1,1; centers[1][3] =  -3,-1,1

 # U                      #D
centers[2][0] =  -1,3,-1;  centers[3][0] =  -1,-3,-1;
centers[2][1] =  -1,3,1;  centers[3][1] =  -1,-3,1;
centers[2][2] =  1,3,1;  centers[3][2] =  1,-3,1;
centers[2][3] =  1,3,-1;  centers[3][3] =  1,-3,-1;

#L                        #R
centers[4][0] =  -1,-1,3;  centers[5][0] =  -1,-1,-3
centers[4][1] =  1,-1,3;  centers[5][1] =  1,-1,-3
centers[4][2] =  1,1,3;  centers[5][2] =  1,1,-3
centers[4][3] =  -1,1,3;  centers[5][3] =  -1,1,-3

op = numpy.zeros((6,4,3),'f') # open points under face layer
 # F                     #B
op[0][0] =  1,-3,-3; op[1][0] =  -1,-3,-3
op[0][1] =  1,3,-3; op[1][1] =  -1,3,-3
op[0][2] =  1,3,3; op[1][2] =  -1,3,3
op[0][3] =  1,-3,3; op[1][3] =  -1,-3,3

 # U                      #D
op[2][0] =  -3,1,-3;  op[3][0] =  -3,-1,-3;
op[2][1] =  -3,1,3;  op[3][1] =  -3,-1,3;
op[2][2] =  3,1,3;  op[3][2] =  3,-1,3;
op[2][3] =  3,1,-3;  op[3][3] =  3,-1,-3;

#L                        #R
op[4][0] =  -3,-3,1;  op[5][0] =  -3,-3,-1
op[4][1] =  3,-3,1;  op[5][1] =  3,-3,-1
op[4][2] =  3,3,1;  op[5][2] =  3,3,-1
op[4][3] =  -3,3,1;  op[5][3] =  -3,3,-1



# define patch connection to corner and edge cubies indices
# using face index and patch index
# Cfp[cubei] = ( (facei,patchi) matching color in x direction of cubei,
#                (facei,patchi) matching color in y direction of cubei,
#                (facei,patchi)) matching color in z direction of cubei
Cfp = ( ((0,8),(2,8),(4,8)),
        ((0,2),(2,2),(5,8)),
        ((1,2),(2,0),(5,6)),
        ((1,8),(2,6),(4,6)),
        ((0,6),(3,8),(4,2)),
        ((0,0),(3,2),(5,2)),
        ((1,0),(3,0),(5,0)),
        ((1,6),(3,6),(4,0))
        )
Efp = (((0,5),(2,5)),
        ((2,1),(5,7)),
        ((1,5),(2,3)),
        ((2,7),(4,7)),
        ((0,7),(4,5)),
        ((0,1),(5,5)),
        ((1,1),(5,3)),
        ((1,7),(4,3)),
        ((0,3),(3,5)),
        ((3,1),(5,1)),
        ((1,3),(3,3)),
        ((3,7),(4,1))
        )


#########################################################################
# functions
#########################################################################
def reset_colors():
    for ic in range(8):
        for k in [0,1,2]:
            Ccif[ic][k] = Cbfc[ic][k]
    for ie in range(12):
        for k in [0,1]:
            Ecif[ie][k] = Ebfc[ie][k]
    return

# rotate_about_ax(c,axn)
# holds color item of index axn and swaps other two.
# ([0,4,2],0) -> [0,2,4]
# ([0,4,2],1) -> [2,4,0]
# ([0,4,2],2) -> [4,0,2]
def rotate_about_ax(c,axn):
    b = []
    for i in (0,1,2):
        if i != axn : b.append(c[i])
    # swap
    t = b[0]
    b[0] = b[1]
    b[1] = t
    b.insert(axn,c[axn])
    return b

def swap4list(l,axn):
    b = []
    for k in [0,1,2,3]:
        c = []
        if axn == 1 : # swap
            c.append(l[k][1])
            c.append(l[k][0])
        else:  # copy
            c.append(l[k][0])
            c.append(l[k][1])
        b.append(c)
    return b

def face_rotate(rot):
    face, turn ,axn = rot_parms(rot)

    if turn == -1 :  # upper case : 0 to 5: cw
        corner_cw_rotate(axn,Cbp[face])
        edge_cw_rotate(axn,Ebp[face])
    else:        # lower case : 6 to 11 : ccw
        corner_ccw_rotate(axn,Cbp[face])
        edge_ccw_rotate(axn,Ebp[face])

def corner_ccw_rotate(axn,bp): #

    # get new color orientation for the corner
    # get colors of ith box
    col = []
    for i in [0,1,2,3]:
        col.append(Ccif[bp[i]])
    # rotate them
    for i in [0,1,2,3]: col[i] = rotate_about_ax(col[i],axn)
    #left shift put back colors into ith box
    for i in [0,1,2,3]:
        k = (i+1)%4
        for j in [0,1,2]:
            Ccif[bp[k]][j] = col[i][j]

    return

def corner_cw_rotate(axn,bp): #

    # get new color orientation for the corner
    # get colors of ith box
    col = []
    for i in [0,1,2,3]:
        col.append(Ccif[bp[i]])
    # rotate them
    for i in [0,1,2,3]: col[i] = rotate_about_ax(col[i],axn)
    #left shift put back colors into ith box
    for i in [0,1,2,3]:
        k = (i-1)%4
        for j in [0,1,2]:
            Ccif[bp[k]][j] = col[i][j]
    #print 'Ccif in fn ',Ccif
    return

def edge_ccw_rotate(axn,bp): #
    # get new color orientation for the corner
    # get colors of ith box
    #print 'inside edge_ccw_rotate'
    col = []
    for i in [0,1,2,3]:
        col.append(Ecif[bp[i]])
    col2 = swap4list(col,axn)
    #left shift put back colors into ith box
    for i in [0,1,2,3]:
        k = (i+1)%4
        for j in [0,1]:
            Ecif[bp[k]][j] = col2[i][j]

    return

def edge_cw_rotate(axn,bp): #
    # get new color orientation for the corner
    # get colors of ith box
    #print 'inside edge_cw_rotate'
    col = []
    for i in [0,1,2,3]:
        col.append(Ecif[bp[i]])
    col2 = swap4list(col,axn)
    #print 'col  ',col
    #print 'col2 ',col2
    #left shift put back colors into ith box
    for i in [0,1,2,3]:
        k = (i-1)%4
        for j in [0,1]:
            Ecif[bp[k]][j] = col2[i][j]
    #print 'ecif in fn: ',Ecif

    return

# rotate_swap face_order list
# about face pair 0,1,2 and about pair 0,1
def rot_swap_facelist(flist,axis,ap):
    nflist = [0,1,2,3,4,5]
    pair = [0,0]
    l0 = (flist[0], flist[1]) # (0,1)
    l1 = (flist[2], flist[3]) # (2,3)
    l2 = (flist[4], flist[5]) # (4,5)
#    print 'flist,afp,ap ',flist,axis,ap
    if axis ==0 :
        pair[0],pair[1]= swap2itemlist([l1,l2])
#        print 'p0 p1 ',pair[0],pair[1]
        if ap == 0:
            item0,item1 = swap2itemlist(pair[0])
#            print 'i0 i1',item0,item1
            nflist = [l0[0],l0[1],item0,item1,pair[1][0],pair[1][1]]
        else:
            item0,item1 = swap2itemlist(pair[1])
#            print 'i0 i1',item0,item1
            nflist = [l0[0],l0[1],pair[0][0],pair[0][1],item0,item1]
    elif axis ==1 :
        pair[0],pair[1]= swap2itemlist([l0,l2])
        if ap == 0:
            item0,item1 = swap2itemlist(pair[0])
            nflist = [item0,item1,l1[0],l1[1],pair[1][0],pair[1][1]]
        else:
            item0,item1 = swap2itemlist(pair[1])
            nflist = [pair[0][0],pair[0][1],l1[0],l1[1],item0,item1]
    elif axis ==2 :
        pair[0],pair[1]= swap2itemlist([l0,l1])
        if ap == 0:
            item0,item1 = swap2itemlist(pair[0])
            nflist = [item0,item1,pair[1][0],pair[1][1],l2[0],l2[1]]
        else:
            item0,item1 = swap2itemlist(pair[1])
            nflist = [pair[0][0],pair[0][1],item0,item1,l2[0],l2[1]]

    for i in face_order:
        ofi_cfi[i]= nflist[i] # redefine face locations
#    print ofi_cfi

    return

# return parameters in terms of desired rot
def rot_parms_request(rot):
    ri = face_rotations.find(rot)
    face = ri
    if ri > 5 : face = ri-6
    turn = -1 # matches angle value : cw
    if rot.islower() : turn = 1 # matches angle rotation ccw
    axn = None


    if face == 0 or face == 1: axn = 0
    elif face == 2 or face == 3: axn = 1
    elif face == 4 or face == 5: axn = 2
#    print ' requested:rot face cw axis ',rot,face,turn,axn
    return face,turn,axn

# return parameters in terms of original fixed cube
def rot_parms(rot):
    ri = face_rotations.find(rot)
    face = ri
    if ri > 5 : face = ri-6
    turn = -1 # matches angle value : cw
    if rot.islower() : turn = 1 # matches angle rotation ccw
    axn = None
    face = ofi_cfi[face]

    if face == 0 or face == 1: axn = 0
    elif face == 2 or face == 3: axn = 1
    elif face == 4 or face == 5: axn = 2
#    print ' history:rot face cw axis ',rot,face,turn,axn
    return face,turn,axn

def swap2itemlist(ilist):
    nlist = []
    nlist.append(ilist[1])
    nlist.append(ilist[0])
    return nlist[0],nlist[1]

def rotate_cube(rot):
    ri = face_rotations.find(rot)
    facei, turn,axis = rot_parms_request(rot)
#    print ' facei, turn,axis ri',facei, turn,axis,ri
    ap = [1,0, 0,1, 1,0,    0,1, 1,0, 0,1] # upper case FBUDLR

    rot_swap_facelist(ofi_cfi,axis,ap[ri])
    return
