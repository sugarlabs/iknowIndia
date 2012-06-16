#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sugargame
import sugargame.canvas
from sugar.activity import activity

import conozcoin

class Activity(activity.Activity):

    def __init__(self, handle):

        activity.Activity.__init__(self, handle)

        self.actividad = conozcoin.ConozcoIn()

        self._pygamecanvas = sugargame.canvas.PygameCanvas(self)

        self.set_canvas(self._pygamecanvas)

        self._pygamecanvas.grab_focus()

        self._pygamecanvas.run_pygame(self.actividad.principal)


    def read_file(self, file_path):
        pass
        #self.actividad.read_file(file_path)
        
    def write_file(self, file_path):
        pass
        #self.actividad.write_file(file_path)



