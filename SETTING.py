#Screen size
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

#Set color with rgb
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
DIMGREY = (105,105,105)
BROWN = (192,192,164)
LIGHT_BROWN = (96,64,32)
GREEN_YELLOW = (173,255,47)

#Size of cell and board
CELL_SIZE = 80
BOARD_LENGTH = 8

#Board position
X_BOARD = (SCREEN_WIDTH - CELL_SIZE * BOARD_LENGTH)/2
X_BOARD = 10
Y_BOARD = (SCREEN_HEIGHT - CELL_SIZE * BOARD_LENGTH)/2

# Chess pieces position 8x8
PIECES_MAP = [
    ["bR","bN","bB","bK","bQ","bB","bN","bR"],
    ["bp","bp","bp","bp","bp","bp","bp","bp"],

    ["--","--","--","--","--","--","--","--"],
    ["--","--","--","--","--","--","--","--"],
    ["--","--","--","--","--","--","--","--"],
    ["--","--","--","--","--","--","--","--"],

    ["wp","wp","wp","wp","wp","wp","wp","wp"],
    ["wR","wN","wB","wK","wQ","wB","wN","wR"]
]

# Chess pieces
PIECES = ["bR","bN","bB","bK","bQ","bp",
          "wR","wN","wB","wK","wQ","wp"]

# AI constant
DEPTH = 1
INF = 2