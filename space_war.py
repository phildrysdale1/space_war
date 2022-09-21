## ---------- IMPORT PACKAGES ---------- ##
from re import X
from tkinter import Y
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
win.setup(screen_width + 220, screen_height + 20)
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
        self.level = 1

    def start_level(self):
        sprites.clear()

        # Add player
        sprites.append(player)
        
        # Add missile
        sprites.append(missile)

        # Add enemies
        for l in range(self.level):
            x = random.randint(-self.width/2+10, self.width/2-10)
            y = random.randint(-self.height/2+10, self.height/2-10)
            dx = random.uniform(-0.5,0.5)
            dy = random.uniform(-0.5,0.5)
            sprites.append(Enemy(x,y,"square", "red"))
            sprites[-1].dx = dx
            sprites[-1].dy = dy

        # Add powerups
        for l in range(self.level):
            x = random.randint(-self.width/2+10, self.width/2-10)
            y = random.randint(-self.height/2+10, self.height/2-10)
            dx = random.uniform(-0.5,0.5)
            dy = random.uniform(-0.5,0.5)
            sprites.append(Powerup(x,y,"circle", "green"))
            sprites[-1].dx = dx
            sprites[-1].dy = dy


    def render_border(self, pen, x_offset, y_offset):
        pen.color("white")
        pen.width(3)
        pen.penup()

        left = -self.width / 2.0
        right = self.width / 2.0
        top = self.height / 2.0
        bottom = -self.height / 2.0

        pen.goto(left - x_offset, top - y_offset)
        pen.pendown()
        pen.goto(right - x_offset, top - y_offset)
        pen.goto(right - x_offset, bottom - y_offset)
        pen.goto(left - x_offset, bottom - y_offset)
        pen.goto(left - x_offset, top- y_offset)

        pen.penup()

    def render_hud(self, pen, score, active_enemies = 0):
        pen.color ("grey")
        pen.penup()
        pen.goto(400,0)
        pen.shape("square")
        pen.setheading(90)
        pen.shapesize(10,32, None)
        pen.stamp()
        pen.penup()
        
        pen.color("white")
        pen.width(3)
        pen.goto(300,400)
        pen.pendown()
        pen.goto(300, -400)

        pen.penup()
        pen.color("white")
        character_pen.scale = 1.0
        character_pen.draw_string(pen, "Space Wars", 400, 270)
        character_pen.draw_string(pen, "Score: {}".format(score), 400, 240)
        character_pen.draw_string(pen, "Lives: {}".format(player.lives), 400, 210)
        character_pen.draw_string(pen, "Level: {}".format(game.level), 400, 180)
        character_pen.draw_string(pen, "Enemies: {}".format(active_enemies), 400, 150)

## ---------- Character Pen class ---------- ##
# For drawing text

