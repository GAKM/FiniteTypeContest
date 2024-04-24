from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer, Page, Currency as c, currency_range, WaitPage
)
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ContestIntro'
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

# PAGES

class Intro(Page):
    pass

class Quiz(Page):
    form_model = 'player'
    quiz1 = models.StringField(widget=widgets.RadioSelect)
    quiz2 = models.StringField(widget=widgets.RadioSelect)
    quiz3 = models.StringField(widget=widgets.RadioSelect)
    quiz4 = models.StringField(widget=widgets.RadioSelect)
    form_fields = ['quiz1', 'quiz2', 'quiz3', 'quiz4']

    @staticmethod
    def error_message(player: Player, values):
        # alternatively, you could make quiz1_error_message, quiz2_error_message, etc.
        # but if you have many similar fields, this is more efficient.
        solutions = dict(
            quiz1='0.5', 
            quiz2 = str(C.SAMPLE_BID_2 * C.COST_HIGH), 
            quiz3 = str(C.SAMPLE_PRIZE) + ' tokens', 
            quiz4 = str(C.ENDOWMENT + C.SAMPLE_PRIZE - C.SAMPLE_BID_2 * C.COST_HIGH) + ' tokens')

        # error_message can return a dict whose keys are field names and whose
        # values are error messages
        errors = {name: 'Wrong' for name in solutions if values[name] != solutions[name]}
        # print('errors is', errors)
        if errors:
            player.num_failed_attempts += 1
            if player.num_failed_attempts >= 3:
                player.failed_too_many = True
                # we don't return any error here; just let the user proceed to the
                # next page, but the next page is the 'failed' page that boots them
                # from the experiment.
            else:
                return errors

class Failed(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.failed_too_many

class Cost_Assignment(Page):
    pass



page_sequence = [Intro, Quiz, Failed]
