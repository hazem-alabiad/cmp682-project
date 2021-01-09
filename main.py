##############    Importing   ##############
import time
from typing import Counter, Dict
from random import random, choices, shuffle
from tabulate import tabulate
from math import inf
from itertools import chain

###############    Globals   ###############
tabulate.PRESERVE_WHITESPACE = True
# Icons dictionary 
AVOCADO = "avocado"
BANANA = "banana"
APPLE = "apple"
CARROT = "carrot"
PROHIBITED = "prohibited"
PIC = "pic"
POINTS = "points"

# people dictionary
SUPERHERO = "Superhero"
ROBOT = "Robot"
SCORE = "score"
NAME = "name"
POS = "pos"

EMOJIS = ["🥑", "🍌", "🍎", "🥕", "🚫"]
EMOJIS_DICT = {"🍎": "apple", "🍌": "banana", "🥑": "avocado", "🥕": "carrot", "🚫": "prohibited"}
N_ROWS = 7
N_COLS = 7
SPLITTER_LEN = 55
EATEN_TILE = "❎"
############################################

########    Functions Definitions   ########
def convert_1d_list_to_2d(list_1_d, n = 7):    
  result=[]               
  start = 0
  end = n
  for i in range(n): 
      result.append(list_1_d[start:end])
      start += n
      end += n
  return result
############################################

##########    Helper Objects   #############
############################################




# 7x7 = 49 - 2 "for players positions" = `47` tiles

