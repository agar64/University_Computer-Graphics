import os
import pygame as pg
import numpy
import imageio as iio
import time

main_dir = os.path.split(os.path.abspath('__file__'))[0]
data_dir = os.path.join(main_dir, "data")

pg.init()
screen = pg.display.set_mode((800, 600), pg.SCALED)
pg.display.set_caption("Burenyu")
m = numpy.zeros((800, 600, 3), dtype=numpy.uint8)

def draw():
    pg.surfarray.blit_array(screen, m)
    pg.display.update()


def clearS():
    m[:,:,:] = 0


def createImg(lenght, height, color):
    m = numpy.copy(numpy.zeros((lenght, height, color), dtype=numpy.uint8))


def setPixel(matrix, x, y, R, G, B):
    if(x >= matrix.shape[0]):
        x = matrix.shape[0]-1
    if(x < 0):
        x = 0
    if(y >= matrix.shape[1]):
        y = matrix.shape[1]-1
    if(y < 0):
        y = 0
    matrix[x,y] = [R, G, B]
    return matrix


def DDA(buf, xi, yi, xf, yf, R, G, B):
    dx = xf-xi
    dy = yf - yi
    step = numpy.absolute(dx)
    if(numpy.absolute(dy) >  numpy.absolute(dx)):
        step = numpy.absolute(dy)
    
    if(step == 0):
        buf = setPixel(buf, xi, yi, R, G, B)
        return buf
    
    stepx = dx/step
    stepy = dy/step
    
    for i in range(0, step):
        x = round(xi + i*stepx)
        y = round(yi + i*stepy)
        buf = setPixel(buf, x, y, R, G, B)
    return buf

def checkLine():
    for i in range(-400, 400):
        m = bres6(m, 500, 500, 900, 500+i, 255, 255, 255)
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        draw()
    for i in range(400, -400, -1):
        m = bres6(m, 500, 500, 500+i, 900, 255, 0, 0)
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        draw()
    for i in range(400, -400, -1):
        m = bres6(m, 500, 500, 100, 500+i, 0, 255, 0)
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        draw()
    for i in range(-400, 400):
        m = bres6(m, 500, 500, 500+i, 100, 0, 0, 255)
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        draw()


def bres6(buf, xi, yi, xf, yf, R, G, B):
    dx = numpy.absolute(xf - xi)
    dy = numpy.absolute(yf - yi)
    x = round(xi)
    y = round(yi)

    gradient = dy/float(dx)

    if gradient > 1:
        dx, dy = dy, dx
        x, y = y, x
        xi, yi = yi, xi
        xf, yf = yf, xf
    
    dx2 = 2*dx
    dy2 = 2*dy
    
    p = -dx + dy2
    
    for i in range (0, dx):
        if(gradient <= 1):
            buf = setPixel(buf, x, y, R, G, B)
        else:
            buf = setPixel(buf, y, x, R, G, B)
        x = x + 1 if x < xf else x - 1
        if(p >= 0):
            y = y + 1 if y < yf else y - 1
            p = p - dx2 + dy2
        else:
            p = p + dy2
    return buf


def circ(buf, cx, cy, r, R, G, B):
    x = 0
    y = r
    p = 3 - 2*r
    buf = setPixel(buf, cx+x, cy+y, R, G, B)
    buf = setPixel(buf, cx+y, cy+x, R, G, B)
    buf = setPixel(buf, cx+y, cy-x, R, G, B)
    buf = setPixel(buf, cx+x, cy-y, R, G, B)
    buf = setPixel(buf, cx-x, cy-y, R, G, B)
    buf = setPixel(buf, cx-y, cy-x, R, G, B)
    buf = setPixel(buf, cx-y, cy+x, R, G, B)
    buf = setPixel(buf, cx-x, cy+y, R, G, B)

    while x < y:
        if p < 0:
            p += 4 * x + 6
        else:
            p += 4 * (x - y) + 10
            y = y - 1
        x = x + 1
        buf = setPixel(buf, cx+x, cy+y, R, G, B)
        buf = setPixel(buf, cx+y, cy+x, R, G, B)
        buf = setPixel(buf, cx+y, cy-x, R, G, B)
        buf = setPixel(buf, cx+x, cy-y, R, G, B)
        buf = setPixel(buf, cx-x, cy-y, R, G, B)
        buf = setPixel(buf, cx-y, cy-x, R, G, B)
        buf = setPixel(buf, cx-y, cy+x, R, G, B)
        buf = setPixel(buf, cx-x, cy+y, R, G, B)
    return buf


