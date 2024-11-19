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

def scanLineCol(buf, poli, color):
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
                
                buf = setPixel(buf, xk, y, color[0], color[1], color[2])
    draw()
    
def poliTri():
    poliColor = createPoli()
    addPoint(poliColor, [350, 50, 255, 0, 0])
    addPoint(poliColor, [600, 550, 0, 255, 0])
    addPoint(poliColor, [100, 550, 0, 0, 255])
    for i in range(0, 511):
        p1 = 255 - i
        if p1 < 0: p1 = 0
        p3 = -255 + i
        if p3 < 0: p3 = 0
        if p3 > 255: p3 = 255
        p2 = 0 + i
        if p2 < 0: p2 = 0
        if p2 > 255: p2 = 255 - p3
        poliColor[0] = [350, 50, p1, p2, p3]
        poliColor[1] = [600, 550, p3, p1, p2]
        poliColor[2] = [100, 550, p2, p3, p1]
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
        scanLineCol(m, poliColor)