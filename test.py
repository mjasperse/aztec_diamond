from aztec import AztecDiamond

# We validate the code by checking that when we feed in the specific "random" selections
# from the video, we achieve the results as shown in the video

# Here are the choices made in the video (0 = up/down, 1 = left/right)
VIDEO_SELECTIONS = [0, 1,0, 1,1,1, 1,0,0,1,0, 1,0,0,1,1,0,0]
def VideoSelections(x,y):
    return VIDEO_SELECTIONS.pop(0)

# Here are the resulting diamonds encoded in the "grid" format
VIDEO_1 = [ [3,4],
            [3,4] ]
VIDEO_2 = [ [-1,1,1,-1],
            [3,2,2,4],
            [3,3,4,4],
            [-1,3,4,-1] ]
VIDEO_3 = [ [-1,-1,1,1,-1,-1],
            [-1,1,1,1,1,-1],
            [3,2,2,2,2,4],
            [3,3,2,2,4,4],
            [-1,3,1,1,4,-1],
            [-1,-1,2,2,-1,-1] ]
VIDEO_4 = [ [-1,-1,-1,1,1,-1,-1,-1],
            [-1,-1,1,1,1,1,-1,-1],
            [-1,1,1,3,4,3,4,-1],
            [3,2,2,3,4,3,4,4],
            [3,3,2,2,2,2,4,4],
            [-1,3,1,1,3,4,4,-1],
            [-1,-1,2,2,3,4,-1,-1],
            [-1,-1,-1,2,2,-1,-1,-1] ]
VIDEO_5 = [ [-1,-1,-1,-1,1,1,-1,-1,-1,-1],
            [-1,-1,-1,1,1,1,1,-1,-1,-1],
            [-1,-1,1,1,1,1,3,4,-1,-1],
            [-1,3,4,3,2,2,3,4,4,-1],
            [3,3,4,3,1,1,1,1,4,4],
            [3,3,2,2,2,2,2,2,4,4],
            [-1,3,3,4,3,2,2,4,4,-1],
            [-1,-1,3,4,3,3,4,4,-1,-1],
            [-1,-1,-1,2,2,3,4,-1,-1,-1],
            [-1,-1,-1,-1,2,2,-1,-1,-1,-1] ]

test = AztecDiamond(callback=VideoSelections)
print('A1:',test.validate(VIDEO_1))
test.grow()
print('A2:',test.validate(VIDEO_2))
test.grow()
print('A3:',test.validate(VIDEO_3))
test.grow()
print('A4:',test.validate(VIDEO_4))
test.grow()
print('A5:',test.validate(VIDEO_5))
