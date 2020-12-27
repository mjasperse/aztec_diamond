import six
if six.PY2:
    from PySide import QtGui
    from PySide import QtGui as QtWidgets
else:
    from PySide2 import QtWidgets, QtGui

from aztec import *
import time

BLOCK_PENS = {
    ENUM_UP: QtGui.QColor('#ff0000'),
    ENUM_DOWN: QtGui.QColor('#ff00ff'),
    ENUM_LEFT: QtGui.QColor('#ffff00'),
    ENUM_RIGHT: QtGui.QColor('#ff8000')
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
        self.resize(600,400)

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
                brush = QtGui.QBrush(col.lighter())
                if z == ENUM_UP or z == ENUM_DOWN:
                    self.scene.addRect(SCALE*j,SCALE*i,SCALE*2,SCALE,col,brush)
                    grid[i,j+1] = ENUM_BAD  # already drawn
                elif z == ENUM_LEFT or z == ENUM_RIGHT:
                    self.scene.addRect(SCALE*j,SCALE*i,SCALE,SCALE*2,col,brush)
                    grid[i+1,j] = ENUM_BAD  # already drawn
        # scale the view
        scale = max(SCALE*(grid.shape[1]+2)/float(self.view.width()), SCALE*(grid.shape[0]+2)/float(self.view.height()))
        self.view.scale(1/scale,1/scale)
        print('draw',time.time()-t0)
        

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    wnd = AztecDiamondUI()
    wnd.show()
    app.exec_()