class CharacterPen():
    def __init__(self,color="white", scale = 1.0):
        self.color = color
        self.scale = scale
        
        self.characters = {}
        self.characters["1"] = ((-5, 10), (0, 10), (0, -10), (-5, -10), (5, -10))
        self.characters["2"] = ((-5, 10),(5, 10),(5, 0), (-5, 0), (-5, -10), (5, -10))
        self.characters["3"] = ((-5, 10),(5, 10),(5, 0), (0, 0), (5, 0), (5,-10), (-5, -10))
        self.characters["4"] = ((-5, 10), (-5, 0), (5, 0), (2,0), (2, 5), (2, -10))
        self.characters["5"] = ((5, 10), (-5, 10), (-5, 0), (5,0), (5,-10), (-5, -10))
        self.characters["6"] = ((5, 10), (-5, 10), (-5, -10), (5, -10), (5, 0), (-5, 0))
        self.characters["7"] = ((-5, 10), (5, 10), (0, -10))
        self.characters["8"] = ((-5, 0), (5, 0), (5, 10), (-5, 10), (-5, -10), (5, -10), (5, 0))
        self.characters["9"] = ((5, -10), (5, 10), (-5, 10), (-5, 0), (5, 0))
        self.characters["0"] = ((-5, 10), (5, 10), (5, -10), (-5, -10), (-5, 10))

        self.characters["A"] = ((-5, -10), (-5, 10), (5, 10), (5, -10), (5, 0), (-5, 0))
        self.characters["B"] = ((-5, -10), (-5, 10), (3, 10), (3, 0), (-5, 0), (5,0), (5, -10), (-5, -10))
        self.characters["C"] = ((5, 10), (-5, 10), (-5, -10), (5, -10))
        self.characters["D"] = ((-5, 10), (-5, -10), (5, -8), (5, 8), (-5, 10))
        self.characters["E"] = ((5, 10), (-5, 10), (-5, 0), (0, 0), (-5, 0), (-5, -10), (5, -10))
        self.characters["F"] = ((5, 10), (-5, 10), (-5, 0), (5, 0), (-5, 0), (-5, -10))
        self.characters["G"] = ((5, 10), (-5, 10), (-5, -10), (5, -10), (5, 0), (0, 0))
        self.characters["H"] = ((-5, 10), (-5, -10), (-5, 0), (5, 0), (5, 10), (5, -10))
        self.characters["I"] = ((-5, 10), (5, 10), (0, 10), (0, -10), (-5, -10), (5, -10))
        self.characters["J"] = ((5, 10), (5, -10), (-5, -10), (-5, 0))   
        self.characters["K"] = ((-5, 10), (-5, -10), (-5, 0), (5, 10), (-5, 0), (5, -10))
        self.characters["L"] = ((-5, 10), (-5, -10), (5, -10))
        self.characters["M"] = ((-5, -10), (-3, 10), (0, 0), (3, 10), (5, -10))
        self.characters["N"] = ((-5, -10), (-5, 10), (5, -10), (5, 10))
        self.characters["O"] = ((-5, 10), (5, 10), (5, -10), (-5, -10), (-5, 10))
        self.characters["P"] = ((-5, -10), (-5, 10), (5, 10), (5, 0), (-5, 0))
        self.characters["Q"] = ((5, -10), (-5, -10), (-5, 10), (5, 10), (5, -10), (2, -7), (6, -11))
        self.characters["R"] = ((-5, -10), (-5, 10), (5, 10), (5, 0), (-5, 0), (5, -10))
        self.characters["S"] = ((5, 8), (5, 10), (-5, 10), (-5, 0), (5, 0), (5, -10), (-5, -10), (-5, -8))
        self.characters["T"] = ((-5, 10), (5, 10), (0, 10), (0, -10)) 
        self.characters["V"] = ((-5, 10), (0, -10), (5, 10)) 
        self.characters["U"] = ((-5, 10), (-5, -10), (5, -10), (5, 10)) 
        self.characters["W"] = ((-5, 10), (-3, -10), (0, 0), (3, -10), (5, 10))   
        self.characters["X"] = ((-5, 10), (5, -10), (0, 0), (-5, -10), (5, 10))   
        self.characters["Y"] = ((-5, 10), (0, 0), (5, 10), (0,0), (0, -10))   
        self.characters["Z"] = ((-5, 10), (5, 10), (-5, -10), (5, -10))   

        self.characters["-"] = ((-3, 0), (3, 0)) 

    def draw_string(self, pen, str, x, y):
        pen.width(2)
        pen.color(self.color)
        
        # center text
        x -= 15 * self.scale * (len(str)-1) / 2

        for character in str:
            self.draw_character(pen, character, x, y)
            x += 15 * self.scale      

    def draw_character(self, pen, character, x, y):
        scale = self.scale

        if character in "abcdefghijklmnopqrstuvwxyz":
            scale *= 0.8

        character = character.upper()
        
        # check for character existence
        if character in self.characters:
            # draw character
            pen.penup()
            xy = self.characters[character][0]
            pen.goto(x + xy[0] * scale, y + xy[1] * scale)
            pen.pendown()
            for i in range(1, len(self.characters[character])):
                xy = self.characters[character][i]
                pen.goto(x + xy[0] * scale, y + xy[1] * scale)
            pen.penup()

character_pen = CharacterPen("white", 3.0)


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
        self.max_dx = 0.5
        self.max_dy = 0.5
        self.heading = 0
        self.da = 0
        self.thrust = 0.0
        self.acceleration = 0.1
        self.health = 100
        self.max_health = 100
        self.width = 20
        self.height = 20
        self.state = "active"
        self.radar = 330
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
    def render(self, pen, x_offset, y_offset):
        if self.state == "active":
            pen.goto(self.x - x_offset, self.y - y_offset)
            pen.setheading(self.heading)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.stamp()

            self.render_health_meter(pen, x_offset, y_offset)

    # Render health bar 
    def render_health_meter(self, pen, x_offset, y_offset):
        pen.goto(self.x - x_offset - 10, self.y - y_offset +20)
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

