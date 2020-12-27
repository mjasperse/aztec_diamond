# AZTEC DIAMOND "SQUARE DANCE"
# Martijn Jasperse, Dec 2020
#
# Inspired by Mathologer's video on the "artic circle theorem"
# https://www.youtube.com/watch?v=Yy7Q8IWNfHM

# We fill a 2D array with numbers representing the "arrows" discussed in the video
# Masking the array with numpy operations allows moderately efficient processing
#
# When we "split" the squares and assign them arrow directions, we can choose to do this randomly
# or via a callback for user selection

import numpy as np
import random

ENUM_BAD = -1
ENUM_EMPTY = 0
ENUM_UP = 1
ENUM_DOWN = 2
ENUM_LEFT = 3
ENUM_RIGHT = 4

class AztecDiamond:
    def __init__(self,callback=None,seed=None):
        # the callback is used to "assign" the squares when growing the diamond
        if callback is None:
            # if no user-specified callback is given, just assign randomly
            self.callback = lambda x,y: random.getrandbits(1)
        else:
            self.callback = callback
        
        if seed is None:
            # Start with an empty 2x2 array that we can grow
            self.n = 1
            self.grid = np.zeros((2,2),dtype=np.int)
            self.assign()
        elif isinstance(seed,str):
            self.from_str(seed)
        else:
            # Assume the user has provided a sane 2D array
            self.grid = np.array(seed,dtype=np.int)
            self.grid[self.grid>ENUM_RIGHT] = ENUM_EMPTY
            self.grid[self.grid<ENUM_EMPTY] = ENUM_BAD
            self.n = self.grid.shape[0] // 2
        
        
    def check(self):
        # Look for left/right clashes
        x,y = np.nonzero((self.grid[:,:-1] == ENUM_RIGHT) * (self.grid[:,1:] == ENUM_LEFT))
        self.grid[x, y] = ENUM_EMPTY
        self.grid[x, y+1] = ENUM_EMPTY
        # Look for up/down clashes
        x,y = np.nonzero((self.grid[:-1,:] == ENUM_DOWN) * (self.grid[1:,:] == ENUM_UP))
        self.grid[x, y] = ENUM_EMPTY
        self.grid[x+1, y] = ENUM_EMPTY
        
    def grow(self, assign=True):
        # Embed array in the next size up
        self.n += 1
        grid = np.zeros((2*self.n, 2*self.n), dtype=np.int)
        # Erase the corners
        xm, ym = np.ogrid[0:grid.shape[0], 0:grid.shape[1]]
        invalid = (abs(xm - self.n + 0.5) + abs(ym - self.n + 0.5)) > self.n
        grid[invalid] = ENUM_BAD
        
        # Check that the translations are valid
        self.check()
        
        # Perform the translations
        for (y,x),z in np.ndenumerate(self.grid):
            if z == ENUM_UP: y -= 1
            elif z == ENUM_DOWN: y += 1
            elif z == ENUM_LEFT: x -= 1
            elif z == ENUM_RIGHT: x += 1
            else: continue  # could be ENUM_EMPTY because of check() or ENUM_BAD at corners
            grid[y+1,x+1] = z

        self.grid = grid
        if assign: self.assign()
        return self.grid
        
    def assign(self):
        # fill the empty blocks
        X,Y = np.nonzero(self.grid[:-1,:-1] == ENUM_EMPTY)
        for x,y in zip(X,Y):
            if self.grid[x,y] != ENUM_EMPTY: continue    # already previously assigned
            if self.callback(x,y):
                self.grid[x,y:y+2] = ENUM_UP
                self.grid[x+1,y:y+2] = ENUM_DOWN
            else:
                self.grid[x:x+2,y] = ENUM_LEFT
                self.grid[x:x+2,y+1] = ENUM_RIGHT
        
    def validate(self, rhs):
        if isinstance(rhs, str):
            return str(self) == rhs
        else:
            return np.all(self.grid == rhs)
        
    def from_str(self, s):
        def parse_row(r):
            for c in r.strip():
                if c == 'U': yield ENUM_UP
                elif c == 'D': yield ENUM_DOWN
                elif c == 'L': yield ENUM_LEFT
                elif c == 'R': yield ENUM_RIGHT
                elif c == ' ': yield ENUM_BAD
                elif c == '-': yield ENUM_EMPTY
                else: raise ValueError('Unknown entry')
        vals = [parse_row(row) for row in s.strip().split('\n')]
        self.grid = np.asarray(vals, dtype=np.int)
        assert self.grid.shape[0] == self.grid.shape[1]
        assert self.grid.shape[0] % 2 == 0
        return self.grid
        
    def __str__(self):
        def to_string(z):
            if z == ENUM_UP: return 'U'
            elif z == ENUM_DOWN: return 'D'
            elif z == ENUM_LEFT: return 'L'
            elif z == ENUM_RIGHT: return 'R'
            elif z == ENUM_BAD: return ' '
            elif z == ENUM_EMPTY: return '-'
            else: raise ValueError('Unknown entry')
        rows = map(lambda x: ''.join(map(to_string,x)),self.grid)
        return '\n'.join(rows)
    
if __name__ == '__main__':
    # simple demonstration
    az = AztecDiamond()
    print(az)
    for i in range(5):
        az.grow()
        print(az)
    
    