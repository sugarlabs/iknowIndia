# -*- coding: utf-8 -*-

from gettext import gettext as _

LEVEL1 = [
        10,
        _('States'),
        ['lineasDepto'],
        [],
[
    (_('Andhra Pradesh'), _("It's in the south")),
    (_('Arunachal Pradesh'), _("It's in the northeast")),
    (_('Assam'), _("It's in the east")),
    (_('Bihar'), _("It's in the northeast")),
    (_('Chhattisgarh'), _("It's in the center")),
    (_('Goa'), _("It's in the southwest")),
    (_('Gujarat'), _("It's in the west")),
    (_('Haryana'), _("It's in the northwest")),
    (_('Himachal Pradesh'), _("It's in the north")),
    (_('Jammu and Kashmir'), _("It's in the north")),
    (_('Jharkhand'), _("It's in the center")),
    (_('Karnataka'), _("It's in the southwest")),
    (_('Kerala'), _("It's in the south")),
    (_('Madhya Pradesh'), _("It's in the center")),
    (_('Maharashtra'), _("It's in the west")),
    (_('Manipur'), _("It's in the east")),
    (_('Meghalaya'), _("It's in the east")),
    (_('Mizoram'), _("It's in the east")),
    (_('Nagaland'), _("It's in the east")),
    (_('Odisha'), _("It's in the east")),
    (_('Punjab'), _("It's in the northwest")),
    (_('Rajasthan'), _("It's in the northwest")),
    (_('Sikkim'), _("It's in the northeast")),
    (_('Tamil Nadu'), _("It's in the south")),
    (_('Tripura'), _("It's in the east")),
    (_('Uttar Pradesh'), _("It's in the north")),
    (_('Uttarakhand'), _("It's in the north")),
    (_('West Bengal'), _("It's in the west")),
    # UNION
    (_('Andaman and Nicobar Islands'), _("It's in the southeast")),
    (_('Dadra and Nagar Haveli'), _("It's in the west")),
    (_('Lakshadweep'), _("It's in the southwest")),
    (_('Delhi'), _("It's in the north"))
]
]

LEVEL2 = [
        2,
        _('State capitals'),
        ['lineasDepto', 'capitales'],
        [],
[
    (_('New Delhi'), _("It's in %s") % _('New Delhi')),
    (_('Hyderabad'), _("It's in %s") % _('Andhra Pradesh')),
    (_('Itanagar'), _("It's in %s") % _('Arunachal Pradesh')),
    (_('Dispur'), _("It's in %s") % _('Assam')),
    (_('Patna'), _("It's in %s") % _('Bihar')),
    (_('Raipur'), _("It's in %s") % _('Chhattisgarh')),
    (_('Panaji'), _("It's in %s") % _('Goa')),
    (_('Gandhinagar'), _("It's in %s") % _('Gujarat')),
    (_('Chandigarh'), _("It's in %s") % _('Haryana')),
    (_('Shimla'), _("It's in %s") % _('Himachal Pradesh')),
    (_('Srinagar'), _("It's in %s") % _('Jammu and Kashmir')),
    (_('Ranchi'), _("It's in %s") % _('Jharkhand')),
    (_('Bengalooru'), _("It's in %s") % _('Karnataka')),
    (_('Thiruvananthapuram'), _("It's in %s") % _('Kerala')),
    (_('Bhopal'), _("It's in %s") % _('Madhya Pradesh')),
    (_('Mumbai'), _("It's in %s") % _('Maharashtra')),
    (_('Imphal'), _("It's in %s") % _('Manipur')),
    (_('Shillong'), _("It's in %s") % _('Meghalaya')),
    (_('Aizawl'), _("It's in %s") % _('Mizoram')),
    (_('Kohima'), _("It's in %s") % _('Nagaland')),
    (_('Bhubaneswar'), _("It's in %s") % _('Odisha')),
    (_('Jaipur'), _("It's in %s") % _('Rajasthan')),
    (_('Gangtok'), _("It's in %s") % _('Sikkim')),
    (_('Chennai'), _("It's in %s") % _('Tamil Nadu')),
    (_('Agartala'), _("It's in %s") % _('Tripura')),
    (_('Lucknow'), _("It's in %s") % _('Uttar Pradesh')),
    (_('Dehradun'), _("It's in %s") % _('Uttarakhand')),
    (_('Kolkata'), _("It's in %s") % _('West Bengal')),
    (_('Port Blair'), _("It's in %s") % _('Andaman and Nicobar Islands')),
    (_('Silvassa'), _("It's in %s") % _('Dadra and Nagar Haveli')),
    (_('Daman'), _("It's in %s") % _('Daman and Diu')),
    (_('Kavaratti'), _("It's in %s") % _('Lakshadweep')),
    (_('Pondicherry'), _("It's in %s") % _('Pondicherry'))
]
]