def elp(buf, cx, cy, r1, r2, R, G, B):
    x = 0
    y = r2
    px = 0
    py = 2*r1*r1*y
    buf = setPixel(buf, cx+x, cy+y, R, G, B)
    buf = setPixel(buf, cx-x, cy+y, R, G, B)
    buf = setPixel(buf, cx+x, cy-y, R, G, B)
    buf = setPixel(buf, cx-x, cy-y, R, G, B)
    
    p = round(r2*r2 - r1*r1*r2 + 0.25*r1*r1)
    while(px < py):
        x += 1
        px += 2*r2*r2
        if(p < 0):
            p += r2*r2 + px
        else:
            y -= 1
            py -= 2*r1*r1
            p += r2*r2 + px - py
        buf = setPixel(buf, cx+x, cy+y, R, G, B)
        buf = setPixel(buf, cx-x, cy+y, R, G, B)
        buf = setPixel(buf, cx+x, cy-y, R, G, B)
        buf = setPixel(buf, cx-x, cy-y, R, G, B)
    while(y > 0):
        y -= 1
        py -= 2*r1*r1
        if(p > 0):
            p += r1*r1 - py
        else:
            x += 1
            px += 2*r2*r2
            p += r1*r1 - py + px
        buf = setPixel(buf, cx+x, cy+y, R, G, B)
        buf = setPixel(buf, cx-x, cy+y, R, G, B)
        buf = setPixel(buf, cx+x, cy-y, R, G, B)
        buf = setPixel(buf, cx-x, cy-y, R, G, B)
    return buf
    

def getPixel(tex, x, y):
    if(x > 1):
        x = 1
    if(x < 0):
        x = 0
    if(y > 1):
        y = 1
    if(y < 0):
        y = 0
    
    x = int(x*(len(tex[0])-1))
    y = int(y*(len(tex)-1))
    color = tex[y, x]
    return color


def validCoord(buf, x, y):
    if x < 0 or y < 0:
        return 0
    if x >= buf.shape[0] or y >= buf.shape[1]:
        return 0
    return 1


def floodFillIt(buf, X, Y, color):
    # Visiting array
    vis = numpy.zeros((buf.shape[0], buf.shape[1]), dtype=numpy.uint8)
     
    # Creating queue for bfs
    obj = []
     
    # Pushing pair of {x, y}
    obj.append([X, Y])
     
    # Marking {x, y} as visited
    vis[X][Y] = 1
    
    iDraw = 0
    # Until queue is empty
    while len(obj) > 0:
        iDraw += 1
        if(iDraw%1000 == 0):
            # Updating the screen
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit
            draw()
        
        # Extracting front pair
        coord = obj[0]
        x = coord[0]
        y = coord[1]
        preColor = numpy.copy(buf[x][y])
   
        buf[x][y] =  numpy.copy(color)

       
        # Popping front pair of queue
        obj.pop(0)

        # For Upside Pixel or Cell
        if validCoord(buf, x + 1, y) == 1 and vis[x + 1][y] == 0 and numpy.array_equal(buf[x + 1][y], preColor):
            obj.append([x + 1, y])
            vis[x + 1][y] = 1
       
        # For Downside Pixel or Cell
        if validCoord(buf, x - 1, y) == 1 and vis[x - 1][y] == 0 and numpy.array_equal(buf[x - 1][y], preColor):
            obj.append([x - 1, y])
            vis[x - 1][y] = 1
       
        # For Right side Pixel or Cell
        if validCoord(buf, x, y + 1) == 1 and vis[x][y + 1] == 0 and numpy.array_equal(buf[x][y + 1], preColor):
            obj.append([x, y + 1])
            vis[x][y + 1] = 1
       
        # For Left side Pixel or Cell
        if validCoord(buf, x, y - 1) == 1 and vis[x][y - 1] == 0 and numpy.array_equal(buf[x][y - 1], preColor):
            obj.append([x, y - 1])
            vis[x][y - 1] = 1
    draw()


def floodFillFast(buf, x, y, color):
    preColor = numpy.copy(buf[x][y])
    if(numpy.array_equal(color, preColor)):
        return buf
    #if not Inside(x, y) then return
    if(not inside(buf, x, y, preColor)):
        return buf
    #let s = new empty queue or stack
    s = []
    #Add (x, x, y, 1) to s
    s.append([x, x, y, 1])
    #Add (x, x, y - 1, -1) to s
    s.append([x, x, y - 1, -1])
    #while s is not empty:
    iDraw = 0
    while(s):
        #Update Screen
        iDraw += 1
        if(iDraw%20 == 0):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit
            draw()
        #Remove an (x1, x2, y, dy) from s
        [x1, x2, y, dy] = s.pop(0)
        x = x1
        if(inside(buf, x, y, preColor)):
            while(inside(buf, x - 1, y, preColor)):
                buf = setPixel(buf, x - 1, y, color[0], color[1], color[2])
                x = x - 1
        if(x < x1):
            #Add (x, x1-1, y-dy, -dy) to s
            s.append([x, x1-1, y-dy, -dy])
        while(x1 <= x2):
            while(inside(buf, x1, y, preColor)):
                buf = setPixel(buf, x1, y, color[0], color[1], color[2])
                x1 = x1 + 1
            #Add (x, x1 - 1, y+dy, dy) to s
            s.append([x, x1 - 1, y+dy, dy])
            if(x1 - 1 > x2):
                #Add (x2 + 1, x1 - 1, y-dy, -dy) to s
                s.append([x2 + 1, x1 - 1, y-dy, -dy])
            x1 = x1 + 1
            while((x1 < x2) and not (inside(buf, x1, y, preColor))):
                x1 = x1 + 1
            x = x1
    draw()


