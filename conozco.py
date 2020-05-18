#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Conozco
# Copyright (C) 2008, 2012 Gabriel Eirea
# Copyright (C) 2011, 2012 Alan Aguiar
# Copyright (C) 2020, Srevin Saju
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information:
# Gabriel Eirea geirea@gmail.com
# Alan Aguiar alanjas@hotmail.com

import configparser
import gettext
import imp
import os
import random
import time

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

import pygame

# constantes
RADIO = 10
RADIO2 = RADIO ** 2
XMAPAMAX = 786
DXPANEL = 414
XCENTROPANEL = 1002
YGLOBITO = 100
DXBICHO = 255
DYBICHO = 412
XBICHO = 1200 - DXBICHO
YBICHO = 900 - DYBICHO - 80
XPUERTA = 786
YPUERTA = 279
XBARRA_P = 840
YBARRA_P = 790
ABARRA_P = 40
YTEXTO = 370
XBARRA_A = XMAPAMAX + 20
YBARRA_A = 900 - ABARRA_P - 20
ABARRA_A = DXPANEL - 40
# control
TOTALAVANCE = 7
EVENTORESPUESTA = pygame.USEREVENT + 1
TIEMPORESPUESTA = 2300
EVENTODESPEGUE = EVENTORESPUESTA + 1
EVENTOREFRESCO = EVENTODESPEGUE + 1
TIEMPOREFRESCO = 250
ESTADONORMAL = 1
ESTADOPESTANAS = 2
ESTADOFRENTE = 3
ESTADODESPEGUE = 4
# paths
CAMINORECURSOS = "recursos"
CAMINOCOMUN = "comun"
CAMINOFUENTES = "fuentes"
CAMINODATOS = "datos"
CAMINOIMAGENES = "imagenes"
CAMINOSONIDOS = "sonidos"
ARCHIVONIVELES = "levels"
ARCHIVOEXPLORACIONES = "explorations"
# colors
COLORNOMBREDEPTO = (10, 10, 10)
COLORNOMBRECAPITAL = (10, 10, 10)
COLORNOMBRERIO = (10, 10, 10)
COLORNOMBRERUTA = (10, 10, 10)
COLORNOMBREELEVACION = (10, 10, 10)
COLORESTADISTICAS1 = (10, 10, 150)
COLORESTADISTICAS2 = (10, 10, 10)
COLORPREGUNTAS = (80, 80, 155)
COLORPANEL = (156, 158, 172)
COLORBARRA_P = (255, 0, 0)
COLORBARRA_A = (0, 0, 255)
COLORBARRA_C = (0, 0, 0)
COLOR_FONDO = (0, 0, 0)
COLOR_ACT_NAME = (255, 255, 255)
COLOR_OPTION_B = (20, 20, 20)
COLOR_OPTION_T = (200, 100, 100)
COLOR_BUTTON_B = (20, 20, 20)
COLOR_BUTTON_T = (100, 200, 100)
COLOR_NEXT = (100, 100, 200)
COLOR_STAT_N = (100, 100, 200)
COLOR_SKIP = (255, 155, 155)
COLOR_CREDITS = (155, 155, 255)
COLOR_SHOW_ALL = (100, 20, 20)

# variables globales para adaptar la display a distintas resoluciones
scale = 1
shift_x = 0
shift_y = 0
xo_resolution = True

clock = pygame.time.Clock()


class Point():
    """
    [EN] Class for geographic objects that can be defined as a point.
    The position is given by a pair of (x, y) coordinates measured in pixels
    within the map.

    [ES] Clase para objetos geograficos que se pueden definir como un point.
    La position esta dada por un par de coordenadas (x,y) medida en pixels
    dentro del mapa.
    """

    def __init__(self, name, kind, symbol, position, position_text):
        self.name = name
        self.kind = int(kind)
        self.position = (int(int(position[0]) * scale + shift_x),
                         int(int(position[1]) * scale + shift_y))
        self.position_text = (int(int(position_text[0]) * scale) + self.position[0],
                              int(int(position_text[1]) * scale) + self.position[1])
        self.symbol = symbol

    def current_position(self, pos):
        """
        [EN] Returns a boolean indicating if it is in the coordinate pos,

        [ES] Devuelve un booleano indicando si esta en la coordenada pos,
        la precision viene dada por la constante global RADIO
        """
        if (pos[0] - self.position[0]) ** 2 + \
                (pos[1] - self.position[1]) ** 2 < RADIO2:
            return True
        else:
            return False

    def display(self, display, flipNow):
        """Draw a point at its position"""
        display.blit(
            self.symbol,
            (self.position[0] - 8,
             self.position[1] - 8))
        if flipNow:
            pygame.display.flip()

    def display_name(self, display, source, color, flipNow):
        """Write the name of point in your position"""
        text = source.render(self.name, 1, color)
        textrect = text.get_rect()
        textrect.center = (self.position_text[0], self.position_text[1])
        display.blit(text, textrect)
        if flipNow:
            pygame.display.flip()


class Zone():
    """
    [EN] Class for geographic objects that can be defined as a zone.

    [ES] Clase para objetos geograficos que se pueden definir como una zona.
    La position esta dada por una image bitmap pintada con un color
    especifico, dado por la clave (valor 0 a 255 del componente rojo).
    """

    def __init__(self, mapa, name, key_color, kind, position, rotation):
        self.mapa = mapa  # does this make a copy in memory or not ????
        self.name = name
        self.key_color = int(key_color)
        self.kind = int(kind)
        self.position = (int(int(position[0]) * scale + shift_x),
                         int(int(position[1]) * scale + shift_y))
        self.rotation = int(rotation)

    def currentPosition(self, pos):
        """Returns True if the pos coordinate is in the zone"""
        if pos[0] < XMAPAMAX * scale + shift_x:
            try:
                colorAca = self.mapa.get_at((int(pos[0] - shift_x),
                                             int(pos[1] - shift_y)))
            except BaseException:  # probably click outside the image
                return False
            if colorAca[0] == self.key_color:
                return True
            else:
                return False
        else:
            return False

    def display_name(self, display, source, color, flipNow):
        """Write the name of the zone in its position"""
        text = source.render(self.name, 1, color)
        textrot = pygame.transform.rotate(text, self.rotation)
        textrect = textrot.get_rect()
        textrect.center = (self.position[0], self.position[1])
        display.blit(textrot, textrect)
        if flipNow:
            pygame.display.flip()


class Level():
    """
    [EN] Class to define the levels of the game.
    Each level has an initial drawing, the elements can be

    [ES] Clase para definir los niveles del game.
    Cada level tiene un dibujo inicial, los elementos pueden estar
    etiquetados con el name o no, y un conjunto de questions.
    """

    def __init__(self, name):
        self.name = name
        self.initial_display = list()
        self.initial_name = list()
        self.questions = list()
        self.current_question_index = 0
        self.active_elements = list()

    def prepare_questions(self):
        """This method is used to prepare the list of questions at random."""
        random.shuffle(self.questions)

    def next_question(self, list_suffixes, list_prefixes):
        """Prepare the text of the next question"""
        self.current_question = self.questions[self.current_question_index]
        self.sufijoActual = random.randint(1, len(list_suffixes)) - 1
        self.prefijoActual = random.randint(1, len(list_prefixes)) - 1
        lines = list_prefixes[self.prefijoActual].split("\n")
        lines.extend(self.current_question[0].split("\n"))
        lines.extend(list_suffixes[self.sufijoActual].split("\n"))
        self.current_question_index = self.current_question_index + 1
        if self.current_question_index == len(self.questions):
            self.current_question_index = 0
        return lines

    def return_help(self):
        """Returns the help line"""
        self.current_question = self.questions[self.current_question_index - 1]
        return self.current_question[3].split("\n")


