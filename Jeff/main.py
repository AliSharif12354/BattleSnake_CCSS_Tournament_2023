# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import math


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
  print("INFO")

  return {
    "apiversion": "1",
    "author": "hasage-brothers",  # TODO: Your Battlesnake Username
    "color": "#FFC0CB",  # TODO: Choose color
    "head": "dragon",  # TODO: Choose head
    "tail": "dragon",  # TODO: Choose tail
  }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
  print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
  print("GAME OVER\n")


def checkDistance(head, snakes, width, length):
  radar = []
  print("checking distance")
  for i in range(head["x"] - 2, head["x"] + 2):
    for j in range(head["y"] - 2, head["y"] + 2):
      for snake in snakes:
        h = snake["head"]
        if (i == h["x"] and j == h["y"]):
          if (i > head["x"]):
            if (j > head["y"]):
              radar.append(["left", "down"])
            else:
              radar.append(["left", "up"])
          else:
            if (j > head["y"]):
              radar.append(["right", "down"])
            else:
              radar.append(["right", "up"])

  print("radar", radar)
  return radar


def get_path(location, head, safe_move):
  m = ""
  if (head["x"] - location["x"] < 0):
    #move right
    if ("right" in safe_move):
      m = "right"
  else:
    if ("left" in safe_move):
      m = "left"

  if (head["y"] - location["y"] < 0):
    if ("up" in safe_move):
      m = "up"
  else:
    if ("down" in safe_move):
      m = "down"

  return m


def foodDistance(locations, head) -> typing.Dict:
  c = 1000
  cords = {}
  for food in locations:
    x = math.pow((head['x'] - food['x']), 2)
    y = math.pow((head['y'] - food['y']), 2)
    i = round(math.sqrt(x + y))
    if i < c:
      c = i
      cords = food
  return (cords)


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
  print(game_state["you"]["health"])
  health = game_state["you"]["health"]
  state = "normal"
  is_move_safe = {"up": True, "down": True, "left": True, "right": True}

  # We've included code to prevent your Battlesnake from moving backwards
  my_head = game_state["you"]["body"][0]  # Coordinates of your head
  my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

  if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
    is_move_safe["left"] = False

  elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
    is_move_safe["right"] = False

  elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
    is_move_safe["down"] = False

  elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
    is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
  board_width = game_state['board']['width']
  board_height = game_state['board']['height']
  #print("width: ", board_width)
  #print("height: ", board_height)
  #print("x: ", my_head["x"])
  #print("y: ", my_head["y"])
  if my_head["x"] == 0:
    is_move_safe["left"] = False

  if my_head["y"] == 0:
    is_move_safe["down"] = False

  if my_head["x"] == board_width - 1:
    is_move_safe["right"] = False

  if my_head["y"] == board_height - 1:
    is_move_safe["up"] = False

  # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
  # my_body = game_state['you']['body']
  i = 0
  body = game_state["you"]["body"]
  for part in body:

    if i > 1:
      if (my_head['x'] - 1) == part['x']:
        if my_head['y'] == part['y']:
          is_move_safe["left"] = False
      if (my_head['x'] + 1) == part['x']:
        if my_head['y'] == part['y']:
          is_move_safe["right"] = False
      if (my_head['y'] - 1) == part['y']:
        if my_head['x'] == part['x']:
          is_move_safe["down"] = False
      if (my_head['y'] + 1) == part['y']:
        if my_head['x'] == part['x']:
          is_move_safe["up"] = False

    i += 1
  # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
  # opponents = game_state['board']['snakes']
  snakes = game_state["board"]["snakes"]
  for snake in snakes:
    o_body = snake["body"]
    for part in o_body:
      if (my_head['x'] - 1) == part['x']:
        if my_head['y'] == part['y']:
          is_move_safe["left"] = False
      if (my_head['x'] + 1) == part['x']:
        if my_head['y'] == part['y']:
          is_move_safe["right"] = False
      if (my_head['y'] - 1) == part['y']:
        if my_head['x'] == part['x']:
          is_move_safe["down"] = False
      if (my_head['y'] + 1) == part['y']:
        if my_head['x'] == part['x']:
          is_move_safe["up"] = False

  # Are there any safe moves left?
  safe_moves = []
  for move, isSafe in is_move_safe.items():
    if isSafe:
      safe_moves.append(move)

  if len(safe_moves) == 0:
    print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
    return {"move": "down"}

  print("safe moves: ", safe_moves)
  # Choose a random move from the safe ones
  '''#if(state == "baby"):
    #closestFood = foodDistance(game_state["board"]["food"],my_head);
    #if(closestFood["x"] > my_head["x"]):
      #if "right" in safe_moves:
        #next_move =  "right"
    #if(game_state["you"]["length"] > 8):
        #actively look for food to grow
        #state = "idle"
  elif(state == "idle"):
    #do good moves
    if(health < 50):
      state = "hungry"
  elif(state == "hungry"):
    #look for food to sustain health
    i = 2
  else:'''
  #check every snakes head if its within out 5 5 radius
  '''danger = checkDistance(my_head,snakes,board_width, board_height)
  print("danger moves: ", danger)
  not_good_move = []
  if(len(danger)>0):
    if(len(safe_moves)>1): 
      for sm in safe_moves:
        for d in danger:
          if sm in d:
            not_good_move.append(sm)

  for nm in not_good_move:
    if(nm in safe_moves):
      safe_moves.remove(nm)
      
  if(len(safe_moves)==0):
    next_move = random.choice(not_good_move)
  else:
    next_move = random.choice(safe_moves)'''

  # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
  snake_size = 0
  if(board_width<=11):
    snake_size = 7
  elif(board_width>11 and board_width<=19):
    snake_size=12
  else:
    snake_size=20
  if (game_state["you"]["length"] < snake_size or game_state["you"]["health"]<40):
    food = game_state['board']['food']
    cords = foodDistance(food, my_head)
    next_move = get_path(cords, my_head, safe_moves)
    if (next_move == ""):
      next_move = random.choice(safe_moves)
  else:
    danger = checkDistance(my_head, snakes, board_width, board_height)
    print("danger moves: ", danger)
    not_good_move = []
    if (len(danger) > 0):
      if (len(safe_moves) > 1):
        for sm in safe_moves:
          for d in danger:
            if sm in d:
              not_good_move.append(sm)

    for nm in not_good_move:
      if (nm in safe_moves):
        safe_moves.remove(nm)

    if (len(safe_moves) == 0):
      next_move = random.choice(not_good_move)
    else:
      next_move = random.choice(safe_moves)

  print(f"MOVE {game_state['turn']}: {next_move}")
  return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
  from server import run_server

  run_server({"info": info, "start": start, "move": move, "end": end})