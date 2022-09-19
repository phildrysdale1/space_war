## ---- IMPORT PACKAGES ---- ##
import turtle
import math
import random
import time
import platform

## ---- VARIABLES ---- ##

screen_width = 800
screen_height = 600


## ---- CREATE DISPLAY ---- ##
win = turtle.Screen()
win.setup(screen_width, screen_height)
win.title("Space Wars by Phil Drysdale")
win.bgcolor("black")
win.tracer(0)


## ---- RENDERING OBJECTS ---- ##
# CREATE MAIN PEN OBJECT FOR RENDERING ALL OBJECTS
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()

# SPRITE CLASS
class Sprite():
    # Constructor - called when creating object
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.dx = 0
        self.dy = 0

    # Update self
    def update(self):
        self.x += self.dx
        self.y += self.dy

    # Render created sprite
    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.shape)
        pen.color(self.color)
        pen.stamp()

## ---- OBJECTS ---- ##
# Create player sprite
player = Sprite(0,0,"triangle", "white")
player.dx = 0.05

# Create a test enemy sprite
enemy = Sprite(100,100,"triangle", "red")
enemy.dx = -0.05

# Create a test powerup sprite
powerup = Sprite(-200,-100,"circle", "blue")
powerup.dy = 0.05


## Sprites List
sprites = []
sprites.append(player)
sprites.append(enemy)
sprites.append(powerup)

## ---- FUNCTIONS ---- ##



## ---- GAME LOOP ---- ##
while True:
    # Clear screen
    pen.clear()

    ## Run game loop

    # Update sprites
    for sprite in sprites:
        sprite.update()

    # Render Sprites
    for sprite in sprites:
        sprite.render(pen)

    # Update screen
    win.update()
    print(sprites)