#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sugargame
import sugargame.canvas
from sugar.activity import activity

import conozco

class Activity(activity.Activity):

    def __init__(self, handle):

        activity.Activity.__init__(self, handle)

        self.actividad = conozco.Conozco()

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