def inside(buf, x, y, preColor):
    if x < 0 or y < 0:
        return 0
    if x >= buf.shape[0] or y >= buf.shape[1]:
        return 0
    if not numpy.array_equal(buf[x, y], preColor) :
        return 0
    return 1


def createPoli():
    p = []
    return p


def addPoint(poli, point):
    poli.append(point)


def drawPoli(buf, poli, color):
    x = poli[0][0]
    y = poli[0][1]
    for i in range(1, len(poli)):
        buf = bres6(buf, x, y, poli[i][0], poli[i][1], color[0], color[1], color[2])
        x = poli[i][0]
        y = poli[i][1]
    buf = bres6(buf, x, y, poli[0][0], poli[0][1], color[0], color[1], color[2])
    return buf


def scanLine(buf, poli, tex):
    data = numpy.array(poli)
    ymin = int(min(data[:, 1]))
    ymax = int(max(data[:, 1]))
    
    for y in range(ymin, ymax):
        i = []
        pi = data[0]
        
        for p in range(1, len(poli)):
            pf = data[p, :]
            
            pInt = lineInterTex(y, [pi, pf])
            
            if(pInt[0] >= 0):
                if(i == []):
                    i = pInt
                else:
                    i = [i, pInt]
            pi = pf
        
        pf = data[0, :]
        
        pInt = lineInterTex(y, [pi, pf])
        
        if(pInt[0] >= 0):
            if(i == []):
                i = pInt
            else:
                i = [i, pInt]
        
        for pi in range(0, len(i), 2):
            p1 = i[pi]
            p2 = i[pi + 1]
            
            x1 = p1[0]
            x2 = p2[0]
            
            if(x2 < x1):
                p1, p2 = p2, p1
            
            for xk in range(int((p1[0])), int(p2[0])):
                if(p2[0] != p1[0]):
                    pc = (xk - p1[0])/(p2[0] - p1[0])
                else:
                    pc = 0
                tx = p1[2] + pc*(p2[2] - p1[2])
                ty = p1[3] + pc*(p2[3] - p1[3])
                
                color = getPixel(tex, tx, ty)
                
                buf = setPixel(buf, xk, y, color[0], color[1], color[2])
    draw()


def lineInterTex(scan, seg):
    #print("seg = ", seg)
    #appendix = numpy.array([0, 0])
    pi = seg[0]
    #pi = numpy.append(pi, appendix)
    #print("pi = ", pi)

    pf = seg[1]
    #pf = numpy.append(pf, appendix)
    #print("pf = ", pf)

    y = scan

    #horizontal seg has no intersections
    if(pi[1] == pf[1]):
        p = [-1, 0, 0, 0]
        return p
    #swap to ensure initial point
    if(pi[1] > pf[1]):
        pi, pf = pf, pi
    
    #compute t
    t = (y - pi[1])/(pf[1] - pi[1])
    
    #print("2nd pi = ", pi)
    #print("2nd pf = ", pf)
    #compute x
    if((t > 0) and (t <= 1)):
        x = pi[0] + t*(pf[0] - pi[0])
        tx = pi[2] + t*(pf[2] - pi[2])
        ty = pi[3] + t*(pf[3] - pi[3])
        
        p = [x, y, tx, ty]
        return p
    
    #no intersections
    p = [-1, 0, 0, 0]
    return p


def createTransf():
    matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    matrix = numpy.copy(matrix)
    return matrix


def makeTranslation(matrix, tx, ty):
    matrixT = numpy.matmul([[1, 0, tx], [0, 1, ty], [0, 0, 1]], matrix)
    return matrixT


def makeScale(matrix, sx, sy):
    matrixS = numpy.matmul([[sx, 0, 0], [0, sy, 0], [0, 0, 1]], matrix)
    return matrixS


def doRotation(matrix, ang):
    ang = ang*numpy.pi/180
    matrixR = numpy.copy([[numpy.cos(ang), -numpy.sin(ang), 0], [numpy.sin(ang), numpy.cos(ang), 0], [0, 0, 1]])
    return matrixR


