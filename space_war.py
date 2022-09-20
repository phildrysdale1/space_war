## ---------- IMPORT PACKAGES ---------- ##
import turtle
import math
import random
import time
import platform
from colour import Color

## ---------- VARIABLES ---------- ##

screen_width = 800
screen_height = 600

## ---------- CREATE DISPLAY ---------- ##
win = turtle.Screen()
win.setup(screen_width, screen_height)
win.title("Space Wars by Phil Drysdale")
win.bgcolor("black")
win.tracer(0)

## ---------- RENDERING OBJECTS ---------- ##
# CREATE MAIN PEN OBJECT FOR RENDERING ALL OBJECTS
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()

## ---------- CLASSES ---------- ##
# Game class

class Game():
    def __init__ (self, width, height):
        self.width = width
        self.height = height
    
    def render_border(self, pen):
        pen.color("white")
        pen.width(3)
        pen.penup()

        left = -self.width / 2.0
        right = self.width / 2.0
        top = self.height / 2.0
        bottom = -self.height / 2.0

        pen.goto(left, top)
        pen.pendown()
        pen.goto(right, top)
        pen.goto(right, bottom)
        pen.goto(left, bottom)
        pen.goto(left, top)

        pen.penup()


## ---------- Sprite parent class ---------- ##
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
        self.width = 20
        self.height = 20
        # Create list spaning full health range and mapping it to a RGB color for a gradient healthbar
        self.colors = list(Color("red").range_to(Color("Green"), self.max_health))

    def is_collision(self,other):
        if self.x < other.x + other.width and\
            self.x + self.width > other.x and\
            self.y < other.y + other.height and\
            self.y + self.height > other.y:
            return True
        else:
            return False

    # Update self
    def update(self):
        self.heading += self.da
        self.heading %= 360

        self.dx += math.cos(math.radians(self.heading)) * self.thrust
        self.dy += math.sin(math.radians(self.heading)) * self.thrust

        self.x += self.dx
        self.y += self.dy

        self.border_col_check()

    # collision check with border
    def border_col_check(self):
        if self.x > game.width / 2.0 - 10:
            self.x = game.width/2.0 - 10
            self.dx *= -1
        elif self.x < -game.width / 2.0 + 10:
            self.x = -game.width/2.0 + 10
            self.dx *= -1
        elif self.y > game.height / 2.0 - 10:
            self.y = game.height/2.0 - 10
            self.dy *= -1
        elif self.y < -game.height / 2.0 + 10:
            self.y = -game.height/2.0 + 10
            self.dy *= -1


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

        # set health bar color from the list 'colors'.
        pen.pencolor(self.colors[self.health-1].get_hex())
        pen.fd(20 * (self.health/self.max_health))
        if self.health != self.max_health:
            pen.color("grey")
            pen.fd(20 * ((self.max_health-self.health)/self.max_health))
        pen.penup()

# Create game object

game = Game(810, 610)



## ---------- Player class ---------- ##
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

    def fire(self):
        missile.fire(self.x, self.y, self.heading, self.dx, self.dy)
    

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

## ---------- Enemy class ---------- ##
class Enemy(Sprite):
    def __init__(self, x, y, shape, color):
        Sprite.__init__(self, x, y, shape, color)

## ---------- Powerup class ---------- ##
class Powerup(Sprite):
    def __init__(self, x, y, shape, color):
        Sprite.__init__(self, x, y, shape, color)

## ---------- Missle class ---------- ##

class Missile(Sprite):
    def __init__ (self, x, y, shape, color):
        Sprite.__init__(self, x, y, shape, color)
        self.state = "ready"
        self.thrust = 1.5
        self.max_fuel = 300
        self.fuel = self.max_fuel
        self.height = 2
        self.widght = 2

    def fire(self, x, y, heading, dx, dy):
        if self.state == "ready":
            self.state = "active"
            self.x = x
            self.y = y
            self.heading = heading
            self.dx = dx
            self.dy = dy

            self.dx += math.cos(math.radians(self.heading)) * self.thrust
            self.dy += math.sin(math.radians(self.heading)) * self.thrust

    def update(self):
        if self.state == "active":
            self.fuel -= self.thrust
            if self.fuel <= 0:
                self.reset()

            self.heading += self.da
            self.heading %= 360

            self.x += self.dx
            self.y += self.dy

            self.border_col_check()

    def reset(self):
        self.fuel = self.max_fuel
        self.dx = 0
        self.dy = 0
        self.state = "ready"


    def render(self, pen):
        if self.state == "active":
            pen.shapesize(0.1, 0.1, None) # modify shape of player ship to make it clear which way it's facing.
            pen.goto(self.x, self.y)
            pen.setheading(self.heading)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.stamp()
            # reset shapesize to stop any other objects being modified
            pen.shapesize(1.0, 1.0, None)

            self.render_health_meter(pen)


## ---------- OBJECTS ---------- ##
# Create player sprite
player = Player(0,0,"triangle", "white")

# Create missle sprite
missile = Missile(0,100, "square", "yellow")

# Create a test enemy sprite
enemy = Enemy(100,100,"triangle", "red")
enemy.dx = -0.05
enemy2 = Enemy(-100,-200,"triangle", "red")
enemy2.dx = -0.05

# Create a test powerup sprite
powerup = Powerup(-200,-100,"circle", "blue")
powerup.dy = 0.05
powerup2 = Powerup(200,100,"circle", "blue")
powerup2.dx = 0.05
powerup2.dy = 0.05

# Sprites List
sprites = []
sprites.append(player)
sprites.append(enemy)
sprites.append(powerup)
sprites.append(missile)
sprites.append(enemy2)
sprites.append(powerup2)

## ---------- KEYBOARD BINDINGS ---------- ##
win.listen()
win.onkeypress(player.accelerate, "w")
win.onkeyrelease(player.decelerate, "w")

win.onkeypress(player.rotate_left, "a")
win.onkeyrelease(player.stop_rotation, "a")

win.onkeypress(player.rotate_right, "d")
win.onkeyrelease(player.stop_rotation, "d")

win.onkeypress(player.fire, "space")

## ---------- FUNCTIONS ---------- ##



## ---------- GAME LOOP ---------- ##
while True:
    # Clear screen
    pen.clear()

    ## Run game loop

    # Update sprites
    for sprite in sprites:
        sprite.update()

    # Check for collisions
    for sprite in sprites:
        if isinstance(sprite, Enemy):
            if player.is_collision(sprite):
                player.x = 0
                player.y = 0
                player.lives -= 1
            
            if missile.state == "active" and missile.is_collision(sprite):
                sprite.x = -100
                sprite.y = -100
                missile.reset()

        if isinstance(sprite, Powerup):
            if player.is_collision(sprite):
                sprite.x = 100
                sprite.y = 100

            if missile.state == "active" and missile.is_collision(sprite):
                sprite.x = 100
                sprite.y = 100
                missile.reset()


    # Render Sprites
    for sprite in sprites:
        sprite.render(pen)

    game.render_border(pen)

    # Update screen
    win.update()