################    Class   ################
class FruitGame:
  icons: Dict[str, Dict] = {
    "avocado":{
      "name": "avocado",
      "pic": "🥑",
      "points": 4,
    },
    "banana":{
      "name": "banana",
      "pic": "🍌",
      "points": 3
    },
    "apple": {
      "name": "apple",
      "pic": "🍎",
      "points": 2
    },
    "carrot":{
      "name": "carrot",
      "pic": "🥕",
      "points": 1
    },
    "prohibited":{
      "name": "prohibited",
      "pic": "🚫",
      "points": 0
    }
  }

  players: Dict[str, Dict] = {
    "Superhero": {
      "name": "Superhero",
      "pic": '🦸',
      "score": 0,
      "pos": (6, 0)
    },
    "Robot": {
      "name": "Robot",
      "pic": "🤖",
      "score": 0, 
      "pos": (0, 6)
    }
  }

  def __init__(self) -> None:
    self.start_game()

  def get_human_player(self):
    return next(iter(self.players))

  def get_robot_player(self):
    return next(reversed(self.players))

  ##############    Fruits    ##############
  def get_icon_by_name(self, name) -> str:
    return self.icons[name]

  def get_score_by_name(self, name) -> int:
    return self.icons[name][SCORE]

  def get_pic_from_str(self, name):
    # check if the name is in icon or players
    if name in self.icons:
      return self.get_icon_by_name(name)[PIC]
    elif name == EATEN_TILE:
      # Check if eaten fruit the, return empty string
      return name
    else:
      return self.get_player_by_name(name)[PIC]
  
  def set_to_eaten(self, current_pos, new_pos) -> None:
    (new_x, new_y) = new_pos
    (cur_x, cur_y) = current_pos
    # Set the new position icon to current player and old player's to empty
    self.state[new_x][new_y] = self.get_player_by_name(self.current_player)[NAME]
    self.state[cur_x][cur_y] = EATEN_TILE
  ##########################################

  ##############    Player    ##############
  def get_player_by_name(self, name) -> dict:
    return self.players[name]

  def get_player_by_name(self, name) -> dict:
    return self.players[name]

  def get_player_pos_by_name(self, name) -> tuple:
    return self.players[name][POS]
  ##########################################
  
  ######    Direction & Position    ########
  def direction_to_coordinates(self, current_pos: tuple, direction: str) -> tuple:
    (x, y) = current_pos
    if direction == "r":
      y += 1
    elif direction == "l":
      y -= 1
    elif direction == "u":
      x -= 1
    else:
      x += 1
    return (x, y)
  ##########################################

  #############    Messages    #############
  def get_instruction_message(self):
    return(f"""\nInput your next move: right, left, up. \nYour input should be one of 
    the following: [r, l, u, d]: """)

  def get_invalid_input_letter_error_message(self):
    return(f"""Your input is not valid! Please enter again:\n""")
  ##########################################

  ##############    Moves    ###############
  def check_prohibited(self, new_x, new_y) -> bool:
    valid = PROHIBITED != self.state[new_x][new_y]
    if not valid:
      print("You cannot move to `PROHIBITED` tile!")
    return valid

  def check_collide_with_other_player(self, new_pos) -> bool:
    opponent_pos = ()
    for player in self.players:
      if (player != self.current_player):
        opponent_pos = self.players[player][POS]
    valid = new_pos != opponent_pos
    if not valid:
      print("You cannot move to `OPPONENT` tile!")
    return valid

  def is_valid_move(self, new_pos) -> bool:
    # Check for limits [0, 6]
    valid = False
    (new_x, new_y) = new_pos
    if 0 <= new_x < N_ROWS:
      valid = True
    else:
      print("New X coordinate is not valid!")
    if 0 <= new_y < N_COLS:
      valid = valid and True
    else: 
      print("New Y coordinate is not valid!")
    # Check for prohibited
    if valid:
      valid = self.check_prohibited(new_x, new_y)
    # Check for hitting the other player
    if valid:
      valid = self.check_collide_with_other_player(new_pos)
    return valid

  def set_next_move(self) -> None:
    current_pos = self.get_player_by_name(self.current_player)[POS]
    # Check for valid letter input
    valid_input = False
    while(not valid_input):
      next_move = input(self.get_instruction_message())
      if next_move not in ["r", "l", "u", "d"]:
        print(self.get_invalid_input_letter_error_message())
      # Check for valid limits [0, 6] & Prohibited & No-Opponent
      else:
        new_pos = self.direction_to_coordinates(current_pos, next_move)
        if self.is_valid_move(new_pos):
          # Valid Move
          valid_input = True
          # Set fruit to eaten
          self.set_to_eaten(current_pos, new_pos)
          # Set player's new pos
          self.get_player_by_name(self.current_player)[POS] = new_pos
  ##########################################

  ###############   State   ################
  def is_all_fruits_eaten(self):
    # Check if all fruits are eaten then game is over
    count_tiles = Counter(chain(*self.state))
    is_eaten = count_tiles[EATEN_TILE] == (
      N_ROWS*N_COLS - 2 - count_tiles[self.get_icon_by_name(PROHIBITED)[NAME]]
    )
    print(N_ROWS*N_COLS - 2 - count_tiles[self.get_icon_by_name(PROHIBITED)[NAME]])
    return is_eaten
  ##########################################

  def get_initial_state(self):
    state = choices(list(self.icons.keys()), k=N_ROWS*N_COLS-2)
    shuffle(state)
    # Check that the tiles next to players at position `5` and `34` if so, shuffle 
    while(state[5] == self.icons[PROHIBITED][NAME] or 
    state[34] == self.icons[PROHIBITED][NAME]):
      shuffle(state)
    # Insert the players at `6` and `42` positions
    state.insert(6, next(reversed(self.players)))
    state.insert(42, next(iter(self.players)))
    return convert_1d_list_to_2d(state)

  def start_game(self):
    # Get a random initial state
    self.state = self.get_initial_state()
    # Set turn to human `players[0]`
    self.current_player = self.get_human_player()

  def get_starts_splitter(self):
    print("\n" + f'/'*SPLITTER_LEN + "\n" + "/"*SPLITTER_LEN + 
    "\n" +  "/"*SPLITTER_LEN + "\n")

  def play(self):
    while True:
      self.draw_points_guide()
      self.draw()
      self.set_next_move()
      self.is_fruits_eaten = self.is_all_fruits_eaten()

  def draw_points_guide(self):
    icon_col = EMOJIS
    score_col = [self.get_icon_by_name(EMOJIS_DICT[EMOJIS[i]])[POINTS] for i in range(0, len(EMOJIS))]
    print(tabulate({"Icon": icon_col, "Score": score_col}, tablefmt="jira"))
    print(tabulate({'Icon': [self.icons[PROHIBITED][PIC], EATEN_TILE], 
    "Expl": ["Prohibited 'cannot move to' tile", "Eaten fruit 'can move to' tile"]}))
    print("-" * SPLITTER_LEN)

  def draw_grid(self):
    self.draw_points_guide()
    print("\n+------+-------+-------+-------+-------+-------+-------+")
    for i in range(0, N_ROWS):
      for j in range(0, N_COLS):
        if j == 0: print("|", end="")
        print("\t{}\t| ".expandtabs(2).format(
          self.get_pic_from_str(self.state[i][j])), end="")
      print("\n+------+-------+-------+-------+-------+-------+-------+", end="")
      print()
    print()

  def min_a_b(self, a, b):
    # Assume min = +infinity
    min = +inf


  def draw(self):
    layout = [[self.get_pic_from_str(self.state[i][j]) if self.state[i][j] != "" else "" for j in range(0, N_ROWS)]
    for i in range(0, N_COLS)]
    self.grid = tabulate(layout)
    print(self.grid)

###############    main    #################
def main():
  game = FruitGame()
  game.play()
############################################

if __name__ == "__main__":
  main()