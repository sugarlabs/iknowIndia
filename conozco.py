#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Conozco
# Copyright (C) 2008, 2012 Gabriel Eirea
# Copyright (C) 2011, 2012 Alan Aguiar
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
# Ceibal Jam http://ceibaljam.org

import os
import sys
import random
import pygame
import time
import imp
import gettext
import ConfigParser
from gettext import gettext as _

gtk_present = True
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
except:
    gtk_present = False

# constantes
RADIO = 10
RADIO2 = RADIO**2
XMAPAMAX = 786
DXPANEL = 414
XCENTROPANEL = 1002
YGLOBITO = 100
DXBICHO = 255
DYBICHO = 412
XBICHO = 1200-DXBICHO
YBICHO = 900-DYBICHO-80
XPUERTA = 786
YPUERTA = 279
XBARRA_P = 840
YBARRA_P = 790
ABARRA_P = 40
YTEXTO = 370
XBARRA_A= XMAPAMAX+20
YBARRA_A = 900 - ABARRA_P - 20
ABARRA_A = DXPANEL-40
#control
TOTALAVANCE = 7
EVENTORESPUESTA = pygame.USEREVENT+1
TIEMPORESPUESTA = 2300
EVENTODESPEGUE = EVENTORESPUESTA+1
EVENTOREFRESCO = EVENTODESPEGUE+1
TIEMPOREFRESCO = 250
ESTADONORMAL = 1
ESTADOPESTANAS = 2
ESTADOFRENTE = 3
ESTADODESPEGUE = 4
#paths
CAMINORECURSOS = "recursos"
CAMINOCOMUN = "comun"
CAMINOFUENTES = "fuentes"
CAMINODATOS = "datos"
CAMINOIMAGENES = "imagenes"
CAMINOSONIDOS = "sonidos"
ARCHIVONIVELES = "levels"
ARCHIVOEXPLORACIONES = "explorations"
#colors
COLORNOMBREDEPTO = (10,10,10)
COLORNOMBRECAPITAL = (10,10,10)
COLORNOMBRERIO = (10,10,10)
COLORNOMBRERUTA = (10,10,10)
COLORNOMBREELEVACION = (10,10,10)
COLORESTADISTICAS1 = (10, 10, 150)
COLORESTADISTICAS2 = (10, 10, 10)
COLORPREGUNTAS = (80,80,155)
COLORPANEL = (156,158,172)
COLORBARRA_P = (255, 0, 0)
COLORBARRA_A = (0, 0, 255)
COLORBARRA_C = (0, 0, 0)
COLOR_FONDO = (0, 0, 0)
COLOR_ACT_NAME = (255,255,255)
COLOR_OPTION_B = (20, 20, 20)
COLOR_OPTION_T = (200,100,100)
COLOR_BUTTON_B = (20, 20, 20)
COLOR_BUTTON_T = (100,200,100)
COLOR_NEXT = (100, 100, 200)
COLOR_STAT_N = (100, 100, 200)
COLOR_SKIP = (255, 155, 155)
COLOR_CREDITS = (155,155,255)
COLOR_SHOW_ALL = (100, 20, 20)

# variables globales para adaptar la pantalla a distintas resoluciones
scale = 1
shift_x = 0
shift_y = 0
xo_resolution = True

clock = pygame.time.Clock()

def wait_events():
    """ Funcion para esperar por eventos de pygame sin consumir CPU """
    global clock
    clock.tick(20)
    return pygame.event.get()

class Punto():
    """Clase para objetos geograficos que se pueden definir como un punto.

    La posicion esta dada por un par de coordenadas (x,y) medida en pixels
    dentro del mapa.
    """

    def __init__(self,nombre,tipo,simbolo,posicion,postexto):
        self.nombre = nombre
        self.tipo = int(tipo)
        self.posicion = (int(int(posicion[0])*scale+shift_x),
                        int(int(posicion[1])*scale+shift_y))
        self.postexto = (int(int(postexto[0])*scale)+self.posicion[0],
                        int(int(postexto[1])*scale)+self.posicion[1])
        self.simbolo = simbolo

    def estaAca(self,pos):
        """Devuelve un booleano indicando si esta en la coordenada pos,
        la precision viene dada por la constante global RADIO"""
        if (pos[0]-self.posicion[0])**2 + \
                (pos[1]-self.posicion[1])**2 < RADIO2:
            return True
        else:
            return False

    def dibujar(self,pantalla,flipAhora):
        """Dibuja un punto en su posicion"""
        pantalla.blit(self.simbolo, (self.posicion[0]-8, self.posicion[1]-8))
        if flipAhora:
            pygame.display.flip()

    def mostrarNombre(self,pantalla,fuente,color,flipAhora):
        """Escribe el nombre del punto en su posicion"""
        text = fuente.render(self.nombre, 1, color)
        textrect = text.get_rect()
        textrect.center = (self.postexto[0], self.postexto[1])
        pantalla.blit(text, textrect)
        if flipAhora:
            pygame.display.flip()


class Zona():
    """Clase para objetos geograficos que se pueden definir como una zona.

    La posicion esta dada por una imagen bitmap pintada con un color
    especifico, dado por la clave (valor 0 a 255 del componente rojo).
    """

    def __init__(self,mapa,nombre,claveColor,tipo,posicion,rotacion):
        self.mapa = mapa # esto hace una copia en memoria o no????
        self.nombre = nombre
        self.claveColor = int(claveColor)
        self.tipo = int(tipo)
        self.posicion = (int(int(posicion[0])*scale+shift_x),
                        int(int(posicion[1])*scale+shift_y))
        self.rotacion = int(rotacion)

    def estaAca(self,pos):
        """Devuelve True si la coordenada pos esta en la zona"""
        if pos[0] < XMAPAMAX*scale+shift_x:
            try:
                colorAca = self.mapa.get_at((int(pos[0]-shift_x),
                                            int(pos[1]-shift_y)))
            except: # probablemente click fuera de la imagen
                return False
            if colorAca[0] == self.claveColor:
                return True
            else:
                return False
        else:
            return False

    def mostrarNombre(self,pantalla,fuente,color,flipAhora):
        """Escribe el nombre de la zona en su posicion"""
        text = fuente.render(self.nombre, 1, color)
        textrot = pygame.transform.rotate(text, self.rotacion)
        textrect = textrot.get_rect()
        textrect.center = (self.posicion[0], self.posicion[1])
        pantalla.blit(textrot, textrect)
        if flipAhora:
            pygame.display.flip()


class Nivel():
    """Clase para definir los niveles del juego.

    Cada nivel tiene un dibujo inicial, los elementos pueden estar
    etiquetados con el nombre o no, y un conjunto de preguntas.
    """

    def __init__(self,nombre):
        self.nombre = nombre
        self.dibujoInicial = list()
        self.nombreInicial = list()
        self.preguntas = list()
        self.indicePreguntaActual = 0
        self.elementosActivos = list()

    def prepararPreguntas(self):
        """Este metodo sirve para preparar la lista de preguntas al azar."""
        random.shuffle(self.preguntas)

    def siguientePregunta(self,listaSufijos,listaPrefijos):
        """Prepara el texto de la pregunta siguiente"""
        self.preguntaActual = self.preguntas[self.indicePreguntaActual]
        self.sufijoActual = random.randint(1,len(listaSufijos))-1
        self.prefijoActual = random.randint(1,len(listaPrefijos))-1
        lineas = listaPrefijos[self.prefijoActual].split("\n")
        lineas.extend(self.preguntaActual[0].split("\n"))
        lineas.extend(listaSufijos[self.sufijoActual].split("\n"))
        self.indicePreguntaActual = self.indicePreguntaActual+1
        if self.indicePreguntaActual == len(self.preguntas):
            self.indicePreguntaActual = 0
        return lineas

    def devolverAyuda(self):
        """Devuelve la linea de ayuda"""
        self.preguntaActual = self.preguntas[self.indicePreguntaActual-1]
        return self.preguntaActual[3].split("\n")