def applyTransform(poli, matrix):
    pol = numpy.copy(poli)
    for i in range(0, (len(poli))):
        pt = numpy.append(pol[i, 0:2], 1)
        pt = numpy.transpose(numpy.atleast_2d(pt))
        
        pt = numpy.matmul(matrix, pt)
        
        pt = numpy.transpose(pt)
        pol[i, 0:2] = numpy.int32(pt[0, 0:2])
    return pol


def animWin():
    view = [1280, 960]
    win = [0, 0, 1279, 959]
    for i in range(0, 1):
        poliNewRot5 = applyTransform(poliNew, matRot5Final)
        for j in range(0, 71):
            poliNewRot5 = applyTransform(poliNewRot5, matRot5Final)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit
            clearS()
            pv = mapWindow(poliNewRot5, win, view)
            scanLine(m, pv, neco)


def mapWindow(poli, win, view):
    lv = view[0]
    av = view[1]
    xi = win[0]
    yi = win[1]
    xf = win[2]
    yf = win[3]
    
    mat = [[(lv/(xf-xi)), 0, (1 - xi*lv/(xf-xi))], [0, (av/(yf-yi)), (1 - yi*av/(yf-yi))], [0, 0, 1]]
    
    poli = applyTransform(poli, mat)
    
    return poli


#criar polígono com R, G, B ao invés de coordenadas de textura com o mesmo algoritmo de criação de polígono pra usar o scanLineCol
def scanLineCol(buf, poli):
    data = numpy.array(poli)
    ymin = int(min(data[:, 1]))
    ymax = int(max(data[:, 1]))
    
    for y in range(ymin, ymax):
        i = []
        pi = data[0]
        
        for p in range(1, len(poli)):
            pf = data[p, :]
            
            pInt = lineInterCol(y, [pi, pf])
            
            if(pInt[0] >= 0):
                if(i == []):
                    i = pInt
                else:
                    i = [i, pInt]
            pi = pf
        
        pf = data[0, :]
        
        pInt = lineInterCol(y, [pi, pf])
        
        if(pInt[0] >= 0):
            if(i == []):
                i = pInt
            else:
                i = [i, pInt]
        
        for pi in range(0, len(i), 2):
            p1 = i[pi]
            p2 = i[pi + 1]
            
            x1 = p1[0]
            x2 = p2[0]
            
            if(x2 < x1):
                p1, p2 = p2, p1
            
            for xk in range(int((p1[0])), int(p2[0])):
                if(p2[0] != p1[0]):
                    pc = (xk - p1[0])/(p2[0] - p1[0])
                else:
                    pc = 0
                R = p1[2] + pc*(p2[2] - p1[2])
                G = p1[3] + pc*(p2[3] - p1[3])
                B = p1[4] + pc*(p2[4] - p1[4])
                
                buf = setPixel(buf, xk, y, R, G, B)
    draw()

def lineInterCol(scan, seg):

    pi = seg[0]

    pf = seg[1]

    y = scan

    #horizontal seg has no intersections
    if(pi[1] == pf[1]):
        p = [-1, 0, 0, 0, 0]
        return p
    #swap to ensure initial point
    if(pi[1] > pf[1]):
        pi, pf = pf, pi
    
    #compute t
    t = (y - pi[1])/(pf[1] - pi[1])
    
    #compute x
    if((t > 0) and (t <= 1)):
        x = pi[0] + t*(pf[0] - pi[0])
        tx = pi[2] + t*(pf[2] - pi[2])
        ty = pi[3] + t*(pf[3] - pi[3])
        tz = pi[4] + t*(pf[4] - pi[4])
        
        p = [x, y, tx, ty, tz]
        return p
    
    #no intersections
    p = [-1, 0, 0, 0, 0]
    return p

def poliTri():
    poliColor = createPoli()
    addPoint(poliColor, [400, 150, 255, 0, 0])
    addPoint(poliColor, [550, 450, 0, 255, 0])
    addPoint(poliColor, [250, 450, 0, 0, 255])
    for i in range(0, 511):
        p1 = 255 - i
        if p1 < 0: p1 = 0
        p3 = -255 + i
        if p3 < 0: p3 = 0
        if p3 > 255: p3 = 255
        p2 = 0 + i
        if p2 < 0: p2 = 0
        if p2 > 255: p2 = 255 - p3
        poliColor[0][2:5] = [p1, p2, p3]
        poliColor[1][2:5] = [p3, p1, p2]
        poliColor[2][2:5] = [p2, p3, p1]
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
        pv = mapWindow(poliColor, win, view)
        scanLineCol(m, pv)

def doRotationOnOrigin(poli, matrix, ang):
    data = numpy.array(poli)
    xmin = min(data[:, 0])
    xmax = max(data[:, 0])
    ymin = min(data[:, 1])
    ymax = max(data[:, 1])
    
    x = xmin + int((xmax-xmin)/2)
    y = ymin + int((ymax-ymin)/2)
    
    toOrigin = makeTranslation(matrix, -x, -y)
    matRot = doRotation(matrix, ang)
    backFromOrigin = makeTranslation(matrix, x, y)
    
    matrixFinal = numpy.matmul(backFromOrigin, numpy.matmul(matRot, toOrigin))
    
    return matrixFinal

