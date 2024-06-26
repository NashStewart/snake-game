import random
import tkinter
import turtle

from time import sleep, time
from typing import Any, Dict, List

# region: Game Variables 
delay: float = 0.15
score: int = 0
high_score: int = 0
segments: List = []
mode = 'normal'

colors: Dict[str, tuple] = {
  'dark_cyan': (0, 43, 54),
  'yellow': (181, 137, 0),
  'blue': (38, 139, 210),
  'light_gray': (131, 148, 159),
  'magenta': (211, 54, 130),
  'dark_gray': (101, 123, 131),
  'cyan': (42, 161, 152)
}

background_color: tuple = colors['dark_cyan']
food_color: tuple = colors['magenta']
head_color: tuple = colors['yellow']
body_color: tuple = colors['blue']
scoreboard_text_color: tuple = colors['light_gray']
vim_mode_text_color: tuple = colors['dark_gray']

canvas: Any = turtle.Screen()
head: Any = turtle.Turtle()
food: Any = turtle.Turtle()
scoreboard_text: Any = turtle.Turtle()
vim_mode_text: Any = turtle.Turtle()
# endregion: Game Variables 

# region: Functions
def random_shape() -> str:
  return random.choice(['square', 'triangle', 'circle'])

def reset_game() -> None:
  global score
  score = 0
  sleep(1)
  head.goto(0, 0)
  head.direction = 'stop'
  for segment in segments:
      segment.goto(1000, 1000)
  segments.clear()  

def update_scoreboard() -> None:
  scoreboard_text.clear()
  scoreboard_text.write(f'High Score : {high_score}\nScore : {score}', align="left", font=("candara", 24, "bold"))

def update_vim_mode_display() -> None:
  global mode
  vim_mode_text.clear()
  if mode != 'normal':
    text = f'--{mode.upper()}--'
  else:
    text = ''
  vim_mode_text.write(text, align="left", font=("candara", 20, "bold"))

def head_direction_up() -> None:
  global mode
  if head.direction != 'down' and mode == 'normal':
    head.direction = 'up'

def head_direction_down() -> None:
  global mode 
  if head.direction != 'up' and mode == 'normal':
    head.direction = 'down'

def head_direction_right() -> None:
  global mode 
  if head.direction != 'left' and mode == 'normal':
    head.direction = 'right'

def head_direction_left() -> None:
  global mode
  if head.direction != 'right' and mode == 'normal':
    head.direction = 'left'

def normal_mode() -> None:
  global mode
  if mode != 'normal':
    mode = 'normal'
    update_vim_mode_display()

def insert_mode() -> None:
  global mode
  if mode != 'insert':
    mode = 'insert'
    update_vim_mode_display()

def move() -> None:
  if head.direction == 'up':
    y = head.ycor()
    head.sety(y + 20) 
  if head.direction == 'down':
    y = head.ycor()
    head.sety(y - 20)
  if head.direction == 'right':
    x = head.xcor()
    head.setx(x + 20)
  if head.direction == 'left':
    x = head.xcor()
    head.setx(x - 20)
# endregion: Functions

# region: Configure Turtles
canvas.title('Snake Game')
canvas.colormode(255)
canvas.bgcolor(background_color)
canvas.width = 800
canvas.height = 800
canvas.setup(width=canvas.width, height=canvas.height)
canvas.tracer(0)
canvas.listen()
canvas.onkey(head_direction_up, 'k')
canvas.onkey(head_direction_down, 'j')
canvas.onkey(head_direction_right, 'l')
canvas.onkey(head_direction_left, 'h')
canvas.onkey(normal_mode, 'Escape')
canvas.onkey(insert_mode, 'i')

head.shape('square')
head.color(head_color)
head.penup()
head.goto(0, 0)
head.direction = 'Stop'

food.speed(0)
food.shape(random_shape())
food.color(food_color)
food.penup()
food.goto(0, 100)

scoreboard_text.speed(0)
scoreboard_text.color(scoreboard_text_color)
scoreboard_text.penup()
scoreboard_text.hideturtle()
scoreboard_text.goto(-int(canvas.width / 2) + 20, int(canvas.height / 2) - 70)

vim_mode_text.speed(0)
vim_mode_text.color(vim_mode_text_color)
vim_mode_text.penup()
vim_mode_text.hideturtle()
vim_mode_text.goto(-int(canvas.width / 2) + 20, -int(canvas.height / 2) + 20)
# endregion: Configure Turtles

update_scoreboard()
update_vim_mode_display()

# region: Main Game Loop
start_time: float = time()
while True:
  try:
    if time() > start_time + delay: 
      canvas.update()

      # Check for head collisions with canvas boundaries
      if head.xcor() > int(canvas.width / 2) - 20 or head.xcor() < -int(canvas.width / 2) + 10 or head.ycor() > int(canvas.height / 2) - 15 or head.ycor() < -int(canvas.height / 2) + 20:
        reset_game()
        update_scoreboard()
      
      # Check for head collisions with food
      if head.distance(food) < 20 and mode == 'insert':
        # Add new segment
        new_segment: Any = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape('square')
        new_segment.color(body_color)
        new_segment.penup()
        segments.append(new_segment)

        # Add new food
        new_food_x: int = random.randint(-(int(canvas.width / 2) - 30), (int(canvas.width / 2) - 30)) // 20 * 20
        new_food_y: int = random.randint(-(int(canvas.height / 2) - 30), (int(canvas.height / 2) - 30)) // 20 * 20
        food.shape(random_shape())
        food.color(food_color)
        food.goto(new_food_x, new_food_y)
        
        # Update scoreboard
        score += 10
        if score > high_score:
          high_score = score
        update_scoreboard()
      
      # Make tail pieces trail each other
      for index in range(len(segments) - 1, 0, -1):
        segment_x: int = segments[index-1].xcor()
        segment_y: int = segments[index-1].ycor()
        segments[index].goto(segment_x, segment_y)

      # Make first tail piece follow the head
      if len(segments) > 0:
        head_x: int = head.xcor()
        head_y: int = head.ycor()
        segments[0].goto(head_x, head_y)
      
      move()
      
      # Check for head collisions with body
      for segment in segments:
        if segment.distance(head) < 20:
          reset_game()
          update_scoreboard()

      start_time = time()
  except turtle.Terminator:
    break
  except tkinter.TclError:
    break
# endregion: Main Game Loop

if __name__ == "__main__":
  canvas.mainloop()
