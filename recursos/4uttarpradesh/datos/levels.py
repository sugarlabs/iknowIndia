# -*- coding: utf-8 -*-

from gettext import gettext as _

LEVEL1 = [
        1,
        _('Divisions'),
        ['lineasDepto'],
        [],
[
    (_('Saharanpur'), 1,_('Saharanpur'),  _("It's in the northwest")),
    (_('Moradabad'), 1, _('Moradabad'), _("It's in the northwest")),
    (_('Bareilly'), 1, _('Bareilly'), _("It's in the north")),
    (_('Lucknow'), 1, _('Lucknow'), _("It's in the center")),
    (_('Devipatan'), 1, _('Devipatan'), _("It's in the northeast")),
    (_('Basti'), 1, _('Basti'), _("It's in the northeast")),
    (_('Gorakhpur'), 1, _('Gorakhpur'), _("It's in the east")),
    (_('Meerut'), 1, _('Meerut'), _("It's in the northwest")),
    (_('Aligarh'), 1, _('Aligarh'), _("It's in the west")),
    (_('Agra'), 1, _('Agra'), _("It's in the west")),
    (_('Kanpur'), 1, _('Kanpur'), _("It's in the center")),
    (_('Faizabad'), 1, _('Faizabad'), _("It's in the center")),
    (_('Azamgarh'), 1, ('Azamgarh'), _("It's in the east")),
    (_('Jhansi'), 1, _('Jhansi'), _("It's in the southwest")),
    (_('Chitrakoot'), 1, _('Chitrakoot'), _("It's in the south")),
    (_('Allahabad'), 1, ('Allahabad'), _("It's in the south")),
    (_('Varanasi'), 1, _('Varanasi'), _("It's in the east")),
    (_('Mirzapur'), 1, _('Mirzapur'), _("It's in the southeast"))
]
]

LEVEL2 = [
        2,
        _('Taluka Headquarters'),
        ['lineasDepto', 'capitales'],
        [],
[
    #(_('Panaji'), _("It's in %s taluka") % _('Tiswadi') + '\n' + _("It's in the west")),

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

LEVELS = [LEVEL1]


