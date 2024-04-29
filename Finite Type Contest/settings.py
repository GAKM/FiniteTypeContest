from os import environ


SESSION_CONFIGS = [
    {
        'name': '2_Players_WTA',
        'display_name': "2 Player Winner Takes It All",
        'num_demo_participants': 12,
      	'app_sequence': ['contest_intro', 'contest_cost_assignment', 'twoplayerWTA', 'Survey'],
        'rounds': 1,
    },
    
    {
        'name': 'Three_Player_WTA',
        'display_name': "3 Player Winner Takes It All",
        'num_demo_participants': 12,
      	'app_sequence': ['contest_intro', 'contest_cost_assignment', 'threeplayerWTA', 'Survey'],
        'rounds': 1,
    },

    {
        'name': 'Three_Player_LGN',
        'display_name': "3 Player Loser Gets Nothing",
        'num_demo_participants': 12,
      	'app_sequence': ['contest_intro', 'contest_cost_assignment', 'threeplayerLGN', 'Survey'],
        'rounds': 1,
    },


]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['COST']
SESSION_FIELDS = ['test22']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPYw
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'tokens'

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5058275150937'

ROOMS = [
    dict(
        name='GabrielsTest',
        display_name='Gabriels oTree Room Tests',
        participant_label_file='_rooms/GabrielTests.txt',
        use_secure_urls=True
    ),
    dict(
        name='econ_lab',
        display_name='Experimental Economics Lab'
    ),
]