game = Game(700, 500)



## ---------- Player class ---------- ##
class Player(Sprite):
    def __init__(self, x, y, shape, color):
        Sprite.__init__(self, 0, 0, shape, color)
        self.lives = 3
        self.score = 0
        self.heading = 90 # determine direction for player sprite
        self.da = 0
        self.max_dx = 0.4
        self.max_dy = 0.4
        self.max_health = 100
        self.health = self.max_health
         # Create list spaning full health range and mapping it to a RGB color for a gradient healthbar
        self.colors = list(Color("red").range_to(Color("Green"), self.max_health))

    def rotate_left(self):
        self.da = 2

    def rotate_right(self):
        self.da = -2

    def stop_rotation(self):
        self.da = 0

    def accelerate(self):
        if self.thrust < self.acceleration * 1.5: ## cap thrust to stop it getting crazy
            self.thrust += self.acceleration

    def decelerate(self):
        self.thrust = 0.0

    def fire(self):
        missile.fire(self.x, self.y, self.heading, self.dx, self.dy)

    def bounce(self, other):
        temp_dx = self.dx
        temp_dy = self.dy

        self.dx = other.dx
        self.dy = other.dy

        other.dx = temp_dx
        other.dy = temp_dy

    def update(self):
        if self.state == "active":
            self.heading += self.da
            self.heading %= 360
            self.current_acc_dx = self.dx + math.cos(math.radians(self.heading)) * self.thrust
            self.current_acc_dy = self.dy + math.cos(math.radians(self.heading)) * self.thrust

            # stop acceleration breaking at max speed
            if self.dx > self.max_dx:
                self.dx = self.max_dx - 0.01
            elif self.dx < -self.max_dx:
                self.dx = -self.max_dx + 0.01
            if self.dy > self.max_dy:
                self.dy = self.max_dy - 0.01
            elif self.dy < -self.max_dy:
                self.dy = -self.max_dy + 0.01
            # accelerate
            self.dx += math.cos(math.radians(self.heading)) * self.thrust
            self.dy += math.sin(math.radians(self.heading)) * self.thrust

            self.x += self.dx
            self.y += self.dy

            self.border_col_check()

            # check health
            if self.health <= 0:
                self.reset()
    
    def reset(self):
        self.x = 0
        self.y = 0
        self.health = self.max_health
        self.heading = 90
        self.dx = 0
        self.dy = 0
        self.lives -= 1


# Render created sprite
    def render(self, pen, x_offset, y_offset):
        pen.shapesize(0.5, 1.0, None) # modify shape of player ship to make it clear which way it's facing.
        pen.goto(self.x - x_offset, self.y - y_offset)
        pen.setheading(self.heading)
        pen.shape(self.shape)
        pen.color(self.color)
        pen.stamp()
        # reset shapesize to stop any other objects being modified
        pen.shapesize(1.0, 1.0, None)

        self.render_health_meter(pen, x_offset, y_offset)

## ---------- Enemy class ---------- ##
class Enemy(Sprite):
    def __init__(self, x, y, shape, color):
        Sprite.__init__(self, x, y, shape, color)
        # Create list spaning full health range and mapping it to a RGB color for a gradient healthbar
        self.colors = list(Color("red").range_to(Color("Green"), self.max_health))

        self.type = random.choice(["hunter", "mine", "spy"])

        if self.type == "hunter":
            self.color = "red"
            self.shape = "square"
            self.max_health = 20
            self.health = self.max_health
        elif self.type == "mine":
            self.color = "orange"
            self.shape = "triangle"
            self.max_health = 10
            self.health = self.max_health
        elif self.type == "spy":
            self.color = "blue"
            self.shape = "square"
            self.max_health = 30
            self.health = self.max_health

    def update(self):
        if self.state == "active":
            self.heading += self.da
            self.heading %= 360

            self.dx += math.cos(math.radians(self.heading)) * self.thrust
            self.dy += math.sin(math.radians(self.heading)) * self.thrust

            self.x += self.dx
            self.y += self.dy

            self.border_col_check()

            if self.type == "hunter":
                if self.x < player.x:
                    self.dx += 0.005
                else:
                    self.dx -= 0.005
                if self.y < player.y:
                    self.dy += 0.005
                else:
                    self.dy -= 0.005               
            
            elif self.type == "mine":
                self.heading += 2
                self.dx += random.uniform(-0.01,0.01)
                self.dy += random.uniform(-0.01,0.01)
            
            elif self.type == "spy":
                if abs(self.x - player.x) < 100:
                    if self.x < player.x:
                        self.dx -= 0.005
                    else:
                        self.dx += 0.005
                else:
                    if self.x < player.x:
                        self.dx += 0.005
                    else:
                        self.dx -= 0.005

                if abs(self.y - player.y) < 100:
                    if self.y < player.y:
                        self.dy -= 0.005
                    else:
                        self.dy += 0.005            
                else:
                    if self.y < player.y:
                        self.dy += 0.005
                    else:
                        self.dy -= 0.005 


            # set max speed
            if self.dx > self.max_dx:
                self.dx = self.max_dx
            elif self.dx < -self.max_dx:
                self.dx = -self.max_dx
            if self.dy > self.max_dy:
                self.dy = self.max_dy
            elif self.dy < -self.max_dy:
                self.dy = -self.max_dy

            # check health
            if self.health <= 0:
                self.reset()
    
    def reset(self):
        self.state = "inactive"

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


    def render(self, pen, x_offset, y_offset):
        if self.state == "active":
            pen.shapesize(0.1, 0.1, None) # modify shape of player ship to make it clear which way it's facing.
            pen.goto(self.x - x_offset, self.y - y_offset)
            pen.setheading(self.heading)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.stamp()
            # reset shapesize to stop any other objects being modified
            pen.shapesize(1.0, 1.0, None)


