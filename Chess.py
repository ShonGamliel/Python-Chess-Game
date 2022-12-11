from tkinter import *
from PIL import Image, ImageTk
import random

places = [
    [-1, 620], [88, 620], [177, 620], [265, 620], [354, 620], [442, 620], [530, 620], [620, 620],
    [-1, 530], [88, 530], [177, 530], [265, 530], [354, 530], [442, 530], [530, 530], [620, 530],
    [-1, 442], [88, 442], [177, 442], [265, 442], [354, 442], [442, 442], [530, 442], [620, 442],
    [-1, 354], [88, 354], [177, 354], [265, 354], [354, 354], [442, 354], [530, 354], [620, 354],
    [-1, 265], [88, 265], [177, 265], [265, 265], [354, 265], [442, 265], [530, 265], [620, 265],
    [-1, 177], [88, 177], [177, 177], [265, 177], [354, 177], [442, 177], [530, 177], [620, 177],
    [-1, 88], [88, 88], [177, 88], [265, 88], [354, 88], [442, 88], [530, 88], [620, 88],
    [-1, -1], [88, -1], [177, -1], [265, -1], [354, -1], [442, -1], [530, -1], [620, -1]
]

pawn = 1
knight = 10
bishop = 20
rook = 30
queen = 50
king = 1000

current_pawn = None

LEFT = -1
RIGHT = 1
UP = 8
DOWN = -8
SLANT_UP_RIGHT = 9
SLANT_UP_LEFT = 7
SLANT_DOWN_RIGHT = -7
SLANT_DOWN_LEFT = -9
LEFT_EDGE = list(dict.fromkeys([i % 8 == 0 and i for i in range(63)]))
RIGHT_EDGE = [i - 1 for i in LEFT_EDGE][1:] + [63]
BOTTOM_EDGE = [i for i in range(8)]
TOP_EDGE = [i for i in range(56, 64)]
LEFT_SECTION = [i + 1 for i in LEFT_EDGE] + LEFT_EDGE
RIGHT_SECTION = [i - 1 for i in RIGHT_EDGE] + RIGHT_EDGE
MAX_MOVES = 8
KNIGHT_MOVES = [15, 17, -15, -17, 6, -6, 10, -10]

checkmate = False


class Board:
    def __init__(self):
        self.board = []
        self.turn = 1
        self.king = {}
        for i in range(64):
            self.board.append(False)

    def update(self, place, new_pawn):
        self.board[place] = new_pawn
        if new_pawn is not False:
            if new_pawn.rank == king:
                self.king['1' if new_pawn.team == 1 else '2'] = new_pawn

        return new_pawn

    def check_place(self, place):
        return self.board[place]

    def active_pawns(self, team):
        active_pawns = []
        for p in self.board:
            if p is not False:
                if p.team == team:
                    active_pawns.append(p)

        return active_pawns

    def get_king(self, team):
        return self.king['1' if team == 1 else '2']

    def king_treat(self, team):
        opponent_pawns = self.active_pawns(1 if team == 2 else 2)

        try:
            team_king_place = self.get_king(team).get_place()
        except:
            return True

        for p in opponent_pawns:
            if team_king_place in p.get_possible_moves():
                return True
        return False

    def copy(self, new_board):
        for p in self.board:
            if p is not False:
                new_board.update(p.get_place(), Pawn(p.rank, p.team, p.get_place(), new_board))

    def check_for_checkmate(self, team):
        for p in self.board:
            if p is not False:
                if p.team == team:
                    if len(p.possible_moves()) != 0:
                        return False
        return True

    def evaluate(self, team):
        evaluation = 0
        for p in self.board:
            if p is not False:
                if p.team == team:
                    evaluation += p.rank

        return evaluation


main_board = Board()


