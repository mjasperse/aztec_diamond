from aztec import AztecDiamond

# We validate the code by checking that when we feed in the specific "random" selections
# from the video, we achieve the results as shown in the video

# Here are the choices made in the video (0 = up/down, 1 = left/right)
VIDEO_SELECTIONS = [0, 1,0, 1,1,1, 1,0,0,1,0, 1,0,0,1,1,0,0]
def VideoSelections(x,y):
    return VIDEO_SELECTIONS.pop(0)

# Here are the resulting diamonds encoded in the "string" format
VIDEO_1 = "LR\nLR"
VIDEO_2 = " UU \nLDDR\nLLRR\n LR "
VIDEO_3 = "  UU  \n UUUU \nLDDDDR\nLLDDRR\n LUUR \n  DD  "
VIDEO_4 = "   UU   \n  UUUU  \n UULRLR \nLDDLRLRR\nLLDDDDRR\n LUULRR \n  DDLR  \n   DD   "
VIDEO_5 = "    UU    \n   UUUU   \n  UUUULR  \n LRLDDLRR \nLLRLUUUURR\nLLDDDDDDRR\n LLRLDDRR \n  LRLLRR  \n   DDLR   \n    DD    "

print('Validation test')
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
