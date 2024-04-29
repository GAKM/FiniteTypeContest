from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer, Page, Currency as c, currency_range
)

class C(BaseConstants):
    NAME_IN_URL = 'Survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    gender = models.StringField(
        choices=['Male', 'Female', 'Other', 'Do not wish to disclose'],
        label="What is your gender?",
        widget=widgets.RadioSelect
    )
    risk_willingness = models.IntegerField(
        choices=[(i, str(i)) for i in range(11)],  # Generates a list of tuples (0, '0') to (10, '10')
        label="<b>Risk measure:</b> How do you see yourself? Are you generally a person who is fully prepared to take risks, or do you try to avoid taking risks? Please tick a box on the scale, where the value 0 means not at all willing to take risks and the value 10 means fully prepared to take risks",
        widget=widgets.RadioSelectHorizontal
    )
    competitiveness = models.IntegerField(
        choices=[(i, str(i)) for i in range(11)],
        label="<b>Competitiveness measure:</b> How do you see yourself? Are you generally a person who is competitive, or do you try to avoid competitive environments? Please tick a box on the scale, where the value 0 means not at all competitive and the value 10 means extremely competitive",
        widget=widgets.RadioSelectHorizontal
    )
    pillow_cost = models.FloatField(
        choices=[
            (5, '$5'),
            (10, '$10'),
            (50, '$50'),
            (105, '$105')
        ],
        label="A pillow and a blanket cost $110 in total. The blanket costs $100 more than the pillow. How much does the pillow cost?",
        widget=widgets.RadioSelect
    )
    machines_time = models.IntegerField(
        choices=[
            (5, '5 minutes'),
            (100, '100 minutes'),
            (500, '500 minutes'),
            (0, 'None of the above')
        ],
        label="If it takes 5 machines 5 minutes to make 5 pens, how long would it take 100 machines to make 100 pens?",
        widget=widgets.RadioSelect
    )
    lily_pad_growth = models.IntegerField(
        choices=[
            (1, '1 day'),
            (25, '25 days'),
            (45, '45 days'),
            (49, '49 days')
        ],
        label="In a lake, there is a patch of lily pads. Every day, the patch doubles in size. If it takes 50 days for the patch to cover the entire lake, how long would it take for the patch to cover half of the lake?",
        widget=widgets.RadioSelect
    )
    bidding_reasoning = models.LongStringField(
        label="When choosing how much to bid in the different contests, can you explain your reasoning process?"
    )

class Survey(Page):
    form_model = 'player'
    form_fields = [
        'gender', 
        'risk_willingness', 
        'competitiveness', 
        'pillow_cost', 
        'machines_time', 
        'lily_pad_growth', 
        'bidding_reasoning'
    ]

page_sequence = [Survey]