#### Action
#load and play music
pg.mixer.music.load(r'assets\theme.mp3')
pg.mixer.music.set_volume(0.75)
pg.mixer.music.play()

#load images
neco = iio.imread(r'assets\neco.png')
cRika = iio.imread(r'assets\Chinese Rika.png')
arc = iio.imread(r'assets\arc_edgy.png')
necoOG = iio.imread(r'assets\neco_arc_og.png')
rika = iio.imread(r'assets\rika.png')
catRika = iio.imread(r'assets\rika_cat.png')
helloArc = iio.imread(r'assets\hello_arc.jpg')
helloRika = iio.imread(r'assets\hello_rika.jpg')
mensagem = iio.imread(r'assets\mensagem.png')

#drawing N
m = bres6(m, 132, 47, 132, 128, 255, 255, 255)
m = bres6(m, 132, 128, 143, 128, 255, 255, 255)
m = bres6(m, 143, 128, 143, 59, 255, 255, 255)
m = bres6(m, 143, 59, 179, 127, 255, 255, 255)
m = bres6(m, 179, 127, 193, 127, 255, 255, 255)
m = bres6(m, 193, 127, 193, 47, 255, 255, 255)
m = bres6(m, 193, 47, 183, 47, 255, 255, 255)
m = bres6(m, 183, 47, 183, 114, 255, 255, 255)
m = bres6(m, 183, 114, 148, 47, 255, 255, 255)
m = bres6(m, 148, 47, 132, 47, 255, 255, 255)
floodFillIt(m, 134, 49, [255, 0, 0])
draw()

#drawing E

m = bres6(m, 215, 47, 215, 127, 255, 255, 255)
m = bres6(m, 215, 127, 260, 127, 255, 255, 255)
m = bres6(m, 260, 127, 260, 119, 255, 255, 255)
m = bres6(m, 260, 119, 225, 119, 255, 255, 255)
m = bres6(m, 225, 119, 225, 89, 255, 255, 255)
m = bres6(m, 225, 89, 254, 89, 255, 255, 255)
m = bres6(m, 254, 89, 254, 81, 255, 255, 255)
m = bres6(m, 254, 81, 225, 81, 255, 255, 255)
m = bres6(m, 225, 81, 225, 55, 255, 255, 255)
m = bres6(m, 225, 55, 259, 55, 255, 255, 255)
m = bres6(m, 259, 55, 259, 47, 255, 255, 255)
m = bres6(m, 259, 47, 215, 47, 255, 255, 255)
floodFillIt(m, 217, 49, [255, 255, 0])
draw()

#drawing C

m = elp(m, 307, 88, 36, 43, 255, 255, 255)
for i in range(330, 370):
    m = bres6(m, i, 50, i, 125, 0, 0, 0)
m = elp(m, 307, 88, 25, 34, 255, 255, 255)
for i in range(320, 350):
    m = bres6(m, i, 65, i, 115, 0, 0, 0)
m = bres6(m, 324, 64, 329, 54, 255, 255, 255)
m = bres6(m, 321, 115, 329, 122, 255, 255, 255)
floodFillIt(m, 273, 88, [255, 0, 255])
draw()

#drawing O

#m = elp(m, 375, 88, 36, 43, 255, 255, 255)
#m = elp(m, 307, 88, 25, 34, 255, 255, 255)
m = circ(m, 373, 88, 43, 255, 255, 255)
m = circ(m, 373, 88, 33, 255, 255, 255)
floodFillIt(m, 335, 88, [0, 255, 255])
draw()

#drawing -
m = bres6(m, 422, 92, 422, 100, 255, 255, 255)
m = bres6(m, 422, 100, 451, 100, 255, 255, 255)
m = bres6(m, 451, 100, 451, 92, 255, 255, 255)
m = bres6(m, 451, 92, 422, 92, 255, 255, 255)
floodFillIt(m, 424, 94, [255, 255, 255])
draw()

#drawing A
m = bres6(m, 487, 47, 458, 127, 255, 255, 255)
m = bres6(m, 458, 127, 468, 127, 255, 255, 255)
m = bres6(m, 468, 127, 476, 106, 255, 255, 255)
m = bres6(m, 476, 106, 509, 106, 255, 255, 255)
m = bres6(m, 509, 106, 517, 127, 255, 255, 255)
m = bres6(m, 517, 127, 528, 127, 255, 255, 255)
m = bres6(m, 528, 127, 500, 47, 255, 255, 255)
m = bres6(m, 500, 47, 487, 47, 255, 255, 255)

