from typing import Any, Dict, List

import random
import time
import turtle

# Setup game variables
delay: float = 0.15
score: int = 0
high_score: int = 0
segments: List = []

colors: Dict[str, tuple] = {
  'black': (13, 13, 13),
  'dark_orange': (242, 110, 34),
  'light_orange': (242, 163, 15),
  'cyan': (13, 217, 217),
  'pink': (217, 17, 127)
}

background_color: tuple = colors['black']
food_color: tuple = colors['pink']
head_color: tuple = colors['dark_orange']
body_color: tuple = colors['light_orange']
text_color: tuple = colors['cyan']

canvas: Any = turtle.Screen()
head: Any = turtle.Turtle()
food: Any = turtle.Turtle()
text: Any = turtle.Turtle()

def random_shape() -> str:
  return random.choice(['square', 'triangle', 'circle'])

def reset_game() -> None:
  global score
  global delay
  score = 0
  delay = 0.15
  time.sleep(1)
  head.goto(0, 0)
  head.direction = 'stop'
  for segment in segments:
      segment.goto(1000, 1000)
  segments.clear()  

def update_scoreboard() -> None:
  text.clear()
  text.write("Score : {} High Score : {} ".format(
      score, high_score), align="center", font=("candara", 24, "bold"))
  
def head_direction_up() -> None:
  if head.direction != 'down':
    head.direction = 'up'

def head_direction_down() -> None:
  if head.direction != 'up':
    head.direction = 'down'

def head_direction_right() -> None:
  if head.direction != 'left':
    head.direction = 'right'

def head_direction_left() -> None:
  if head.direction != 'right':
    head.direction = 'left'

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

# Create a window
canvas.title('Snake Game')
canvas.colormode(255)
canvas.bgcolor(background_color)
canvas.setup(width=600, height=600)
canvas.tracer(0)

# Setup snake head
head.shape('square')
head.color(head_color)
head.penup()
head.goto(0, 0)
head.direction = 'Stop'

# Setup food
food.speed(0)
food.shape(random_shape())
food.color(food_color)
food.penup()
food.goto(0, 100)

# Setup scoreboard
text.speed(0)
text.color(text_color)
text.penup()
text.hideturtle()
text.goto(0, 250)

update_scoreboard()

# Register keys
canvas.listen()
canvas.onkey(head_direction_up, 'w')
canvas.onkey(head_direction_down, 's')
canvas.onkey(head_direction_right, 'd')
canvas.onkey(head_direction_left, 'a')

# Gameplay Loop
while True:
  canvas.update()

  # Check for head collisions with canvas boundaries
  if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
    reset_game()
    update_scoreboard()
  
  # Check for head collisions with food
  if head.distance(food) < 20:
    # Add new segment
    new_segment: Any = turtle.Turtle()
    new_segment.speed(0)
    new_segment.shape('square')
    new_segment.color(body_color)
    new_segment.penup()
    segments.append(new_segment)

    # Add new food
    new_food_x: int = random.randint(-270, 270) // 20 * 20
    new_food_y: int = random.randint(-270, 270) // 20 * 20
    food.shape(random_shape())
    food.color(food_color)
    food.goto(new_food_x, new_food_y)
    
    # Update scoreboard
    delay -= 0.001
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

  time.sleep(delay)

canvas.mainloop()
