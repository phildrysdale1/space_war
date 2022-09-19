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

## ---- CLASSES ---- ##
# Sprite Class
class Sprite():
    # Constructor - called when creating object
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.dx = 0
        self.dy = 0
        self.heading = 0
        self.da = 0
        self.thrust = 0.0
        self.acceleration = 0.0002
        self.health = 100
        self.max_health = 100

    # Update self
    def update(self):
        self.heading += self.da
        self.heading %= 360

        self.dx += math.cos(math.radians(self.heading)) * self.thrust
        self.dy += math.sin(math.radians(self.heading)) * self.thrust

        self.x += self.dx
        self.y += self.dy

    # Render created sprite
    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.setheading(self.heading)
        pen.shape(self.shape)
        pen.color(self.color)
        pen.stamp()

        self.render_health_meter(pen)

    # Render health bar 
    def render_health_meter(self, pen):
        pen.goto(self.x -10, self.y +20)
        pen.width(3)
        pen.pendown()
        pen.setheading(0)

        if self.health/self.max_health <0.3:
            pen.color("red")
        elif self.health/self.max_health <0.7:
            pen.color("yellow")
        else:
            pen.color("green")

        pen.fd(20 * (self.health/self.max_health))
        pen.color("grey")
        pen.fd(20 * ((self.max_health-self.health+10)/self.max_health))
        pen.penup()


        

# Player child class
class Player(Sprite):
    def __init__(self, x, y, shape, color):
        Sprite.__init__(self, 0, 0, shape, color)
        self.lives = 3
        self.score = 0
        self.heading = 90 # determine direction for player sprite
        self.da = 0

    def rotate_left(self):
        self.da = 0.2

    def rotate_right(self):
        self.da = -0.2

    def stop_rotation(self):
        self.da = 0

    def accelerate(self):
        if self.thrust < 0.00001: ## cap thrust to stop it getting crazy
            self.thrust += self.acceleration

    def decelerate(self):
        self.thrust = 0.0
    

# Render created sprite
    def render(self, pen):
        pen.shapesize(0.5, 1.0, None) # modify shape of player ship to make it clear which way it's facing.
        pen.goto(self.x, self.y)
        pen.setheading(self.heading)
        pen.shape(self.shape)
        pen.color(self.color)
        pen.stamp()
        # reset shapesize to stop any other objects being modified
        pen.shapesize(1.0, 1.0, None)

        self.render_health_meter(pen)

        

## ---- OBJECTS ---- ##
# Create player sprite
player = Player(0,0,"triangle", "white")

# Create a test enemy sprite
enemy = Sprite(100,100,"triangle", "red")
enemy.dx = -0.05

# Create a test powerup sprite
powerup = Sprite(-200,-100,"circle", "blue")
powerup.dy = 0.05

# Sprites List
sprites = []
sprites.append(player)
sprites.append(enemy)
sprites.append(powerup)

## ---- KEYBOARD BINDINGS ---- ##
win.listen()
win.onkeypress(player.accelerate, "w")
win.onkeyrelease(player.decelerate, "w")

win.onkeypress(player.rotate_left, "a")
win.onkeyrelease(player.stop_rotation, "a")

win.onkeypress(player.rotate_right, "d")
win.onkeyrelease(player.stop_rotation, "d")

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