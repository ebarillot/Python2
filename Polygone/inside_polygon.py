#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Emmanuel Barillot'

import math as m
import Tkinter as tk

# un polygone est une liste de points, dont chaque coordonnée est un couple
polygon_ex1=[(1.0,1.0), (1.0,1.5), (1.5,2.0), (2.0,1.5)]

point_guess_list = [(1.1,1.1), (2.0,2.0), (1.5,2.5), (1.6,1.3), (2.0,1.9)]

def flatten(list_of_tuple):
    """
    Pour aplatir une liste de liste ou une liste de tuples dans une liste de valeurs simples
    :param list_of_tuple: la liste de tuples à aplatir
    :return: la liste aplatie
    """
    from itertools import chain
    return list(chain.from_iterable(list_of_tuple))


def segments_from_polygon(polygon):
    polygon2 = polygon[1:]
    polygon2.append(polygon[0])
    zz = zip(polygon,polygon2)
    return zz


def calc_sinus(vect1, vect2):
    # sinus calculé à partir du produit vectoriel
    x1, y1 = (vect1[1][0] - vect1[0][0], vect1[1][1] - vect1[0][1])
    x2, y2 = (vect2[1][0] - vect2[0][0], vect2[1][1] - vect2[0][1])
    pvect = x1*y2 - x2*y1
    norm_v1 = m.sqrt(x1 * x1 + y1 * y1)
    norm_v2 = m.sqrt(x2 * x2 + y2 * y2)
    res = pvect / (norm_v1*norm_v2)
    return res



def main(point_list, polygon_ex):
    inside_list = []
    for one_point in point_list:
        segments = segments_from_polygon(polygon_ex)
        nb_summits = len(polygon_ex)
        is_inside = True
        for i in range(nb_summits):
            segment = segments[i]
            pp = segments[i][0]
            res_sinus = calc_sinus((pp,one_point),segment)
            if res_sinus < 0:
                is_inside = False
                break
        inside_list.append((one_point, is_inside))
    return inside_list


def draw(point_list,polygon):
    x0 = 2
    y0 = 2
    factor = 200
    radius = 2
    the_width=800
    the_height=600
    root = tk.Tk()
    root.title('Very simple Tkinter line')
    canvas_1 = tk.Canvas(root, width=the_width, height=the_height, background="#ffffff")
    canvas_1.grid(row=0, column=0)
    pp = flatten(polygon)
    pp2 = [x*factor for x in pp]
    pp3 = [the_height-pp2[i] if ((i+1)%2 == 0) else pp2[i] for i in range(len(pp2))]
    polygon_flat = tuple(pp3)
    canvas_1.create_polygon(polygon_flat,fill='',outline='black')
    canvas_1.create_rectangle(x0, y0, the_width-1, the_height-1)
    for point in polygon:
        canvas_1.create_oval(point[0] * factor - 1, the_height - point[1] * factor - 1,
                             point[0] * factor + 1, the_height - point[1] * factor + 1,
                             fill='black', outline='')
        canvas_1.create_text(point[0] * factor, the_height - point[1] * factor, text=str(point), anchor=tk.NW)
    for point in point_list:
        canvas_1.create_oval(point[0] * factor - radius, the_height - point[1] * factor - radius,
                             point[0] * factor + radius, the_height - point[1] * factor + radius,
                             fill='red', outline='')
        canvas_1.create_text(point[0] * factor, the_height - point[1] * factor, text=str(point), anchor=tk.NW)
    root.mainloop()


#####################
# programme principal
#####################
if __name__ == "__main__":
    res = main(point_guess_list, polygon_ex1)
    for elem in res:
        print ("{}".format(str(elem)))
    draw(point_guess_list, polygon_ex1)
