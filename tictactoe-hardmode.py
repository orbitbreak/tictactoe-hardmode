# A Tic-Tac-Toe game
#   ...without mercy

from functools import partial
import random, tkMessageBox, sys
from Tkinter import *

textsize = 16

class TicTacToe(object):
	# possible ways to win TTT
    winners = ({1, 2, 3}, {4, 5, 6}, {7, 8, 9},
                    {1, 4, 7}, {2, 5, 8}, {3, 6, 9},
                    {1, 5, 9}, {3, 5, 7})

    def __init__(self, top):
        self.player = bool(random.randint(0,1))  # randomize who starts
        self.display(('Player = O\nHumanKiller9000 = X\nHK9k\'s Move.' if self.player
                     else 'Player = O\nHumanKiller9000 = X\nMake Your Move.') +
                     '\nClose to meet your maker.\n')

        self.button_dic = {}   # pointer to buttons and StringVar()
        self.top = top
        self.top.geometry("240x240+20+20")
        self.top.wm_attributes('-topmost', True)

        self.X_O_dict = {"X":[], "O":[]}  # list of "X" and "O" moves
        self.top.title('TicTacToe Hard Mode')
        self.top_frame = Frame(self.top, width = 240, height = 240)
        self.top_frame.grid(row = 0, column = 1)
        self.next_player = BooleanVar()
        
        self.buttons()
        
        # tie if moves finish
        self.tie = True
        self.moves = 0
        self.next_player.set(self.player)


    def play(self):
        while self.moves < 9 and self.tie:
            self.selection()
        try:
            self.stop()
        except TclError:
            pass

    def buttons(self):
        b_row = 1
        b_col = 0
        for j in range(1, 10):
            sv=StringVar()
            sv.set(j)
            b = Button(self.top_frame, textvariable = sv, font = (None, textsize),
                       command = partial(self.cb_handler, j), bg = 'white')
            b.grid(row = b_row, column = b_col, padx = 5, pady = 5)
            self.button_dic[j] = [sv, b]

            b_col += 1
            if b_col > 2:
                b_col = 0
                b_row += 1
				
        # don't know how to separate from play field using grid
        Button(self.top, text = 'Accept Defeat', font = ('Arial', textsize * 3/4),
                command = self.stop).grid(row = 2, column = 1, columnspan = 3)


    def stop(self):
          
        if not self.tie:
            self.display("Winner is O" if self.player else "Winner is X")
        elif self.moves == 9:
            self.display("You survived. This time." )
        else:
            self.display("Only a matter of time.")
            self.moves = 99
            self.tie = False

        # unsetting wait events
        self.next_player.set(self.player)

        self.top.destroy()
        raise SystemExit('Bye.')

    def cb_handler(self, square_number):
        this_player = "X" if self.player  else "O"

        # square not already occupied
        if self.legal_move(square_number):

            # change button's text to "X" or "O"
            self.button_dic[square_number][0].set(this_player)
            self.X_O_dict[this_player].append(square_number)

            # set background to occupied color
            self.button_dic[square_number][1].config(bg = 'red')

            self.check_for_winner(self.X_O_dict[this_player])
            self.player = not self.player
            self.next_player.set(self.player)
        else:
            print "Occupied, pick another", square_number

    def check_for_winner( self, list_in):
        set_in = set(list_in)
        if any(winner.issubset(set_in) for winner in self.winners):
            self.tie = False

    def check_two_in_a_row(self):
        # check to win first and then to block
        for player in ["X", "O"]:
            this = set(self.X_O_dict[player])
            for sub_set in self.winners:
                if len(this & sub_set) == 2:
                    one_to_return = next(iter(sub_set - this))
                    # all one of  them legal, then return
                    if self.legal_move(one_to_return):
                        return one_to_return

    def display(self, msg, title='Instructions'):
        tl=Toplevel()
        tl.geometry("300x300+30+60")
        tl.title(title)
        tl.wm_attributes('-topmost', True)
        lb=Label(tl, text = msg, font = ('Arial', 16))
        lb.pack(fill = 'both', expand = True)
        tl.lift()
        tl.wait_window()

    def legal_move(self, square_number):
        return (square_number not in self.X_O_dict["X"] and
                   square_number not in self.X_O_dict["O"])

    def selection(self):
        # computer moves
        if self.player:
            # don't accept button clicks when it is computer's (X) turn
            for but in self.button_dic:
                self.button_dic[but][1].state = DISABLED

            move_to_take = self.check_two_in_a_row()
            if move_to_take is not None:
                self.cb_handler(move_to_take)
            else:
                # sequence = middle square, and then each corner as the
                # 2 middle rows are elmininated by the middle square
                for chosen in (5, 1, 3, 7, 9, 2, 4, 6, 8):
                    if self.legal_move(chosen):
                        self.cb_handler(chosen)
                        break
        else:
            # person moves, set buttons back to normal
            for but in self.button_dic:
                self.button_dic[but][1].state = NORMAL
            # we can wait variable change, because they are BooleanVars
            self.top.wait_variable(self.next_player)
        self.moves += 1


game = TicTacToe(Tk())
game.play()
print('Finished')
sys.exit()