#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Conozco India
# Copyright (C) 2008,2009,2010 Gabriel Eirea
# Copyright (C) 2011 Alan Aguiar
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

import sys
import random
import os
import pygame
import gtk
import time
from gettext import gettext as _

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
CAMINORECURSOS = "recursos"
CAMINOCOMUN = "comun"
CAMINOFUENTES = "fuentes"
CAMINODATOS = _("datos/en")
CAMINOIMAGENES = "imagenes"
CAMINOSONIDOS = "sonidos"
ARCHIVODEPTOS = "departamentos.txt"
ARCHIVOLUGARES = "ciudades.txt"
ARCHIVONIVELES = "niveles.txt"
ARCHIVOEXPLORACIONES = "exploraciones.txt"
ARCHIVORIOS = "rios.txt"
ARCHIVORUTAS = "rutas.txt"
ARCHIVOCUCHILLAS = "cuchillas.txt"
ARCHIVOCREDITOS = "creditos.txt"
ARCHIVOPRESENTACION = "presentacion.txt"
ARCHIVONOMBRE = _("nombreEN.txt")
ARCHIVOESTADISTICAS = "estadisticas.txt"
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
        global scale, shift_x, shift_y
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
        lineas = listaPrefijos[self.prefijoActual].split("\\")
        lineas.extend(self.preguntaActual[0].split("\\"))
        lineas.extend(listaSufijos[self.sufijoActual].split("\\"))
        self.indicePreguntaActual = self.indicePreguntaActual+1
        if self.indicePreguntaActual == len(self.preguntas):
            self.indicePreguntaActual = 0
        return lineas

    def devolverAyuda(self):
        """Devuelve la linea de ayuda"""
        self.preguntaActual = self.preguntas[self.indicePreguntaActual-1]
        return self.preguntaActual[3].split("\\")