class Pawn:
    global pawn, knight, bishop, rook, queen, king
    global main_board

    def __init__(self, rank, team, place, board=main_board):
        self.rank = rank
        self.team = team
        self.moved = False
        self.board = board

        if board == main_board:
            rank_name = ""
            if rank == pawn:
                rank_name = "pawn"
            elif rank == knight:
                rank_name = "knight"
            elif rank == bishop:
                rank_name = "bishop"
            elif rank == rook:
                rank_name = "rook"
            elif rank == queen:
                rank_name = "queen"
            elif rank == king:
                rank_name = "king"

            path = "pieces/%s_%s.png" % ("black" if team == 1 else "white", rank_name)
            self.image = ImageTk.PhotoImage(Image.open(path), master=canvas)
            self.img = canvas.create_image(places[place][0], places[place][1], image=self.image, anchor="nw")

    def get_place(self):
        return self.board.board.index(self)


    def move(self, place):
        global current_pawn, checkmate

        if self.board == main_board:
            if main_board.check_place(place) is not False:
                canvas.delete(main_board.check_place(place).img)

            canvas.moveto(self.img, places[place][0], places[place][1])

            canvas.moveto(target, -100, -100)
            current_pawn = None


        self.board.update(self.get_place(), False)
        self.board.update(place, self)
        # In the right order
        self.board.turn = 1 if self.board.turn == 2 else 2
        self.moved = True


        if self.board == main_board:
            if main_board.check_for_checkmate(1 if self.team == 2 else 2) is True:
                print("Checkmate")
                label = Label(canvas, text='GAME OVER')
                label.pack()
                checkmate = True
                root.after(4000, root.destroy)
                exit()
            else:
                if main_board.turn == 2:
                # bm = find_best_move(main_board.turn)
                # if bm != -1:
                #     main_board.check_place(bm[0]).move(bm[1])
                #     # print(f"best is to move from {bm[0]} to {bm[1]}")
                # else:
                #     # print("do what you want")
                    root.after(100,random_move)



    def get_directions(self, moves, *directions):
        dirs = []
        for d in directions:
            last_place = self.get_place()
            for i in range(moves):
                if d in [LEFT, SLANT_UP_LEFT, SLANT_DOWN_LEFT] and last_place in LEFT_EDGE:
                    break
                elif d in [RIGHT, SLANT_UP_RIGHT, SLANT_DOWN_RIGHT] and last_place in RIGHT_EDGE:
                    break
                elif d in [DOWN, SLANT_DOWN_LEFT, SLANT_DOWN_RIGHT] and last_place in BOTTOM_EDGE:
                    break
                elif d in [UP, SLANT_UP_RIGHT, SLANT_UP_LEFT] and last_place in TOP_EDGE:
                    break

                if self.rank == pawn:
                    if d in [SLANT_UP_LEFT, SLANT_DOWN_LEFT, SLANT_DOWN_RIGHT, SLANT_UP_RIGHT]:
                        if self.board.check_place(last_place + d) is False:
                            break
                    elif d in [UP, DOWN]:
                        if self.board.check_place(last_place + d) is not False:
                            break

                if self.board.check_place(last_place + d) is False:
                    dirs.append(last_place + d)
                    last_place = last_place + d
                elif self.board.check_place(last_place + d) is not False and self.board.check_place(
                        last_place + d).team != self.team:
                    dirs.append(last_place + d)
                    break
                elif self.board.check_place(last_place + d) is not False and self.board.check_place(
                        last_place + d).team == self.team:
                    break

        return dirs

    def get_possible_moves(self):
        pm = []
        place = self.get_place()
        if self.rank == pawn:
            if self.team == 1:
                pm = pm + self.get_directions(1 if self.moved is True else 2, UP)
                pm = pm + self.get_directions(1, SLANT_UP_RIGHT, SLANT_UP_LEFT)
            else:
                pm = pm + self.get_directions(1 if self.moved is True else 2, DOWN)
                pm = pm + self.get_directions(1, SLANT_DOWN_RIGHT, SLANT_DOWN_LEFT)

        elif self.rank == knight:
            for move in KNIGHT_MOVES:
                if place + move > 63 or place + move < 0:
                    continue
                if place in RIGHT_SECTION and place + move in LEFT_SECTION:
                    continue
                if place in LEFT_SECTION and place + move in RIGHT_SECTION:
                    continue

                if self.board.check_place(place + move) is not False:
                    if self.board.check_place(place + move).team == self.team:
                        continue
                    else:
                        pm.append(place + move)
                else:
                    pm.append(place + move)

        elif self.rank == bishop:
            pm = pm + self.get_directions(MAX_MOVES, SLANT_UP_LEFT, SLANT_DOWN_LEFT, SLANT_DOWN_RIGHT, SLANT_UP_RIGHT)

        elif self.rank == rook:
            pm = pm + self.get_directions(MAX_MOVES, UP, DOWN, LEFT, RIGHT)

        elif self.rank == queen:
            pm = pm + self.get_directions(MAX_MOVES, UP, DOWN, LEFT, RIGHT, SLANT_UP_LEFT, SLANT_DOWN_LEFT,
                                          SLANT_DOWN_RIGHT, SLANT_UP_RIGHT)

        elif self.rank == king:
            pm = pm + self.get_directions(1, UP, DOWN, LEFT, RIGHT, SLANT_UP_LEFT, SLANT_DOWN_LEFT, SLANT_DOWN_RIGHT,
                                          SLANT_UP_RIGHT)

        return pm

    def possible_moves(self):
        pms = self.get_possible_moves()
        edited_pms = []

        # predict a move that can risk the king
        temp_board = Board()
        main_board.copy(temp_board)

        backup = temp_board.board[:]

        pawn_object_in_temp_board = temp_board.check_place(self.get_place())
        for move in pms:
            p_moved = self.moved

            pawn_object_in_temp_board.move(move)
            if temp_board.king_treat(self.team) is False:
                edited_pms.append(move)

            self.moved = p_moved
            temp_board.board = backup

        return edited_pms

