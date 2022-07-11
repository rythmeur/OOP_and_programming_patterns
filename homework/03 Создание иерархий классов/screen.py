#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)

class Vec2d():
    def __init__(self, coord_tochki):
        self.x = coord_tochki[0]
        self.y = coord_tochki[1]

    def __sub__(self, other_vector):
        """"возвращает разность двух векторов"""
        self.x -= other_vector.x
        self.y -= other_vector.y
        return Vec2d((self.x, self.y))

    def __add__(self, other_vector):
        """возвращает сумму двух векторов"""
        self.x = self.x + other_vector.x
        self.y = self.y + other_vector.y
        return Vec2d((self.x, self.y))

    def __mul__(self, k):
        """возвращает произведение вектора на число"""
        self.x = self.x * k
        self.y = self.y * k
        return Vec2d((self.x, self.y))

    def __len__(self):
        """возвращает длину вектора"""
        return int(math.sqrt(self.x * self.x + self.y * self.y))

    def int_pair(self):
        """возвращает пару координат, определяющих вектор (координаты точки конца вектора),
        координаты начальной точки вектора совпадают с началом системы координат (0, 0)"""
        return (self.x,self.y)


class Polyline():
    def __init__(self, list_of_points):
        self.list_of_points =list_of_points


    def add_point(self,single_point_Vec2d):
        # print("self.list_of_points start", self.list_of_points)
        # print ("single_point_Vec2d.int_pair()", single_point_Vec2d.int_pair())
        self.list_of_points.append(single_point_Vec2d)
        # print ("self.list_of_points end", self.list_of_points)

    def draw_points(self, style="points", width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране
        передаете список пар координат точек, функция проходит по этому списку
        и "наносит" на дисплей линии соединяющие каждую пару точек с помощью pygame.draw.line"""
        if style == "line":
            for p_n in range(-1, len( self.list_of_points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 (int( self.list_of_points[p_n].int_pair()[0]), int( self.list_of_points[p_n].int_pair()[1])),
                                 (int( self.list_of_points[p_n + 1].int_pair()[0]), int( self.list_of_points[p_n + 1].int_pair()[1])), width)

        elif style == "points":
            for p in  self.list_of_points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(p.int_pair()[0]), int(p.int_pair()[1])), width)

    def draw_help(self):
        """функция отрисовки экрана справки программы"""
        gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["", ""])
        data.append([str(steps), "Current points"])

        pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

    def set_points(self, speeds):
        """функция перерасчета координат опорных точек"""
        for p in range(len( self.list_of_points)):
            self.list_of_points[p] = self.list_of_points[p] + speeds.list_of_points[p]
            if self.list_of_points[p].int_pair()[0] > SCREEN_DIM[0] or  self.list_of_points[p].int_pair()[0] < 0:
                speeds.list_of_points[p].x = - speeds.list_of_points[p].int_pair()[0]
                speeds.list_of_points[p].y = speeds.list_of_points[p].int_pair()[1]
                # speeds.list_of_points[p] = (- speeds.list_of_points[p][0], speeds.list_of_points[p][1])
            if self.list_of_points[p].int_pair()[1] > SCREEN_DIM[1] or  self.list_of_points[p].int_pair()[1] < 0:
                speeds.list_of_points[p].x = speeds.list_of_points[p].int_pair()[0]
                speeds.list_of_points[p].y = -speeds.list_of_points[p].int_pair()[1]
                # speeds.list_of_points[p] = (speeds.list_of_points[p][0], -speeds[p].list_of_points[1])



class Knot(Polyline):
    def __init__(self, list_of_points):
        super().__init__(list_of_points)
        self.list_of_points = list_of_points

    def get_point(self, points, alpha, deg=None):  # возвращаем одну точку сглаживания
        if deg is None:
            deg = len(points) - 1
            # print ("deg", deg)
        if deg == 0:
            return points[0] # возврат координат первой точки из трех
        # print ("(self.list_of_points[deg] * alpha) + (self.get_point(alpha, deg - 1) * (1 - alpha))", (self.list_of_points[deg] * alpha) + (self.get_point(alpha, deg - 1) * (1 - alpha)))
        return  (points[deg] * alpha) + (self.get_point(points, alpha, deg - 1) * (1 - alpha))

    def get_points(self, base_points, count):  # возвращает список точек сглаживания, кол-во = steps - это точки сглаживания
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        # print ("res get_points", res)
        return res

    def get_knot(self, count):  # возвращает набор всех точек которые надо нарисовать, состоящий только из точек сглаживания
        if len(self.list_of_points) < 3:
            return []
        res = []
        for i in range(-2, len(self.list_of_points) - 2):
            ptn = []
            ptn.append(((self.list_of_points[i] + self.list_of_points[i + 1]) * 0.5))
            ptn.append(self.list_of_points[i + 1])
            ptn.append( ( (self.list_of_points[i + 1] + self.list_of_points[i + 2]) * 0.5))

            res.extend(self.get_points(ptn,count))
        print ("len(res), len(self.list_of_points)",len(res), len(self.list_of_points) )
        new_knot=Knot (res)
        return new_knot




# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":



    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 1
    working = True
    points = []

    knot_class = Knot([])

    speeds = []
    knot_class_speeds = Knot([])

    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                a = Vec2d(event.pos)
                # polyl_class.add_point(a)
                knot_class.add_point(a)
                b =  Vec2d((random.random() * 2, random.random() * 2))
                knot_class_speeds.add_point(b)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        # draw_points(points)
        # draw_points(get_knot(points, steps), "line", 3, color)

        # polyl_class.draw_points()
        # polyl_class.draw_points("line", 3, color)
        knot_class.draw_points()
        # knot_class.draw_points("line", 3, color)

        # print ("knot_class.get_knot(  steps)", knot_class.get_knot(  steps))
        c = knot_class.get_knot(steps)
        print (c, type(c))
        if isinstance(c, Knot):
            c.draw_points("line", 3, color )

        # knot_class.get_knot(steps)
        # knot_class.get_knot(  steps).draw_points( "line", 3, color)




        if not pause:
            # polyl_class.set_points(speeds)
            knot_class.set_points(knot_class_speeds)
        if show_help:
            # polyl_class.draw_help()
            knot_class.draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
