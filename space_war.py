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
        self.acceleration = 0.001
        self.health = 100
        self.max_health = 100
        self.width = 20
        self.height = 20
        self.state = "active"
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
        if self.state == "active":
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

game = Game(800, 600)



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
        self.da = 0.75

    def rotate_right(self):
        self.da = -0.75

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

        self.dx = other.dx * 0.7
        self.dy = other.dy * 0.7

        other.dx = temp_dx * 0.7
        other.dy = temp_dy * 0.7

    def update(self):
        if self.state == "active":
            self.heading += self.da
            self.heading %= 360
            self.current_acc_dx = self.dx + math.cos(math.radians(self.heading)) * self.thrust
            self.current_acc_dy = self.dy + math.cos(math.radians(self.heading)) * self.thrust

            # accelerate up to max speed
            if self.current_acc_dx < self.max_dx and self.current_acc_dx > -self.max_dx:
                    self.dx += math.cos(math.radians(self.heading)) * self.thrust
            if self.current_acc_dy < self.max_dy and self.current_acc_dy > -self.max_dy:
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
        self.max_health = 30
        self.health = self.max_health
        # Create list spaning full health range and mapping it to a RGB color for a gradient healthbar
        self.colors = list(Color("red").range_to(Color("Green"), self.max_health))

    def update(self):
        if self.state == "active":
            self.heading += self.da
            self.heading %= 360

            self.dx += math.cos(math.radians(self.heading)) * self.thrust
            self.dy += math.sin(math.radians(self.heading)) * self.thrust

            self.x += self.dx
            self.y += self.dy

            self.border_col_check()

            # check health
            if self.health <= 0:
                self.reset()
    
    def reset(self):
        self.state = "inactive"


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

    # Update sprites
    for sprite in sprites:
        sprite.update()

    # Check for collisions
    for sprite in sprites:
        if isinstance(sprite, Enemy) and sprite.state == "active":
            if player.is_collision(sprite):
                sprite.health -= 10
                player.health -= 10
                player.bounce(sprite)
                player.lives -= 1
            
            if missile.state == "active" and missile.is_collision(sprite):
                sprite.health -= 10
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