LEVEL3 = [
        2,
        _('Cities'),
        ['lineasDepto', 'capitales', 'ciudades'],
        [],
[
    (_('New Delhi'), _("It's in %s") % _('New Delhi')),
    (_('Hyderabad'), _("It's in %s") % _('Andhra Pradesh')),
    (_('Itanagar'), _("It's in %s") % _('Arunachal Pradesh')),
    (_('Dispur'), _("It's in %s") % _('Assam')),
    (_('Patna'), _("It's in %s") % _('Bihar')),
    (_('Raipur'), _("It's in %s") % _('Chhattisgarh')),
    (_('Panaji'), _("It's in %s") % _('Goa')),
    (_('Gandhinagar'), _("It's in %s") % _('Gujarat')),
    (_('Chandigarh'), _("It's in %s") % _('Haryana')),
    (_('Shimla'), _("It's in %s") % _('Himachal Pradesh')),
    (_('Srinagar'), _("It's in %s") % _('Jammu and Kashmir')),
    (_('Ranchi'), _("It's in %s") % _('Jharkhand')),
    (_('Bengalooru'), _("It's in %s") % _('Karnataka')),
    (_('Thiruvananthapuram'), _("It's in %s") % _('Kerala')),
    (_('Bhopal'), _("It's in %s") % _('Madhya Pradesh')),
    (_('Mumbai'), _("It's in %s") % _('Maharashtra')),
    (_('Imphal'), _("It's in %s") % _('Manipur')),
    (_('Shillong'), _("It's in %s") % _('Meghalaya')),
    (_('Aizawl'), _("It's in %s") % _('Mizoram')),
    (_('Kohima'), _("It's in %s") % _('Nagaland')),
    (_('Bhubaneswar'), _("It's in %s") % _('Odisha')),
    (_('Jaipur'), _("It's in %s") % _('Rajasthan')),
    (_('Gangtok'), _("It's in %s") % _('Sikkim')),
    (_('Chennai'), _("It's in %s") % _('Tamil Nadu')),
    (_('Agartala'), _("It's in %s") % _('Tripura')),
    (_('Lucknow'), _("It's in %s") % _('Uttar Pradesh')),
    (_('Dehradun'), _("It's in %s") % _('Uttarakhand')),
    (_('Kolkata'), _("It's in %s") % _('West Bengal')),
    (_('Port Blair'), _("It's in %s") % _('Andaman and Nicobar Islands')),
    (_('Silvassa'), _("It's in %s") % _('Dadra and Nagar Haveli')),
    (_('Daman'), _("It's in %s") % _('Daman and Diu')),
    (_('Kavaratti'), _("It's in %s") % _('Lakshadweep')),
    (_('Pondicherry'), _("It's in %s") % _('Pondicherry')),
    (_('Amarnath'), _("It's in %s") % _('Jammu and Kashmir')),
    (_('Leh'), _("It's in %s") % _('Jammu and Kashmir')),
    (_('Vaishno Devi'), _("It's in %s") % _('Jammu and Kashmir')),
    (_('Patni Top'), _("It's in %s") % _('Jammu and Kashmir')),
    (_('Chamba'), _("It's in %s") % _('Himachal Pradesh')),
    (_('Manali'), _("It's in %s") % _('Himachal Pradesh')),
    (_('Amritsar'), _("It's in %s") % _('Punjab')),
    (_('Attari'), _("It's in %s") % _('Punjab')),
    (_('Bathinda'), _("It's in %s") % _('Punjab')),
    (_('Panipat'), _("It's in %s") % _('Haryana')),
    (_('Kedarnath'), _("It's in %s") % _('Uttarakhand')),
    (_('Badrinath'), _("It's in %s") % _('Uttarakhand')),
    (_('Nainital'), _("It's in %s") % _('Uttarakhand')),
    (_('Sravasti'), _("It's in %s") % _('Uttar Pradesh')),
    (_('Ayodhya'), _("It's in %s") % _('Uttar Pradesh')),
    (_('Agra'), _("It's in %s") % _('Uttar Pradesh')),
    (_('Kanpur'), _("It's in %s") % _('Uttar Pradesh')),
    (_('Varanasi'), _("It's in %s") % _('Uttar Pradesh')),
    (_('Allahabad'), _("It's in %s") % _('Uttar Pradesh')),
    (_('Tezpur'), _("It's in %s") % _('Assam')),
    (_('Darjeeling'), _("It's in %s") % _('West Bengal')),
    (_('Murshidabad'), _("It's in %s") % _('West Bengal')),
    (_('Shantiniketan'), _("It's in %s") % _('West Bengal')),
    (_('Digha'), _("It's in %s") % _('West Bengal')),
    (_('Hazaribag'), _("It's in %s") % _('Jharkhand')),
    (_('Bihar-Sharif'), _("It's in %s") % _('Bihar')),
    (_('Nalanda'), _("It's in %s") % _('Bihar')),
    (_('Bodhgaya'), _("It's in %s") % _('Bihar')),
    (_('Pilani'), _("It's in %s") % _('Rajasthan')),
    (_('Bikaner'), _("It's in %s") % _('Rajasthan')),
    (_('Jaisalmer'), _("It's in %s") % _('Rajasthan')),
    (_('Jodhpur'), _("It's in %s") % _('Rajasthan')),
    (_('Ranakpur'), _("It's in %s") % _('Rajasthan')),
    (_('Bundi'), _("It's in %s") % _('Rajasthan')),
    (_('Kota'), _("It's in %s") % _('Rajasthan')),
    (_('Chittaurgarh'), _("It's in %s") % _('Rajasthan')),
    (_('Mount Abu'), _("It's in %s") % _('Rajasthan')),
    (_('Gwalior'), _("It's in %s") % _('Madhya Pradesh')),
    (_('Shivpuri'), _("It's in %s") % _('Madhya Pradesh')),
    (_('Orchha'), _("It's in %s") % _('Madhya Pradesh')),
    (_('Khajuraho'), _("It's in %s") % _('Madhya Pradesh')),
    (_('Sanchi'), _("It's in %s") % _('Madhya Pradesh')),
    (_('Ujjain'), _("It's in %s") % _('Madhya Pradesh')),
    (_('Indore'), _("It's in %s") % _('Madhya Pradesh')),
    (_('Jabalpur'), _("It's in %s") % _('Madhya Pradesh')),
    (_('Amarkantak'), _("It's in %s") % _('Madhya Pradesh')),
    (_('Ambikapur'), _("It's in %s") % _('Chhattisgarh')),
    (_('Chitrakote Falls'), _("It's in %s") % _('Chhattisgarh')),
    (_('Hirakud Dam'), _("It's in %s") % _('Odisha')),
    (_('Cuttack'), _("It's in %s") % _('Odisha')),
    (_('Paradip'), _("It's in %s") % _('Odisha')),
    (_('Konarak'), _("It's in %s") % _('Odisha')),
    (_('Puri'), _("It's in %s") % _('Odisha')),
    (_('Gopalpur'), _("It's in %s") % _('Odisha')),
    (_('Bhuj'), _("It's in %s") % _('Gujarat')),
    (_('Lothal'), _("It's in %s") % _('Gujarat')),
    (_('Vadodara'), _("It's in %s") % _('Gujarat')),
    (_('Dwarka'), _("It's in %s") % _('Gujarat')),
    (_('Rajkot'), _("It's in %s") % _('Gujarat')),
    (_('Porbandar'), _("It's in %s") % _('Gujarat')),
    (_('Somnath'), _("It's in %s") % _('Gujarat')),
    (_('Diu'), _("It's in %s") % _('Gujarat')),
    (_('Bhavnagar'), _("It's in %s") % _('Gujarat')),
    (_('Saputara'), _("It's in %s") % _('Gujarat')),
    (_('Melghat'), _("It's in %s") % _('Maharashtra')),
    (_('Wardha'), _("It's in %s") % _('Maharashtra')),
    (_('Chandrapur'), _("It's in %s") % _('Maharashtra')),
    (_('Ajanta'), _("It's in %s") % _('Maharashtra')),
    (_('Ellora'), _("It's in %s") % _('Maharashtra')),
    (_('Aurangabad'), _("It's in %s") % _('Maharashtra')),
    (_('Shirdi'), _("It's in %s") % _('Maharashtra')),
    (_('Pune'), _("It's in %s") % _('Maharashtra')),
    (_('Murud'), _("It's in %s") % _('Maharashtra')),
    (_('Mahabaleshwar'), _("It's in %s") % _('Maharashtra')),
    (_('Ganpatipule'), _("It's in %s") % _('Maharashtra')),
    (_('Panhala'), _("It's in %s") % _('Maharashtra')),
    (_('Warangal'), _("It's in %s") % _('Andhra Pradesh')),
    (_('Vishakhapatnam'), _("It's in %s") % _('Andhra Pradesh')),
    (_('Bhadrachalam'), _("It's in %s") % _('Andhra Pradesh')),
    (_('Amaravati'), _("It's in %s") % _('Andhra Pradesh')),
    (_('Srisailam'), _("It's in %s") % _('Andhra Pradesh')),
    (_('Lepakshi'), _("It's in %s") % _('Andhra Pradesh')),
    (_('Tirupati'), _("It's in %s") % _('Andhra Pradesh')),
    (_('Vasco da Gama'), _("It's in %s") % _('Goa')),
    (_('Bider'), _("It's in %s") % _('Karnataka')),
    (_('Gulbarga'), _("It's in %s") % _('Karnataka')),
    (_('Bijapur'), _("It's in %s") % _('Karnataka')),
    (_('Raichur'), _("It's in %s") % _('Karnataka')),
    (_('Hampi'), _("It's in %s") % _('Karnataka')),
    (_('Jog Falls'), _("It's in %s") % _('Karnataka')),
    (_('Chitradurga'), _("It's in %s") % _('Karnataka')),
    (_('Udupi'), _("It's in %s") % _('Karnataka')),
    (_('Mangalore'), _("It's in %s") % _('Karnataka')),
    (_('Belur'), _("It's in %s") % _('Karnataka')),
    (_('Kozhikode'), _("It's in %s") % _('Kerala')),
    (_('Kochi'), _("It's in %s") % _('Kerala')),
    (_('Alappuzha'), _("It's in %s") % _('Kerala')),
    (_('Mamallapuram'), _("It's in %s") % _('Tamil Nadu')),
    (_('Chidambaram'), _("It's in %s") % _('Tamil Nadu')),
    (_('Mudumalai'), _("It's in %s") % _('Tamil Nadu')),
    (_('Thanjavur'), _("It's in %s") % _('Tamil Nadu')),
    (_('Kodaikanal'), _("It's in %s") % _('Tamil Nadu')),
    (_('Madurai'), _("It's in %s") % _('Tamil Nadu')),
    (_('Kanniyakumari'), _("It's in %s") % _('Tamil Nadu')),
    (_('Rameswaram'), _("It's in %s") % _('Tamil Nadu'))    
]
]

LEVELS = [LEVEL1, LEVEL2, LEVEL3]


