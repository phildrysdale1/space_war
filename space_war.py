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



## CREATE MAIN PEN OBJECT FOR RENDERING ALL OBJECTS
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()

## Sprite Class

class Sprite():
    # Constructor - called when creating object
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
    
    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.shape)
        pen.color(self.color)
        pen.stamp()

## Create player sprite

player = Sprite(0,0,"triangle", "white")
player.render(pen)

## Create a test enemy sprite

enemy = Sprite(100,100,"triangle", "red")
enemy.render(pen)

## Create a test powerup sprite
powerup = Sprite(-200,-100,"circle", "red")
powerup.render(pen)

## ---- GAME LOOP ---- ##
win.mainloop()