class ConozcoIn():
    """Clase principal del juego.

    """

    def mostrarTexto(self,texto,fuente,posicion,color):
        """Muestra texto en una determinada posicion"""
        text = fuente.render(texto, 1, color)
        textrect = text.get_rect()
        textrect.center = posicion
        self.pantalla.blit(text, textrect)

    def cargarDepartamentos(self):
        """Carga las imagenes y los datos de los departamentos"""
        self.deptos = self.cargarImagen("deptos.png")
        self.deptosLineas = self.cargarImagen("deptosLineas.png")
        self.listaDeptos = list()
        # falta sanitizar manejo de archivo
        f = open(os.path.join(self.camino_datos,ARCHIVODEPTOS),"r")
        linea = f.readline()
        while linea:
            if linea[0] == "#":
                linea = f.readline()
                continue
            [nombreDepto,claveColor,posx,posy,rotacion] = \
                linea.strip().split("|")
            nuevoDepto = Zona(self.deptos,
                            unicode(nombreDepto,'iso-8859-1'),
                            claveColor,1,(posx,posy),rotacion)
            self.listaDeptos.append(nuevoDepto)
            linea = f.readline()
        f.close()

    def cargarRios(self):
        """Carga las imagenes y los datos de los rios"""
        self.rios = self.cargarImagen("rios.png")
        self.riosDetectar = self.cargarImagen("riosDetectar.png")
        self.listaRios = list()
        # falta sanitizar manejo de archivo
        f = open(os.path.join(self.camino_datos,ARCHIVORIOS),"r")
        linea = f.readline()
        while linea:
            if linea[0] == "#":
                linea = f.readline()
                continue
            [nombreRio,claveColor,posx,posy,rotacion] = \
                linea.strip().split("|")
            nuevoRio = Zona(self.riosDetectar,
                            unicode(nombreRio,'iso-8859-1'),
                            claveColor,3,(posx,posy),rotacion)
            self.listaRios.append(nuevoRio)
            linea = f.readline()
        f.close()

    def cargarRutas(self):
        """Carga las imagenes y los datos de las rutas"""
        self.rutas = self.cargarImagen("rutas.png")
        self.rutasDetectar = self.cargarImagen("rutasDetectar.png")
        self.listaRutas = list()
        # falta sanitizar manejo de archivo
        f = open(os.path.join(self.camino_datos,ARCHIVORUTAS),"r")
        linea = f.readline()
        while linea:
            if linea[0] == "#":
                linea = f.readline()
                continue
            [nombreRuta,claveColor,posx,posy,rotacion] = \
                linea.strip().split("|")
            nuevaRuta = Zona(self.rutasDetectar,
                            unicode(nombreRuta,'iso-8859-1'),
                            claveColor,6,(posx,posy),rotacion)
            self.listaRutas.append(nuevaRuta)
            linea = f.readline()
        f.close()

    def cargarCuchillas(self):
        """Carga las imagenes y los datos de las cuchillas"""
        self.cuchillas = self.cargarImagen("cuchillas.png")
        self.cuchillasDetectar = self.cargarImagen("cuchillasDetectar.png")
        self.listaCuchillas = list()
        # falta sanitizar manejo de archivo
        f = open(os.path.join(self.camino_datos,ARCHIVOCUCHILLAS),"r")
        linea = f.readline()
        while linea:
            if linea[0] == "#":
                linea = f.readline()
                continue
            [nombreCuchilla,claveColor,posx,posy,rotacion] = \
                linea.strip().split("|")
            nuevaCuchilla = Zona(self.cuchillasDetectar,
                                unicode(nombreCuchilla,'iso-8859-1'),
                                claveColor,4,(posx,posy),rotacion)
            self.listaCuchillas.append(nuevaCuchilla)
            linea = f.readline()
        f.close()

    def cargarLugares(self):
        """Carga los datos de las ciudades y otros puntos de interes"""
        self.listaLugares = list()
        # falta sanitizar manejo de archivo
        f = open(os.path.join(self.camino_datos,ARCHIVOLUGARES),"r")
        linea = f.readline()
        while linea:
            if linea[0] == "#":
                linea = f.readline()
                continue
            [nombreLugar,posx,posy,tipo,incx,incy] = \
                linea.strip().split("|")
            if int(tipo) == 0:
                simbolo = self.simboloCapitalN
            elif int(tipo) == 1:
                simbolo = self.simboloCapitalD
            elif int(tipo) == 2:
                simbolo = self.simboloCiudad
            elif int(tipo) == 5:
                simbolo = self.simboloCerro
            else:
                simbolo = self.simboloCiudad
            nuevoLugar = Punto(unicode(nombreLugar,'iso-8859-1'),
                            int(tipo),simbolo,
                            (posx,posy),(incx,incy))
            self.listaLugares.append(nuevoLugar)
            linea = f.readline()
        f.close()

    def cargarListaDirectorios(self):
        """Carga la lista de directorios con los distintos mapas"""
        self.listaDirectorios = list()
        self.listaNombreDirectorios = list()
        listaTemp = os.listdir(CAMINORECURSOS)
        listaTemp.sort()
        for d in listaTemp:
            if d == "comun":
                pass
            else:
                self.listaDirectorios.append(d)
                f = open(os.path.join(CAMINORECURSOS,d,ARCHIVONOMBRE),"r")
                linea = f.readline()
                self.listaNombreDirectorios.append(\
                    unicode(linea.strip(),'iso-8859-1'))
                f.close()

    def cargarNiveles(self):
        """Carga los niveles del archivo de configuracion"""
        self.listaNiveles = list()
        self.listaPrefijos = list()
        self.listaSufijos = list()
        self.listaCorrecto = list()
        self.listaMal = list()
        self.listaDespedidasB = list()
        self.listaDespedidasM = list()
        # falta sanitizar manejo de archivo
        f = open(os.path.join(self.camino_datos,ARCHIVONIVELES),"r")
        linea = f.readline()
        while linea:
            if linea[0] == "#":
                linea = f.readline()
                continue
            if linea[0] == "[":
                # empieza nivel
                nombreNivel = linea.strip("[]\n")
                nombreNivel = unicode(nombreNivel,'iso-8859-1')
                nuevoNivel = Nivel(nombreNivel)
                self.listaNiveles.append(nuevoNivel)
                linea = f.readline()
                continue
            if linea.find("=") == -1:
                linea = f.readline()
                continue
            [var,valor] = linea.strip().split("=")
            if var.startswith("Prefijo"):
                self.listaPrefijos.append(
                    unicode(valor.strip(),'iso-8859-1'))
            elif var.startswith("Sufijo"):
                self.listaSufijos.append(
                    unicode(valor.strip(),'iso-8859-1'))
            elif var.startswith("Correcto"):
                self.listaCorrecto.append(
                    unicode(valor.strip(),'iso-8859-1'))
            elif var.startswith("Mal"):
                self.listaMal.append(
                    unicode(valor.strip(),'iso-8859-1'))
            elif var.startswith("DespedidaB"):
                self.listaDespedidasB.append(
                    unicode(valor.strip(),'iso-8859-1'))
            elif var.startswith("DespedidaM"):
                self.listaDespedidasM.append(
                    unicode(valor.strip(),'iso-8859-1'))
            elif var.startswith("dibujoInicial"):
                listaDibujos = valor.split(",")
                for i in listaDibujos:
                    nuevoNivel.dibujoInicial.append(i.strip())
            elif var.startswith("nombreInicial"):
                listaNombres = valor.split(",")
                for i in listaNombres:
                    nuevoNivel.nombreInicial.append(i.strip())
            elif var.startswith("Pregunta"):
                [texto,tipo,respuesta,ayuda] = valor.split("|")
                nuevoNivel.preguntas.append(
                    (unicode(texto.strip(),'iso-8859-1'),
                    int(tipo),
                    unicode(respuesta.strip(),'iso-8859-1'),
                    unicode(ayuda.strip(),'iso-8859-1')))
            linea = f.readline()
        f.close()
        self.indiceNivelActual = 0
        self.numeroNiveles = len(self.listaNiveles)
        self.numeroSufijos = len(self.listaSufijos)
        self.numeroPrefijos = len(self.listaPrefijos)
        self.numeroCorrecto = len(self.listaCorrecto)
        self.numeroMal = len(self.listaMal)
        self.numeroDespedidasB = len(self.listaDespedidasB)
        self.numeroDespedidasM = len(self.listaDespedidasM)

    def cargarExploraciones(self):
        """Carga los niveles de exploracion del archivo de configuracion"""
        self.listaExploraciones = list()
        # falta sanitizar manejo de archivo
        f = open(os.path.join(self.camino_datos,ARCHIVOEXPLORACIONES),"r")
        linea = f.readline()
        while linea:
            if linea[0] == "#":
                linea = f.readline()
                continue
            if linea[0] == "[":
                # empieza nivel
                nombreNivel = linea.strip("[]\n")
                nuevoNivel = Nivel(nombreNivel)
                self.listaExploraciones.append(nuevoNivel)
                linea = f.readline()
                continue
            if linea.find("=") == -1:
                linea = f.readline()
                continue
            [var,valor] = linea.strip().split("=")
            if var.startswith("dibujoInicial"):
                listaDibujos = valor.split(",")
                for i in listaDibujos:
                    nuevoNivel.dibujoInicial.append(i.strip())
            elif var.startswith("nombreInicial"):
                listaNombres = valor.split(",")
                for i in listaNombres:
                    nuevoNivel.nombreInicial.append(i.strip())
            elif var.startswith("elementosActivos"):
                listaNombres = valor.split(",")
                for i in listaNombres:
                    nuevoNivel.elementosActivos.append(i.strip())
            linea = f.readline()
        f.close()
        self.numeroExploraciones = len(self.listaExploraciones)

    def pantallaAcercaDe(self):
        """Pantalla con los datos del juego, creditos, etc"""
        global scale, shift_x, shift_y, xo_resolution
        self.pantallaTemp = pygame.Surface(
            (self.anchoPantalla,self.altoPantalla))
        self.pantallaTemp.blit(self.pantalla,(0,0))
        self.pantalla.fill((0,0,0))
        self.pantalla.blit(self.terron,
                        (int(20*scale+shift_x),
                            int(20*scale+shift_y)))
        self.pantalla.blit(self.jp1,
                        (int(925*scale+shift_x),
                            int(468*scale+shift_y)))
        self.mostrarTexto(unicode(_("About I know India"), "UTF-8"),
                        self.fuente40,
                        (int(600*scale+shift_x),
                        int(100*scale+shift_y)),
                        (255,255,255))
        # falta sanitizar acceso a archivo
        f = open(os.path.join(CAMINORECURSOS,
                            CAMINOCOMUN,
                            CAMINODATOS,
                            ARCHIVOCREDITOS),"r")
        yLinea = int(200*scale+shift_y)
        for linea in f:
            self.mostrarTexto(linea.strip(),
                            self.fuente32,
                            (int(600*scale+shift_x),yLinea),
                            (155,155,255))
            yLinea = yLinea + int(40*scale)
        f.close()
        self.mostrarTexto(_("Press any key to return"),
                        self.fuente32,
                        (int(600*scale+shift_x),
                        int(800*scale+shift_y)),
                        (255,155,155))
        pygame.display.flip()
        while 1:
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
        global scale, shift_x, shift_y
        self.pantalla.fill((0,0,0))
        self.mostrarTexto(unicode(_("I know India"), "UTF-8"),
                        self.fuente60,
                        (int(600*scale+shift_x),
                        int(80*scale+shift_y)),
                        (255,255,255))
        self.mostrarTexto(_("You have chosen the map ")+\
                            self.listaNombreDirectorios\
                            [self.indiceDirectorioActual],
                        self.fuente40,
                        (int(600*scale+shift_x), int(140*scale+shift_y)),
                        (200,100,100))
        self.mostrarTexto(_("Play"),
                        self.fuente60,
                        (int(300*scale+shift_x), int(220*scale+shift_y)),
                        (200,100,100))
        yLista = int(300*scale+shift_y)
        for n in self.listaNiveles:
            self.pantalla.fill((20,20,20),
                            (int(10*scale+shift_x),
                                yLista-int(24*scale),
                                int(590*scale),
                                int(48*scale)))
            self.mostrarTexto(n.nombre,
                            self.fuente40,
                            (int(300*scale+shift_x), yLista),
                            (200,100,100))
            yLista += int(50*scale)
        self.mostrarTexto(_("Explore"),
                        self.fuente60,
                        (int(900*scale+shift_x), int(220*scale+shift_y)),
                        (100,100,200))
        yLista = int(300*scale+shift_y)
        for n in self.listaExploraciones:
            self.pantalla.fill((20,20,20),
                            (int(610*scale+shift_x),
                                yLista-int(24*scale),
                                int(590*scale),
                                int(48*scale)))
            self.mostrarTexto(n.nombre,
                            self.fuente40,
                            (int(900*scale+shift_x),yLista),
                            (100,100,200))
            yLista += int(50*scale)
        self.pantalla.fill((20,20,20),
                        (int(10*scale+shift_x),
                            int(801*scale+shift_y),
                            int(590*scale),int(48*scale)))
        self.mostrarTexto(_("About this game"),
                        self.fuente40,
                        (int(300*scale+shift_x),int(825*scale+shift_y)),
                        (100,200,100))
        self.pantalla.fill((20,20,20),
                        (int(610*scale+shift_x),
                            int(801*scale+shift_y),
                            int(590*scale),int(48*scale)))
        self.mostrarTexto(_("Return"),
                        self.fuente40,
                        (int(900*scale+shift_x),int(825*scale+shift_y)),
                        (100,200,100))
        pygame.display.flip()
        while 1:
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
                    if pos[1] > 275*scale + shift_y: # zona de opciones
                        if pos[0] < 600*scale + shift_x: # primera columna
                            if pos[1] < 275*scale + shift_y + \
                                    len(self.listaNiveles)*50*scale: # nivel
                                self.indiceNivelActual = \
                                    int((pos[1]-int(275*scale+shift_y))//\
                                            int(50*scale))
                                self.jugar = True
                                return
                            elif pos[1] > 800*scale + shift_y and \
                                    pos[1] < 850*scale + shift_y: # acerca de
                                self.pantallaAcercaDe()
                        else: # segunda columna
                            if pos[1] < 275*scale + shift_y+\
                                    len(self.listaExploraciones)*50*scale:
                                # nivel de exploracion
                                self.indiceNivelActual = \
                                    int((pos[1]-int(275*scale+shift_y))//\
                                            int(50*scale))
                                self.jugar = False
                                return
                            elif pos[1] > 800*scale + shift_y and \
                                    pos[1] < 850*scale+shift_y: # volver
                                self.elegir_directorio = True
                                return
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()

    def pantallaDirectorios(self):
        """Pantalla con el menu de directorios"""
        global scale, shift_x, shift_y
        self.pantalla.fill((0,0,0))
        self.mostrarTexto(unicode(_("I know India"), "UTF-8"),
                        self.fuente60,
                        (int(600*scale+shift_x),int(80*scale+shift_y)),
                        (255,255,255))
        self.mostrarTexto(_("Choose the map to use"),
                        self.fuente40,
                        (int(600*scale+shift_x),int(140*scale+shift_y)),
                        (200,100,100))
        nDirectorios = len(self.listaNombreDirectorios)
        paginaDirectorios = self.paginaDir
        while 1:
            yLista = int(200*scale+shift_y)
            self.pantalla.fill((0,0,0),
                            (int(shift_x),yLista-int(24*scale),
                                int(1200*scale),int(600*scale)))
            if paginaDirectorios == 0:
                paginaAnteriorActiva = False
            else:
                paginaAnteriorActiva = True
            paginaSiguienteActiva = False
            if paginaAnteriorActiva:
                self.pantalla.fill((20,20,20),
                                (int(10*scale+shift_x),yLista-int(24*scale),
                                    int(590*scale),int(48*scale)))
                self.mostrarTexto(unicode(_("<<< Previous page"), "UTF-8"),
                                self.fuente40,
                                (int(300*scale+shift_x),yLista),
                                (100,100,200))
            yLista += int(50*scale)
            indiceDir = paginaDirectorios * 20
            terminar = False
            while not terminar:
                self.pantalla.fill((20,20,20),
                                (int(10*scale+shift_x),yLista-int(24*scale),
                                    int(590*scale),int(48*scale)))
                self.mostrarTexto(self.listaNombreDirectorios[indiceDir],
                                self.fuente40,
                                (int(300*scale+shift_x),yLista),
                                (200,100,100))
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
                    self.pantalla.fill((20,20,20),
                                    (int(610*scale+shift_x),
                                        yLista-int(24*scale),
                                        int(590*scale),int(48*scale)))
                    self.mostrarTexto(self.listaNombreDirectorios[indiceDir],
                                    self.fuente40,
                                    (int(900*scale+shift_x),yLista),
                                    (200,100,100))
                    yLista += int(50*scale)
                    indiceDir = indiceDir + 1
                    if indiceDir == nDirectorios or \
                            indiceDir == paginaDirectorios * 20 + 20:
                        terminar = True
                if indiceDir == paginaDirectorios * 20 + 20:
                    if indiceDir < nDirectorios:
                        self.pantalla.fill((20,20,20),
                                        (int(610*scale+shift_x),
                                            yLista-int(24*scale),
                                            int(590*scale),int(48*scale)))
                        self.mostrarTexto(unicode(_("Next page >>>"), "UTF-8"),
                                        self.fuente40,
                                        (int(900*scale+shift_x),yLista),
                                        (100,100,200))
                        paginaSiguienteActiva = True
                    nDirectoriosCol2 = 10
                else:
                    nDirectoriosCol2 = indiceDir - paginaDirectorios * 20 - 10
            else:
                nDirectoriosCol1 = indiceDir - paginaDirectorios * 20
                nDirectoriosCol2 = 0
            self.pantalla.fill((20,20,20),
                            (int(10*scale+shift_x),int(801*scale+shift_y),
                                int(590*scale),int(48*scale)))
            self.mostrarTexto(_("About this game"),
                            self.fuente40,
                            (int(300*scale+shift_x),int(825*scale+shift_y)),
                            (100,200,100))
            self.pantalla.fill((20,20,20),
                            (int(610*scale+shift_x),int(801*scale+shift_y),
                                int(590*scale),int(48*scale)))
            self.mostrarTexto(_("Exit"),
                            self.fuente40,
                            (int(900*scale+shift_x),int(825*scale+shift_y)),
                            (100,200,100))
            pygame.display.flip()
            cambiarPagina = False
            while not cambiarPagina:
                for event in wait_events():
                    if event.type == pygame.KEYDOWN:
                        if event.key == 27: # escape: salir
                            if self.sound:
                                self.click.play()
                            sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.sound:
                            self.click.play()
                        pos = event.pos
                        if pos[1] > 175*scale+shift_y: # zona de opciones
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
                                elif pos[1] > 800*scale + shift_y and \
                                        pos[1] < 850*scale + shift_y: # acerca
                                    self.pantallaAcercaDe()
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
                                elif pos[1] > 800*scale+shift_y and \
                                        pos[1] < 850*scale+shift_y: # salir
                                    sys.exit()
                    elif event.type == EVENTOREFRESCO:
                        pygame.display.flip()

    def cargarImagen(self,nombre):
        """Carga una imagen y la escala de acuerdo a la resolucion"""
        global scale, xo_resolution
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

    def __init__(self):
        """Esta es la inicializacion del juego"""
        global scale, shift_x, shift_y, xo_resolution
        pygame.init()
        # crear pantalla
        self.anchoPantalla = gtk.gdk.screen_width()
        self.altoPantalla = gtk.gdk.screen_height()
        self.pantalla = pygame.display.set_mode((self.anchoPantalla,
                                                self.altoPantalla))
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
        # fondo presentacion
        self.fondo1 = self.cargarImagen("fondo1.png")
        self.fondo2 = self.cargarImagen("fondo2.png")
        # JP presentacion
        self.jpp1 = self.cargarImagen("jpp1.png")
        self.jpp2 = self.cargarImagen("jpp2.png")
        # globo
        self.globo1 = self.cargarImagen("globo1.png")
        self.globo2 = pygame.transform.flip(self.globo1, True, False)
        self.globo3 = self.cargarImagen("globo3.png")
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
                            self.camino_sonidos,"junggle_btn045.wav"))
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
        self.cargarDepartamentos()
        try:
            self.cargarRios()
        except:
            pass
        try:
            self.cargarRutas()
        except:
            pass
        try:
            self.cargarCuchillas()
        except:
            pass
        self.cargarLugares()
        self.cargarNiveles()
        self.cargarExploraciones()

    def mostrarGlobito(self,lineas):
        """Muestra texto en el globito"""
        global scale, shift_x, shift_y
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
        global scale, shift_x, shift_y
        self.pantalla.blit(self.globito,
                        (int(XMAPAMAX*scale+shift_x),
                            int(YGLOBITO*scale+shift_y)))

    def correcto(self):
        """Muestra texto en el globito cuando la respuesta es correcta"""
        global scale, shift_x, shift_y
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
            encontrado = False
            for d in self.listaDeptos:
                if d.nombre == respCorrecta:
                    encontrado = True
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
            encontrado = False
            for l in self.listaLugares:
                if l.nombre == respCorrecta:
                    encontrado = True
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
            encontrado = False
            for d in self.listaRios:
                if d.nombre == respCorrecta:
                    encontrado = True
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
            encontrado = False
            for d in self.listaCuchillas:
                if d.nombre == respCorrecta:
                    encontrado = True
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
            encontrado = False
            for l in self.listaLugares:
                if l.nombre == respCorrecta:
                    encontrado = True
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
            encontrado = False
            for d in self.listaRutas:
                if d.nombre == respCorrecta:
                    encontrado = True
                    break
            if d.estaAca(pos):
                d.mostrarNombre(self.pantalla,
                                self.fuente24,
                                COLORNOMBRERUTA,
                                True)
                return True
            else:
                return False

    def explorarNombres(self):
        """Juego principal en modo exploro."""
        self.nivelActual = self.listaExploraciones[self.indiceNivelActual]
        # presentar nivel
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
        # boton terminar
        self.pantalla.fill((100,20,20),(int(975*scale+shift_x),
                                        int(25*scale+shift_y),
                                        int(200*scale),
                                        int(50*scale)))
        self.mostrarTexto(_("End"),
                        self.fuente40,
                        (int(1075*scale+shift_x),
                        int(50*scale+shift_y)),
                        (255,155,155))
        pygame.display.flip()
        # boton mostrar todo
        self.pantalla.fill((100,20,20),(int(975*scale+shift_x),
                                        int(90*scale+shift_y),
                                        int(200*scale),
                                        int(50*scale)))
        self.mostrarTexto(_("Show all"),
                        self.fuente40,
                        (int(1075*scale+shift_x),
                        int(115*scale+shift_y)),
                        (255,155,155))
        pygame.display.flip()
        # lazo principal de espera por acciones del usuario
        while 1:
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
                                        break
                            elif i.startswith("ciudades"):
                                for l in self.listaLugares:
                                    if l.tipo == 2 and l.estaAca(event.pos):
                                        l.mostrarNombre(self.pantalla,
                                                        self.fuente24,
                                                        COLORNOMBRECAPITAL,
                                                        True)
                                        break
                            elif i.startswith("rios"):
                                for d in self.listaRios:
                                    if d.estaAca(event.pos):
                                        d.mostrarNombre(self.pantalla,
                                                        self.fuente24,
                                                        COLORNOMBRERIO,
                                                        True)
                                        break
                            elif i.startswith("rutas"):
                                for d in self.listaRutas:
                                    if d.estaAca(event.pos):
                                        d.mostrarNombre(self.pantalla,
                                                        self.fuente24,
                                                        COLORNOMBRERUTA,
                                                        True)
                                        break
                            elif i.startswith("cuchillas"):
                                for d in self.listaCuchillas:
                                    if d.estaAca(event.pos):
                                        d.mostrarNombre(self.pantalla,
                                                        self.fuente24,
                                                        COLORNOMBREELEVACION,
                                                        True)
                                        break
                            elif i.startswith("cerros"):
                                for l in self.listaLugares:
                                    if l.tipo == 5 and l.estaAca(event.pos):
                                        l.mostrarNombre(self.pantalla,
                                                        self.fuente24,
                                                        COLORNOMBREELEVACION,
                                                        True)
                                        break
                            elif i.startswith("deptos"):
                                for d in self.listaDeptos:
                                    if d.estaAca(event.pos):
                                        d.mostrarNombre(self.pantalla,
                                                        self.fuente32,
                                                        COLORNOMBREDEPTO,
                                                        True)
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
        self.nivelActual = self.listaNiveles[self.indiceNivelActual]
        self.avanceNivel = 0
        self.nivelActual.prepararPreguntas()
        # presentar nivel
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
            if i.startswith("rios"):
                for d in self.listaRios:
                    d.mostrarNombre(self.pantalla,self.fuente24,
                                    COLORNOMBRERIO,False)
            if i.startswith("rutas"):
                for d in self.listaRutas:
                    d.mostrarNombre(self.pantalla,self.fuente24,
                                    COLORNOMBRERUTA,False)
            if i.startswith("cuchillas"):
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
        self.pantalla.fill((100,20,20),
                        (int(975*scale+shift_x),
                            int(26*scale+shift_y),
                            int(200*scale),
                            int(48*scale)))
        self.mostrarTexto(_("End"),
                        self.fuente40,
                        (int(1075*scale+shift_x),
                        int(50*scale+shift_y)),
                        (255,155,155))
        pygame.display.flip()
        # presentar pregunta inicial
        self.lineasPregunta = self.nivelActual.siguientePregunta(\
                self.listaSufijos,self.listaPrefijos)
        self.mostrarGlobito(self.lineasPregunta)
        # barra puntaje
        rect = pygame.draw.rect(self.pantalla, (0,0,0),
                                (int(XBARRA_P*scale+shift_x),
                                int((YBARRA_P-350)*scale+shift_y),
                                int(ABARRA_P*scale),
                                int(350*scale)), 3)
        self.mostrarTexto('0',self.fuente32,
            (int((XBARRA_P+ABARRA_P/2)*scale+shift_x),
            int(YBARRA_P+10)*scale+shift_y), COLORBARRA_P)
        # barra avance
        unidad = ABARRA_A / TOTALAVANCE
        rect = pygame.draw.rect(self.pantalla, (0,0,0),
                                (int(XBARRA_A*scale+shift_x),
                                int(YBARRA_A*scale+shift_y),
                                int(ABARRA_A*scale),
                                int(ABARRA_P*scale)), 3)
        for i in range(TOTALAVANCE-1):
            posx = int((XBARRA_A + unidad * (i+1))*scale+shift_x)
            l = pygame.draw.line(self.pantalla, (0,0,0),
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
        # leer eventos y ver si la respuesta es correcta
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == 27: # escape: salir
                        self.click.play()
                        pygame.time.set_timer(EVENTORESPUESTA,0)
                        pygame.time.set_timer(EVENTODESPEGUE,0)
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.click.play()
                    if self.avanceNivel < TOTALAVANCE:
                        if event.pos[0] < XMAPAMAX*scale+shift_x: # zona mapa
                            self.borrarGlobito()
                            if self.esCorrecta(self.nivelActual,
                                            event.pos):
                                if not(self.otorgado):
                                    self.correcto()
                                    self.otorgado = True
                            else:
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
                                rect = pygame.draw.rect(self.pantalla, (0,0,0),
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
                            rect = pygame.draw.rect(self.pantalla, (0,0,0),
                                                (int(XBARRA_A*scale+shift_x),
                                                int(YBARRA_A*scale+shift_y),
                                                int(ABARRA_A*scale),
                                                int(ABARRA_P*scale)), 3)
                            for i in range(TOTALAVANCE-1):
                                posx = int((XBARRA_A + unidad * (i+1))*scale+shift_x)
                                l = pygame.draw.line(self.pantalla, (0,0,0),
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
                        rect = pygame.draw.rect(self.pantalla, (0,0,0),
                                            (int(XBARRA_A*scale+shift_x),
                                            int((YBARRA_A)*scale+shift_y),
                                            int(ABARRA_A*scale),
                                            int(ABARRA_P*scale)), 3)
                        for i in range(TOTALAVANCE-1):
                            posx = int((XBARRA_A + unidad * (i+1))*scale+shift_x)
                            l = pygame.draw.line(self.pantalla, (0,0,0),
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
                                .split("\\")
                        else:
                            self.lineasPregunta =  self.listaDespedidasM[\
                                random.randint(1,self.numeroDespedidasM)-1]\
                                .split("\\")
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

    def presentacion(self):

        #***************************** cuadro 1 ******************************
        self.pantalla.fill((0,0,0))
        self.pantalla.blit(self.fondo1,
                        (int(75*scale+shift_x),int(75*scale+shift_y)))
        self.mostrarTexto(_("Press any key to skip"),
                        self.fuente32,
                        (int(600*scale+shift_x),int(800*scale+shift_y)),
                        (255,155,155))
        pygame.display.flip()
        # esperar o no esperar, esa es la cuestion
        time.sleep(0.5)
        # cargo el texto de la presentacion
        self.listaPresentacion = list()
        f = open(os.path.join(CAMINORECURSOS,
                              CAMINOCOMUN,
                              CAMINODATOS,ARCHIVOPRESENTACION),"r")
        for linea in f:
            self.listaPresentacion.append(unicode(linea,'iso-8859-1'))
        f.close()

        # comienzo animacion
        self.pantalla.blit(self.globo1,
                        (int(180*scale+shift_x),int(260*scale+shift_y)))
        yLinea = int(330*scale+shift_y)
        # hola amigos
        lineas = self.listaPresentacion[0].split("\\")
        for l in lineas:
            text = self.fuente40.render(l.strip(), 1, COLORPREGUNTAS)
            textrect = text.get_rect()
            textrect.center = (int(384*scale+shift_x),yLinea)
            self.pantalla.blit(text, textrect)
            yLinea = yLinea+self.fuente32.get_height()+int(10*scale)
        pygame.display.flip()

        #time.sleep(2)
        terminar = False
        pygame.time.set_timer(EVENTORESPUESTA, 2000)
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound:
                        self.click.play()
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    return
                elif event.type == EVENTORESPUESTA:
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    terminar = True
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()
            if terminar:
                break

        self.pantalla.blit(self.globo1,
                        (int(180*scale+shift_x),int(260*scale+shift_y)))
        yLinea = int(315*scale+shift_y)
        # mañana tengo...
        lineas = self.listaPresentacion[1].split("\\")
        for l in lineas:
            text = self.fuente40.render(l.strip(), 1, COLORPREGUNTAS)
            textrect = text.get_rect()
            textrect.center = (int(384*scale+shift_x),yLinea)
            self.pantalla.blit(text, textrect)
            yLinea = yLinea+self.fuente32.get_height()+int(10*scale)
        pygame.display.flip()
        terminar = False
        pygame.time.set_timer(EVENTORESPUESTA, 2000)
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound:
                        self.click.play()
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    return
                elif event.type == EVENTORESPUESTA:
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    terminar = True
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()
            if terminar:
                break

        #***************************** cuadro 3 ******************************
        self.pantalla.blit(self.globo3,
                        (int(618*scale+shift_x),int(78*scale+shift_y)))
        pygame.display.flip()
        terminar = False
        pygame.time.set_timer(EVENTORESPUESTA, 2000)
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound:
                        self.click.play()
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    return
                elif event.type == EVENTORESPUESTA:
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    terminar = True
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()
            if terminar:
                break

        #***************************** cuadro 4 ******************************
        # **************************** fondo 2 *******************************
        self.pantalla.blit(self.fondo2,
                        (int(75*scale+shift_x),int(75*scale+shift_y)))
        self.pantalla.blit(self.jpp1,
                        (int(487*scale+shift_x),int(347*scale+shift_y)))
        self.mostrarTexto(_("Press any key to skip"),
                        self.fuente32,
                        (int(600*scale+shift_x),int(800*scale+shift_y)),
                        (255,155,155))
        pygame.display.flip()
        # espero
        time.sleep(0.5)
        self.pantalla.blit(self.globo1,
                        (int(160*scale+shift_x),int(240*scale+shift_y)))
        yLinea = int(310*scale+shift_y)
        # y no se nada
        lineas = self.listaPresentacion[2].split("\\")
        for l in lineas:
            text = self.fuente40.render(l.strip(), 1, COLORPREGUNTAS)
            textrect = text.get_rect()
            textrect.center = (int(360*scale+shift_x),yLinea)
            self.pantalla.blit(text, textrect)
            yLinea = yLinea+self.fuente32.get_height()+int(10*scale)
        pygame.display.flip()
        terminar = False
        pygame.time.set_timer(EVENTORESPUESTA, 1000)
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound:
                        self.click.play()
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    return
                elif event.type == EVENTORESPUESTA:
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    terminar = True
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()
            if terminar:
                break

        #***************************** cuadro 5 ******************************
        self.pantalla.blit(self.globo2,
                        (int(570*scale+shift_x),int(260*scale+shift_y)))
        yLinea = int(330*scale+shift_y)
        # que hago
        lineas = self.listaPresentacion[3].split("\\")
        for l in lineas:
            text = self.fuente40.render(l.strip(), 1, COLORPREGUNTAS)
            textrect = text.get_rect()
            textrect.center = (int(770*scale+shift_x),yLinea)
            self.pantalla.blit(text, textrect)
            yLinea = yLinea + self.fuente32.get_height()+int(10*scale)
        pygame.display.flip()
        terminar = False
        pygame.time.set_timer(EVENTORESPUESTA, 2000)
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound:
                        self.click.play()
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    return
                elif event.type == EVENTORESPUESTA:
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    terminar = True
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()
            if terminar:
                break

        #***************************** cuadro 6 ******************************
        self.pantalla.blit(self.fondo2,
                        (int(75*scale+shift_x),int(75*scale+shift_y)))
        self.pantalla.blit(self.jpp2,
                        (int(487*scale+shift_x),int(347*scale+shift_y)))
        self.mostrarTexto(_("Press any key to skip"),
                        self.fuente32,
                        (int(600*scale+shift_x),int(800*scale+shift_y)),
                        (255,155,155))
        pygame.display.flip()
        # espero
        time.sleep(0.5)

        self.pantalla.blit(self.globo1,
                        (int(160*scale+shift_x),int(240*scale+shift_y)))
        yLinea = int(310*scale+shift_y)
        # te puedo pedir
        lineas = self.listaPresentacion[4].split("\\")
        for l in lineas:
            text = self.fuente40.render(l.strip(), 1, COLORPREGUNTAS)
            textrect = text.get_rect()
            textrect.center = (int(360*scale+shift_x),yLinea)
            self.pantalla.blit(text, textrect)
            yLinea = yLinea + self.fuente32.get_height()+int(10*scale)
        pygame.display.flip()

        #time.sleep(1)
        terminar = False
        pygame.time.set_timer(EVENTORESPUESTA, 1500)
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound:
                        self.click.play()
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    return
                elif event.type == EVENTORESPUESTA:
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    terminar = True
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()
            if terminar:
                break

        self.pantalla.blit(self.globo1,
                        (int(160*scale+shift_x),int(240*scale+shift_y)))
        yLinea = int(310*scale+shift_y)
        # me ayudas
        lineas = self.listaPresentacion[5].split("\\")
        for l in lineas:
            text = self.fuente40.render(l.strip(), 1, COLORPREGUNTAS)
            textrect = text.get_rect()
            textrect.center = (int(360*scale+shift_x),yLinea)
            self.pantalla.blit(text, textrect)
            yLinea = yLinea + self.fuente32.get_height()+int(10*scale)
        pygame.display.flip()
        terminar = False
        pygame.time.set_timer(EVENTORESPUESTA, 2000)
        while 1:
            for event in wait_events():
                if event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sound:
                        self.click.play()
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    return
                elif event.type == EVENTORESPUESTA:
                    pygame.time.set_timer(EVENTORESPUESTA,0)
                    terminar = True
                elif event.type == EVENTOREFRESCO:
                    pygame.display.flip()
            if terminar:
                break

        return

    def principal(self):
        """Este es el loop principal del juego"""
        global scale, shift_x, shift_y
        pygame.time.set_timer(EVENTOREFRESCO,TIEMPOREFRESCO)
        self.presentacion()
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
                else:
                    self.pantalla.blit(self.bandera,
                                    (int((XMAPAMAX+47)*scale+shift_x),
                                    int(155*scale+shift_y)))
                    f = open(os.path.join(CAMINORECURSOS,
                                        self.directorio,
                                        CAMINODATOS,ARCHIVOESTADISTICAS),"r")
                    yLinea = int(YTEXTO*scale) + shift_y + \
                                self.fuente9.get_height()
                    linea = f.readline()
                    while linea:
                        [parte1,parte2] = linea.strip().split("|")
                        text1 = self.fuente9.render(parte1, 1, COLORESTADISTICAS1)
                        self.pantalla.blit(text1,
                                ((XMAPAMAX+10)*scale+shift_x, yLinea))
                        text2 = self.fuente9.render(parte2, 1, COLORESTADISTICAS2)
                        self.pantalla.blit(text2,
                                ((XMAPAMAX+135)*scale+shift_x, yLinea))
                        yLinea = yLinea+self.fuente9.get_height()+int(5*scale)
                        linea = f.readline()
                    f.close()
                    pygame.display.flip()
                    self.explorarNombres()


def main():
    juego = ConozcoIn()
    juego.principal()


if __name__ == "__main__":
    main()
