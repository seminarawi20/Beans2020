from os import environ

#############################################
###########  DO NOT TOUCH ###################
#############################################

mturk_hit_settings = {
        'keywords': ['academic','study','exeriment'],
        'title': "Study on decision making (5 minutes)",
        'description': 'Decision making experiment',
        'frame_height':500,
        'template': 'global/mturk_template.html',
        'minutes_allotted_per_assignment':100,
        'expiration_hours':2*24,
        'qualification_requirements':[
            # Only US
            {
                'QualificationTypeId': "00000000000000000071",
                'Comparator': "EqualTo",
                'LocaleValues': [{'Country': "US"}]
            },
            # At least 15 HITs approved
            {
                'QualificationTypeId': "00000000000000000040",
                'Comparator': "GreaterThanOrEqualTo",
                'IntegerValues': [15]
            },
            # At least 95% of HITs approved
            {
                'QualificationTypeId': "000000000000000000L0",
                'Comparator': "GreaterThanOrEqualTo",
                'IntegerValues': [95]
            },
        ]

}
#############################################

PARTICIPANT_FIELDS = {'category', 'take'}
SESSION_FIELDS = {'treatment'}

################################################################
#Only touch real_world_currency per point in alignment with us
################################################################

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']


SESSION_CONFIG_DEFAULTS= {
    "real_world_currency_per_point": 0.05,
    'participation_fee': 0.70,
    'doc': "",
    "mturk_hit_settings": mturk_hit_settings
}



##################################################
####### ENTER THE SESSIONS YOU WANT TO PLAY ######
#################################################
SESSION_CONFIGS = [
    dict(name='Endogen',
        display_name="Endogen",
        num_demo_participants=3,
        app_sequence=['Endogen','Endogen_part2', 'Endogen_part3'],
        treatment = False
    ),
    dict(name='Edogen_Treat',
        display_name="Endogen_Treat",
        num_demo_participants=3,
        app_sequence=['Endogen', 'Endogen_part2', 'Endogen_part3'],
        treatment = True
    )
]


#############################################


#############################################
###########  DO NOT TOUCH ###################
#############################################
# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('password ')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'gqu#5o1o$fci0cbu!9%*8$1obvpnm9&=w%*^z4nur4pb(dw!^p'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

AWS_ACCESS_KEY_ID = environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY_ID = environ.get("AWS_SECRET_ACCESS_KEY_ID")
#############################################