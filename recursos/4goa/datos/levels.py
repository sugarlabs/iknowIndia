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
        _('Taluka Headquarters'),
        ['lineasDepto', 'capitales'],
        [],
[
    (_('Panaji'), _("It's in %s taluka") % _('Tiswadi') + '\n' + _("It's in the west")),
    (_('Pernem'), _("It's in %s taluka") % _('Pernem') + '\n' + _("It's in the northwest")),
    (_('Mapusa'), _("It's in %s taluka") % _('Bardez') + '\n' + _("It's in the northwest")),
    (_('Bicholim'), _("It's in %s taluka") % _('Bicholim') + '\n' + _("It's in the north")),
    (_('Vasco da Gama'), _("It's in %s taluka") % _('Mormugao') + '\n' + _("It's in the west")),
    (_('Valpoi'), _("It's in %s taluka") % _('Sattari') + '\n' + _("It's in the northeast")),
    (_('Sanguem'), _("It's in %s taluka") % _('Sanguem') + '\n' + _("It's in the east")),
    (_('Margao'), _("It's in %s taluka") % _('Salcete') + '\n' + _("It's in the west")),
    (_('Quepem'), _("It's in %s taluka") % _('Quepem') + '\n' + _("It's in the south")),
    (_('Chaudi'), _("It's in %s taluka") % _('Canacona') + '\n' + _("It's in the south")),
    (_('Ponda'), _("It's in %s taluka") % _('Ponda') + '\n' + _("It's in the center"))
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


