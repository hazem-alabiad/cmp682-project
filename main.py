# Importing 
import time
from random import random, choices, shuffle

####################    Globals   ####################
# fruits dictionary 
AVOCADO = "avocado"
BANANA = "banana"
APPLE = "apple"
CARROT = "carrot"
PROHIBITED = "prohibited"
PIC = "pic"
POINTS = "points"

# people dictionary
SUPERMAN = "Superman"
VAMPIRE = "Vampire"
SCORE = "score"
NAME = "name"

EMOJIS = ["🍎", "🍌", "🥑", "🥕", "🚫"]


#############    Functions Definitions   #############
def convert_1d_list_to_2d(list_1_d, n = 7):    
  result=[]               
  start = 0
  end = n
  for i in range(n): 
      result.append(list_1_d[start:end])
      start += n
      end += n
  return result


################    Helper Objects   #################




# 7x7 = 49 - 2 "for players positions" = `47` tiles

#####################    Class   #####################
class FruitGame:
  fruits = {
    "avocado":{
      "name": "avocado",
      "pic": "🥑",
      "points": 4
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

  players = {
    "Superman": {
      "name": "Superman",
      "pic": "🦸‍♂️",
      "score": 0
    },
    "Vampire": {
      "name": "Vampire",
      "pic": "🧛‍♀️",
      "score": 0
    }
  }

  def __init__(self) -> None:
    self.start_game()

  def get_first_player(self):
    return next(iter(self.players))

  def get_second_player(self):
    return next(reversed(self.players))

  def get_player_by_name(self, name):
    return self.players[name]

  def get_initial_state(self):
    state = choices(list(self.fruits.keys()), k=47)
    shuffle(state)
    # Check that the tiles next to players at position `5` and `35` if so, shuffle 
    while(state[5] == self.fruits[PROHIBITED][PIC] or 
    state[35] == self.fruits[PROHIBITED][PIC]):
      shuffle(state)
    # Insert the players at `6` and `36` positions
    # out.insert(7, )
    state.insert(6, next(iter(self.players)))
    state.insert(36, next(reversed(self.players)))
    return convert_1d_list_to_2d(state)

  def start_game(self):
    # Get a random initial state
    self.game_state = self.get_initial_state()

    # Set current player to `players[1]`


#####################    Main    #####################
def main():
  game = FruitGame()

if __name__ == "__main__":
  main()