m = bres6(m, 478, 98, 507, 98, 255, 255, 255)
m = bres6(m, 507, 98, 493, 57, 255, 255, 255)
m = bres6(m, 493, 57, 478, 98, 255, 255, 255)
floodFillIt(m, 489, 49, [0, 255, 0])
draw()

#drawing R
m = bres6(m, 541, 47, 541, 127, 255, 255, 255)
m = bres6(m, 541, 127, 551, 127, 255, 255, 255)
m = bres6(m, 551, 127, 551, 91, 255, 255, 255)
m = bres6(m, 551, 91, 568, 91, 255, 255, 255)
m = bres6(m, 568, 91, 585, 127, 255, 255, 255)
m = bres6(m, 585, 127, 595, 127, 255, 255, 255)
m = bres6(m, 595, 127, 576, 88, 255, 255, 255)
m = bres6(m, 576, 88, 585, 81, 255, 255, 255)
m = bres6(m, 585, 81, 589, 74, 255, 255, 255)
m = bres6(m, 589, 74, 589, 61, 255, 255, 255)
m = bres6(m, 589, 61, 583, 52, 255, 255, 255)
m = bres6(m, 583, 52, 572, 47, 255, 255, 255)
m = bres6(m, 572, 47, 541, 47, 255, 255, 255)

m = bres6(m, 551, 55, 551, 83, 255, 255, 255)
m = bres6(m, 551, 83, 569, 83, 255, 255, 255)
m = bres6(m, 569, 83, 579, 75, 255, 255, 255)
m = bres6(m, 579, 75, 579, 64, 255, 255, 255)
m = bres6(m, 579, 64, 570, 55, 255, 255, 255)
m = bres6(m, 570, 55, 551, 55, 255, 255, 255)
floodFillIt(m, 543, 49, [0, 0, 255])
draw()

#drawing C
m = elp(m, 643, 88, 36, 43, 255, 255, 255)
for i in range(666, 696):
    m = bres6(m, i, 50, i, 125, 0, 0, 0)
m = elp(m, 643, 88, 25, 34, 255, 255, 255)
for i in range(656, 686):
    m = bres6(m, i, 65, i, 115, 0, 0, 0)
m = bres6(m, 660, 64, 665, 54, 255, 255, 255)
m = bres6(m, 657, 115, 665, 122, 255, 255, 255)
floodFillIt(m, 609, 88, [128, 0, 128])
draw()

#drawing A
m = bres6(m, 342, 148, 313, 228, 255, 255, 255)
m = bres6(m, 313, 228, 323, 228, 255, 255, 255)
m = bres6(m, 323, 228, 331, 207, 255, 255, 255)
m = bres6(m, 331, 207, 364, 207, 255, 255, 255)
m = bres6(m, 364, 207, 372, 228, 255, 255, 255)
m = bres6(m, 372, 228, 383, 228, 255, 255, 255)
m = bres6(m, 383, 228, 355, 148, 255, 255, 255)
m = bres6(m, 355, 148, 342, 148, 255, 255, 255)

m = bres6(m, 333, 199, 362, 199, 255, 255, 255)
m = bres6(m, 362, 199, 348, 158, 255, 255, 255)
m = bres6(m, 348, 158, 333, 199, 255, 255, 255)
floodFillIt(m, 344, 150, [148, 65, 118])
draw()

#drawing D
m = bres6(m, 396, 148, 396, 228, 255, 255, 255)
m = bres6(m, 396, 228, 428, 228, 255, 255, 255)
m = bres6(m, 428, 228, 444, 221, 255, 255, 255)
m = bres6(m, 444, 221, 453, 210, 255, 255, 255)
m = bres6(m, 453, 210, 457, 198, 255, 255, 255)
m = bres6(m, 457, 198, 457, 176, 255, 255, 255)
m = bres6(m, 457, 176, 451, 162, 255, 255, 255)
m = bres6(m, 451, 162, 441, 153, 255, 255, 255)
m = bres6(m, 441, 153, 428, 148, 255, 255, 255)
m = bres6(m, 428, 148, 396, 148, 255, 255, 255)

m = bres6(m, 406, 156, 406, 220, 255, 255, 255)
m = bres6(m, 406, 220, 426, 220, 255, 255, 255)
m = bres6(m, 426, 220, 440, 213, 255, 255, 255)
m = bres6(m, 440, 213, 447, 200, 255, 255, 255)
m = bres6(m, 447, 200, 447, 178, 255, 255, 255)
m = bres6(m, 447, 178, 440, 164, 255, 255, 255)
m = bres6(m, 440, 164, 426, 156, 255, 255, 255)
m = bres6(m, 426, 156, 406, 156, 255, 255, 255)
floodFillIt(m, 398, 150, [99, 198, 158])
draw()