class Conozco():
    """Clase principal del juego.

    """

    def mostrarTexto(self,texto,fuente,posicion,color):
        """Muestra texto en una determinada posicion"""
        text = fuente.render(texto, 1, color)
        textrect = text.get_rect()
        textrect.center = posicion
        self.pantalla.blit(text, textrect)

    def loadInfo(self):
        """Carga las imagenes y los datos de cada pais"""
        r_path = os.path.join(self.camino_datos, self.directorio + '.py')
        a_path = os.path.abspath(r_path)
        f = None
        try:
            f = imp.load_source(self.directorio, a_path)
        except:
            print _('Cannot open %s') % self.directorio

        if f:
            lugares = []
            if hasattr(f, 'CAPITALS'):
                lugares = lugares + f.CAPITALS
            if hasattr(f, 'CITIES'):
                lugares = lugares + f.CITIES
            if hasattr(f, 'HILLS'):
                lugares = lugares + f.HILLS
            self.listaLugares = list()
            for c in lugares:
                nombreLugar = unicode(c[0], 'UTF-8')
                posx = c[1]
                posy = c[2]
                tipo = c[3]
                incx = c[4]
                incy = c[5]
                if tipo == 0:
                    simbolo = self.simboloCapitalN
                elif tipo == 1:
                    simbolo = self.simboloCapitalD
                elif tipo == 2:
                    simbolo = self.simboloCiudad
                elif tipo == 5:
                    simbolo = self.simboloCerro
                else:
                    simbolo = self.simboloCiudad

                nuevoLugar = Punto(nombreLugar, tipo, simbolo,
                            (posx,posy),(incx,incy))
                self.listaLugares.append(nuevoLugar)

            if hasattr(f, 'STATES'):
                self.deptos = self.cargarImagen("deptos.png")
                self.deptosLineas = self.cargarImagen("deptosLineas.png")
                self.listaDeptos = list()
                for d in f.STATES:
                    nombreDepto = unicode(d[0], 'UTF-8')
                    claveColor = d[1]
                    posx = d[2]
                    posy = d[3]
                    rotacion = d[4]
                    nuevoDepto = Zona(self.deptos, nombreDepto,
                                    claveColor,1,(posx,posy),rotacion)
                    self.listaDeptos.append(nuevoDepto)

            if hasattr(f, 'CUCHILLAS'):
                self.cuchillas = self.cargarImagen("cuchillas.png")
                self.cuchillasDetectar = self.cargarImagen("cuchillasDetectar.png")
                self.listaCuchillas = list()
                for c in f.CUCHILLAS:
                    nombreCuchilla = unicode(c[0], 'UTF-8')
                    claveColor = c[1]
                    posx = c[2]
                    posy = c[3]
                    rotacion = c[4]
                    nuevaCuchilla = Zona(self.cuchillasDetectar, nombreCuchilla,
                                    claveColor,4,(posx,posy),rotacion)
                    self.listaCuchillas.append(nuevaCuchilla)

            if hasattr(f, 'RIVERS'):
                self.rios = self.cargarImagen("rios.png")
                self.riosDetectar = self.cargarImagen("riosDetectar.png")
                self.listaRios = list()
                for r in f.RIVERS:
                    nombreRio = unicode(r[0], 'UTF-8')
                    claveColor = r[1]
                    posx = r[2]
                    posy = r[3]
                    rotacion = r[4]
                    nuevoRio = Zona(self.riosDetectar, nombreRio,
                                    claveColor,3,(posx,posy),rotacion)
                    self.listaRios.append(nuevoRio)

            if hasattr(f, 'ROUTES'):
                self.rutas = self.cargarImagen("rutas.png")
                self.rutasDetectar = self.cargarImagen("rutasDetectar.png")
                self.listaRutas = list()
                for r in f.ROUTES:
                    nombreRuta = unicode(r[0], 'UTF-8')
                    claveColor = r[1]
                    posx = r[2]
                    posy = r[3]
                    rotacion = r[4]
                    nuevaRuta = Zona(self.rutasDetectar, nombreRuta,
                                claveColor,6,(posx,posy),rotacion)
                    self.listaRutas.append(nuevaRuta)
            self.lista_estadisticas = list()
            if hasattr(f, 'STATS'):
                for e in f.STATS:
                    p1 = unicode(e[0], 'UTF-8')
                    p2 = unicode(e[1], 'UTF-8')
                    self.lista_estadisticas.append((p1, p2))


    def cargarListaDirectorios(self):
        """Carga la lista de directorios con los distintos mapas"""
        self.listaDirectorios = list()
        self.listaNombreDirectorios = list()
        listaTemp = os.listdir(CAMINORECURSOS)
        listaTemp.sort()
        for d in listaTemp:
            if not (d == 'comun'):
                r_path = os.path.join(CAMINORECURSOS, d, 'datos', d + '.py')
                a_path = os.path.abspath(r_path)
                f = None
                try:
                    f = imp.load_source(d, a_path)
                except:
                    print _('Cannot open %s') % d

                if hasattr(f, 'NAME'):
                    name = unicode(f.NAME, 'UTF-8')
                    self.listaNombreDirectorios.append(name)
                    self.listaDirectorios.append(d)

    def loadCommons(self):
                
        self.listaPrefijos = list()
        self.listaSufijos = list()
        self.listaCorrecto = list()
        self.listaMal = list()
        self.listaDespedidasB = list()
        self.listaDespedidasM = list()
        self.listaPresentacion = list()
        self.listaCreditos = list()
        

        r_path = os.path.join(CAMINORECURSOS, CAMINOCOMUN, 'datos', 'commons.py')
        a_path = os.path.abspath(r_path)
        f = None
        try:
            f = imp.load_source('commons', a_path)
        except:
            print _('Cannot open %s') % 'commons'

        if f:
            if hasattr(f, 'ACTIVITY_NAME'):
                e = f.ACTIVITY_NAME
                self.activity_name = unicode(e, 'UTF-8')
            if hasattr(f, 'PREFIX'):
                for e in f.PREFIX:
                    e1 = unicode(e, 'UTF-8')
                    self.listaPrefijos.append(e1)
            if hasattr(f, 'SUFIX'):
                for e in f.SUFIX:
                    e1 = unicode(e, 'UTF-8')
                    self.listaSufijos.append(e1)  
            if hasattr(f, 'CORRECT'):
                for e in f.CORRECT:
                    e1 = unicode(e, 'UTF-8')
                    self.listaCorrecto.append(e1)
            if hasattr(f, 'WRONG'):
                for e in f.WRONG:
                    e1 = unicode(e, 'UTF-8')
                    self.listaMal.append(e1)
            if hasattr(f, 'BYE_C'):
                for e in f.BYE_C:
                    e1 = unicode(e, 'UTF-8')
                    self.listaDespedidasB.append(e1)
            if hasattr(f, 'BYE_W'):
                for e in f.BYE_W:
                    e1 = unicode(e, 'UTF-8')
                    self.listaDespedidasM.append(e1)
            if hasattr(f, 'PRESENTATION'):
                for e in f.PRESENTATION:
                    e1 = unicode(e, 'UTF-8')
                    self.listaPresentacion.append(e1)
            if hasattr(f, 'CREDITS'):
                for e in f.CREDITS:
                    e1 = unicode(e, 'UTF-8')
                    self.listaCreditos.append(e1)

        self.numeroSufijos = len(self.listaSufijos)
        self.numeroPrefijos = len(self.listaPrefijos)
        self.numeroCorrecto = len(self.listaCorrecto)
        self.numeroMal = len(self.listaMal)
        self.numeroDespedidasB = len(self.listaDespedidasB)
        self.numeroDespedidasM = len(self.listaDespedidasM)

    def cargarNiveles(self):
        """Carga los niveles del archivo de configuracion"""
        self.listaNiveles = list()

        r_path = os.path.join(self.camino_datos, ARCHIVONIVELES + '.py')
        a_path = os.path.abspath(r_path)
        f = None
        try:
            f = imp.load_source(ARCHIVONIVELES, a_path)
        except:
            print _('Cannot open %s') % ARCHIVONIVELES

        if hasattr(f, 'LEVELS'):
            for ln in f.LEVELS:
                index = ln[0]
                nombreNivel = unicode(ln[1], 'UTF-8')
                nuevoNivel = Nivel(nombreNivel)

                listaDibujos = ln[2]
                for i in listaDibujos:
                    nuevoNivel.dibujoInicial.append(i.strip())

                listaNombres = ln[3]
                for i in listaNombres:
                    nuevoNivel.nombreInicial.append(i.strip())

                listpreguntas = ln[4]

                if (index == 1):
                    for i in listpreguntas:
                        texto = unicode(i[0], 'UTF-8')
                        tipo = i[1]
                        respuesta = unicode(i[2], 'UTF-8')
                        ayuda = unicode(i[3], 'UTF-8')
                        nuevoNivel.preguntas.append((texto, tipo, respuesta, ayuda))
                else:
                    for i in listpreguntas:
                        respuesta = unicode(i[0], 'UTF-8')
                        ayuda = unicode(i[1], 'UTF-8')
                        if (index == 2):
                            tipo = 2
                            texto = _('the city of\n%s') % respuesta
                        elif (index == 7):
                            tipo = 1
                            texto = _('the department of\n%s') % respuesta
                        elif (index == 8):
                            tipo = 1
                            texto = _('the province of\n%s') % respuesta
                        elif (index == 9):
                            tipo = 1
                            texto = _('the district of\n%s') % respuesta
                        elif (index == 10):
                            tipo = 1
                            texto = _('the state of\n%s') % respuesta
                        elif (index == 11):
                            tipo = 1
                            texto = _('the region of\n%s') % respuesta
                        elif (index == 12):
                            tipo = 1
                            texto = _('the parish of\n%s') % respuesta
                        elif (index == 14):
                            tipo = 1
                            texto = _('the taluka of\n%s') % respuesta
                        elif (index == 6):
                            tipo = 1
                            texto = _('the municipality of\n%s') % respuesta
                        elif (index == 4):
                            tipo = 3
                            texto = _('the %s') % respuesta
                        elif (index == 5):
                            tipo = 6
                            texto = _('the %(route)s') % {'route': respuesta}

                        nuevoNivel.preguntas.append((texto, tipo, respuesta, ayuda))

                self.listaNiveles.append(nuevoNivel)

        self.indiceNivelActual = 0
        self.numeroNiveles = len(self.listaNiveles)


    def cargarExploraciones(self):
        """Carga los niveles de exploracion del archivo de configuracion"""
        self.listaExploraciones = list()

        r_path = os.path.join(self.camino_datos, ARCHIVOEXPLORACIONES + '.py')
        a_path = os.path.abspath(r_path)
        f = None
        try:
            f = imp.load_source(ARCHIVOEXPLORACIONES, a_path)
        except:
            print _('Cannot open %s') % ARCHIVOEXPLORACIONES

        if hasattr(f, 'EXPLORATIONS'):
            for e in f.EXPLORATIONS:
                nombreNivel= unicode(e[0], 'UTF-8')
                nuevoNivel = Nivel(nombreNivel)

                listaDibujos = e[1]
                for i in listaDibujos:
                    nuevoNivel.dibujoInicial.append(i.strip())

                listaNombres = e[2]
                for i in listaNombres:
                    nuevoNivel.nombreInicial.append(i.strip())

                listaNombres = e[3]
                for i in listaNombres:
                    nuevoNivel.elementosActivos.append(i.strip())

                self.listaExploraciones.append(nuevoNivel)

        self.numeroExploraciones = len(self.listaExploraciones)

    def pantallaAcercaDe(self):
        """Pantalla con los datos del juego, creditos, etc"""
        self.pantallaTemp = pygame.Surface(
            (self.anchoPantalla,self.altoPantalla))
        self.pantallaTemp.blit(self.pantalla,(0,0))
        self.pantalla.fill(COLOR_FONDO)
        self.pantalla.blit(self.terron,
                        (int(20*scale+shift_x),
                            int(20*scale+shift_y)))
        self.pantalla.blit(self.jp1,
                        (int(925*scale+shift_x),
                            int(468*scale+shift_y)))
        self.mostrarTexto(_("About %s") % self.activity_name,
                        self.fuente40,
                        (int(600*scale+shift_x),
                        int(100*scale+shift_y)),
                        COLOR_ACT_NAME)

        yLinea = int(200*scale+shift_y)
        for linea in self.listaCreditos:
            self.mostrarTexto(linea.strip(),
                            self.fuente32,
                            (int(600*scale+shift_x),yLinea),
                            COLOR_CREDITS)
            yLinea = yLinea + int(40*scale)

        self.mostrarTexto(_("Press any key to return"),
                        self.fuente32,
                        (int(600*scale+shift_x),
                        int(800*scale+shift_y)),
                        COLOR_SKIP)
        pygame.display.flip()
        while 1:
            if gtk_present:
                while Gtk.events_pending():
                    Gtk.main_iteration()

            for event in wait_events():
                if event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound:
                        self.click.play()
                    self.pantalla.blit(self.pantallaTemp,(0,0))
                    pygame.display.flip()
                    return
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()

    def pantallaStats(self):
        """Pantalla con los datos del juego, creditos, etc"""
        self.pantallaTemp = pygame.Surface(
            (self.anchoPantalla,self.altoPantalla))
        self.pantallaTemp.blit(self.pantalla,(0,0))
        self.pantalla.fill(COLOR_FONDO)
        self.pantalla.blit(self.jp1,
                        (int(925*scale+shift_x),
                            int(468*scale+shift_y)))
        msg = _("Stats of %s") % self.activity_name
        self.mostrarTexto(msg,
                        self.fuente40,
                        (int(600*scale+shift_x),
                        int(100*scale+shift_y)),
                        COLOR_ACT_NAME)
        msg = _('Total score: %s') % self._score
        self.mostrarTexto(unicode(msg, 'UTF-8'),
                        self.fuente32,
                        (int(400*scale+shift_x),
                        int(300*scale+shift_y)),
                        COLOR_STAT_N)
        msg = _('Game average score: %s') % self._average
        self.mostrarTexto(unicode(msg, 'UTF-8'),
                        self.fuente32,
                        (int(400*scale+shift_x),
                        int(350*scale+shift_y)),
                        COLOR_STAT_N)
        msg = _('Times using Explore Mode: %s') % self._explore_times
        self.mostrarTexto(unicode(msg, 'UTF-8'),
                        self.fuente32,
                        (int(400*scale+shift_x),
                        int(400*scale+shift_y)),
                        COLOR_STAT_N)
        msg = _('Places Explored: %s') % self._explore_places
        self.mostrarTexto(unicode(msg, 'UTF-8'),
                        self.fuente32,
                        (int(400*scale+shift_x),
                        int(450*scale+shift_y)),
                        COLOR_STAT_N)
        msg = _('Times using Game Mode: %s') % self._game_times
        self.mostrarTexto(unicode(msg, 'UTF-8'),
                        self.fuente32,
                        (int(400*scale+shift_x),
                        int(500*scale+shift_y)),
                        COLOR_STAT_N)
        t = int(time.time() - self._init_time) / 60
        t = t + self._time
        msg = _('Total time: %s minutes') % t
        self.mostrarTexto(unicode(msg, 'UTF-8'),
                        self.fuente32,
                        (int(400*scale+shift_x),
                        int(550*scale+shift_y)),
                        COLOR_STAT_N)

        self.mostrarTexto(_("Press any key to return"),
                        self.fuente32,
                        (int(600*scale+shift_x),
                        int(800*scale+shift_y)),
                        COLOR_SKIP)

        pygame.display.flip()
        while 1:
            if gtk_present:
                while Gtk.events_pending():
                    Gtk.main_iteration()

            for event in wait_events():
                if event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound:
                        self.click.play()
                    self.pantalla.blit(self.pantallaTemp,(0,0))
                    pygame.display.flip()
                    return
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()

    def pantallaInicial(self):
        """Pantalla con el menu principal del juego"""
        self.pantalla.fill(COLOR_FONDO)
        self.mostrarTexto(self.activity_name,
                        self.fuente60,
                        (int(600*scale+shift_x),
                        int(80*scale+shift_y)),
                        COLOR_ACT_NAME)
        self.mostrarTexto(_("You have chosen the map ")+\
                            self.listaNombreDirectorios\
                            [self.indiceDirectorioActual],
                        self.fuente40,
                        (int(600*scale+shift_x), int(140*scale+shift_y)),
                        COLOR_OPTION_T)
        self.mostrarTexto(_("Play"),
                        self.fuente60,
                        (int(300*scale+shift_x), int(220*scale+shift_y)),
                        COLOR_OPTION_T)
        yLista = int(300*scale+shift_y)
        for n in self.listaNiveles:
            self.pantalla.fill(COLOR_OPTION_B,
                            (int(10*scale+shift_x),
                                yLista-int(24*scale),
                                int(590*scale),
                                int(48*scale)))
            self.mostrarTexto(n.nombre,
                            self.fuente40,
                            (int(300*scale+shift_x), yLista),
                            COLOR_OPTION_T)
            yLista += int(50*scale)
        self.mostrarTexto(_("Explore"),
                        self.fuente60,
                        (int(900*scale+shift_x), int(220*scale+shift_y)),
                        COLOR_NEXT)
        yLista = int(300*scale+shift_y)
        for n in self.listaExploraciones:
            self.pantalla.fill(COLOR_OPTION_B,
                            (int(610*scale+shift_x),
                                yLista-int(24*scale),
                                int(590*scale),
                                int(48*scale)))
            self.mostrarTexto(n.nombre,
                            self.fuente40,
                            (int(900*scale+shift_x),yLista),
                            COLOR_NEXT)
            yLista += int(50*scale)
            # about button
            self.pantalla.fill(COLOR_BUTTON_B,
                            (int(20*scale+shift_x),int(801*scale+shift_y),
                                int(370*scale),int(48*scale)))
            self.mostrarTexto(_("About this game"),
                            self.fuente40,
                            (int(205*scale+shift_x),int(825*scale+shift_y)),
                            COLOR_BUTTON_T)
            # stats button
            self.pantalla.fill(COLOR_BUTTON_B,
                            (int(420*scale+shift_x),int(801*scale+shift_y),
                                int(370*scale),int(48*scale)))
            self.mostrarTexto(unicode(_("Stats"), 'UTF-8'),
                            self.fuente40,
                            (int(605*scale+shift_x),int(825*scale+shift_y)),
                            COLOR_BUTTON_T)
            # return button
            self.pantalla.fill(COLOR_BUTTON_B,
                            (int(820*scale+shift_x),int(801*scale+shift_y),
                                int(370*scale),int(48*scale)))
            self.mostrarTexto(_("Return"),
                            self.fuente40,
                            (int(1005*scale+shift_x),int(825*scale+shift_y)),
                            COLOR_BUTTON_T)
        pygame.display.flip()
        while 1:
            if gtk_present:
                while Gtk.events_pending():
                    Gtk.main_iteration()

            for event in wait_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == 27: # escape: volver
                        if self.sound:
                            self.click.play()
                        self.elegir_directorio = True
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound:
                        self.click.play()
                    pos = event.pos
                    # zona de opciones
                    if pos[1] < 800*scale+shift_y:
                        if pos[1] > 275*scale + shift_y:
                            if pos[0] < 600*scale + shift_x: # primera columna
                                if pos[1] < 275*scale + shift_y + \
                                        len(self.listaNiveles)*50*scale: # nivel
                                    self.indiceNivelActual = \
                                        int((pos[1]-int(275*scale+shift_y))//\
                                                int(50*scale))
                                    self.jugar = True
                                    return
                            else: # segunda columna
                                if pos[1] < 275*scale + shift_y+\
                                        len(self.listaExploraciones)*50*scale:
                                    # nivel de exploracion
                                    self.indiceNivelActual = \
                                        int((pos[1]-int(275*scale+shift_y))//\
                                                int(50*scale))
                                    self.jugar = False
                                    return
                    # buttons zone
                    else:
                        if pos[1] < 850*scale + shift_y:
                            if pos[0] > 20*scale+shift_x and \
                               pos[0] < 390*scale+shift_x:
                                self.pantallaAcercaDe() # acerca
                            elif pos[0] > 420*scale+shift_x and \
                                 pos[0] < 790*scale+shift_x:
                                self.pantallaStats() # stats
                            elif pos[0] > 820*scale+shift_x and \
                                    pos[0] < 1190*scale+shift_x:
                                self.elegir_directorio = True
                                return
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()

    def pantallaDirectorios(self):
        """Pantalla con el menu de directorios"""
        self.pantalla.fill(COLOR_FONDO)
        self.mostrarTexto(self.activity_name,
                        self.fuente60,
                        (int(600*scale+shift_x),int(80*scale+shift_y)),
                        COLOR_ACT_NAME)
        self.mostrarTexto(_("Choose the map to use"),
                        self.fuente40,
                        (int(600*scale+shift_x),int(140*scale+shift_y)),
                        COLOR_OPTION_T)
        nDirectorios = len(self.listaNombreDirectorios)
        paginaDirectorios = self.paginaDir
        while 1:
            yLista = int(200*scale+shift_y)
            self.pantalla.fill(COLOR_FONDO,
                            (int(shift_x),yLista-int(24*scale),
                                int(1200*scale),int(600*scale)))
            if paginaDirectorios == 0:
                paginaAnteriorActiva = False
            else:
                paginaAnteriorActiva = True
            paginaSiguienteActiva = False
            if paginaAnteriorActiva:
                self.pantalla.fill(COLOR_OPTION_B,
                                (int(10*scale+shift_x),yLista-int(24*scale),
                                    int(590*scale),int(48*scale)))
                self.mostrarTexto(unicode("<<< " + _("Previous page"), "UTF-8"),
                                self.fuente40,
                                (int(300*scale+shift_x),yLista),
                                COLOR_NEXT)
            yLista += int(50*scale)
            indiceDir = paginaDirectorios * 20
            terminar = False
            while not terminar:
                self.pantalla.fill(COLOR_OPTION_B,
                                (int(10*scale+shift_x),yLista-int(24*scale),
                                    int(590*scale),int(48*scale)))
                self.mostrarTexto(self.listaNombreDirectorios[indiceDir],
                                self.fuente40,
                                (int(300*scale+shift_x),yLista),
                                COLOR_OPTION_T)
                yLista += int(50*scale)
                indiceDir = indiceDir + 1
                if indiceDir == nDirectorios or \
                        indiceDir == paginaDirectorios * 20 + 10:
                    terminar = True
            if indiceDir == paginaDirectorios * 20 + 10 and \
                    not indiceDir == nDirectorios:
                nDirectoriosCol1 = 10
                yLista = int(250*scale+shift_y)
                terminar = False
                while not terminar:
                    self.pantalla.fill(COLOR_OPTION_B,
                                    (int(610*scale+shift_x),
                                        yLista-int(24*scale),
                                        int(590*scale),int(48*scale)))
                    self.mostrarTexto(self.listaNombreDirectorios[indiceDir],
                                    self.fuente40,
                                    (int(900*scale+shift_x),yLista),
                                    COLOR_OPTION_T)
                    yLista += int(50*scale)
                    indiceDir = indiceDir + 1
                    if indiceDir == nDirectorios or \
                            indiceDir == paginaDirectorios * 20 + 20:
                        terminar = True
                if indiceDir == paginaDirectorios * 20 + 20:
                    if indiceDir < nDirectorios:
                        self.pantalla.fill(COLOR_OPTION_B,
                                        (int(610*scale+shift_x),
                                            yLista-int(24*scale),
                                            int(590*scale),int(48*scale)))
                        self.mostrarTexto(unicode(_("Next page") + " >>>", "UTF-8"),
                                        self.fuente40,
                                        (int(900*scale+shift_x),yLista),
                                        COLOR_NEXT)
                        paginaSiguienteActiva = True
                    nDirectoriosCol2 = 10
                else:
                    nDirectoriosCol2 = indiceDir - paginaDirectorios * 20 - 10
            else:
                nDirectoriosCol1 = indiceDir - paginaDirectorios * 20
                nDirectoriosCol2 = 0
            # about button
            self.pantalla.fill(COLOR_BUTTON_B,
                            (int(20*scale+shift_x),int(801*scale+shift_y),
                                int(370*scale),int(48*scale)))
            self.mostrarTexto(_("About this game"),
                            self.fuente40,
                            (int(205*scale+shift_x),int(825*scale+shift_y)),
                            (100,200,100))
            # stats button
            self.pantalla.fill(COLOR_BUTTON_B,
                            (int(420*scale+shift_x),int(801*scale+shift_y),
                                int(370*scale),int(48*scale)))
            self.mostrarTexto(unicode(_("Stats"), 'UTF-8'),
                            self.fuente40,
                            (int(605*scale+shift_x),int(825*scale+shift_y)),
                            (100,200,100))
            # exit button
            self.pantalla.fill(COLOR_BUTTON_B,
                            (int(820*scale+shift_x),int(801*scale+shift_y),
                                int(370*scale),int(48*scale)))
            self.mostrarTexto(_("Exit"),
                            self.fuente40,
                            (int(1005*scale+shift_x),int(825*scale+shift_y)),
                            (100,200,100))
            pygame.display.flip()
            cambiarPagina = False
            while not cambiarPagina:
                if gtk_present:
                    while Gtk.events_pending():
                        Gtk.main_iteration()

                for event in wait_events():
                    if event.type == pygame.KEYDOWN:
                        if event.key == 27: # escape: salir
                            if self.sound:
                                self.click.play()
                            self.save_stats()
                            sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.sound:
                            self.click.play()
                        pos = event.pos
                        # zona de opciones
                        if pos[1] < 800*scale+shift_y:
                            if pos[1] > 175*scale+shift_y: 
                                if pos[0] < 600*scale+shift_x: # primera columna
                                    if pos[1] < 175*scale + shift_y + \
                                            (nDirectoriosCol1+1)*50*scale: # mapa
                                        self.indiceDirectorioActual = \
                                            int((pos[1]-int(175*scale+shift_y))//\
                                                    int(50*scale)) - 1 + \
                                                    paginaDirectorios*20
                                        if self.indiceDirectorioActual == \
                                                paginaDirectorios*20-1 and \
                                                paginaAnteriorActiva: # pag. ant.
                                            paginaDirectorios = paginaDirectorios-1
                                            paginaSiguienteActiva = True
                                            cambiarPagina = True
                                        elif self.indiceDirectorioActual>\
                                                paginaDirectorios*20-1:
                                            self.paginaDir = paginaDirectorios
                                            return
                                else:
                                    if pos[1] < 225*scale + shift_y + \
                                            nDirectoriosCol2*50*scale or \
                                            (paginaSiguienteActiva and \
                                                pos[1]<775*scale+shift_y): # mapa
                                        self.indiceDirectorioActual = \
                                            int((pos[1]-int(225*scale+shift_y))//\
                                                    int(50*scale)) + \
                                                    paginaDirectorios*20 + 10
                                        if self.indiceDirectorioActual == \
                                                paginaDirectorios*20+9:
                                            pass # ignorar; espacio vacio
                                        elif self.indiceDirectorioActual == \
                                                paginaDirectorios*20+20 and \
                                                paginaSiguienteActiva: # pag. sig.
                                            paginaDirectorios = \
                                                paginaDirectorios + 1
                                            paginaAnteriorActiva = True
                                            cambiarPagina = True
                                        elif self.indiceDirectorioActual<\
                                                paginaDirectorios*20+20:
                                            self.paginaDir = paginaDirectorios
                                            return
                        # buttons zone
                        else:
                            if pos[1] < 850*scale + shift_y:
                                if pos[0] > 20*scale+shift_x and \
                                   pos[0] < 390*scale+shift_x:
                                    self.pantallaAcercaDe() # acerca
                                elif pos[0] > 420*scale+shift_x and \
                                     pos[0] < 790*scale+shift_x:
                                    self.pantallaStats() # stats
                                elif pos[0] > 820*scale+shift_x and \
                                        pos[0] < 1190*scale+shift_x:
                                    self.save_stats()
                                    sys.exit()  # exit
                    elif event.type == EVENTOREFRESCO:
                        pygame.display.flip()

    def cargarImagen(self,nombre):
        """Carga una imagen y la escala de acuerdo a la resolucion"""
        imagen = None
        archivo = os.path.join(self.camino_imagenes, nombre)
        if os.path.exists(archivo):
            if xo_resolution:
                imagen = pygame.image.load( \
                    os.path.join(self.camino_imagenes,nombre))
            else:
                imagen0 = pygame.image.load( \
                    os.path.join(self.camino_imagenes,nombre))
                imagen = pygame.transform.scale(imagen0,
                            (int(imagen0.get_width()*scale),
                            int(imagen0.get_height()*scale)))
                del imagen0
        return imagen

    def __init__(self, parent=None):
        self.parent = parent
        file_activity_info = ConfigParser.ConfigParser()
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
            l = []
            for i in range(7):
                l.append(0)
            try:
                folder = self.parent.get_activity_root()
                path = os.path.join(folder, 'data', 'stats.dat')
                if os.path.exists(path):
                    f = open(path, 'r')
                    for i in range(7):
                        val = f.readline()
                        val = val.strip('\n')
                        if not(val == ''):
                            l[i] = int(val)
                    f.close()
            except Exception, err:
                print 'Cannot load stats', err
                return
            if self._validate_stats(l):
                self._score = l[0]
                self._average = l[1]
                self._explore_times = l[2]
                self._explore_places = l[3]
                self._game_times = l[4]
                self._time = l[5]

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
                l = []
                for i in range(7):
                    l.append(0)
                l[0] = self._score
                l[1] = self._average
                l[2] = self._explore_times
                l[3] = self._explore_places
                l[4] = self._game_times
                l[5] = self._time
                l[6] = self._calc_sum(l)
                # save
                f = open(path, 'w')
                for i in range(7):
                    f.write(str(l[i]) + '\n')
                f.close()
            except Exception, err:
                print 'Error saving stats', err

    def loadAll(self):
        global scale, shift_x, shift_y, xo_resolution
        pygame.init()
        pygame.display.init()
        self.pantalla = pygame.display.get_surface()
        if not(self.pantalla):
            info = pygame.display.Info()
            self.pantalla = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
            pygame.display.set_caption(_(self.activity_name))
        self.anchoPantalla = self.pantalla.get_width()
        self.altoPantalla = self.pantalla.get_height()
        pygame.display.flip()
        if self.anchoPantalla==1200 and self.altoPantalla==900:
            xo_resolution = True
            scale = 1
            shift_x = 0
            shift_y = 0
        else:
            xo_resolution = False
            if self.anchoPantalla/1200.0<self.altoPantalla/900.0:
                scale = self.anchoPantalla/1200.0
                shift_x = 0
                shift_y = int((self.altoPantalla-scale*900)/2)
            else:
                scale = self.altoPantalla/900.0
                shift_x = int((self.anchoPantalla-scale*1200)/2)
                shift_y = 0
        # cargar imagenes generales
        self.camino_imagenes = os.path.join(CAMINORECURSOS,
                                            CAMINOCOMUN,
                                            CAMINOIMAGENES)
        # JP para el juego
        self.jp1 = self.cargarImagen("jp1.png")
        # Ojos JP
        self.ojos1 = self.cargarImagen("ojos1.png")
        self.ojos2 = self.cargarImagen("ojos2.png")
        self.ojos3 = self.cargarImagen("ojos3.png")
        # Puerta fin
        self.puerta1 = self.cargarImagen("puerta01.png")
        self.puerta2 = self.cargarImagen("puerta02.png")
        # Otros
        self.globito = self.cargarImagen("globito.png")
        self.terron = self.cargarImagen("terron.png")
        self.simboloCapitalD = self.cargarImagen("capitalD.png")
        self.simboloCapitalN = self.cargarImagen("capitalN.png")
        self.simboloCiudad = self.cargarImagen("ciudad.png")
        self.simboloCerro = self.cargarImagen("cerro.png")
        # cargar sonidos
        self.camino_sonidos = os.path.join(CAMINORECURSOS,
                                        CAMINOCOMUN,
                                        CAMINOSONIDOS)
        self.sound = True
        try:
            self.click = pygame.mixer.Sound(os.path.join(\
                            self.camino_sonidos,"junggle_btn117.wav"))
            self.click.set_volume(0.2)
        except:
            self.sound = False
        # cargar directorios
        self.cargarListaDirectorios()
        # cargar fuentes
        self.fuente60 = pygame.font.Font(os.path.join(CAMINORECURSOS,\
                                                        CAMINOCOMUN,\
                                                        CAMINOFUENTES,\
                                                        "Share-Regular.ttf"),
                                        int(60*scale))
        self.fuente40 = pygame.font.Font(os.path.join(CAMINORECURSOS,\
                                                        CAMINOCOMUN,\
                                                        CAMINOFUENTES,\
                                                        "Share-Regular.ttf"),
                                        int(34*scale))
        self.fuente9 = pygame.font.Font(os.path.join(CAMINORECURSOS,\
                                                        CAMINOCOMUN,\
                                                        CAMINOFUENTES,\
                                                        "Share-Regular.ttf"),
                                        int(20*scale))
        self.fuente32 = pygame.font.Font(None, int(30*scale))
        self.fuente24 = pygame.font.Font(None, int(24*scale))
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
        pygame.mouse.set_cursor((32,32), (1,1), *self.cursor)
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
        self.cursor_espera = pygame.cursors.compile(datos_cursor_espera)

    def cargarDirectorio(self):
        """Carga la informacion especifica de un directorio"""
        self.camino_imagenes = os.path.join(CAMINORECURSOS,
                                            self.directorio,
                                            CAMINOIMAGENES)
        self.camino_sonidos = os.path.join(CAMINORECURSOS,
                                            self.directorio,
                                            CAMINOSONIDOS)
        self.camino_datos = os.path.join(CAMINORECURSOS,
                                            self.directorio,
                                            CAMINODATOS)
        self.fondo = self.cargarImagen("fondo.png")
        self.bandera = self.cargarImagen("bandera.png")

        self.loadInfo()

        self.cargarNiveles()
        self.cargarExploraciones()

    def mostrarGlobito(self,lineas):
        """Muestra texto en el globito"""
        self.pantalla.blit(self.globito,
                        (int(XMAPAMAX*scale+shift_x),
                            int(YGLOBITO*scale+shift_y)))
        yLinea = int(YGLOBITO*scale) + shift_y + \
            self.fuente32.get_height()*3
        for l in lineas:
            text = self.fuente32.render(l, 1, COLORPREGUNTAS)
            textrect = text.get_rect()
            textrect.center = (int(XCENTROPANEL*scale+shift_x),yLinea)
            self.pantalla.blit(text, textrect)
            yLinea = yLinea + self.fuente32.get_height() + int(10*scale)
        pygame.display.flip()

    def borrarGlobito(self):
        """ Borra el globito, lo deja en blanco"""
        self.pantalla.blit(self.globito,
                        (int(XMAPAMAX*scale+shift_x),
                            int(YGLOBITO*scale+shift_y)))

    def correcto(self):
        """Muestra texto en el globito cuando la respuesta es correcta"""
        self.correctoActual = random.randint(1,self.numeroCorrecto)-1
        self.mostrarGlobito([self.listaCorrecto[self.correctoActual]])
        self.esCorrecto = True
        if self.nRespuestasMal >= 1:
            self.puntos = self.puntos + 5
        else:
            self.puntos = self.puntos + 10
        pygame.time.set_timer(EVENTORESPUESTA,TIEMPORESPUESTA)

    def mal(self):
        """Muestra texto en el globito cuando la respuesta es incorrecta"""
        self.malActual = random.randint(1,self.numeroMal)-1
        self.mostrarGlobito([self.listaMal[self.malActual]])
        self.esCorrecto = False
        self.nRespuestasMal += 1
        pygame.time.set_timer(EVENTORESPUESTA,TIEMPORESPUESTA)

    def esCorrecta(self,nivel,pos):
        """Devuelve True si las coordenadas cliqueadas corresponden a la
        respuesta correcta
        """
        respCorrecta = nivel.preguntaActual[2]
        # primero averiguar tipo
        if nivel.preguntaActual[1] == 1: # DEPTO
            # buscar depto correcto
            for d in self.listaDeptos:
                if d.nombre == respCorrecta:
                    break
            if d.estaAca(pos):
                d.mostrarNombre(self.pantalla,
                                self.fuente32,
                                COLORNOMBREDEPTO,
                                True)
                return True
            else:
                return False
        elif nivel.preguntaActual[1] == 2: # CAPITAL o CIUDAD
            # buscar lugar correcto
            for l in self.listaLugares:
                if l.nombre == respCorrecta:
                    break
            if l.estaAca(pos):
                l.mostrarNombre(self.pantalla,
                                self.fuente24,
                                COLORNOMBRECAPITAL,
                                True)
                return True
            else:
                return False
        if nivel.preguntaActual[1] == 3: # RIO
            # buscar rio correcto
            for d in self.listaRios:
                if d.nombre == respCorrecta:
                    break
            if d.estaAca(pos):
                d.mostrarNombre(self.pantalla,
                                self.fuente24,
                                COLORNOMBRERIO,
                                True)
                return True
            else:
                return False
        if nivel.preguntaActual[1] == 4: # CUCHILLA
            # buscar cuchilla correcta
            for d in self.listaCuchillas:
                if d.nombre == respCorrecta:
                    break
            if d.estaAca(pos):
                d.mostrarNombre(self.pantalla,
                                self.fuente24,
                                COLORNOMBREELEVACION,
                                True)
                return True
            else:
                return False
        elif nivel.preguntaActual[1] == 5: # CERRO
            # buscar lugar correcto
            for l in self.listaLugares:
                if l.nombre == respCorrecta:
                    break
            if l.estaAca(pos):
                l.mostrarNombre(self.pantalla,
                                self.fuente24,
                                COLORNOMBREELEVACION,
                                True)
                return True
            else:
                return False
        if nivel.preguntaActual[1] == 6: # RUTA
            # buscar ruta correcta
            for d in self.listaRutas:
                if d.nombre == respCorrecta:
                    break
            if d.estaAca(pos):
                d.mostrarNombre(self.pantalla,
                                self.fuente24,
                                COLORNOMBRERUTA,
                                True)
                return True
            else:
                return False

    def presentLevel(self):
        for i in self.nivelActual.dibujoInicial:
            if i.startswith("lineasDepto"):
                self.pantalla.blit(self.deptosLineas, (shift_x, shift_y))
            elif i.startswith("rios"):
                self.pantalla.blit(self.rios, (shift_x, shift_y))
            elif i.startswith("rutas"):
                self.pantalla.blit(self.rutas, (shift_x, shift_y))
            elif i.startswith("cuchillas"):
                self.pantalla.blit(self.cuchillas, (shift_x, shift_y))
            elif i.startswith("capitales"):
                for l in self.listaLugares:
                    if ((l.tipo == 0) or (l.tipo == 1)):
                        l.dibujar(self.pantalla,False)
            elif i.startswith("ciudades"):
                for l in self.listaLugares:
                    if l.tipo == 2:
                        l.dibujar(self.pantalla,False)
            elif i.startswith("cerros"):
                for l in self.listaLugares:
                    if l.tipo == 5:
                        l.dibujar(self.pantalla,False)
        for i in self.nivelActual.nombreInicial:
            if i.startswith("deptos"):
                for d in self.listaDeptos:
                    d.mostrarNombre(self.pantalla,self.fuente32,
                                    COLORNOMBREDEPTO,False)
            elif i.startswith("rios"):
                for d in self.listaRios:
                    d.mostrarNombre(self.pantalla,self.fuente24,
                                    COLORNOMBRERIO,False)
            elif i.startswith("rutas"):
                for d in self.listaRutas:
                    d.mostrarNombre(self.pantalla,self.fuente24,
                                    COLORNOMBRERUTA,False)
            elif i.startswith("cuchillas"):
                for d in self.listaCuchillas:
                    d.mostrarNombre(self.pantalla,self.fuente24,
                                    COLORNOMBREELEVACION,False)
            elif i.startswith("capitales"):
                for l in self.listaLugares:
                    if ((l.tipo == 0) or (l.tipo == 1)):
                        l.mostrarNombre(self.pantalla,self.fuente24,
                                        COLORNOMBRECAPITAL,False)
            elif i.startswith("ciudades"):
                for l in self.listaLugares:
                    if l.tipo == 2:
                        l.mostrarNombre(self.pantalla,self.fuente24,
                                        COLORNOMBRECAPITAL,False)
            elif i.startswith("cerros"):
                for l in self.listaLugares:
                    if l.tipo == 5:
                        l.mostrarNombre(self.pantalla,self.fuente24,
                                        COLORNOMBREELEVACION,False)

    def explorarNombres(self):
        """Juego principal en modo exploro."""
        self._explore_times = self._explore_times + 1
        self.nivelActual = self.listaExploraciones[self.indiceNivelActual]
        # presentar nivel
        self.presentLevel()
        # boton terminar
        self.pantalla.fill(COLOR_SHOW_ALL,(int(975*scale+shift_x),
                                        int(25*scale+shift_y),
                                        int(200*scale),
                                        int(50*scale)))
        self.mostrarTexto(_("End"),
                        self.fuente40,
                        (int(1075*scale+shift_x),
                        int(50*scale+shift_y)),
                        COLOR_SKIP)
        pygame.display.flip()
        # boton mostrar todo
        self.pantalla.fill(COLOR_SHOW_ALL,(int(975*scale+shift_x),
                                        int(90*scale+shift_y),
                                        int(200*scale),
                                        int(50*scale)))
        self.mostrarTexto(_("Show all"),
                        self.fuente40,
                        (int(1075*scale+shift_x),
                        int(115*scale+shift_y)),
                        COLOR_SKIP)
        pygame.display.flip()
        # lazo principal de espera por acciones del usuario
        while 1:
            if gtk_present:
                while Gtk.events_pending():
                    Gtk.main_iteration()

            for event in wait_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == 27: # escape: salir
                        if self.sound:
                            self.click.play()
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound:
                        self.click.play()
                    if event.pos[0] < XMAPAMAX*scale+shift_x: # zona de mapa
                        for i in self.nivelActual.elementosActivos:
                            if i.startswith("capitales"):
                                for l in self.listaLugares:
                                    if ((l.tipo == 0) or (l.tipo == 1)) and l.estaAca(event.pos):
                                        l.mostrarNombre(self.pantalla,
                                                        self.fuente24,
                                                        COLORNOMBRECAPITAL,
                                                        True)
                                        self._explore_places += 1
                                        break
                            elif i.startswith("ciudades"):
                                for l in self.listaLugares:
                                    if l.tipo == 2 and l.estaAca(event.pos):
                                        l.mostrarNombre(self.pantalla,
                                                        self.fuente24,
                                                        COLORNOMBRECAPITAL,
                                                        True)
                                        self._explore_places += 1
                                        break
                            elif i.startswith("rios"):
                                for d in self.listaRios:
                                    if d.estaAca(event.pos):
                                        d.mostrarNombre(self.pantalla,
                                                        self.fuente24,
                                                        COLORNOMBRERIO,
                                                        True)
                                        self._explore_places += 1
                                        break
                            elif i.startswith("rutas"):
                                for d in self.listaRutas:
                                    if d.estaAca(event.pos):
                                        d.mostrarNombre(self.pantalla,
                                                        self.fuente24,
                                                        COLORNOMBRERUTA,
                                                        True)
                                        self._explore_places += 1
                                        break
                            elif i.startswith("cuchillas"):
                                for d in self.listaCuchillas:
                                    if d.estaAca(event.pos):
                                        d.mostrarNombre(self.pantalla,
                                                        self.fuente24,
                                                        COLORNOMBREELEVACION,
                                                        True)
                                        self._explore_places += 1
                                        break
                            elif i.startswith("cerros"):
                                for l in self.listaLugares:
                                    if l.tipo == 5 and l.estaAca(event.pos):
                                        l.mostrarNombre(self.pantalla,
                                                        self.fuente24,
                                                        COLORNOMBREELEVACION,
                                                        True)
                                        self._explore_places += 1
                                        break
                            elif i.startswith("deptos"):
                                for d in self.listaDeptos:
                                    if d.estaAca(event.pos):
                                        d.mostrarNombre(self.pantalla,
                                                        self.fuente32,
                                                        COLORNOMBREDEPTO,
                                                        True)
                                        self._explore_places += 1
                                        break
                    elif event.pos[0] > 975*scale+shift_x and \
                            event.pos[0] < 1175*scale+shift_x:
                        if event.pos[1] > 25*scale+shift_y and \
                            event.pos[1] < 75*scale+shift_y: # terminar
                            return
                        elif event.pos[1] > 90*scale+shift_y and \
                            event.pos[1] < 140*scale+shift_y: # mostrar todo
                            for i in self.nivelActual.elementosActivos:
                                if i.startswith("deptos"):
                                    for d in self.listaDeptos:
                                        d.mostrarNombre(self.pantalla,self.fuente32,
                                                        COLORNOMBREDEPTO,False)
                                elif i.startswith("rios"):
                                    for d in self.listaRios:
                                        d.mostrarNombre(self.pantalla,self.fuente24,
                                                        COLORNOMBRERIO,False)
                                elif i.startswith("rutas"):
                                    for d in self.listaRutas:
                                        d.mostrarNombre(self.pantalla,self.fuente24,
                                                        COLORNOMBRERUTA,False)
                                elif i.startswith("cuchillas"):
                                    for d in self.listaCuchillas:
                                        d.mostrarNombre(self.pantalla,self.fuente24,
                                                        COLORNOMBREELEVACION,False)
                                elif i.startswith("capitales"):
                                    for l in self.listaLugares:
                                        if ((l.tipo == 0) or (l.tipo == 1)):
                                            l.mostrarNombre(self.pantalla,self.fuente24,
                                                            COLORNOMBRECAPITAL,False)
                                elif i.startswith("ciudades"):
                                    for l in self.listaLugares:
                                        if l.tipo == 2:
                                            l.mostrarNombre(self.pantalla,self.fuente24,
                                                            COLORNOMBRECAPITAL,False)
                                elif i.startswith("cerros"):
                                    for l in self.listaLugares:
                                        if l.tipo == 5:
                                            l.mostrarNombre(self.pantalla,self.fuente24,
                                                            COLORNOMBREELEVACION,False)
                            pygame.display.flip()
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()


    def jugarNivel(self):
        """Juego principal de preguntas y respuestas"""
        self._game_times = self._game_times + 1
        self.nivelActual = self.listaNiveles[self.indiceNivelActual]
        self.avanceNivel = 0
        self.nivelActual.prepararPreguntas()
        # presentar nivel
        self.presentLevel()
        self.pantalla.fill(COLOR_SHOW_ALL,
                        (int(975*scale+shift_x),
                            int(26*scale+shift_y),
                            int(200*scale),
                            int(48*scale)))
        self.mostrarTexto(_("End"),
                        self.fuente40,
                        (int(1075*scale+shift_x),
                        int(50*scale+shift_y)),
                        COLOR_SKIP)
        pygame.display.flip()
        # presentar pregunta inicial
        self.lineasPregunta = self.nivelActual.siguientePregunta(\
                self.listaSufijos,self.listaPrefijos)
        self.mostrarGlobito(self.lineasPregunta)
        # barra puntaje
        pygame.draw.rect(self.pantalla, COLORBARRA_C,
                                (int(XBARRA_P*scale+shift_x),
                                int((YBARRA_P-350)*scale+shift_y),
                                int(ABARRA_P*scale),
                                int(350*scale)), 3)
        self.mostrarTexto('0',self.fuente32,
            (int((XBARRA_P+ABARRA_P/2)*scale+shift_x),
            int(YBARRA_P+10)*scale+shift_y), COLORBARRA_P)
        # barra avance
        unidad = ABARRA_A / TOTALAVANCE
        pygame.draw.rect(self.pantalla, COLORBARRA_C,
                                (int(XBARRA_A*scale+shift_x),
                                int(YBARRA_A*scale+shift_y),
                                int(ABARRA_A*scale),
                                int(ABARRA_P*scale)), 3)
        for i in range(TOTALAVANCE-1):
            posx = int((XBARRA_A + unidad * (i+1))*scale+shift_x)
            l = pygame.draw.line(self.pantalla, COLORBARRA_C,
                            (int(posx),
                            int(YBARRA_A*scale+shift_y)), 
                            (int(posx),
                            int(YBARRA_A+ABARRA_P)*scale+shift_y), 3)
        self.nBien = 0
        self.nMal = 0
        self.puntos = 0
        self.nRespuestasMal = 0
        self.otorgado = False
        self.estadodespedida = 0
        self.primera = False
        self.respondiendo = False
        self.avanceNivel = 0
        pygame.time.set_timer(EVENTORESPUESTA,0)
        # leer eventos y ver si la respuesta es correcta
        while 1:
            if gtk_present:
                while Gtk.events_pending():
                    Gtk.main_iteration()

            for event in wait_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == 27: # escape: salir
                        self.click.play()
                        pygame.time.set_timer(EVENTORESPUESTA,0)
                        pygame.time.set_timer(EVENTODESPEGUE,0)
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.click.play()
                    if event.pos[0] < XMAPAMAX*scale+shift_x: # zona mapa
                        if self.avanceNivel < TOTALAVANCE:
                            if not(self.respondiendo):
                                self.respondiendo = True
                                if self.esCorrecta(self.nivelActual, event.pos):
                                    if not(self.otorgado):
                                        self.borrarGlobito()
                                        self.correcto()
                                        self.otorgado = True
                                else:
                                    self.borrarGlobito()
                                    self.mal()
                                if self.puntos < 0:
                                    self.mostrarTexto('0',self.fuente32,
                                        (int((XBARRA_P+ABARRA_P/2)*scale+shift_x),
                                        int(YBARRA_P+15)*scale+shift_y),
                                        COLORBARRA_P)
                                else:
                                    self.pantalla.fill(COLORPANEL, (
                                            int(XBARRA_P*scale+shift_x),
                                            int((YBARRA_P-350)*scale+shift_y),
                                            int(ABARRA_P*scale),
                                            int(390*scale)
                                            )
                                            )
                                    self.pantalla.fill(COLORBARRA_P, (
                                            int(XBARRA_P*scale+shift_x),
                                            int((YBARRA_P-self.puntos*5)*scale+shift_y),
                                            int(ABARRA_P*scale),
                                            int(self.puntos*5*scale)
                                            )
                                            )
                                    pygame.draw.rect(self.pantalla, COLORBARRA_C,
                                        (int(XBARRA_P*scale+shift_x),
                                        int((YBARRA_P-350)*scale+shift_y),
                                        int(ABARRA_P*scale),
                                        int(350*scale)), 3)
                                    self.mostrarTexto(str(self.puntos),self.fuente32,
                                        (int((XBARRA_P+ABARRA_P/2)*scale+shift_x),
                                        int(YBARRA_P+15)*scale+shift_y),
                                        COLORBARRA_P)
                            elif event.pos[0] > 975*scale+shift_x and \
                                    event.pos[0] < 1175*scale+shift_x and \
                                    event.pos[1] > 25*scale+shift_y and \
                                    event.pos[1] < 75*scale+shift_y: # terminar
                                return
                    else:
                        if event.pos[0] > 975*scale+shift_x and \
                           event.pos[0] < 1175*scale+shift_x and \
                           event.pos[1] > 25*scale+shift_y and \
                           event.pos[1] < 75*scale+shift_y: # terminar
                            pygame.time.set_timer(EVENTODESPEGUE,0)
                            return
                elif event.type == EVENTORESPUESTA:
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    self.respondiendo = False
                    if not(self.esCorrecto):
                        if self.nRespuestasMal == 1: # ayuda
                            linea = self.lineasPregunta
                            linea2 = self.nivelActual.devolverAyuda()
                            linea3 = linea + linea2
                            self.mostrarGlobito(linea3)
                            pygame.time.set_timer(
                                EVENTORESPUESTA,TIEMPORESPUESTA)
                        elif self.nRespuestasMal > 1:
                            self.lineasPregunta = \
                                self.nivelActual.siguientePregunta(\
                                self.listaSufijos,self.listaPrefijos)
                            self.mostrarGlobito(self.lineasPregunta)
                            self.nRespuestasMal = 0
                            # avanzo
                            self.avanceNivel = self.avanceNivel + 1
                            # barra avance
                            av = unidad*self.avanceNivel
                            self.pantalla.fill(COLORBARRA_A, (
                                            int(XBARRA_A*scale+shift_x),
                                            int(YBARRA_A*scale+shift_y),
                                            int(av*scale),
                                            int(ABARRA_P*scale)
                                            )
                                            )
                            pygame.draw.rect(self.pantalla, COLORBARRA_C,
                                                (int(XBARRA_A*scale+shift_x),
                                                int(YBARRA_A*scale+shift_y),
                                                int(ABARRA_A*scale),
                                                int(ABARRA_P*scale)), 3)
                            for i in range(TOTALAVANCE-1):
                                posx = int((XBARRA_A + unidad * (i+1))*scale+shift_x)
                                l = pygame.draw.line(self.pantalla, COLORBARRA_C,
                                            (int(posx),
                                            int(YBARRA_A*scale+shift_y)), 
                                            (int(posx),
                                            int(YBARRA_A+ABARRA_P)*scale+shift_y), 3)
                            # fin barra avance
                        else: # volver a preguntar
                            self.mostrarGlobito(self.lineasPregunta)
                    else:
                        self.avanceNivel = self.avanceNivel + 1
                        # barra avance
                        av = unidad*self.avanceNivel
                        self.pantalla.fill(COLORBARRA_A, (
                                        int(XBARRA_A*scale+shift_x),
                                        int((YBARRA_A)*scale+shift_y),
                                        int(av*scale),
                                        int(ABARRA_P*scale)
                                        )
                                        )
                        pygame.draw.rect(self.pantalla, COLORBARRA_C,
                                            (int(XBARRA_A*scale+shift_x),
                                            int((YBARRA_A)*scale+shift_y),
                                            int(ABARRA_A*scale),
                                            int(ABARRA_P*scale)), 3)
                        for i in range(TOTALAVANCE-1):
                            posx = int((XBARRA_A + unidad * (i+1))*scale+shift_x)
                            l = pygame.draw.line(self.pantalla, COLORBARRA_C,
                                        (int(posx),
                                        int(YBARRA_A*scale+shift_y)), 
                                        (int(posx),
                                        int(YBARRA_A+ABARRA_P)*scale+shift_y), 3)
                        # fin barra avance
                        if not(self.avanceNivel == TOTALAVANCE):
                            self.lineasPregunta = \
                                self.nivelActual.siguientePregunta(\
                                self.listaSufijos,self.listaPrefijos)
                            self.mostrarGlobito(self.lineasPregunta)
                            self.nRespuestasMal = 0
                            self.otorgado = False
                    if self.avanceNivel == TOTALAVANCE: # inicia despedida
                        if self.puntos == 70:
                            self.lineasPregunta =  self.listaDespedidasB[\
                                random.randint(1,self.numeroDespedidasB)-1]\
                                .split("\n")
                        else:
                            self.lineasPregunta =  self.listaDespedidasM[\
                                random.randint(1,self.numeroDespedidasM)-1]\
                                .split("\n")
                        self.mostrarGlobito(self.lineasPregunta)
                        pygame.time.set_timer(EVENTODESPEGUE,
                                            TIEMPORESPUESTA*2)

                elif event.type == EVENTODESPEGUE:
                    self.estadobicho = ESTADODESPEGUE
                    self.pantalla.fill(COLORPANEL,
                                    (int(XMAPAMAX*scale+shift_x),int(76*scale+shift_y),
                                         int(DXPANEL*scale),
                                         int(824*scale)))
                    if self.estadodespedida == 0:
                        self.pantalla.blit(self.puerta1,
                            (int(XPUERTA*scale+shift_x), YPUERTA*scale+shift_y))
                        self.pantalla.blit(self.jp1,
                                         (int(XBICHO*scale+shift_x),
                                          int(YBICHO*scale+shift_y)))
                    elif self.estadodespedida == 1:
                        self.pantalla.blit(self.puerta2,
                            (int(XPUERTA*scale+shift_x), YPUERTA*scale+shift_y))
                        self.pantalla.blit(self.jp1,
                                         (int(XBICHO*scale+shift_x),
                                          int(YBICHO*scale+shift_y)))
                    elif self.estadodespedida == 2:
                        self.pantalla.blit(self.puerta1,
                            (int(XPUERTA*scale+shift_x), YPUERTA*scale+shift_y))
                    elif self.estadodespedida == 3:
                        pygame.time.set_timer(EVENTODESPEGUE,0)
                        return
                    pygame.display.flip()
                    self.estadodespedida = self.estadodespedida + 1
                    pygame.time.set_timer(EVENTODESPEGUE,1000)

                elif event.type == EVENTOREFRESCO:
                    if self.estadobicho == ESTADONORMAL:
                        if random.randint(1,15) == 1:
                            self.estadobicho = ESTADOPESTANAS
                            self.pantalla.blit(self.ojos3,
                                            (int(1020*scale+shift_x),
                                                int(547*scale+shift_y)))
                        elif random.randint(1,20) == 1:
                            self.estadobicho = ESTADOFRENTE
                            self.pantalla.blit(self.ojos2,
                                            (int(1020*scale+shift_x),
                                                int(547*scale+shift_y)))
                    elif self.estadobicho == ESTADOPESTANAS:
                        self.estadobicho = ESTADONORMAL
                        self.pantalla.blit(self.ojos1,
                                            (int(1020*scale+shift_x),
                                                int(547*scale+shift_y)))
                    elif self.estadobicho == ESTADOFRENTE:
                        if random.randint(1,10) == 1:
                            self.estadobicho = ESTADONORMAL
                            self.pantalla.blit(self.ojos1,
                                            (int(1020*scale+shift_x),
                                                int(547*scale+shift_y)))
                    elif self.estadobicho == ESTADODESPEGUE:
                        pass
                    pygame.display.flip()

    def principal(self):
        """Este es el loop principal del juego"""
        pygame.time.set_timer(EVENTOREFRESCO,TIEMPOREFRESCO)

        self.loadAll()

        self.loadCommons()

        self.load_stats()

        self.paginaDir = 0
        while 1:
            self.pantallaDirectorios() # seleccion de mapa
            pygame.mouse.set_cursor((32,32), (1,1), *self.cursor_espera)
            self.directorio = self.listaDirectorios\
                [self.indiceDirectorioActual]
            self.cargarDirectorio()
            pygame.mouse.set_cursor((32,32), (1,1), *self.cursor)
            while 1:
                # pantalla inicial de juego
                self.elegir_directorio = False
                self.pantallaInicial()
                if self.elegir_directorio: # volver a seleccionar mapa
                    break
                # dibujar fondo y panel
                self.pantalla.blit(self.fondo, (shift_x, shift_y))
                self.pantalla.fill(COLORPANEL,
                                (int(XMAPAMAX*scale+shift_x),shift_y,
                                int(DXPANEL*scale),int(900*scale)))
                if self.jugar:
                    self.pantalla.blit(self.jp1,
                                    (int(XBICHO*scale+shift_x),
                                    int(YBICHO*scale+shift_y)))
                    self.estadobicho = ESTADONORMAL
                    pygame.display.flip()
                    self.jugarNivel()
                    self._score = self._score + self.puntos
                    self._average = self._score / self._game_times
                else:
                    if self.bandera:
                        self.pantalla.blit(self.bandera,
                                        (int((XMAPAMAX+47)*scale+shift_x),
                                        int(155*scale+shift_y)))
                    yLinea = int(YTEXTO*scale) + shift_y + \
                                self.fuente9.get_height()
                    for par in self.lista_estadisticas:
                        text1 = self.fuente9.render(par[0], 1, COLORESTADISTICAS1)
                        self.pantalla.blit(text1,
                                ((XMAPAMAX+10)*scale+shift_x, yLinea))
                        text2 = self.fuente9.render(par[1], 1, COLORESTADISTICAS2)
                        self.pantalla.blit(text2,
                                ((XMAPAMAX+135)*scale+shift_x, yLinea))
                        yLinea = yLinea+self.fuente9.get_height()+int(5*scale)

                    pygame.display.flip()
                    self.explorarNombres()


def main():
    juego = Conozco()
    juego.principal()

if __name__ == "__main__":
    main()
