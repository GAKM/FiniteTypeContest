from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer, Page, Currency as c, currency_range, WaitPage
)
import random

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ContestGame'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10
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
    winning_bid = models.CurrencyField()


class Player(BasePlayer):

    bid = models.IntegerField(
        min=0, max=C.ENDOWMENT, label="How much do you want to bid?"
    )

    is_winner = models.BooleanField()


# FUNCTIONS

def creating_session(subsession):
    subsession.group_randomly()

def set_payoffs(group: Group):

    players = group.get_players()
    group.winning_bid = max([p.bid for p in players])
    winners = [p for p in players if p.bid == group.winning_bid]
    winner = random.choice(winners)
    for p in players:
        if p == winner:
            p.is_winner = True
            p.payoff = C.TWO_PLAYER_PRIZE - p.bid * p.participant.COST
        else:
            p.is_winner = False
            p.payoff = 0

def other_player(player: Player):
    return player.get_others_in_group()[0]


# PAGES

class PairingWaitPage(WaitPage):
    wait_for_all_groups = True
    body_text = "Waiting to pair you with someone"

class Two_Player(Page):
    form_model = 'player'
    form_fields = ['bid']


    @staticmethod
    def js_vars(player: Player):
        return dict(endowment=C.ENDOWMENT)

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        opponent = other_player(player)
        return dict(
            opponent=opponent,
            opponent_bid=opponent.bid,
        )




page_sequence = [PairingWaitPage, Two_Player, ResultsWaitPage, Results]
