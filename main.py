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

def move_turtle(turtle, speed_factor):
    #print("moving turtle")
    turtle.goto(turtle.xcor() + turtle.movevector[0]*speed_factor, turtle.ycor() + turtle.movevector[1]*speed_factor)

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
    turtles[turtle].pensize(2)
    turtles[turtle].penup()
    turtles[turtle].speed(0)
    turtles[turtle].origin = [row['origin_lon'],row['origin_lat']]
    turtles[turtle].destination = [row['dest_lon'],row['dest_lat']]
    origin_window_coords = coordinate_conversion(turtles[turtle].origin, wn.window_width())
    destination_window_coords = coordinate_conversion(turtles[turtle].destination, wn.window_width())
    turtles[turtle].goto(origin_window_coords[0],origin_window_coords[1])
    turtles[turtle].movevector = [.01*(destination_window_coords[0]-turtles[turtle].xcor()),.01*(destination_window_coords[1]-turtles[turtle].ycor())]
    turtles[turtle].pendown()
    turtles[turtle].showturtle()
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
turtles[turtle].movevector = [0,0] #the dc turtle won't move
turtles[turtle].pendown()
turtles[turtle].showturtle()

speed_factor=1.1
in_transit=True
moves=0
while True:
    wn.update()

    print("Main Loop")
    if moves < 23:
        speed_factor*=1.1
        for turtle in turtles:
            move_turtle(turtle, speed_factor)
    moves+=1


print("done")