#drawing V
m = bres6(m, 465, 148, 493, 228, 255, 255, 255)
m = bres6(m, 493, 228, 505, 228, 255, 255, 255)
m = bres6(m, 505, 228, 533, 148, 255, 255, 255)
m = bres6(m, 533, 148, 523, 148, 255, 255, 255)
m = bres6(m, 523, 148, 500, 218, 255, 255, 255)
m = bres6(m, 500, 218, 475, 148, 255, 255, 255)
m = bres6(m, 475, 148, 465, 148, 255, 255, 255)
floodFillIt(m, 467, 150, [200, 150, 100])
draw()

#drawing left eye
m = elp(m, 245, 436, 151, 75, 255, 255, 255)

draw()

#drawing right eye
m = elp(m, 560, 436, 151, 75, 255, 255, 255)

draw()

#drawing left pupil
m = elp(m, 245, 436, 33, 73, 255, 255, 255)

draw()

#drawing left pupil
m = elp(m, 560, 436, 33, 73, 255, 255, 255)

#making sure the pupils finished drawing before trying to paint them
pg.time.wait(500)

#paint eyes and pupils
draw()
floodFillIt(m, 150, 436, [255, 255, 255])
floodFillIt(m, 660, 436, [255, 255, 255])
floodFillIt(m, 245, 436, [164, 0, 0])
floodFillIt(m, 560, 436, [164, 0, 0])

#tickTime = pg.time.get_ticks()
#print(tickTime)

#pg.time.wait(10000) #time to appreciate the title screen

tickTime = pg.time.get_ticks()
while(tickTime < 13104):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
    tickTime = pg.time.get_ticks()
    

#draw neco-arc sus in the screen in a big polygon
clearS()
draw()

poli = createPoli()

addPoint(poli, [100, 50, 0, 0])
addPoint(poli, [600, 50, 1, 0])
addPoint(poli, [600, 550, 1, 1])
addPoint(poli, [100, 550, 0, 1])

scanLine(m, poli, neco)

pg.time.wait(1000)

#scale neco-arc sus down leaving a funny trail behind
matrix = createTransf()
matrixT = makeTranslation(matrix, -350, -300)
matrixS = makeScale(matrixT, 0.9, 0.9)
matrixTMinus = makeTranslation(matrixS, 350, 300)

pol = applyTransform(poli, matrixTMinus)

scanLine(m, pol, neco)

pg.time.wait(1000)

for i in range(0, 15):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
    pol = applyTransform(pol, matrixTMinus)
    scanLine(m, pol, neco)

pg.time.wait(1000)

#draw neco-arc sus again to make sure she's visible
clearS()
scanLine(m, pol, neco)

pg.time.wait(1000)

#translate neco-arc sus down and to the right leaving behind a funny trail
matrixTra = makeTranslation(matrix, 10, 10)
for i in range(0, 15):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
    pol = applyTransform(pol, matrixTra)
    scanLine(m, pol, neco)
pg.time.wait(1000)

#translate neco-arc sus to the right leaving behind a funny trail
matrixTra = makeTranslation(matrixTra, 5, -10)
for i in range(0, 15):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
    pol = applyTransform(pol, matrixTra)
    scanLine(m, pol, neco)
pg.time.wait(1000)

#translate neco-arc sus up leaving behind a funny trail
matrixTra = makeTranslation(matrixTra, -15, -10)
for i in range(0, 30):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
    pol = applyTransform(pol, matrixTra)
    scanLine(m, pol, neco)
pg.time.wait(1000)

#translate neco-arc sus up and to the left leaving behind a funny trail, going out of screen
matrixTra = makeTranslation(matrixTra, -10, 0)
for i in range(0, 40):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
    pol = applyTransform(pol, matrixTra)
    scanLine(m, pol, neco)
pg.time.wait(1000)

#clear screen, then translate neco-arc sus down into view again
clearS()
matrixTra = makeTranslation(matrixTra, 10, 20)
for i in range(0, 40):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
    pol = applyTransform(pol, matrixTra)
    scanLine(m, pol, neco)
pg.time.wait(1000)

#add window and viewport, change to perform scanline on it
view = [800, 600]
win = [0, 0, 799, 599]
pv = mapWindow(pol, win, view)
scanLine(m, pv, neco)
pg.time.wait(1000)

#increase viewport size
view = [1600, 1200]
pv = mapWindow(pol, win, view)
scanLine(m, pv, neco)
pg.time.wait(1000)
win = [100, 0, 899, 599]

draw()
pv = mapWindow(pol, win, view)
scanLine(m, pv, neco)
pg.time.wait(1000)
#matrixTra = makeTranslation(matrix, -322, -193)
#matrixRot = doRotation(matrixTra, 5)
#matrixTraMinus = makeTranslation(matrixRot, 322, 193)
matrixTraMinus = doRotationOnOrigin(pol, matrix, 5)

