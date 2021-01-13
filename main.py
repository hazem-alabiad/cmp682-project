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
PENALTY = "penalty"
EATEN = "eaten"
PIC = "pic"
POINTS = "points"

# people dictionary
SUPERHERO = "Superhero"
ROBOT = "Robot"
SCORE = "score"
NAME = "name"
POS = "pos"

EMOJIS = ["🥑", "🍌", "🍎", "🥕", "🚫"]
EMOJIS_DICT = {"🍎": APPLE, "🍌": BANANA, "🥑": AVOCADO, 
  "🥕": CARROT, "🚫": PENALTY, "❎": EATEN} 
N_ROWS = 5
N_COLS = 5
SPLITTER_LEN = 55
TIE = "="
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
  icons: Dict[str, Dict] = {
    AVOCADO:{
      "name": AVOCADO,
      "pic": "🥑",
      "points": 4,
    },
    BANANA:{
      "name": BANANA,
      "pic": "🍌",
      "points": 3
    },
    APPLE: {
      "name": APPLE,
      "pic": "🍎",
      "points": 2
    },
    CARROT:{
      "name": CARROT,
      "pic": "🥕",
      "points": 1
    },
    PENALTY:{
      "name": PENALTY,
      "pic": "🚫",
      "points": -1
    }, 
    EATEN:{
      "name": EATEN,
      "pic": "❎",
      "points": 0
    }
  }

  players: Dict[str, Dict] = {
    "Superhero": {
      "name": "Superhero",
      "pic": '🦸',
      "score": 0,
      "pos": ()
    },
    "Robot": {
      "name": "Robot",
      "pic": "🤖",
      "score": 0, 
      "pos": ()
    }
  }

  def __init__(self) -> None:
    self.start_game()

  def get_human_player_name(self):
    return next(iter(self.players))

  def get_robot_player_name(self):
    return next(reversed(self.players))

  def get_opponent_name(self):
    return [player for player in self.players.keys() if player != self.current_player][0] 

  ###############    ICON    ###############
  def get_icon_by_name(self, name) -> str:
    return self.icons[name]

  def get_pic_from_str(self, name):
    # check if the name is in icon or players
    if name in self.icons:
      return self.get_icon_by_name(name)[PIC]
    else:
      return self.get_player_by_name(name)[PIC]

  def get_point_by_icon_pic(self, pic):
    return self.get_icon_by_name(EMOJIS_DICT[pic])[POINTS]
  
  def get_point_by_icon_name(self, name) -> tuple:
    return self.get_icon_by_name(name)[POINTS]
  
  def set_to_eaten(self, cur_pos, new_pos) -> None:
    (new_x, new_y) = new_pos
    # Set the new position icon to current player and old player's to either 
    # eaten or start point based on coordinates
    self.state[new_x][new_y] = self.current_player
    if cur_pos:
      (cur_x, cur_y) = cur_pos
      self.state[cur_x][cur_y] = EATEN
  ##########################################

  ##############    Player    ##############
  def get_player_by_name(self, name) -> dict:
    return self.players[name]

  def get_player_pos_by_name(self, name) -> tuple:
    return self.players[name][POS]

  def get_player_score_by_name(self, name) -> tuple:
    return self.get_player_by_name(name)[SCORE]
  
  def collect_points(self, fruit_name) -> None:
    point = self.get_point_by_icon_name(fruit_name)
    self.get_player_by_name(self.current_player)[SCORE] += point
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
    return(f"""\nInput your next move as: [row col] values sequentely. 
    \ne.g. '0 4' -->\t""")

  def get_invalid_input_coord_error_message(self):
    return(f"""Your input is not valid! Please enter again:\n""")
  ##########################################

  ##############    Moves    ###############
  def check_collide_with_other_player(self, new_pos) -> bool:
    # If the opponent has not played yet
    if not self.get_player_pos_by_name(self.get_opponent_name()):
      return True 
    opponent_pos = ()
    for player in self.players:
      if (player != self.current_player):
        opponent_pos = self.get_player_pos_by_name(self.players[player])
    valid = new_pos != opponent_pos
    if not valid:
      print("You cannot move to `OPPONENT` tile!")
    return valid

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
    # Check for hitting the other player
    if valid:
      valid = self.check_collide_with_other_player(new_pos)
    return valid

  def set_next_move(self) -> None:
    current_pos = self.get_player_pos_by_name(self.current_player)
    # Check for valid letter input
    valid_input = False
    while(not valid_input):
      next_move = input(self.get_instruction_message())
      next_move = next_move.split()
      next_move[0] = int(next_move[0])
      next_move[1] = int(next_move[1])
      if len(next_move) != 2:
        print(self.get_invalid_input_coord_error_message())
      # Check for valid limits [0, N_ROW] & No-Opponent
      else:
        if self.is_valid_move(next_move):
          fruit_name = self.state[next_move[0]][next_move[1]]
          # Valid Move
          valid_input = True
          # Set fruit to eaten
          self.set_to_eaten(current_pos, next_move)
          # Set player's new pos
          self.get_player_by_name(self.current_player)[POS] = next_move
          # Collect points
          self.collect_points(fruit_name)
  ##########################################

  ###############   State   ################
  def is_all_fruits_eaten(self):
    # Check if all fruits are eaten then game is over
    count_tiles = Counter(chain(*self.state))
    is_eaten = count_tiles[self.icons[EATEN][PIC]] == (
      N_ROWS*N_COLS - 2 - count_tiles[PENALTY]
    )
    return is_eaten

  def is_game_over(self):
    if not self.is_all_fruits_eaten():
      # Set winner
      if self.get_player_score_by_name(self.get_human_player_name()) > self.get_player_score_by_name(self.get_robot_player_name()):
        return self.get_human_player_name()
      elif self.get_player_score_by_name(self.get_human_player_name()) < self.get_player_score_by_name(self.get_robot_player_name()):
        return self.get_robot_player_name()
      else:
        return TIE
    else:
      None

  def get_initial_state(self):
    state = choices([icon for icon in self.icons.keys() if icon not in [EATEN]], k=N_ROWS*N_COLS)
    shuffle(state)
    # Set turn to AI
    self.current_player = self.get_robot_player_name()
    return convert_1d_list_to_2d(state)
  ##########################################

  #############   Interface   ##############
  def get_starts_splitter(self):
    print("\n" + f'/'*SPLITTER_LEN + "\n" + "/"*SPLITTER_LEN + 
    "\n" +  "/"*SPLITTER_LEN + "\n")

  def draw_points_guide(self):
    icon_col = EMOJIS
    score_col = [self.get_icon_by_name(EMOJIS_DICT[EMOJIS[i]])[POINTS] for i in range(0, len(EMOJIS))]
    print(tabulate({"Icon": icon_col, "Score": score_col}, tablefmt="jira"))
    print(tabulate({'Icon': [self.get_pic_from_str(EATEN), self.get_pic_from_str(PENALTY)], 
    "Expl": ["Eaten fruit", "Penalty"]}))
    print("/" * SPLITTER_LEN)

  def draw(self):
    layout = [[f'{self.get_pic_from_str(self.state[i][j])} {i} {j}' for j in range(0, N_COLS)]
      for i in range(0, N_ROWS)]
    self.grid = tabulate(layout)
    print(self.grid)
  ##########################################

  ############   Alpha-Beta   ##############
  def min_a_b(self, a, b):
    # Human turn
    min_v = +inf
    min_x = None
    min_y = None

    # Check if game is over
    self.is_over = self.is_game_over()

    # Iterate over all possibilities
    for i in range(0, N_ROWS):
      for j in range(0, N_COLS):
        if self.state[i][j] != EATEN:
          fruit = self.state[i][j]
          self.state[i][j] = EATEN
          (max_v, max_x, max_y) = self.max_a_b(a, b)
          # If found max child is less than current min value, replace
          if max_v < min_v:
            min_v = max_v
            min_x = i
            min_y = j
          self.state[i][j] = fruit

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

    # Iterate over all possibilities
    for i in range(0, N_ROWS):
      for j in range(0, N_COLS):
        if self.state[i][j] != EATEN:
          fruit = self.state[i][j]
          self.state[i][j] = EATEN
          (min_v, min_x, min_y) = self.min_a_b(a, b)
          # If found min child is larger than current max value, replace
          if min_v > max_v:
            # Update best value for Max
            max_v = min_v
            max_x = i
            max_y = j
          self.state[i][j] = fruit

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
    self.state = self.get_initial_state()

  def play(self):
    while True:
      self.draw_points_guide()
      self.result = self.is_game_over()
      # self.draw()
      # self.set_next_move()
      # self.is_fruits_eaten = self.is_all_fruits_eaten()
      # If AI's turn

      # While not all fruits eaten
      if self.result != None:
        if self.result != TIE:
          print("It is a tie!")
        else:
          print(f'The winner is {self.result}')
        self.start_game()
        return

      if self.current_player == self.get_robot_player():
        (v, x, y) = self.max_a_b(-inf, +inf)
        self.state[x][y] = self.get_pic_from_str(self.get_robot_player_name())
        # Set turn to human
        self.current_player = self.get_human_player()
      
      # If human's turn
      else:
        print("HUMAN")


###############    main    #################
def main():
  game = FruitGame()
  game.play()
############################################

if __name__ == "__main__":
  main()