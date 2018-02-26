#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sugargame
import sugargame.canvas
import pygame
from sugar3.activity import activity

import conozco

class Activity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        self.max_participants = 1
        self.game = conozco.Conozco(self)
        self.game.canvas = sugargame.canvas.PygameCanvas(self,
                main=self.game.principal,
                modules=[pygame.display, pygame.font])
        self.set_canvas(self.game.canvas)
        self.game.canvas.grab_focus()
