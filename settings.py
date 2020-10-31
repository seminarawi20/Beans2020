from os import environ

SESSION_CONFIGS = [
     dict(
        name='Exogen_Cont',
        display_name="Exogen_Controll",
        num_demo_participants=3,
        app_sequence=['Exogen'],
        treatment = False
     ),
    dict(name='Exogen',
        display_name="Exogen",
        num_demo_participants=3,
        app_sequence=['Exogen'],
        treatment = True
    ),
    dict(name='Endogen',
        display_name="Endogen_Controll",
        num_demo_participants=3,
        app_sequence=['Endogen'],
        treatment = False
    ),
    dict(name='Edogen_Cont',
        display_name="Endogen",
        num_demo_participants=3,
        app_sequence=['Endogen'],
        treatment = True
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('password')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'gqu#5o1o$fci0cbu!9%*8$1obvpnm9&=w%*^z4nur4pb(dw!^p'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
