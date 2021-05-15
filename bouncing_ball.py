import turtle

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("bouncing ball")
print(wn.window_width())

ball=turtle.Turtle()
ball.shape("circle")
ball.penup()
ball.speed(0)
ball.color("green")
ball.goto(0,200)
ball.dy=0

gravity=0.1

while True:
    ball.dy -= gravity
    ball.sety(ball.ycor() + ball.dy)

    if ball.ycor() < -300:
        ball.dy *= -1