pol = applyTransform(pol, matrixTraMinus)
pv = mapWindow(pol, win, view)
clearS()
scanLine(m, pv, neco)
pg.time.wait(1000)
for i in range(0, 71):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
    pol = applyTransform(pol, matrixTraMinus)
    view = numpy.subtract(view, [10, 10])
    pv = mapWindow(pol, win, view)
    scanLine(m, pv, neco)
pg.time.wait(1000)

for i in range(0, 71):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
    pol = applyTransform(pol, matrixTraMinus)
    pv = mapWindow(pol, win, view)
    clearS()
    scanLine(m, pv, neco)
pg.time.wait(1000)
'''
view = [800, 600]
win = [0, 0, 799, 599]
clearS()
pv = mapWindow(pol, win, view)
scanLine(m, pv, neco)
'''
pg.time.wait(1000)

pol = numpy.copy(poli)
pv = mapWindow(pol, win, view)
scanLine(m, pv, neco)

pg.time.wait(1000)

view = [600, 400]
pv = mapWindow(pol, win, view)
clearS()
scanLine(m, pv, neco)

pg.time.wait(1000)

view = [300, 225]
win = [0, 0, 399, 299]
pv = mapWindow(pol, win, view)
clearS()
scanLine(m, pv, neco)

view = [600, 400]
pg.time.wait(1000)
win = [-50, -50, 749, 549]
pv = mapWindow(pol, win, view)
clearS()
scanLine(m, pv, neco)
win = [-100, -100, 699, 499]
pv = mapWindow(pol, win, view)
clearS()
pg.time.wait(1000)
scanLine(m, pv, neco)
win = [-150, -150, 549, 349]
pv = mapWindow(pol, win, view)
clearS()
pg.time.wait(1000)
scanLine(m, pv, neco)

pg.time.wait(1000)

matrixTra = makeTranslation(matrix, -350, -300)
matrixRot = doRotation(matrixTra, 5)
matrixTraMinus = makeTranslation(matrixRot, 350, 300)

for i in range(0, 3):
    pol = applyTransform(pol, matrixTraMinus)
    clearS()
    scanLine(m, pol, neco)
'''
outtatime = iio.imread(r'assets\outtatime.png')

matS = makeScale(matrix, 1, 0.5)
pol = applyTransform(poli, matS)
clearS()
scanLine(m, pol, outtatime)

pg.time.wait(1000)

matS = makeScale(matrix, 0.5, 0.5)
pol = applyTransform(poli, matS)
clearS()
scanLine(m, pol, outtatime)
'''

win = [0, 0, 799, 599]
view = [800, 600]

clearS()

poliArc = createPoli()

addPoint(poliArc, [100, 250, 0, 0])
addPoint(poliArc, [300, 250, 1, 0])
addPoint(poliArc, [300, 550, 1, 1])
addPoint(poliArc, [100, 550, 0, 1])

pv = mapWindow(poliArc, win, view)
scanLine(m, pv, arc)

poliRika = createPoli()

addPoint(poliRika, [500, 300, 0, 0])
addPoint(poliRika, [700, 300, 1, 0])
addPoint(poliRika, [700, 550, 1, 1])
addPoint(poliRika, [500, 550, 0, 1])

pv = mapWindow(poliRika, win, view)
scanLine(m, pv, rika)

poliHelloArc = createPoli()

addPoint(poliHelloArc, [100, 100, 0, 0])
addPoint(poliHelloArc, [300, 100, 1, 0])
addPoint(poliHelloArc, [300, 200, 1, 1])
addPoint(poliHelloArc, [100, 200, 0, 1])

pv = mapWindow(poliHelloArc, win, view)
scanLine(m, pv, helloRika)

poliHelloRika = createPoli()

addPoint(poliHelloRika, [500, 100, 0, 0])
addPoint(poliHelloRika, [700, 100, 1, 0])
addPoint(poliHelloRika, [700, 200, 1, 1])
addPoint(poliHelloRika, [500, 200, 0, 1])

pv = mapWindow(poliHelloRika, win, view)
scanLine(m, pv, helloArc)

pg.time.wait(5000)

pv = mapWindow(poliArc, win, view)
scanLine(m, pv, necoOG)

pg.time.wait(5000)

pv = mapWindow(poliRika, win, view)
scanLine(m, pv, catRika)

pg.time.wait(5000)

poliMensagem = createPoli()

addPoint(poliMensagem, [250, 0, 0, 0])
addPoint(poliMensagem, [550, 0, 1, 0])
addPoint(poliMensagem, [550, 120, 1, 1])
addPoint(poliMensagem, [250, 120, 0, 1])

pv = mapWindow(poliMensagem, win, view)

clearS()
scanLine(m, pv, mensagem)

poliTri()
