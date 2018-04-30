def triangle(a,b,c,niveau):
    turtle.penup();turtle.setpos(a);turtle.pendown();
    turtle.setpos(b);turtle.setpos(c);turtle.setpos(a);
    if niveau:
        niveau=niveau-1
        ab=[.5*(a[0]+b[0]), .5*(a[1]+b[1])]
        ac=[.5*(a[0]+c[0]), .5*(a[1]+c[1])]
        bc=[.5*(b[0]+c[0]), .5*(b[1]+c[1])]
        triangle(ab,bc,ac,niveau)
        


import turtle
turtle.pensize(5)
turtle.hideturtle()
a=[0,300];b=[400,-100];c=[-300,90]
triangle(a,b,c,7)
turtle.exitonclick()