# def find_best_move(team):
#     # opponent_pawns = main_board.active_pawns(1 if team == 2 else 2)
#
#     temp_board = Board()
#     main_board.copy(temp_board)
#     team_pawns = temp_board.active_pawns(team)
#
#     backup = temp_board.board[:]
#
#     evals = []
#     for p in team_pawns:
#         place = p.get_place()
#         pm = p.possible_moves()
#         for move in pm:
#             p.move(move)
#
#             evals.append([place, move, temp_board.evaluate(1 if team == 2 else 2)])
#
#             temp_board.board = backup
#
#     all_evals = []
#     for e in evals:
#         all_evals.append(e[2])
#
#     all_evals = list(dict.fromkeys(all_evals))
#
#     if len(all_evals) > 1:
#         min_eval = []
#         for e in evals:
#             if len(min_eval) == 0:
#                 min_eval = e
#             else:
#                 if e[2] < min_eval[2]:
#                     min_eval = e
#
#         return min_eval
#
#     else:
#         return -1


def random_move():
    team = main_board.turn
    team_pawns = main_board.active_pawns(team)
    opponent_pawns = main_board.active_pawns(1 if team == 2 else 2)

    pawns_can_eat = []

    for p in team_pawns:
        pms = p.possible_moves()
        for op in opponent_pawns:
            if op.get_place() in pms:
                pawns_can_eat.append([p, op.get_place()])

    for p in pawns_can_eat:
        for op in opponent_pawns:
            if p[1] in op.possible_moves():
                pawns_can_eat.remove(op)

    if len(pawns_can_eat) != 0:
        p = random.choice(pawns_can_eat)
        p[0].move(p[1])

    else:
        p = random.choice(team_pawns)
        m = p.possible_moves()
        while True:
            if len(m) == 0:
                p = random.choice(team_pawns)
                m = p.possible_moves()
                for i in m:
                    if i < 0 or i > 63:
                        m = []
            else:
                break

        m = random.choice(m)
        p.move(m)

def mark_places(pms):
    global targets
    unmark_places()
    for idx, place in list(enumerate(pms)):
        canvas.moveto(targets[idx], places[place][0]+21, places[place][1]+21)

def unmark_places():
    global targets
    for i in range(22):
        canvas.moveto(targets[i],-100,-100)

def clicked(place):
    global current_pawn
    cp = main_board.check_place(place)

    if current_pawn is None:
        if cp is not False:
            if cp.team != main_board.turn:
                return
            current_pawn = cp
            canvas.moveto(target, places[place][0] + 1, places[place][1])

            mark_places(cp.possible_moves())
            # print(main_board.find_best_move(main_board.turn))

    else:
        if cp is not False and cp.team == current_pawn.team:
            if cp.team != main_board.turn:
                return
            current_pawn = cp
            canvas.moveto(target, places[place][0] + 1, places[place][1])
            mark_places(cp.possible_moves())
            return

        if place in current_pawn.possible_moves():
            current_pawn.move(place)
            unmark_places()


def click(event):
    if checkmate is False:
        for idx, place in list(enumerate(places)):
            if event.x < place[0] + 90 and event.y > place[1]:
                clicked(idx)
                break


if __name__ == "__main__":
    root = Tk()
    root.title("Chess Game")
    root.geometry("710x710")
    root.resizable(False, False)

    canvas = Canvas(root)
    board_img = ImageTk.PhotoImage(Image.open("board.png"), master=root)
    board_canvas = canvas.create_image(0, 0, image=board_img, anchor="nw")


    img = ImageTk.PhotoImage(Image.open("red_frame.png"), master=canvas)
    target = canvas.create_image(-100, -100, image=img, anchor="nw")

    target_images = []
    targets = []
    for i in range(22):
        target_image = ImageTk.PhotoImage(Image.open("target.png"), master=canvas)
        target_images.append(target_image)
        targets.append(canvas.create_image(-100, -100, image=target_image, anchor="nw"))

    canvas.bind("<Button-1>", click)
    canvas.pack(fill=BOTH, expand=1)

    # Bottom Player
    for i in range(8, 16):
        main_board.update(i, Pawn(pawn, 1, i))  # 0,1,2,3,4,5,6,7
    main_board.update(1, Pawn(knight, 1, 1))  # 8
    main_board.update(6, Pawn(knight, 1, 6))  # 9
    main_board.update(2, Pawn(bishop, 1, 2))  # 10
    main_board.update(5, Pawn(bishop, 1, 5))  # 11
    main_board.update(0, Pawn(rook, 1, 0))  # 12
    main_board.update(7, Pawn(rook, 1, 7))  # 13
    main_board.update(3, Pawn(queen, 1, 3))  # 14
    main_board.update(4, Pawn(king, 1, 4))  # 15

    # Top Player
    for i in range(48, 56):
        main_board.update(i, Pawn(pawn, 2, i))  # 16,17,18,19,20,21,22,23
    main_board.update(57, Pawn(knight, 2, 57))  # 24
    main_board.update(62, Pawn(knight, 2, 62))  # 25
    main_board.update(58, Pawn(bishop, 2, 58))  # 26
    main_board.update(61, Pawn(bishop, 2, 61))  # 27
    main_board.update(56, Pawn(rook, 2, 56))  # 28
    main_board.update(63, Pawn(rook, 2, 63))  # 29
    main_board.update(59, Pawn(queen, 2, 59))  # 30
    main_board.update(60, Pawn(king, 2, 60))  # 31

    root.mainloop()
