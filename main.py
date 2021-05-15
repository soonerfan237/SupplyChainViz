import turtle
import time
import bigquery
import random
import math
from decimal import Decimal

department_color = {
    1:"green",
    2:"blue",
    3:"yellow",
    4:"red"
}

wn = turtle.Screen()
#wn.screensize(40, 40)
wn.title("Animation Demo")
wn.bgcolor("white")
wn.register_shape("truck_smaller.gif")
wn.bgpic('usa_map.gif')
wn.update()

print(wn.window_width())

results = bigquery.get_turtles()
turtles = [turtle.Turtle(visible=False) for _ in range(results.total_rows)]
turtle=0
for row in results:
    turtles[turtle].color(department_color[row['department']])
    turtles[turtle].shapesize(row['volume']/100, row['volume']/100, row['volume']/100)
    turtles[turtle].shape("circle")
    turtles[turtle].penup()
    turtles[turtle].speed(0)
    turtles[turtle].origin = [row['origin_lon'],row['origin_lat']]
    turtles[turtle].destination = [row['dest_lon'],row['dest_lat']]
    print("latitude: " + str(turtles[turtle].origin[1]))
    print("percent along lat axis??? " + str((turtles[turtle].origin[1]-29)*(turtles[turtle].origin[1]/40)/100))
    print("spot on window??? " + str(Decimal(-wn.window_width()/2)-wn.window_width()*(turtles[turtle].origin[1]-29)*(turtles[turtle].origin[1]/40)/100))

    turtles[turtle].goto(-wn.window_width()/2-float(wn.window_width()*(turtles[turtle].origin[1]+43)*(turtles[turtle].origin[1]/-110)/100)        , -wn.window_width()/2-float(wn.window_width()*(turtles[turtle].origin[1]-29)*(turtles[turtle].origin[1]/40)/100))
    #turtles[turtle].goto(10 - random.randint(-wn.window_width()/2, wn.window_width()/2), random.randint(-wn.window_width()/2, wn.window_width()/2) - 10)

    turtles[turtle].pendown()
    turtles[turtle].showturtle()
    turtles[turtle].movevector = [.01*(0-turtles[turtle].xcor()),.01*(0-turtles[turtle].ycor())]
    turtle+=1

def turn_turtle(turtle): #turns turtle toward the center of screen
    print("turning turtle")
    print(turtle.pos())
    if turtle.pos()[0] < 0:
        turtle.left(math.degrees(math.atan(-turtle.pos()[1]/-turtle.pos()[0])))
    else:
        turtle.right(180-math.degrees(math.atan(turtle.pos()[1]/turtle.pos()[0])))

def player_animate(turtle): #moves turtle forward
    time.sleep(0.001)
    turtle.forward(1)

def move_turtle(turtle, speed_factor):
    #print("moving turtle")
    turtle.goto(turtle.xcor() + turtle.movevector[0]*speed_factor, turtle.ycor() + turtle.movevector[1]*speed_factor)

#for turtle in turtles:
#    turn_turtle(turtle)

speed_factor=1
while True:
    wn.update()
    speed_factor*=1.1
    print("Main Loop")
    for turtle in turtles:
        move_turtle(turtle, speed_factor)

print("done")