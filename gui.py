# AZTEC DIAMOND "SQUARE DANCE"
# Martijn Jasperse, Dec 2020
#
# Inspired by Mathologer's video on the "arctic circle theorem"
# https://www.youtube.com/watch?v=Yy7Q8IWNfHM

# This is a really simple PySide-based GUI that draws the result of the aztec diamond iteration algorithm
# Allows user to see how the pattern evolves as the dimension increases
# Calculates A50 in <50ms, draws in <40ms

# Some TODOs:
# - Handle resize() event
# - Allow zooming in to see detail in diamond
# - Animate the moving blocks (hard)
# - Allow user to specify assignment of empty blocks

import six
# this is a poor attempt at py2/py3 compatibility (only tested py3)
if six.PY2:
    from PySide import QtGui
    from PySide import QtGui as QtWidgets
else:
    from PySide2 import QtWidgets, QtGui

from aztec import *
import time

BLOCK_PENS = {
    ENUM_UP: QtGui.QColor('#f6511d'),
    ENUM_DOWN: QtGui.QColor('#ffb400'),
    ENUM_LEFT: QtGui.QColor('#00a6ed'),
    ENUM_RIGHT: QtGui.QColor('#7fb800')
}
SCALE = 10

class AztecDiamondUI(QtWidgets.QDialog):
    def __init__(self):
        super(AztecDiamondUI,self).__init__()
        self.setWindowTitle('Aztec diamond demo')
        
        self.scene = QtWidgets.QGraphicsScene()
        
        vb = QtWidgets.QVBoxLayout(self)
        self.view = QtWidgets.QGraphicsView(self.scene)
        vb.addWidget(self.view)
        
        btns = QtWidgets.QDialogButtonBox(self)
        vb.addWidget(btns)
        
        btn = btns.addButton("Reset", QtWidgets.QDialogButtonBox.ActionRole)
        btn.pressed.connect(self.reset)
        btn = btns.addButton("Grow", QtWidgets.QDialogButtonBox.ActionRole)
        btn.pressed.connect(self.grow)
        
        self.reset()
        self.resize(500,400)

    def reset(self):
        self.az = AztecDiamond()
        self.redraw()
        
    def grow(self):
        t0 = time.time()
        self.az.grow()
        print('calc',self.az.n,time.time()-t0)
        self.redraw()
        
    def redraw(self):
        t0 = time.time()
        # wipe the previous visualisation
        self.scene.clear()
        self.view.resetTransform()
        # add the blocks
        shape = self.az.grid.shape
        grid = self.az.grid.copy()
        for j in range(grid.shape[0]):
            for i in range(grid.shape[1]):
                z = grid[i,j]
                if not z in BLOCK_PENS: continue
                col = BLOCK_PENS[z]
                brush = QtGui.QBrush(col.lighter(150))
                if z == ENUM_UP or z == ENUM_DOWN:
                    self.scene.addRect(SCALE*j,SCALE*i,SCALE*2,SCALE,col,brush)
                    grid[i,j+1] = ENUM_BAD  # i.e. already drawn
                elif z == ENUM_LEFT or z == ENUM_RIGHT:
                    self.scene.addRect(SCALE*j,SCALE*i,SCALE,SCALE*2,col,brush)
                    grid[i+1,j] = ENUM_BAD  # i.e. already drawn
        # scale the view to show the whole diamond
        scale = min(self.view.width()/float(SCALE*(grid.shape[1]+2)), self.view.height()/float(SCALE*(grid.shape[0]+2)))
        self.view.scale(scale,scale)
        print('draw',time.time()-t0)
        

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    wnd = AztecDiamondUI()
    wnd.show()
    app.exec_()

