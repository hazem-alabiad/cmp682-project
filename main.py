##############    Importing   ##############
import time
from itertools import chain
from math import inf
from random import choices, random, shuffle
from typing import Counter, Dict

from tabulate import tabulate

###############    Globals   ###############
# Icons dictionary 
EMPTY = "⬜"

# people dictionary
SUPERHERO = "Superhero"
ROBOT = "Robot"
NAME = "name"
PIC = "pic"

N_ROWS = 3
N_COLS = 3
SPLITTER_LEN = 55
TIE = "="
MAP = {"🔴": SUPERHERO, "🔵": ROBOT}
############################################

########    Functions Definitions   ########
def convert_1d_list_to_2d(list_1_d):    
  result=[]               
  start = 0
  end = N_ROWS
  for i in range(N_ROWS): 
    result.append(list_1_d[start:end])
    start += N_ROWS
    end += N_ROWS
  return result
############################################

##########    Helper Objects   #############
############################################

################    Class   ################
class FruitGame:
  players: Dict[str, Dict] = {
    SUPERHERO: {
      NAME: SUPERHERO,
      PIC: "🔴",
    },
    ROBOT: {
      NAME: ROBOT,
      PIC: "🔵",
    }
  }

  def __init__(self) -> None:
    self.state = []
    self.is_over = None
    self.start_game()

  def get_human_player_name(self):
    return next(iter(self.players))

  def get_robot_player_name(self):
    return next(reversed(self.players))

  def get_opponent_name(self):
    return [player for player in self.players.keys() if player != self.current_player][0] 
  ############################################

  #############    Players    ##############
  def get_player_by_name(self, name:str) -> dict:
    return self.players[name]

  def get_pic_by_player_name(self, name:str) -> str:
    return self.players[name][PIC]
  
  def get_name_by_player_pic(self, pic:str) -> str:
    return MAP[pic]
  ##########################################
  
  #############    Messages    #############
  @staticmethod
  def get_instruction_message():
    return(f"""\nInput your next move as: [row col] values sequentely. 
    \ne.g. '0 4' -->\t""")

  @staticmethod
  def get_invalid_input_coord_error_message():
    return(f"""Your input is not valid! Please enter again:\n""")
  ##########################################

  ##############    Moves    ###############
  def is_valid_move(self, new_pos) -> bool:
    # Check for limits [0, N_COL]
    valid = False
    (new_x, new_y) = new_pos
    if 0 <= new_x < N_ROWS:
      valid = True
    else:
      print("'row' coordinate is not valid!")
    if 0 <= new_y < N_COLS:
      valid = valid and True
    else: 
      print("'col' coordinate is not valid!")
      valid = False
    return valid

  def set_next_move(self) -> None:
    # Check for valid letter input
    valid_input = False
    while(not valid_input):
      next_move = input(self.get_instruction_message())
      next_move = next_move.split()
      if len(next_move) != 2:
        print(self.get_invalid_input_coord_error_message())
      # Check for valid limits [0, N_ROW] & No-Opponent
      else:
        next_move[0] = int(next_move[0])
        next_move[1] = int(next_move[1])
        (next_x, next_y) = next_move
        if not self.state[next_x][next_y] and self.is_valid_move(next_move):
          # Valid Move
          valid_input = True
          self.state[next_x][next_y] = self.get_pic_by_player_name(self.current_player)
  ##########################################

  ###############   State   ################
  def set_initial_state(self):
    self.state = [[None for j in range(N_COLS)] for i in range(N_ROWS)]
    # Set turn to AI
    self.current_player = self.get_robot_player_name()
  
  def is_game_over(self):
    # "🔴": SUPERHERO, "🔵": ROBOT
    # Check for winning state
    for i in range(N_ROWS):
      for j in range(N_COLS):
        tile_pic = self.state[i][j]
        # Skip if None
        if not tile_pic: continue
        if i+1 < N_COLS:
          if j+1 < N_ROWS and self.state[i][j+1] == tile_pic:
            if self.state[i+1][j+1] == tile_pic or self.state[i+1][j]:
                return self.get_name_by_player_pic(tile_pic)
          elif self.state[i+1][j] == tile_pic:
            if (j+1 < N_ROWS and self.state[i+1][j+1] == tile_pic) or (
              j-1 >= 0 and self.state[i+1][j-1] == tile_pic):
              return self.get_name_by_player_pic(tile_pic)
    # Check if tiles are full
    null_counter = list(chain(*self.state)).count(None)
    if null_counter != 0: return False
    
    # It's a tie
    return TIE
  
  def check_winner(self):
    if self.is_over == TIE:
      print("It is a tie! Good luck in the next rounds :)")
    elif self.is_over != True:
      print(f"The winner is {self.is_over}!")
  ##########################################

  #############   Interface   ##############
  def get_starts_splitter(self):
    print("\n" + f'/'*SPLITTER_LEN + "\n" )

  def render(self):
    self.grid = [[f"{self.state[i][j] if self.state[i][j] else EMPTY} {i} {j}" 
      for j in range(N_COLS)] for i in range(N_ROWS)]
    print(tabulate(self.grid, tablefmt="jira"))
  ##########################################

  ############   Alpha-Beta   ##############
  def min_a_b(self, a, b):
    # Human turn
    min_v = +inf
    min_x = None
    min_y = None

    # Check if game is over
    self.is_over = self.is_game_over()
    if self.is_over == TIE: 
      return (0, 0, 0)
    elif self.is_over == self.get_human_player_name():
      return (-1, 0, 0)
    elif self.is_over == self.get_robot_player_name():
      return (1, 0, 0)

    # Iterate over all possibilities
    for i in range(0, N_ROWS):
      for j in range(0, N_COLS):
        if self.state[i][j] == None:
          self.state[i][j] = self.get_pic_by_player_name(self.get_human_player_name())
          (max_v, max_x, max_y) = self.max_a_b(a, b)
          # If found max child is less than current min value, replace
          if max_v < min_v:
            min_v = max_v
            min_x = i
            min_y = j
          self.state[i][j] = None

          # If the obtained min value is less than alpha, Prune
          # as Max already has a larger value
          if min_v <= a:
            return (min_v, min_x, min_y)

          # If the found value is less than beta, update accordingly
          if min_v < b:
            b = min_v
    return (min_v, min_x, min_y)
          
  def max_a_b(self, a, b):
    # AI turn
    max_v = -inf
    max_x = None
    max_y = None

    # Check if game is over
    self.is_over = self.is_game_over()
    if self.is_over == TIE: 
      return (0, 0, 0)
    elif self.is_over == self.get_human_player_name():
      return (-1, 0, 0)
    elif self.is_over == self.get_robot_player_name():
      return (1, 0, 0)

    # Iterate over all possibilities
    for i in range(0, N_ROWS):
      for j in range(0, N_COLS):
        if self.state[i][j] == None:
          self.state[i][j] = self.get_pic_by_player_name(self.get_robot_player_name())
          (min_v, min_x, min_y) = self.min_a_b(a, b)
          # If found min child is larger than current max value, replace
          if min_v > max_v:
            # Update best value for Max
            max_v = min_v
            max_x = i
            max_y = j
          self.state[i][j] = None

          # If the obtained max value is larger than beta, Prune
          # as Min will not allow it
          if max_v >= b:
            return (max_v, max_x, max_y)

          # If the found value is larger than a, update accordingly
          if max_v > a:
            a = max_v
    return (max_v, max_x, max_y)
  ##########################################

  def start_game(self):
    # Get a random initial state
    self.set_initial_state()

  def play(self):
    while True:
      self.render()
      self.is_over = self.is_game_over()
      
      # Check winner
      if self.is_over: 
        self.check_winner()
        return

      # if AI's turn
      if self.current_player == self.get_robot_player_name():
        (v, i, j) = self.max_a_b(-inf, +inf)
        self.state[i][j] = self.get_pic_by_player_name(self.get_robot_player_name())

        # Set turn to human
        self.current_player = self.get_human_player_name()
      # Human turn
      else:
        self.set_next_move()
        
        # Set turn to AI
        self.current_player = self.get_robot_player_name()
      self.get_starts_splitter()
###############    main    #################
def main():
  game = FruitGame()
  game.play()
############################################

if __name__ == "__main__":
  main()