## ---------- Powerup class ---------- ##
class Powerup(Sprite):
    def __init__(self, x, y, shape, color):
        Sprite.__init__(self, x, y, shape, color)


## ---------- Camera class ---------- ##
class Camera():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, x, y):
        self.x = x
        self.y  = y

## ---------- Radar class ---------- ## 
class Radar():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self, pen, sprites):

        # draw radar circle
        pen.setheading(90)
        pen.color("white")
        pen.goto(self.x + self.width / 2.0, self.y)
        pen.pendown()
        pen.circle(self.width / 2.0)
        pen.penup()

        # draw sprites on radar
        for sprite in sprites:
            if sprite.state == "active":
                radar_x = self.x + (sprite.x - player.x) * (self.width/game.width)
                radar_y = self.y + (sprite.y - player.y) * (self.height/game.height)
                pen.goto(radar_x, radar_y)
                pen.color(sprite.color)
                pen.shape(sprite.shape)
                pen.shapesize(0.2,0.2,None)
                pen.setheading(sprite.heading)

                # set radar distance
                distance = ((player.x - sprite.x)**2 + (player.y-sprite.y)**2)**0.5
                if distance < player.radar:
                    pen.stamp()


## ---------- OBJECTS ---------- ##
# Create player sprite
player = Player(0,0,"triangle", "white")

# Create camera 
camera = Camera(player.x, player.y)

# Create missle sprite
missile = Missile(0,100, "square", "yellow")

# Create radar object
radar = Radar(400, -150, 180, 180)

# Sprites List
sprites = []

# Setup the level

game.start_level()

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

    # update camera
    camera.update(player.x, player.y)

    # Update sprites
    for sprite in sprites:
        sprite.update()

    # Check for collisions
    for sprite in sprites:
        if isinstance(sprite, Enemy) and sprite.state == "active":
            if player.is_collision(sprite):
                sprite.health -= 10
                if sprite.type == "mine":
                    player.health = 0
                else:
                    player.health -= 10
                if sprite.health <= 0:
                    sprite.reset()
                player.bounce(sprite)
            
            if missile.state == "active" and missile.is_collision(sprite):
                sprite.health -= 10
                if sprite.health <= 0:
                    sprite.reset()
                missile.reset()

        if isinstance(sprite, Powerup):
            if player.is_collision(sprite):
                pass

            if missile.state == "active" and missile.is_collision(sprite):
                missile.reset()

    # Render Sprites
    for sprite in sprites:
        sprite.render(pen, camera.x + 100, camera.y)

    game.render_border(pen, camera.x + 100, camera.y)

    # draw text
    game.render_hud(pen, 0,0)

    # Render radar

    radar.render(pen, sprites)

    # Check for end of level
    end_of_level = True
    for sprite in sprites:
        #look for active enemy
        if isinstance(sprite, Enemy) and sprite.state == "active":
            end_of_level = False
            break
    if end_of_level:
        game.level += 1
        game.start_level()
    # Update screen
    win.update()