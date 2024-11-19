matrix = createTransf()

poli = createPoli()

addPoint(poli, [100, 50, 0, 0])
addPoint(poli, [600, 50, 1, 0])
addPoint(poli, [600, 550, 1, 1])
addPoint(poli, [100, 550, 0, 1])

scanLine(m, poli, neco)

sleep(1)

matrixT = makeTranslation(matrix, -350, -300)
matrixS = makeScale(matrixT, 0.9, 0.9)
matrixTMinus = makeTranslation(matrixS, 350, 300)

pol = applyTransform(poli, matrixTMinus)

scanLine(m, pol, neco)

sleep(1)

for i in range(0, 15):
    pol = applyTransform(pol, matrixTMinus)
    scanLine(m, pol, neco)

sleep(1)

clearS()
scanLine(m, pol, neco)

sleep(1)

matrixTra = makeTranslation(matrix, 10, 10)

for i in range(0, 15):
    pol = applyTransform(pol, matrixTra)
    scanLine(m, pol, neco)
sleep(1)
matrixTra = makeTranslation(matrixTra, 5, -10)

for i in range(0, 15):
    pol = applyTransform(pol, matrixTra)
    scanLine(m, pol, neco)

sleep(1)
matrixTra = makeTranslation(matrixTra, -15, -10)

for i in range(0, 30):
    pol = applyTransform(pol, matrixTra)
    scanLine(m, pol, neco)

sleep(1)
matrixTra = makeTranslation(matrixTra, -10, 0)

for i in range(0, 40):
    pol = applyTransform(pol, matrixTra)
    scanLine(m, pol, neco)
sleep(1)
clearS()

matrixTra = makeTranslation(matrixTra, 10, 20)

for i in range(0, 40):
    pol = applyTransform(pol, matrixTra)
    scanLine(m, pol, neco)
sleep(1)
view = [800, 600]
win = [0, 0, 799, 599]
pv = mapWindow(pol, win, view)
scanLine(m, pv, neco)
sleep(1)
view = [1600, 1200]

pv = mapWindow(pol, win, view)
scanLine(m, pv, neco)
sleep(1)
win = [100, 0, 899, 599]

drawS()
pv = mapWindow(pol, win, view)
scanLine(m, pv, neco)
sleep(1)
matrixTra = makeTranslation(matrix, -322, -193)
matrixRot = doRotation(matrixTra, 5)
matrixTraMinus = makeTranslation(matrixRot, 322, 193)

pol = applyTransform(pol, matrixTraMinus)
pv = mapWindow(pol, win, view)
clearS()
scanLine(m, pv, neco)
sleep(1)
for i in range(0, 71):
    pol = applyTransform(pol, matrixTraMinus)
    view = numpy.subtract(view, [10, 10])
    pv = mapWindow(pol, win, view)
    scanLine(m, pv, neco)
sleep(1)

for i in range(0, 71):
    pol = applyTransform(pol, matrixTraMinus)
    pv = mapWindow(pol, win, view)
    clearS()
    scanLine(m, pv, neco)
sleep(1)

view = [800, 600]
win = [0, 0, 799, 599]
clearS()
pv = mapWindow(pol, win, view)
scanLine(m, pv, neco)

sleep(1)

pol = numpy.copy(poli)
pv = mapWindow(pol, win, view)
scanLine(m, pv, neco)

sleep(1)

view = [600, 400]
pv = mapWindow(pol, win, view)
clearS()
scanLine(m, pv, neco)

sleep(1)

win = [-50, -50, 749, 549]
pv = mapWindow(pol, win, view)
clearS()
sleep(1)
scanLine(m, pv, neco)
win = [-100, -100, 699, 499]
pv = mapWindow(pol, win, view)
clearS()
sleep(1)
scanLine(m, pv, neco)
win = [-150, -150, 549, 349]
pv = mapWindow(pol, win, view)
clearS()
sleep(1)
scanLine(m, pv, neco)

sleep(1)

matrixTra = makeTranslation(matrix, -350, -300)
matrixRot = doRotation(matrixTra, 5)
matrixTraMinus = makeTranslation(matrixRot, 350, 300)

for i in range(0, 71):
    pol = applyTransform(pol, matrixTraMinus)
    clearS()
    scanLine(m, pol, neco)

time = iio.imread(r'outtatime.png')

matS = makeScale(matrix, 1, 0.5)
pol = applyTransform(poli, matS)
clearS()
scanLine(m, pol, time)

sleep(10)

matS = makeScale(matrix, 0.5, 0.5)
pol = applyTransform(poli, matS)
clearS()
scanLine(m, pol, time)

for i in range(0, 255):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
    scanLineCol(m, pol, [i, i, i])
