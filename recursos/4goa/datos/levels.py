# -*- coding: utf-8 -*-

from gettext import gettext as _

LEVEL1 = [
        14,
        _('Talukas'),
        ['lineasDepto'],
        [],
[
    (_('Pernem'), _("It's in the northwest")),
    (_('Bardez'), _("It's in the northwest")),
    (_('Bicholim'), _("It's in the north")),
    (_('Sattari'), _("It's in the northeast")),
    (_('Tiswadi'), _("It's in the west")),
    (_('Ponda'), _("It's in the center")),
    (_('Mormugao'), _("It's in the west")),
    (_('Salcete'), _("It's in the west")),
    (_('Sanguem'), _("It's in the east")),
    (_('Quepem'), _("It's in the south")),
    (_('Canacona'), _("It's in the south"))
]
]

LEVEL2 = [
        2,
        _('Talukas capitals'),
        ['lineasDepto', 'capitales'],
        [],
[
    (_('Panaji'), _("It's in %s") % _('Tiswadi')),
    (_('Pernem'), _("It's in %s") % _('Pernem')),
    (_('Mapusa'), _("It's in %s") % _('Bardez')),
    (_('Bicholim'), _("It's in %s") % _('Bicholim')),
    (_('Vasco da Gama'), _("It's in %s") % _('Mormugao')),
    (_('Valpoi'), _("It's in %s") % _('Sattari')),
    (_('Sanguem'), _("It's in %s") % _('Sanguem')),
    (_('Margao'), _("It's in %s") % _('Salcete')),
    (_('Quepem'), _("It's in %s") % _('Quepem')),
    (_('Chaudi'), _("It's in %s") % _('Canacona')),
    (_('Ponda'), _("It's in %s") % _('Ponda'))
]
]


LEVEL3 = [
        2,
        _('Cities'),
        ['lineasDepto', 'capitales', 'ciudades'],
        [],
[
    #(_('New Delhi'), _('It is in %s') % _('New Delhi')),
  
]
]

LEVELS = [LEVEL1, LEVEL2]


