from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer, Page, Currency as c, currency_range, WaitPage
)
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ContestCostAssignment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ENDOWMENT = 200
    COST_HIGH = 2
    COST_LOW = 1
    SAMPLE_BID = 22
    SAMPLE_BID_2 = 33
    SAMPLE_BIDDING_COST_HIGH = SAMPLE_BID * COST_HIGH
    SAMPLE_BIDDING_COST_LOW = SAMPLE_BID * COST_LOW
    SAMPLE_PRIZE = 100
    TWO_PLAYER_PRIZE = 100
    THREE_PLAYER_WTA_PRIZE = 100
    THREE_PLAYER_LGN_PRIZE_1 = 100
    THREE_PLAYER_LGN_PRIZE_2 = 100
    QUIZ1_CHOICES = ['0', '0.5', '1', 'None of the above']
    QUIZ2_CHOICES = [SAMPLE_BID_2/COST_HIGH, SAMPLE_BID_2 * COST_LOW, str(SAMPLE_BID_2 * COST_HIGH), 'None of the above']
    QUIZ3_CHOICES = ['0 tokens', str(SAMPLE_PRIZE / 2) + ' tokens', str(SAMPLE_PRIZE) + ' tokens', "Depends on my opponent's cost-per-bid"]
    QUIZ4_CHOICES = [str(SAMPLE_PRIZE - SAMPLE_BID_2) + ' tokens', str(ENDOWMENT - SAMPLE_BID_2 * COST_HIGH) + ' tokens', str(ENDOWMENT + SAMPLE_PRIZE - SAMPLE_BID_2 * COST_HIGH) + ' tokens', str(ENDOWMENT + SAMPLE_PRIZE - SAMPLE_BID_2) + ' tokens']


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
	pass

class Player(BasePlayer):
    COST = models.IntegerField()
    quiz1 = models.StringField(
        choices=C.QUIZ1_CHOICES,
        widget=widgets.RadioSelect
    )
    quiz2 = models.StringField(
        choices=C.QUIZ2_CHOICES,
        widget=widgets.RadioSelect    
    )

    quiz3= models.StringField(
        choices=C.QUIZ3_CHOICES,
        widget=widgets.RadioSelect
    )

    quiz4= models.StringField(
        choices=C.QUIZ4_CHOICES,
        widget=widgets.RadioSelect
    )

    num_failed_attempts = models.IntegerField(initial=0)
    failed_too_many = models.BooleanField(initial=False)


# FUNCTIONS

def creating_session(self): # Assigning costs

    for p in self.get_players():
            COST = random.choice([C.COST_HIGH, C.COST_LOW])
            p.COST = COST
            participant = p.participant
            participant.COST = p.COST

#def vars_for_template(player):
#    player.participant.COST = player.COST





## TRYING TO SAVE PLAYER.COST SO IT DOESN'T GET RANDOMIZED IN FUTURE ROUNDS.
# DOES NOT YET WORK.
#def before_next_page(player: Player):
 # player.participant.vars['cost'] = player.COST


# PAGES

class Cost_Assignment(Page):
    pass



page_sequence = [Cost_Assignment]