class Conozco():
    """
    [EN] Main class of the game.
    [ES] Clase principal del game.
    """

    def show_text(self, texto, source, position, color):
        """Show text in a certain position"""
        text = source.render(texto, 1, color)
        textrect = text.get_rect()
        textrect.center = position
        self.display.blit(text, textrect)

    def load_info(self):
        """Upload images and data for each country"""
        r_path = os.path.join(self.data_path, self.directories + '.py')
        a_path = os.path.abspath(r_path)
        f = None
        try:
            f = imp.load_source(self.directories, a_path)
        except BaseException:
            print(_('Cannot open %s') % self.directories)

        if f:
            lugares = []
            if hasattr(f, 'CAPITALS'):
                lugares = lugares + f.CAPITALS
            if hasattr(f, 'CITIES'):
                lugares = lugares + f.CITIES
            if hasattr(f, 'HILLS'):
                lugares = lugares + f.HILLS
            self.list_places = list()
            for c in lugares:
                placeName = c[0]
                posx = c[1]
                posy = c[2]
                kind = c[3]
                incx = c[4]
                incy = c[5]
                if kind == 0:
                    symbol = self.symbolCapitalN
                elif kind == 1:
                    symbol = self.symbolCapitalD
                elif kind == 2:
                    symbol = self.symbolCity
                elif kind == 5:
                    symbol = self.symbolHill
                else:
                    symbol = self.symbolCity

                new_place = Point(placeName, kind, symbol,
                                  (posx, posy), (incx, incy))
                self.list_places.append(new_place)

            if hasattr(f, 'STATES'):
                self.apartments = self.load_image("deptos.png")
                self.apartmentsLineas = self.load_image("deptosLineas.png")
                self.listDeptos = list()
                for d in f.STATES:
                    nameDepto = d[0]
                    key_color = d[1]
                    posx = d[2]
                    posy = d[3]
                    rotation = d[4]
                    nuevoDepto = Zone(self.apartments, nameDepto,
                                      key_color, 1, (posx, posy), rotation)
                    self.listDeptos.append(nuevoDepto)

            if hasattr(f, 'CUCHILLAS'):
                self.cuchillas = self.load_image("cuchillas.png")
                self.cuchillasDetected = self.load_image(
                    "cuchillasDetectar.png")
                self.list_blades = list()
                for c in f.CUCHILLAS:
                    nameCuchilla = c[0]
                    key_color = c[1]
                    posx = c[2]
                    posy = c[3]
                    rotation = c[4]
                    newCuchilla = Zone(self.cuchillasDetected, nameCuchilla,
                                       key_color, 4, (posx, posy), rotation)
                    self.list_blades.append(newCuchilla)

            if hasattr(f, 'RIVERS'):
                self.rivers = self.load_image("rios.png")
                self.riversDetected = self.load_image("riosDetectar.png")
                self.listRivers = list()
                for r in f.RIVERS:
                    nameRiver = r[0]
                    key_color = r[1]
                    posx = r[2]
                    posy = r[3]
                    rotation = r[4]
                    newRiver = Zone(self.riversDetected, nameRiver,
                                    key_color, 3, (posx, posy), rotation)
                    self.listRivers.append(newRiver)

            if hasattr(f, 'ROUTES'):
                self.routes = self.load_image("rutas.png")
                self.routesDetected = self.load_image("rutasDetectar.png")
                self.listRutas = list()
                for r in f.ROUTES:
                    nameRuta = r[0]
                    key_color = r[1]
                    posx = r[2]
                    posy = r[3]
                    rotation = r[4]
                    newRoute = Zone(self.routesDetected, nameRuta,
                                    key_color, 6, (posx, posy), rotation)
                    self.listRutas.append(newRoute)
            self.list_statistics = list()
            if hasattr(f, 'STATS'):
                for e in f.STATS:
                    p1 = e[0]
                    p2 = e[1]
                    self.list_statistics.append((p1, p2))

    def loadListDirectories(self):
        """Load the directory list with the different maps"""
        self.directories_list = list()
        self.directory_name_list = list()
        listTemp = sorted(os.listdir(CAMINORECURSOS))
        for d in listTemp:
            if not (d == 'comun'):
                r_path = os.path.join(CAMINORECURSOS, d, 'datos', d + '.py')
                a_path = os.path.abspath(r_path)
                f = None
                try:
                    f = imp.load_source(d, a_path)
                except BaseException:
                    print(_('Cannot open %s') % d)

                if hasattr(f, 'NAME'):
                    name = f.NAME
                    self.directory_name_list.append(name)
                    self.directories_list.append(d)

    def load_commons(self):

        self.list_prefixes = list()
        self.list_suffixes = list()
        self.correct_list = list()
        self.listMal = list()
        self.listEndB = list()
        self.listEndM = list()
        self.presentation_list = list()
        self.credit_list = list()

        r_path = os.path.join(CAMINORECURSOS, CAMINOCOMUN,
                              'datos', 'commons.py')
        a_path = os.path.abspath(r_path)
        f = None
        try:
            f = imp.load_source('commons', a_path)
        except BaseException:
            print(_('Cannot open %s') % 'commons')

        if f:
            if hasattr(f, 'ACTIVITY_NAME'):
                e = f.ACTIVITY_NAME
                self.activity_name = e
            if hasattr(f, 'PREFIX'):
                for e in f.PREFIX:
                    e1 = e
                    self.list_prefixes.append(e1)
            if hasattr(f, 'SUFIX'):
                for e in f.SUFIX:
                    e1 = e
                    self.list_suffixes.append(e1)
            if hasattr(f, 'CORRECT'):
                for e in f.CORRECT:
                    e1 = e
                    self.correct_list.append(e1)
            if hasattr(f, 'WRONG'):
                for e in f.WRONG:
                    e1 = e
                    self.listMal.append(e1)
            if hasattr(f, 'BYE_C'):
                for e in f.BYE_C:
                    e1 = e
                    self.listEndB.append(e1)
            if hasattr(f, 'BYE_W'):
                for e in f.BYE_W:
                    e1 = e
                    self.listEndM.append(e1)
            if hasattr(f, 'PRESENTATION'):
                for e in f.PRESENTATION:
                    e1 = e
                    self.presentation_list.append(e1)
            if hasattr(f, 'CREDITS'):
                for e in f.CREDITS:
                    e1 = e
                    self.credit_list.append(e1)

        self.suffixTotal = len(self.list_suffixes)
        self.prefixTotal = len(self.list_prefixes)
        self.correctTotal = len(self.correct_list)
        self.wrongTotal = len(self.listMal)
        self.numeroEndB = len(self.listEndB)
        self.numeroEndM = len(self.listEndM)

    def loadLevels(self):
        """Carga los niveles del archive de configuracion"""
        self.levels_list = list()

        r_path = os.path.join(self.data_path, ARCHIVONIVELES + '.py')
        a_path = os.path.abspath(r_path)
        f = None
        try:
            f = imp.load_source(ARCHIVONIVELES, a_path)
        except BaseException:
            print(_('Cannot open %s') % ARCHIVONIVELES)

        if hasattr(f, 'LEVELS'):
            for ln in f.LEVELS:
                index = ln[0]
                nameLevel = str(ln[1])
                new_level = Level(nameLevel)

                listDibujos = ln[2]
                for i in listDibujos:
                    new_level.initial_display.append(i.strip())

                name_list = ln[3]
                for i in name_list:
                    new_level.initial_name.append(i.strip())

                listquestions = ln[4]

                if (index == 1):
                    for i in listquestions:
                        texto = i[0]
                        kind = i[1]
                        respuesta = i[2]
                        help = i[3]
                        respuesta = str(i[2])
                        help = str(i[3])
                        new_level.questions.append(
                            (texto, kind, respuesta, help))
                else:
                    for i in listquestions:
                        respuesta = i[0]
                        help = i[1]
                        if index == 2:
                            kind = 2
                            texto = _('the city of\n%s') % respuesta
                        elif index == 7:
                            kind = 1
                            texto = _('the department of\n%s') % respuesta
                        elif index == 8:
                            kind = 1
                            texto = _('the province of\n%s') % respuesta
                        elif index == 9:
                            kind = 1
                            texto = _('the district of\n%s') % respuesta
                        elif index == 10:
                            kind = 1
                            texto = _('the state of\n%s') % respuesta
                        elif index == 11:
                            kind = 1
                            texto = _('the region of\n%s') % respuesta
                        elif index == 12:
                            kind = 1
                            texto = _('the parish of\n%s') % respuesta
                        elif index == 14:
                            kind = 1
                            texto = _('the taluka of\n%s') % respuesta
                        elif index == 6:
                            kind = 1
                            texto = _('the municipality of\n%s') % respuesta
                        elif index == 4:
                            kind = 3
                            texto = _('the %s') % respuesta
                        elif index == 5:
                            kind = 6
                            texto = _('the %(route)s') % {'route': respuesta}

                        new_level.questions.append(
                            (texto, kind, respuesta, help))

                self.levels_list.append(new_level)

        self.current_level_idx = 0
        self.level_number = len(self.levels_list)

    def load_scans(self):
        """Carga los niveles de exploracion del archive de configuracion"""
        self.exploration_list = list()

        r_path = os.path.join(self.data_path, ARCHIVOEXPLORACIONES + '.py')
        a_path = os.path.abspath(r_path)
        f = None
        try:
            f = imp.load_source(ARCHIVOEXPLORACIONES, a_path)
        except BaseException:
            print(_('Cannot open %s') % ARCHIVOEXPLORACIONES)

        if hasattr(f, 'EXPLORATIONS'):
            for e in f.EXPLORATIONS:
                nameLevel = e[0]
                new_level = Level(nameLevel)

                listDibujos = e[1]
                for i in listDibujos:
                    new_level.initial_display.append(i.strip())

                name_list = e[2]
                for i in name_list:
                    new_level.initial_name.append(i.strip())

                name_list = e[3]
                for i in name_list:
                    new_level.active_elements.append(i.strip())

                self.exploration_list.append(new_level)

        self.numeroExploraciones = len(self.exploration_list)

    def displayAbout(self):
        """Screen with game data, credits, etc."""
        self.displayTemp = pygame.Surface(
            (self.screen_width, self.screen_height))
        self.displayTemp.blit(self.display, (0, 0))
        self.display.fill(COLOR_FONDO)
        self.display.blit(self.terron,
                          (int(20 * scale + shift_x),
                           int(20 * scale + shift_y)))
        self.display.blit(self.jp1,
                          (int(925 * scale + shift_x),
                           int(468 * scale + shift_y)))
        self.show_text(_("About %s") % self.activity_name,
                       self.source40,
                       (int(600 * scale + shift_x),
                        int(100 * scale + shift_y)),
                       COLOR_ACT_NAME)

        yLinea = int(200 * scale + shift_y)
        for linea in self.credit_list:
            self.show_text(linea.strip(),
                           self.source32,
                           (int(600 * scale + shift_x), yLinea),
                           COLOR_CREDITS)
            yLinea = yLinea + int(40 * scale)

        self.show_text(_("Press any key to return"),
                       self.source32,
                       (int(600 * scale + shift_x),
                        int(800 * scale + shift_y)),
                       COLOR_SKIP)
        pygame.display.flip()
        while True:
            clock.tick(20)
            while Gtk.events_pending():
                Gtk.main_iteration()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound:
                        self.click.play()
                    self.display.blit(self.displayTemp, (0, 0))
                    pygame.display.flip()
                    return
                elif event.type == pygame.QUIT:
                    if self.sound:
                        self.click.play()
                    self.save_stats()
                    return 1
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()

    def displayStats(self):
        """Pantalla con los datos del game, creditos, etc"""
        self.displayTemp = pygame.Surface(
            (self.screen_width, self.screen_height))
        self.displayTemp.blit(self.display, (0, 0))
        self.display.fill(COLOR_FONDO)
        self.display.blit(self.jp1,
                          (int(925 * scale + shift_x),
                           int(468 * scale + shift_y)))
        msg = _("Stats of %s") % self.activity_name
        self.show_text(msg,
                       self.source40,
                       (int(600 * scale + shift_x),
                        int(100 * scale + shift_y)),
                       COLOR_ACT_NAME)
        msg = _('Total score: %s') % self._score
        self.show_text(msg,
                       self.source32,
                       (int(400 * scale + shift_x),
                        int(300 * scale + shift_y)),
                       COLOR_STAT_N)
        msg = _('Game average score: %s') % self._average
        self.show_text(msg,
                       self.source32,
                       (int(400 * scale + shift_x),
                        int(350 * scale + shift_y)),
                       COLOR_STAT_N)
        msg = _('Times using Explore Mode: %s') % self._explore_times
        self.show_text(msg,
                       self.source32,
                       (int(400 * scale + shift_x),
                        int(400 * scale + shift_y)),
                       COLOR_STAT_N)
        msg = _('Places Explored: %s') % self._explore_places
        self.show_text(msg,
                       self.source32,
                       (int(400 * scale + shift_x),
                        int(450 * scale + shift_y)),
                       COLOR_STAT_N)
        msg = _('Times using Game Mode: %s') % self._game_times
        self.show_text(msg,
                       self.source32,
                       (int(400 * scale + shift_x),
                        int(500 * scale + shift_y)),
                       COLOR_STAT_N)
        t = int(time.time() - self._init_time) / 60
        t = t + self._time
        msg = _('Total time: %s minutes') % t
        self.show_text(msg,
                       self.source32,
                       (int(400 * scale + shift_x),
                        int(550 * scale + shift_y)),
                       COLOR_STAT_N)

        self.show_text(_("Press any key to return"),
                       self.source32,
                       (int(600 * scale + shift_x),
                        int(800 * scale + shift_y)),
                       COLOR_SKIP)

        pygame.display.flip()
        while True:
            clock.tick(20)
            while Gtk.events_pending():
                Gtk.main_iteration()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound:
                        self.click.play()
                    self.display.blit(self.displayTemp, (0, 0))
                    pygame.display.flip()
                    return
                elif event.type == pygame.QUIT:
                    if self.sound:
                        self.click.play()
                    self.save_stats()
                    return 1
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()

    def displayInitial(self):
        """Screen with the main menu of the game"""
        self.display.fill(COLOR_FONDO)
        self.show_text(self.activity_name,
                       self.source60,
                       (int(600 * scale + shift_x),
                        int(80 * scale + shift_y)),
                       COLOR_ACT_NAME)
        self.show_text(_("You have chosen the map ") +
                       self.directory_name_list
                       [self.directory_index],
                       self.source40,
                       (int(600 * scale + shift_x), int(140 * scale + shift_y)),
                       COLOR_OPTION_T)
        self.show_text(_("Play"),
                       self.source60,
                       (int(300 * scale + shift_x),
                        int(220 * scale + shift_y)),
                       COLOR_OPTION_T)
        yList = int(300 * scale + shift_y)
        for n in self.levels_list:
            self.display.fill(COLOR_OPTION_B,
                              (int(10 * scale + shift_x),
                               yList - int(24 * scale),
                               int(590 * scale),
                               int(48 * scale)))
            self.show_text(n.name,
                           self.source40,
                           (int(300 * scale + shift_x), yList),
                           COLOR_OPTION_T)
            yList += int(50 * scale)
        self.show_text(_("Explore"), self.source60, (int(
            900 * scale + shift_x), int(220 * scale + shift_y)), COLOR_NEXT)
        yList = int(300 * scale + shift_y)
        for n in self.exploration_list:
            self.display.fill(COLOR_OPTION_B,
                              (int(610 * scale + shift_x),
                               yList - int(24 * scale),
                               int(590 * scale),
                               int(48 * scale)))
            self.show_text(n.name,
                           self.source40,
                           (int(900 * scale + shift_x), yList),
                           COLOR_NEXT)
            yList += int(50 * scale)
            # about button
            self.display.fill(COLOR_BUTTON_B,
                              (int(20 * scale + shift_x),
                               int(801 * scale + shift_y),
                               int(370 * scale),
                               int(48 * scale)))
            self.show_text(_("About this game"), self.source40, (int(
                205 * scale + shift_x), int(825 * scale + shift_y)), COLOR_BUTTON_T)
            # stats button
            self.display.fill(COLOR_BUTTON_B,
                              (int(420 * scale + shift_x),
                               int(801 * scale + shift_y),
                               int(370 * scale),
                               int(48 * scale)))
            self.show_text(_("Stats"),
                           self.source40,
                           (int(605 * scale + shift_x),
                            int(825 * scale + shift_y)),
                           COLOR_BUTTON_T)
            # return button
            self.display.fill(COLOR_BUTTON_B,
                              (int(820 * scale + shift_x),
                               int(801 * scale + shift_y),
                               int(370 * scale),
                               int(48 * scale)))
            self.show_text(_("Return"),
                           self.source40,
                           (int(1005 * scale + shift_x),
                            int(825 * scale + shift_y)),
                           COLOR_BUTTON_T)
        pygame.display.flip()
        while True:
            clock.tick(20)

            while Gtk.events_pending():
                Gtk.main_iteration()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == 27:  # escape: volver
                        if self.sound:
                            self.click.play()
                        self.choose_directory = True
                        return
                elif event.type == pygame.QUIT:
                    if self.sound:
                        self.click.play()
                    self.save_stats()
                    return 1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound:
                        self.click.play()
                    pos = event.pos
                    # zona de opciones
                    if pos[1] < 800 * scale + shift_y:
                        if pos[1] > 275 * scale + shift_y:
                            if pos[0] < 600 * scale + \
                                    shift_x:  # primera columna
                                if pos[1] < 275 * scale + shift_y + \
                                        len(self.levels_list) * 50 * scale:  # level
                                    self.current_level_idx = \
                                        int((pos[1] - int(275 * scale + shift_y)) //
                                            int(50 * scale))
                                    self.play = True
                                    return
                            else:  # segunda columna
                                if pos[1] < 275 * scale + shift_y + \
                                        len(self.exploration_list) * 50 * scale:
                                    # level de exploracion
                                    self.current_level_idx = \
                                        int((pos[1] - int(275 * scale + shift_y)) //
                                            int(50 * scale))
                                    self.play = False
                                    return
                    # buttons zone
                    else:
                        if pos[1] < 850 * scale + shift_y:
                            if pos[0] > 20 * scale + shift_x and \
                                    pos[0] < 390 * scale + shift_x:
                                if self.displayAbout() == 1:
                                    return  # acerca
                            elif pos[0] > 420 * scale + shift_x and \
                                    pos[0] < 790 * scale + shift_x:
                                if self.displayStats() == 1:
                                    return  # stats
                            elif pos[0] > 820 * scale + shift_x and \
                                    pos[0] < 1190 * scale + shift_x:
                                self.choose_directory = True
                                return
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()

    def dispay_directories(self):
        """Directory menu screen"""
        self.display.fill(COLOR_FONDO)
        self.show_text(self.activity_name, self.source60, (int(
            600 * scale + shift_x), int(80 * scale + shift_y)), COLOR_ACT_NAME)
        self.show_text(_("Choose the map to use"), self.source40, (int(
            600 * scale + shift_x), int(140 * scale + shift_y)), COLOR_OPTION_T)
        nDirectorios = len(self.directory_name_list)
        directories_page = self.dirPage
        while True:
            while Gtk.events_pending():
                Gtk.main_iteration()
            yList = int(200 * scale + shift_y)
            self.display.fill(COLOR_FONDO,
                              (int(shift_x), yList - int(24 * scale),
                               int(1200 * scale), int(600 * scale)))
            if directories_page == 0:
                is_previous_page_active = False
            else:
                is_previous_page_active = True
            nextActivePage = False
            if is_previous_page_active:
                self.display.fill(COLOR_OPTION_B,
                                  (int(10 * scale + shift_x),
                                   yList - int(24 * scale),
                                   int(590 * scale),
                                   int(48 * scale)))
                self.show_text("<<< " + _("Previous page"),
                               self.source40,
                               (int(300 * scale + shift_x), yList),
                               COLOR_NEXT)
            yList += int(50 * scale)
            dirIndex = directories_page * 20
            terminate = False
            while not terminate:
                self.display.fill(COLOR_OPTION_B,
                                  (int(10 * scale + shift_x),
                                   yList - int(24 * scale),
                                   int(590 * scale),
                                   int(48 * scale)))
                self.show_text(self.directory_name_list[dirIndex],
                               self.source40,
                               (int(300 * scale + shift_x), yList),
                               COLOR_OPTION_T)
                yList += int(50 * scale)
                dirIndex = dirIndex + 1
                if dirIndex == nDirectorios or \
                        dirIndex == directories_page * 20 + 10:
                    terminate = True
            if dirIndex == directories_page * 20 + 10 and \
                    not dirIndex == nDirectorios:
                nDirectoriosCol1 = 10
                yList = int(250 * scale + shift_y)
                terminate = False
                while not terminate:
                    self.display.fill(COLOR_OPTION_B,
                                      (int(610 * scale + shift_x),
                                       yList - int(24 * scale),
                                       int(590 * scale), int(48 * scale)))
                    self.show_text(self.directory_name_list[dirIndex],
                                   self.source40,
                                   (int(900 * scale + shift_x), yList),
                                   COLOR_OPTION_T)
                    yList += int(50 * scale)
                    dirIndex = dirIndex + 1
                    if dirIndex == nDirectorios or \
                            dirIndex == directories_page * 20 + 20:
                        terminate = True
                if dirIndex == directories_page * 20 + 20:
                    if dirIndex < nDirectorios:
                        self.display.fill(COLOR_OPTION_B,
                                          (int(610 * scale + shift_x),
                                           yList - int(24 * scale),
                                           int(590 * scale), int(48 * scale)))
                        self.show_text(_("Next page") + " >>>",
                                       self.source40,
                                       (int(900 * scale + shift_x), yList),
                                       COLOR_NEXT)
                        nextActivePage = True
                    nDirectoriosCol2 = 10
                else:
                    nDirectoriosCol2 = dirIndex - directories_page * 20 - 10
            else:
                nDirectoriosCol1 = dirIndex - directories_page * 20
                nDirectoriosCol2 = 0
            # about button
            self.display.fill(COLOR_BUTTON_B,
                              (int(20 * scale + shift_x),
                               int(801 * scale + shift_y),
                               int(370 * scale),
                               int(48 * scale)))
            self.show_text(_("About this game"), self.source40, (int(
                205 * scale + shift_x), int(825 * scale + shift_y)), (100, 200, 100))
            # stats button
            self.display.fill(COLOR_BUTTON_B,
                              (int(420 * scale + shift_x),
                               int(801 * scale + shift_y),
                               int(370 * scale),
                               int(48 * scale)))
            self.show_text(_("Stats"), self.source40, (int(
                605 * scale + shift_x), int(825 * scale + shift_y)), (100, 200, 100))
            # exit button
            self.display.fill(COLOR_BUTTON_B,
                              (int(820 * scale + shift_x),
                               int(801 * scale + shift_y),
                               int(370 * scale),
                               int(48 * scale)))
            self.show_text(_("Exit"), self.source40, (int(
                1005 * scale + shift_x), int(825 * scale + shift_y)), (100, 200, 100))
            pygame.display.flip()
            changePage = False
            while not changePage:
                clock.tick(20)
                while Gtk.events_pending():
                    Gtk.main_iteration()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == 27:  # escape: salir
                            if self.sound:
                                self.click.play()
                            self.save_stats()
                            if self.parent is not None:
                                self.parent.close(skip_save=True)
                            return 1
                    elif event.type == pygame.QUIT:
                        if self.sound:
                            self.click.play()
                        self.save_stats()
                        return 1
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.sound:
                            self.click.play()
                        pos = event.pos
                        # options area
                        if pos[1] < 800 * scale + shift_y:
                            if pos[1] > 175 * scale + shift_y:
                                if pos[0] < 600 * scale + \
                                        shift_x:  # primera columna
                                    if pos[1] < 175 * scale + shift_y + \
                                            (nDirectoriosCol1 + 1) * 50 * scale:  # mapa
                                        self.directory_index = \
                                            int((pos[1] - int(175 * scale + shift_y)) //
                                                int(50 * scale)) - 1 + \
                                            directories_page * 20
                                        if self.directory_index == \
                                                directories_page * 20 - 1 and \
                                                is_previous_page_active:  # pag. ant.
                                            directories_page = directories_page - 1
                                            nextActivePage = True
                                            changePage = True
                                        elif self.directory_index > \
                                                directories_page * 20 - 1:
                                            self.dirPage = directories_page
                                            return
                                else:
                                    if pos[1] < 225 * scale + shift_y + \
                                            nDirectoriosCol2 * 50 * scale or \
                                            (nextActivePage and
                                             pos[1] < 775 * scale + shift_y):  # mapa
                                        self.directory_index = \
                                            int((pos[1] - int(225 * scale + shift_y)) //
                                                int(50 * scale)) + \
                                            directories_page * 20 + 10
                                        if self.directory_index == \
                                                directories_page * 20 + 9:
                                            pass  # ignorar; espacio vacio
                                        elif self.directory_index == \
                                                directories_page * 20 + 20 and \
                                                nextActivePage:  # pag. sig.
                                            directories_page = \
                                                directories_page + 1
                                            is_previous_page_active = True
                                            changePage = True
                                        elif self.directory_index < \
                                                directories_page * 20 + 20:
                                            self.dirPage = directories_page
                                            return
                        # buttons zone
                        else:
                            if pos[1] < 850 * scale + shift_y:
                                if pos[0] > 20 * scale + shift_x and \
                                        pos[0] < 390 * scale + shift_x:
                                    if self.displayAbout() == 1:
                                        return 1  # acerca
                                elif pos[0] > 420 * scale + shift_x and \
                                        pos[0] < 790 * scale + shift_x:
                                    if self.displayStats() == 1:
                                        return 1  # stats
                                elif pos[0] > 820 * scale + shift_x and \
                                        pos[0] < 1190 * scale + shift_x:
                                    self.save_stats()
                                    if self.parent is not None:
                                        self.parent.close(skip_save=True)
                                    return 1
                    elif event.type == EVENTOREFRESCO:
                        pygame.display.flip()

    def load_image(self, name):
        """Load an image and scale it according to the resolution"""
        image = None
        archive = os.path.join(self.image_file_path, name)
        if os.path.exists(archive):
            if xo_resolution:
                image = pygame.image.load(
                    os.path.join(self.image_file_path, name))
            else:
                image0 = pygame.image.load(
                    os.path.join(self.image_file_path, name))
                image = pygame.transform.scale(image0,
                                               (int(image0.get_width() * scale),
                                                int(image0.get_height() * scale)))
                del image0
        return image

    def __init__(self, parent=None):
        self.parent = parent
        self.running = True
        file_activity_info = configparser.ConfigParser()
        activity_info_path = os.path.abspath('activity/activity.info')
        file_activity_info.read(activity_info_path)
        bundle_id = file_activity_info.get('Activity', 'bundle_id')
        self.activity_name = file_activity_info.get('Activity', 'name')
        path = os.path.abspath('locale')
        gettext.bindtextdomain(bundle_id, path)
        gettext.textdomain(bundle_id)
        global _
        _ = gettext.gettext
        # initial time
        self._init_time = time.time()
        # stats
        self._score = 0
        self._average = 0
        self._explore_times = 0
        self._explore_places = 0
        self._game_times = 0
        self._time = 0

    def load_stats(self):
        if self.parent is not None:
            _stats_list = []
            for i in range(7):
                _stats_list.append(0)
            try:
                folder = self.parent.get_activity_root()
                path = os.path.join(folder, 'data', 'stats.dat')
                if os.path.exists(path):
                    f = open(path, 'r')
                    for i in range(7):
                        val = f.readline()
                        val = val.strip('\n')
                        if not (val == ''):
                            _stats_list[i] = int(float(val))
                    f.close()
            except Exception as err:
                print('Cannot load stats', err)
                return
            if self._validate_stats(_stats_list):
                self._score = _stats_list[0]
                self._average = _stats_list[1]
                self._explore_times = _stats_list[2]
                self._explore_places = _stats_list[3]
                self._game_times = _stats_list[4]
                self._time = _stats_list[5]

    def _validate_stats(self, l):
        return (self._calc_sum(l) == l[6])

    def _calc_sum(self, l):
        s = 0
        for i in range(6):
            s = s + l[i]
        return s % 7

    def save_stats(self):
        if self.parent is not None:
            try:
                t = int(time.time() - self._init_time) / 60
                self._time = self._time + t
                folder = self.parent.get_activity_root()
                path = os.path.join(folder, 'data', 'stats.dat')
                # use aux list
                _stats_list = []
                for i in range(7):
                    _stats_list.append(0)
                _stats_list[0] = self._score
                _stats_list[1] = self._average
                _stats_list[2] = self._explore_times
                _stats_list[3] = self._explore_places
                _stats_list[4] = self._game_times
                _stats_list[5] = self._time
                _stats_list[6] = self._calc_sum(_stats_list)
                # save
                f = open(path, 'w')
                for i in range(7):
                    f.write(str(_stats_list[i]) + '\n')
                f.close()
            except Exception as err:
                print('Error saving stats', err)

    def loadAll(self):
        global scale, shift_x, shift_y, xo_resolution
        self.display = pygame.display.get_surface()
        if not (self.display):
            info = pygame.display.Info()
            self.display = pygame.display.set_mode(
                (info.current_w, info.current_h), pygame.FULLSCREEN)
            pygame.display.set_caption(_(self.activity_name))
        self.screen_width = self.display.get_width()
        self.screen_height = self.display.get_height()
        pygame.display.flip()
        if self.screen_width == 1200 and self.screen_height == 900:
            xo_resolution = True
            scale = 1
            shift_x = 0
            shift_y = 0
        else:
            xo_resolution = False
            if self.screen_width / 1200.0 < self.screen_height / 900.0:
                scale = self.screen_width / 1200.0
                shift_x = 0
                shift_y = int((self.screen_height - scale * 900) / 2)
            else:
                scale = self.screen_height / 900.0
                shift_x = int((self.screen_width - scale * 1200) / 2)
                shift_y = 0
        # cargar imagenes generales
        self.image_file_path = os.path.join(CAMINORECURSOS,
                                            CAMINOCOMUN,
                                            CAMINOIMAGENES)
        # JP para el game
        self.jp1 = self.load_image("jp1.png")
        # Ojos JP
        self.ojos1 = self.load_image("ojos1.png")
        self.ojos2 = self.load_image("ojos2.png")
        self.ojos3 = self.load_image("ojos3.png")
        # Puerta fin
        self.gate1 = self.load_image("puerta01.png")
        self.door2 = self.load_image("puerta02.png")
        # Otros
        self.balloon = self.load_image("globito.png")
        self.terron = self.load_image("terron.png")
        self.symbolCapitalD = self.load_image("capitalD.png")
        self.symbolCapitalN = self.load_image("capitalN.png")
        self.symbolCity = self.load_image("ciudad.png")
        self.symbolHill = self.load_image("cerro.png")
        # cargar sonidos
        self.sound_file_path = os.path.join(CAMINORECURSOS,
                                            CAMINOCOMUN,
                                            CAMINOSONIDOS)
        self.sound = True
        try:
            self.click = pygame.mixer.Sound(os.path.join(
                self.sound_file_path, "junggle_btn117.wav"))
            self.click.set_volume(0.2)
        except BaseException:
            self.sound = False
        # cargar directorios
        self.loadListDirectories()
        # cargar sources
        self.source60 = pygame.font.Font(
            os.path.join(
                CAMINORECURSOS,
                CAMINOCOMUN,
                CAMINOFUENTES,
                "Share-Regular.ttf"
            ),
            int(60 * scale)
        )
        self.source40 = pygame.font.Font(os.path.join(CAMINORECURSOS,
                                                      CAMINOCOMUN,
                                                      CAMINOFUENTES,
                                                      "Share-Regular.ttf"),
                                         int(34 * scale))
        self.source9 = pygame.font.Font(os.path.join(CAMINORECURSOS,
                                                     CAMINOCOMUN,
                                                     CAMINOFUENTES,
                                                     "Share-Regular.ttf"),
                                        int(20 * scale))
        self.source32 = pygame.font.Font(None, int(30 * scale))
        self.source24 = pygame.font.Font(None, int(24 * scale))
        # cursor
        datos_cursor = (
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  ",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ",
            "XXX.........................XXXX",
            "XXX..........................XXX",
            "XXX..........................XXX",
            "XXX.........................XXXX",
            "XXX.......XXXXXXXXXXXXXXXXXXXXX ",
            "XXX........XXXXXXXXXXXXXXXXXXX  ",
            "XXX.........XXX                 ",
            "XXX..........XXX                ",
            "XXX...........XXX               ",
            "XXX....X.......XXX              ",
            "XXX....XX.......XXX             ",
            "XXX....XXX.......XXX            ",
            "XXX....XXXX.......XXX           ",
            "XXX....XXXXX.......XXX          ",
            "XXX....XXXXXX.......XXX         ",
            "XXX....XXX XXX.......XXX        ",
            "XXX....XXX  XXX.......XXX       ",
            "XXX....XXX   XXX.......XXX      ",
            "XXX....XXX    XXX.......XXX     ",
            "XXX....XXX     XXX.......XXX    ",
            "XXX....XXX      XXX.......XXX   ",
            "XXX....XXX       XXX.......XXX  ",
            "XXX....XXX        XXX.......XXX ",
            "XXX....XXX         XXX.......XXX",
            "XXX....XXX          XXX......XXX",
            "XXX....XXX           XXX.....XXX",
            "XXX....XXX            XXX...XXXX",
            " XXX..XXX              XXXXXXXX ",
            "  XXXXXX                XXXXXX  ",
            "   XXXX                  XXXX   ")
        self.cursor = pygame.cursors.compile(datos_cursor)
        pygame.mouse.set_cursor((32, 32), (1, 1), *self.cursor)
        datos_cursor_espera = (
            "                                ",
            "                                ",
            "                                ",
            "                                ",
            "                                ",
            "                                ",
            "                                ",
            "                                ",
            "                                ",
            "                                ",
            "  XXXXXX     XXXXXX     XXXXXX  ",
            " XXXXXXXX   XXXXXXXX   XXXXXXXX ",
            "XXXX..XXXX XXXX..XXXX XXXX..XXXX",
            "XXX....XXX XXX....XXX XXX....XXX",
            "XXX....XXX XXX....XXX XXX....XXX",
            "XXX....XXX XXX....XXX XXX....XXX",
            "XXXX..XXXX XXXX..XXXX XXXX..XXXX",
            " XXXXXXXX   XXXXXXXX   XXXXXXXX ",
            "  XXXXXX     XXXXXX      XXXXX  ",
            "                                ",
            "                                ",
            "                                ",
            "                                ",
            "                                ",
            "                                ",
            "                                ",
            "                                ",
            "                                ",
            "                                ",
            "                                ",
            "                                ",
            "                                ")
        self.wait_cursor = pygame.cursors.compile(datos_cursor_espera)

    def load_directory(self):
        """Loads specific information from a directories"""
        self.image_file_path = os.path.join(CAMINORECURSOS,
                                            self.directories,
                                            CAMINOIMAGENES)
        self.sound_file_path = os.path.join(CAMINORECURSOS,
                                            self.directories,
                                            CAMINOSONIDOS)
        self.data_path = os.path.join(CAMINORECURSOS,
                                      self.directories,
                                      CAMINODATOS)
        self.fondo = self.load_image("fondo.png")
        self.flag = self.load_image("flag.png")

        self.load_info()

        self.loadLevels()
        self.load_scans()

    def show_balloon(self, lines):
        """Show text in the balloon"""
        self.display.blit(self.balloon,
                          (int(XMAPAMAX * scale + shift_x),
                           int(YGLOBITO * scale + shift_y)))
        yLinea = int(YGLOBITO * scale) + shift_y + \
                 self.source32.get_height() * 3
        for l in lines:
            text = self.source32.render(l, 1, COLORPREGUNTAS)
            textrect = text.get_rect()
            textrect.center = (int(XCENTROPANEL * scale + shift_x), yLinea)
            self.display.blit(text, textrect)
            yLinea = yLinea + self.source32.get_height() + int(10 * scale)
        pygame.display.flip()

    def delete_balloon(self):
        """Delete the balloon, leave it blank"""
        self.display.blit(self.balloon,
                          (int(XMAPAMAX * scale + shift_x),
                           int(YGLOBITO * scale + shift_y)))

    def correcto(self):
        """Show text in the balloon when the answer is correct"""
        self.currentCorrect = random.randint(1, self.correctTotal) - 1
        self.show_balloon([self.correct_list[self.currentCorrect]])
        self.is_correct = True
        if self.n_bad_answer >= 1:
            self.points = self.points + 5
        else:
            self.points = self.points + 10
        pygame.time.set_timer(EVENTORESPUESTA, TIEMPORESPUESTA)

    def wrong(self):
        """Show text in the balloon when the answer is wrong"""
        self.wrongActual = random.randint(1, self.wrongTotal) - 1
        self.show_balloon([self.listMal[self.wrongActual]])
        self.is_correct = False
        self.n_bad_answer += 1
        pygame.time.set_timer(EVENTORESPUESTA, TIEMPORESPUESTA)

    def isCorrect(self, level, pos):
        """
        Returns True if the locked coordinates
        correspond to the correct answer
        """
        correct = level.current_question[2]
        # primero averiguar kind
        if level.current_question[1] == 1:  # DEPTO
            # buscar depto correcto
            for d in self.listDeptos:
                if d.name == correct:
                    break
            if d.currentPosition(pos):
                d.display_name(self.display,
                               self.source32,
                               COLORNOMBREDEPTO,
                               True)
                return True
            else:
                return False
        elif level.current_question[1] == 2:  # CAPITAL o CIUDAD
            # buscar lugar correcto
            for l in self.list_places:
                if l.name == correct:
                    break
            if l.current_position(pos):
                l.display_name(self.display,
                               self.source24,
                               COLORNOMBRECAPITAL,
                               True)
                return True
            else:
                return False
        if level.current_question[1] == 3:  # RIO
            # buscar rio correcto
            for d in self.listRivers:
                if d.name == correct:
                    break
            if d.currentPosition(pos):
                d.display_name(self.display,
                               self.source24,
                               COLORNOMBRERIO,
                               True)
                return True
            else:
                return False
        if level.current_question[1] == 4:  # CUCHILLA
            # buscar cuchilla correcta
            for d in self.list_blades:
                if d.name == correct:
                    break
            if d.currentPosition(pos):
                d.display_name(self.display,
                               self.source24,
                               COLORNOMBREELEVACION,
                               True)
                return True
            else:
                return False
        elif level.current_question[1] == 5:  # CERRO
            # buscar lugar correcto
            for l in self.list_places:
                if l.name == correct:
                    break
            if l.current_position(pos):
                l.display_name(self.display,
                               self.source24,
                               COLORNOMBREELEVACION,
                               True)
                return True
            else:
                return False
        if level.current_question[1] == 6:  # RUTA
            # buscar ruta correcta
            for d in self.listRutas:
                if d.name == correct:
                    break
            if d.currentPosition(pos):
                d.display_name(self.display,
                               self.source24,
                               COLORNOMBRERUTA,
                               True)
                return True
            else:
                return False

    def presentLevel(self):
        for i in self.current_level.initial_display:
            if i.startswith("lineasDepto"):
                self.display.blit(self.apartmentsLineas, (shift_x, shift_y))
            elif i.startswith("rios"):
                self.display.blit(self.rivers, (shift_x, shift_y))
            elif i.startswith("rutas"):
                self.display.blit(self.routes, (shift_x, shift_y))
            elif i.startswith("cuchillas"):
                self.display.blit(self.cuchillas, (shift_x, shift_y))
            elif i.startswith("capitales"):
                for l in self.list_places:
                    if ((l.kind == 0) or (l.kind == 1)):
                        l.display(self.display, False)
            elif i.startswith("ciudades"):
                for l in self.list_places:
                    if l.kind == 2:
                        l.display(self.display, False)
            elif i.startswith("cerros"):
                for l in self.list_places:
                    if l.kind == 5:
                        l.display(self.display, False)

        for i in self.current_level.initial_name:
            if i.startswith("apartments"):
                for d in self.listDeptos:
                    d.display_name(self.display, self.source32,
                                   COLORNOMBREDEPTO, False)
            elif i.startswith("rios"):
                for d in self.listRivers:
                    d.display_name(self.display, self.source24,
                                   COLORNOMBRERIO, False)
            elif i.startswith("rutas"):
                for d in self.listRutas:
                    d.display_name(self.display, self.source24,
                                   COLORNOMBRERUTA, False)
            elif i.startswith("cuchillas"):
                for d in self.list_blades:
                    d.display_name(self.display, self.source24,
                                   COLORNOMBREELEVACION, False)
            elif i.startswith("capitales"):
                for l in self.list_places:
                    if (l.kind == 0) or (l.kind == 1):
                        l.display_name(self.display, self.source24,
                                       COLORNOMBRECAPITAL, False)
            elif i.startswith("ciudades"):
                for l in self.list_places:
                    if l.kind == 2:
                        l.display_name(self.display, self.source24,
                                       COLORNOMBRECAPITAL, False)
            elif i.startswith("cerros"):
                for l in self.list_places:
                    if l.kind == 5:
                        l.display_name(self.display, self.source24,
                                       COLORNOMBREELEVACION, False)

    def explore_names(self):
        """Juego principal en modo exploro."""
        self._explore_times = self._explore_times + 1
        self.current_level = self.exploration_list[self.current_level_idx]
        # presentar level
        self.presentLevel()
        # boton terminate
        self.display.fill(COLOR_SHOW_ALL, (int(975 * scale + shift_x),
                                           int(25 * scale + shift_y),
                                           int(200 * scale),
                                           int(50 * scale)))
        self.show_text(_("End"),
                       self.source40,
                       (int(1075 * scale + shift_x),
                        int(50 * scale + shift_y)),
                       COLOR_SKIP)
        pygame.display.flip()
        # boton mostrar todo
        self.display.fill(COLOR_SHOW_ALL, (int(975 * scale + shift_x),
                                           int(90 * scale + shift_y),
                                           int(200 * scale),
                                           int(50 * scale)))
        self.show_text(_("Show all"),
                       self.source40,
                       (int(1075 * scale + shift_x),
                        int(115 * scale + shift_y)),
                       COLOR_SKIP)
        pygame.display.flip()
        # lazo principal de espera por acciones del usuario
        while True:
            clock.tick(20)
            while Gtk.events_pending():
                Gtk.main_iteration()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == 27:  # escape: salir
                        if self.sound:
                            self.click.play()
                        return
                elif event.type == pygame.QUIT:
                    if self.sound:
                        self.click.play()
                    self.save_stats()
                    return 1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound:
                        self.click.play()
                    if event.pos[0] < XMAPAMAX * \
                            scale + shift_x:  # zona de mapa
                        for i in self.current_level.active_elements:
                            if i.startswith("capitales"):
                                for l in self.list_places:
                                    if ((l.kind == 0) or (l.kind == 1)
                                    ) and l.current_position(event.pos):
                                        l.display_name(self.display,
                                                       self.source24,
                                                       COLORNOMBRECAPITAL,
                                                       True)
                                        self._explore_places += 1
                                        break
                            elif i.startswith("ciudades"):
                                for l in self.list_places:
                                    if l.kind == 2 and l.current_position(
                                            event.pos):
                                        l.display_name(self.display,
                                                       self.source24,
                                                       COLORNOMBRECAPITAL,
                                                       True)
                                        self._explore_places += 1
                                        break
                            elif i.startswith("rios"):
                                for d in self.listRivers:
                                    if d.currentPosition(event.pos):
                                        d.display_name(self.display,
                                                       self.source24,
                                                       COLORNOMBRERIO,
                                                       True)
                                        self._explore_places += 1
                                        break
                            elif i.startswith("rutas"):
                                for d in self.listRutas:
                                    if d.currentPosition(event.pos):
                                        d.display_name(self.display,
                                                       self.source24,
                                                       COLORNOMBRERUTA,
                                                       True)
                                        self._explore_places += 1
                                        break
                            elif i.startswith("cuchillas"):
                                for d in self.list_blades:
                                    if d.currentPosition(event.pos):
                                        d.display_name(self.display,
                                                       self.source24,
                                                       COLORNOMBREELEVACION,
                                                       True)
                                        self._explore_places += 1
                                        break
                            elif i.startswith("cerros"):
                                for l in self.list_places:
                                    if l.kind == 5 and l.current_position(
                                            event.pos):
                                        l.display_name(self.display,
                                                       self.source24,
                                                       COLORNOMBREELEVACION,
                                                       True)
                                        self._explore_places += 1
                                        break
                            elif i.startswith("apartments"):
                                for d in self.listDeptos:
                                    if d.currentPosition(event.pos):
                                        d.display_name(self.display,
                                                       self.source32,
                                                       COLORNOMBREDEPTO,
                                                       True)
                                        self._explore_places += 1
                                        break
                    elif 975 * scale + shift_x < event.pos[0] < 1175 * scale + shift_x:
                        if 25 * scale + shift_y < event.pos[1] < 75 * scale + shift_y:
                            # terminate
                            return
                        elif 90 * scale + shift_y < event.pos[1] < 140 * scale + shift_y:
                            # mostrar todo
                            for i in self.current_level.active_elements:
                                if i.startswith("apartments"):
                                    for d in self.listDeptos:
                                        d.display_name(
                                            self.display, self.source32, COLORNOMBREDEPTO, False)
                                elif i.startswith("rios"):
                                    for d in self.listRivers:
                                        d.display_name(
                                            self.display, self.source24, COLORNOMBRERIO, False)
                                elif i.startswith("rutas"):
                                    for d in self.listRutas:
                                        d.display_name(
                                            self.display, self.source24, COLORNOMBRERUTA, False)
                                elif i.startswith("cuchillas"):
                                    for d in self.list_blades:
                                        d.display_name(
                                            self.display,
                                            self.source24,
                                            COLORNOMBREELEVACION,
                                            False
                                        )
                                elif i.startswith("capitales"):
                                    for l in self.list_places:
                                        if (l.kind == 0) or (l.kind == 1):
                                            l.display_name(
                                                self.display,
                                                self.source24,
                                                COLORNOMBRECAPITAL,
                                                False
                                            )
                                elif i.startswith("ciudades"):
                                    for l in self.list_places:
                                        if l.kind == 2:
                                            l.display_name(
                                                self.display,
                                                self.source24,
                                                COLORNOMBRECAPITAL,
                                                False
                                            )
                                elif i.startswith("cerros"):
                                    for l in self.list_places:
                                        if l.kind == 5:
                                            l.display_name(
                                                self.display,
                                                self.source24,
                                                COLORNOMBREELEVACION,
                                                False
                                            )
                            pygame.display.flip()
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()

    def play_level(self):
        """Main game of questions and answers"""
        self._game_times = self._game_times + 1
        self.current_level = self.levels_list[self.current_level_idx]
        self.advance_level = 0
        self.current_level.prepare_questions()
        # presentar level
        self.presentLevel()
        self.display.fill(COLOR_SHOW_ALL,
                          (int(975 * scale + shift_x),
                           int(26 * scale + shift_y),
                           int(200 * scale),
                           int(48 * scale)))
        self.show_text(_("End"),
                       self.source40,
                       (int(1075 * scale + shift_x),
                        int(50 * scale + shift_y)),
                       COLOR_SKIP)
        pygame.display.flip()
        # presentar pregunta inicial
        self.lines_question = self.current_level.next_question(
            self.list_suffixes, self.list_prefixes)
        self.show_balloon(self.lines_question)
        # barra puntaje
        pygame.draw.rect(self.display, COLORBARRA_C,
                         (int(XBARRA_P * scale + shift_x),
                          int((YBARRA_P - 350) * scale + shift_y),
                          int(ABARRA_P * scale),
                          int(350 * scale)), 3)
        self.show_text('0', self.source32,
                       (int((XBARRA_P + ABARRA_P / 2) * scale + shift_x),
                        int(YBARRA_P + 10) * scale + shift_y), COLORBARRA_P)
        # barra avance
        unit = ABARRA_A / TOTALAVANCE
        pygame.draw.rect(self.display, COLORBARRA_C,
                         (int(XBARRA_A * scale + shift_x),
                          int(YBARRA_A * scale + shift_y),
                          int(ABARRA_A * scale),
                          int(ABARRA_P * scale)), 3)
        for i in range(TOTALAVANCE - 1):
            posx = int((XBARRA_A + unit * (i + 1)) * scale + shift_x)
            _pygame_line = pygame.draw.line(self.display,
                                            COLORBARRA_C,
                                            (int(posx),
                                             int(YBARRA_A * scale + shift_y)),
                                            (int(posx),
                                             int(YBARRA_A + ABARRA_P) * scale + shift_y),
                                            3)
        self.nBien = 0
        self.nMal = 0
        self.points = 0
        self.n_bad_answer = 0
        self.otorgado = False
        self.been_fired = 0
        self.primera = False
        self.respondiendo = False
        self.advance_level = 0
        pygame.time.set_timer(EVENTORESPUESTA, 0)
        # leer eventos y ver si la respuesta es correcta
        while True:
            while Gtk.events_pending():
                Gtk.main_iteration()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == 27:  # escape: salir
                        if self.sound:
                            self.click.play()
                        pygame.time.set_timer(EVENTORESPUESTA, 0)
                        pygame.time.set_timer(EVENTODESPEGUE, 0)
                        return
                elif event.type == pygame.QUIT:
                    if self.sound:
                        self.click.play()
                    self.save_stats()
                    return 1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound:
                        self.click.play()
                    if event.pos[0] < XMAPAMAX * scale + shift_x:  # zona mapa
                        if self.advance_level < TOTALAVANCE:
                            if not (self.respondiendo):
                                self.respondiendo = True
                                if self.isCorrect(
                                        self.current_level, event.pos):
                                    if not (self.otorgado):
                                        self.delete_balloon()
                                        self.correcto()
                                        self.otorgado = True
                                else:
                                    self.delete_balloon()
                                    self.wrong()
                                if self.points < 0:
                                    self.show_text(
                                        '0', self.source32, (int(
                                            (XBARRA_P + ABARRA_P / 2) * scale + shift_x), int(
                                            YBARRA_P + 15) * scale + shift_y), COLORBARRA_P)
                                else:
                                    self.display.fill(COLORPANEL,
                                                      (int(XBARRA_P * scale + shift_x),
                                                       int((YBARRA_P - 350) * scale + shift_y),
                                                       int(ABARRA_P * scale),
                                                       int(390 * scale)))
                                    self.display.fill(COLORBARRA_P, (
                                        int(XBARRA_P * scale + shift_x),
                                        int((YBARRA_P - self.points * 5)
                                            * scale + shift_y),
                                        int(ABARRA_P * scale),
                                        int(self.points * 5 * scale)
                                    )
                                                      )
                                    pygame.draw.rect(self.display,
                                                     COLORBARRA_C,
                                                     (int(XBARRA_P * scale + shift_x),
                                                      int((YBARRA_P - 350) * scale + shift_y),
                                                      int(ABARRA_P * scale),
                                                      int(350 * scale)),
                                                     3)
                                    self.show_text(str(self.points), self.source32,
                                                   (int((XBARRA_P + ABARRA_P / 2) * scale + shift_x),
                                                    int(YBARRA_P + 15) * scale + shift_y),
                                                   COLORBARRA_P)
                            elif event.pos[0] > 975 * scale + shift_x and \
                                    event.pos[0] < 1175 * scale + shift_x and \
                                    event.pos[1] > 25 * scale + shift_y and \
                                    event.pos[1] < 75 * scale + shift_y:  # terminate
                                return
                    else:
                        if event.pos[0] > 975 * scale + shift_x and \
                                event.pos[0] < 1175 * scale + shift_x and \
                                event.pos[1] > 25 * scale + shift_y and \
                                event.pos[1] < 75 * scale + shift_y:  # terminate
                            pygame.time.set_timer(EVENTODESPEGUE, 0)
                            return
                elif event.type == EVENTORESPUESTA:
                    pygame.time.set_timer(EVENTORESPUESTA, 0)
                    self.respondiendo = False
                    if not (self.is_correct):
                        if self.n_bad_answer == 1:  # help
                            linea = self.lines_question
                            linea2 = self.current_level.return_help()
                            linea3 = linea + linea2
                            self.show_balloon(linea3)
                            pygame.time.set_timer(
                                EVENTORESPUESTA, TIEMPORESPUESTA)
                        elif self.n_bad_answer > 1:
                            self.lines_question = \
                                self.current_level.next_question(
                                    self.list_suffixes, self.list_prefixes)
                            self.show_balloon(self.lines_question)
                            self.n_bad_answer = 0
                            # avanzo
                            self.advance_level = self.advance_level + 1
                            # barra avance
                            av = unit * self.advance_level
                            self.display.fill(COLORBARRA_A, (
                                int(XBARRA_A * scale + shift_x),
                                int(YBARRA_A * scale + shift_y),
                                int(av * scale),
                                int(ABARRA_P * scale)
                            )
                                              )
                            pygame.draw.rect(self.display,
                                             COLORBARRA_C,
                                             (int(XBARRA_A * scale + shift_x),
                                              int(YBARRA_A * scale + shift_y),
                                              int(ABARRA_A * scale),
                                              int(ABARRA_P * scale)),
                                             3)
                            for i in range(TOTALAVANCE - 1):
                                posx = int(
                                    (XBARRA_A + unit * (i + 1)) * scale + shift_x)
                                _pygame_line = pygame.draw.line(
                                    self.display, COLORBARRA_C, (int(posx), int(
                                        YBARRA_A * scale + shift_y)), (int(posx), int(
                                        YBARRA_A + ABARRA_P) * scale + shift_y), 3)
                            # fin barra avance
                        else:  # volver a preguntar
                            self.show_balloon(self.lines_question)
                    else:
                        self.advance_level = self.advance_level + 1
                        # barra avance
                        av = unit * self.advance_level
                        self.display.fill(COLORBARRA_A, (
                            int(XBARRA_A * scale + shift_x),
                            int((YBARRA_A) * scale + shift_y),
                            int(av * scale),
                            int(ABARRA_P * scale)
                        )
                                          )
                        pygame.draw.rect(self.display, COLORBARRA_C,
                                         (int(XBARRA_A * scale + shift_x),
                                          int((YBARRA_A) * scale + shift_y),
                                          int(ABARRA_A * scale),
                                          int(ABARRA_P * scale)), 3)
                        for i in range(TOTALAVANCE - 1):
                            posx = int((XBARRA_A + unit * (i + 1))
                                       * scale + shift_x)
                            _pygame_line = pygame.draw.line(self.display, COLORBARRA_C,
                                                            (int(posx),
                                                             int(YBARRA_A * scale + shift_y)),
                                                            (int(posx),
                                                             int(YBARRA_A + ABARRA_P) * scale + shift_y), 3)
                        # fin barra avance
                        if not (self.advance_level == TOTALAVANCE):
                            self.lines_question = \
                                self.current_level.next_question(
                                    self.list_suffixes, self.list_prefixes)
                            self.show_balloon(self.lines_question)
                            self.n_bad_answer = 0
                            self.otorgado = False
                    if self.advance_level == TOTALAVANCE:  # inicia despedida
                        if self.points == 70:
                            self.lines_question = self.listEndB[
                                random.randint(1, self.numeroEndB) - 1] \
                                .split("\n")
                        else:
                            self.lines_question = self.listEndM[
                                random.randint(1, self.numeroEndM) - 1] \
                                .split("\n")
                        self.show_balloon(self.lines_question)
                        pygame.time.set_timer(EVENTODESPEGUE,
                                              TIEMPORESPUESTA * 2)

                elif event.type == EVENTODESPEGUE:
                    self.bug_status = ESTADODESPEGUE
                    self.display.fill(COLORPANEL,
                                      (int(XMAPAMAX * scale + shift_x),
                                       int(76 * scale + shift_y),
                                       int(DXPANEL * scale),
                                       int(824 * scale)))
                    if self.been_fired == 0:
                        self.display.blit(
                            self.gate1,
                            (int(
                                XPUERTA *
                                scale +
                                shift_x),
                             YPUERTA *
                             scale +
                             shift_y))
                        self.display.blit(self.jp1,
                                          (int(XBICHO * scale + shift_x),
                                           int(YBICHO * scale + shift_y)))
                    elif self.been_fired == 1:
                        self.display.blit(
                            self.door2,
                            (int(
                                XPUERTA *
                                scale +
                                shift_x),
                             YPUERTA *
                             scale +
                             shift_y))
                        self.display.blit(self.jp1,
                                          (int(XBICHO * scale + shift_x),
                                           int(YBICHO * scale + shift_y)))
                    elif self.been_fired == 2:
                        self.display.blit(
                            self.gate1,
                            (int(
                                XPUERTA *
                                scale +
                                shift_x),
                             YPUERTA *
                             scale +
                             shift_y))
                    elif self.been_fired == 3:
                        pygame.time.set_timer(EVENTODESPEGUE, 0)
                        return
                    pygame.display.flip()
                    self.been_fired = self.been_fired + 1
                    pygame.time.set_timer(EVENTODESPEGUE, 1000)

                elif event.type == EVENTOREFRESCO:
                    if self.bug_status == ESTADONORMAL:
                        if random.randint(1, 15) == 1:
                            self.bug_status = ESTADOPESTANAS
                            self.display.blit(self.ojos3,
                                              (int(1020 * scale + shift_x),
                                               int(547 * scale + shift_y)))
                        elif random.randint(1, 20) == 1:
                            self.bug_status = ESTADOFRENTE
                            self.display.blit(self.ojos2,
                                              (int(1020 * scale + shift_x),
                                               int(547 * scale + shift_y)))
                    elif self.bug_status == ESTADOPESTANAS:
                        self.bug_status = ESTADONORMAL
                        self.display.blit(self.ojos1,
                                          (int(1020 * scale + shift_x),
                                           int(547 * scale + shift_y)))
                    elif self.bug_status == ESTADOFRENTE:
                        if random.randint(1, 10) == 1:
                            self.bug_status = ESTADONORMAL
                            self.display.blit(self.ojos1,
                                              (int(1020 * scale + shift_x),
                                               int(547 * scale + shift_y)))
                    elif self.bug_status == ESTADODESPEGUE:
                        pass
                    pygame.display.flip()

    def principal(self):
        """
        This is the main loop of the game
        """
        pygame.time.set_timer(EVENTOREFRESCO, TIEMPOREFRESCO)

        self.loadAll()

        self.load_commons()

        self.load_stats()

        self.dirPage = 0
        self.running = True
        while self.running:
            if self.dispay_directories() == 1:
                return
            # select map
            pygame.mouse.set_cursor((32, 32), (1, 1), *self.wait_cursor)
            self.directories = self.directories_list[self.directory_index]
            self.load_directory()
            pygame.mouse.set_cursor((32, 32), (1, 1), *self.cursor)
            while self.running:
                # display inicial de game
                self.choose_directory = False
                if self.displayInitial() == 1:
                    return
                if self.choose_directory:  # reselect maps
                    break
                # display fondo y panel
                self.display.blit(self.fondo, (shift_x, shift_y))
                self.display.fill(COLORPANEL,
                                  (int(XMAPAMAX * scale + shift_x), shift_y,
                                   int(DXPANEL * scale), int(900 * scale)))
                if self.play:
                    self.display.blit(self.jp1,
                                      (int(XBICHO * scale + shift_x),
                                       int(YBICHO * scale + shift_y)))
                    self.bug_status = ESTADONORMAL
                    pygame.display.flip()
                    if self.play_level() == 1:
                        return
                    self._score = self._score + self.points
                    self._average = self._score / self._game_times
                else:
                    if self.flag:
                        self.display.blit(self.flag,
                                          (int((XMAPAMAX + 47) * scale + shift_x),
                                           int(155 * scale + shift_y)))
                    yLinea = int(YTEXTO * scale) + shift_y + \
                             self.source9.get_height()
                    for par in self.list_statistics:
                        text1 = self.source9.render(
                            par[0], 1, COLORESTADISTICAS1)
                        self.display.blit(
                            text1, ((XMAPAMAX + 10) * scale + shift_x, yLinea))
                        text2 = self.source9.render(
                            par[1], 1, COLORESTADISTICAS2)
                        self.display.blit(
                            text2, ((XMAPAMAX + 135) * scale + shift_x, yLinea))
                        yLinea = yLinea + self.source9.get_height() + int(5 * scale)

                    pygame.display.flip()
                    if self.explore_names() == 1:
                        return


def main():
    game = Conozco()
    game.principal()


if __name__ == "__main__":
    pygame.init()
    pygame.display.init()
    main()
