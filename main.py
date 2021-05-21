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

def coordinate_conversion(lat_long, window_width):
    #longitude is range 73 to 122 (49 difference)
    #longitude is x coords (left and right)
    longitude = float(lat_long[0])
    xcor = ((longitude-73)/49*-window_width)+(window_width/2)
    #latitude is range 29-40 (11 difference)
    #latitude is y coords (up and down)
    latitude = float(lat_long[1])
    ycor = ((latitude-29)/11*window_width)-(window_width/2)

    window_coords=[xcor,ycor]
    return window_coords

wn = turtle.Screen()
#wn.screensize(40, 40)
wn.title("Animation Demo")
wn.bgcolor("white")
wn.register_shape('warehouse.gif')
wn.bgpic('usa_map.gif')
wn.update()

print("window width: " + str(wn.window_width()))

results = bigquery.get_turtles()
turtles = [turtle.Turtle(visible=False) for _ in range(results.total_rows+1)] #the plus 1 here is for the extra turtle which is the destination DC
turtle=0
for row in results:
    turtles[turtle].type = "truck" #turtles will be labeled either as trucks or DCs
    turtles[turtle].color(department_color[row['department']])
    turtles[turtle].shapesize(row['volume']/100, row['volume']/100, row['volume']/100)
    turtles[turtle].shape("circle")
    turtles[turtle].penup()
    turtles[turtle].speed(0)
    turtles[turtle].origin = [row['origin_lon'],row['origin_lat']]
    turtles[turtle].destination = [row['dest_lon'],row['dest_lat']]
    print("origin longitude: " + str(turtles[turtle].origin[0]))
    print("origin latitude: " + str(turtles[turtle].origin[1]))
    origin_window_coords = coordinate_conversion(turtles[turtle].origin, wn.window_width())
    destination_window_coords = coordinate_conversion(turtles[turtle].destination, wn.window_width())
    turtles[turtle].goto(origin_window_coords[0],origin_window_coords[1])
    turtles[turtle].pendown()
    turtles[turtle].showturtle()

    turtles[turtle].movevector = [.01*(destination_window_coords[0]-turtles[turtle].xcor()),.01*(destination_window_coords[1]-turtles[turtle].ycor())]
    turtle+=1

#this part creates the turtle that will represent the destination
#only a single destination supported here which is grabbed from final row
turtles[turtle].type = "dc"
turtles[turtle].shape("warehouse.gif")
turtles[turtle].penup()
turtles[turtle].speed(0)
turtles[turtle].destination = [row['dest_lon'],row['dest_lat']]
print("DC longitude: " + str(turtles[turtle].destination[0]))
print("DC latitude: " + str(turtles[turtle].destination[1]))
dc_window_coords = coordinate_conversion(turtles[turtle].destination, wn.window_width())
turtles[turtle].goto(dc_window_coords[0],dc_window_coords[1])
turtles[turtle].pendown()
turtles[turtle].showturtle()
turtles[turtle].movevector = [0,0] #the dc turtle won't move

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