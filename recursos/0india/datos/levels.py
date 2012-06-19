# -*- coding: utf-8 -*-

from gettext import gettext as _

LEVEL1 = [
        10,
        _('States'),
        ['lineasDepto'],
        [],
[
    (_('Andhra Pradesh'), _('Is south')),
    (_('Arunachal Pradesh'), _('Is northeast')),
    (_('Assam'), _('Is east')),
    (_('Bihar'), _('Is northeast')),
    (_('Chhattisgarh'), _('Is in the center')),
    (_('Goa'), _('Is southwest')),
    (_('Gujarat'), _('Is west')),
    (_('Haryana'), _('Is northwest')),
    (_('Himachal Pradesh'), _('Is north')),
    (_('Jammu and Kashmir'), _('Is north')),
    (_('Jharkhand'), _('Is in the center')),
    (_('Karnataka'), _('Is southwest')),
    (_('Kerala'), _('Is south')),
    (_('Madhya Pradesh'), _('Is in the center')),
    (_('Maharashtra'), _('Is west')),
    (_('Manipur'), _('Is east')),
    (_('Meghalaya'), _('Is east')),
    (_('Mizoram'), _('Is east')),
    (_('Nagaland'), _('Is east')),
    (_('Orissa'), _('Is east')),
    (_('Punjab'), _('Is northwest')),
    (_('Rajasthan'), _('Is northwest')),
    (_('Sikkim'), _('Is northeast')),
    (_('Tamil Nadu'), _('Is south')),
    (_('Tripura'), _('Is east')),
    (_('Uttar Pradesh'), _('Is north')),
    (_('Uttarakhand'), _('Is north')),
    (_('West Bengal'), _('Is west')),
    # UNION
    (_('Andaman and Nicobar Islands'), _('Is southeast')),
    #Chandigarh, 225, , , 0
    (_('Dadra and Nagar Haveli'), _('Is west')),
    #Daman and Diu, 223, , , 0
    (_('Lakshadweep'), _('Is southwest')),
    #Pondicherry, 221, , , 0
    (_('Delhi'), _('Is north'))
]
]

LEVEL2 = [
        2,
        _('State capitals'),
        ['lineasDepto', 'capitales'],
        [],
[
    (_('New Delhi'), _('Is in %s') % _('New Delhi')),
    (_('Hyderabad'), _('Is in %s') % _('Andhra Pradesh')),
    (_('Itanagar'), _('Is in %s') % _('Arunachal Pradesh')),
    (_('Dispur'), _('Is in %s') % _('Assam')),
    (_('Patna'), _('Is in %s') % _('Bihar')),
    (_('Raipur'), _('Is in %s') % _('Chhattisgarh')),
    (_('Panaji'), _('Is in %s') % _('Goa')),
    (_('Gandhinagar'), _('Is in %s') % _('Gujarat')),
    (_('Chandigarh'), _('Is in %s') % _('Haryana')),
    (_('Shimla'), _('Is in %s') % _('Himachal Pradesh')),
    (_('Srinagar'), _('Is in %s') % _('Jammu and Kashmir')),
    (_('Ranchi'), _('Is in %s') % _('Jharkhand')),
    (_('Bengalooru'), _('Is in %s') % _('Karnataka')),
    (_('Thiruvananthapuram'), _('Is in %s') % _('Kerala')),
    (_('Bhopal'), _('Is in %s') % _('Madhya Pradesh')),
    (_('Mumbai'), _('Is in %s') % _('Maharashtra')),
    (_('Imphal'), _('Is in %s') % _('Manipur')),
    (_('Shillong'), _('Is in %s') % _('Meghalaya')),
    (_('Aizawl'), _('Is in %s') % _('Mizoram')),
    (_('Kohima'), _('Is in %s') % _('Nagaland')),
    (_('Bhubaneswar'), _('Is in %s') % _('Orissa')),
    (_('Jaipur'), _('Is in %s') % _('Rajasthan')),
    (_('Gangtok'), _('Is in %s') % _('Sikkim')),
    (_('Chennai'), _('Is in %s') % _('Tamil Nadu')),
    (_('Agartala'), _('Is in %s') % _('Tripura')),
    (_('Lucknow'), _('Is in %s') % _('Uttar Pradesh')),
    (_('Dehradun'), _('Is in %s') % _('Uttarakhand')),
    (_('Kolkata'), _('Is in %s') % _('West Bengal')),
    (_('Port Blair'), _('Is in %s') % _('Andaman and Nicobar Islands')),
    (_('Silvassa'), _('Is in %s') % _('Dadra and Nagar Haveli')),
    (_('Daman'), _('Is in %s') % _('Daman and Diu')),
    (_('Kavaratti'), _('Is in %s') % _('Lakshadweep')),
    (_('Pondicherry'), _('Is in %s') % _('Pondicherry'))
]
]

LEVELS = [LEVEL1, LEVEL2]


