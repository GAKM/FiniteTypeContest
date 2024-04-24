from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer, Page, Currency as c, currency_range, WaitPage
)
import random

doc = """
Three player LGN (LGN)
"""


class C(BaseConstants):
    NAME_IN_URL = 'ThreePlayerLGN'
    PLAYERS_PER_GROUP = 3
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
    THREE_PLAYER_LGN_PRIZE_1 = 50
    THREE_PLAYER_LGN_PRIZE_2 = 50
    QUIZ1_CHOICES = ['0', '0.5', '1', 'None of the above']
    QUIZ2_CHOICES = [SAMPLE_BID_2/COST_HIGH, SAMPLE_BID_2 * COST_LOW, str(SAMPLE_BID_2 * COST_HIGH), 'None of the above']
    QUIZ3_CHOICES = ['0 tokens', str(SAMPLE_PRIZE / 2) + ' tokens', str(SAMPLE_PRIZE) + ' tokens', "Depends on my opponent's cost-per-bid"]
    QUIZ4_CHOICES = [str(SAMPLE_PRIZE - SAMPLE_BID_2) + ' tokens', str(ENDOWMENT - SAMPLE_BID_2 * COST_HIGH) + ' tokens', str(ENDOWMENT + SAMPLE_PRIZE - SAMPLE_BID_2 * COST_HIGH) + ' tokens', str(ENDOWMENT + SAMPLE_PRIZE - SAMPLE_BID_2) + ' tokens']


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    winning_bid_1 = models.IntegerField()
    winning_bid_2 = models.IntegerField()


class Player(BasePlayer):

    bid = models.IntegerField(
        min=0, max=C.ENDOWMENT, label="How much do you want to bid?"
    )

    is_winner1 = models.BooleanField()
    is_winner2 = models.BooleanField()    


# FUNCTIONS

def creating_session(subsession):
    subsession.group_randomly()

def set_payoffs(group: Group):

    players = group.get_players()
    sorted_bids = sorted(players, key=lambda p: p.bid, reverse=True)
    group.winning_bid_1 = sorted_bids[0].bid
    group.winning_bid_2 = sorted_bids[1].bid
    winners1 = [p for p in players if p.bid == group.winning_bid_1]
    winner1 = random.choice(winners1)
    winners2 = [p for p in players if p.bid == group.winning_bid_2]
    winner2 = random.choice(winners2)
    for p in players:
        if p == winner1:
            p.is_winner1 = True
            p.is_winner2 = False
            p.payoff = C.THREE_PLAYER_LGN_PRIZE_1 - p.bid * p.participant.COST
        elif p == winner2:
            p.is_winner2 = True
            p.is_winner1 = False
            p.payoff = C.THREE_PLAYER_LGN_PRIZE_2 - p.bid * p.participant.COST

        else:
            p.is_winner1 = False
            p.is_winner2 = False

def other_player1(player: Player):
    return player.get_others_in_group()[0]

def other_player2(player: Player):
    return player.get_others_in_group()[1]



# PAGES

class PairingWaitPage(WaitPage):
    wait_for_all_groups = True
    body_text = "Waiting to pair you with someone"

class Three_Player_LGN(Page):
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
        opponent1 = other_player1(player)
        opponent2 = other_player2(player)
        winner1 = None  # Default no winner
        winner2 = None  # Default no winner

        if opponent1.is_winner1:
            winner1 = "Opponent 1"
            opponent1.is_winner2 = False
        elif opponent2.is_winner1:
            winner1 = "Opponent 2"
            opponent2.is_winner2 = False

        if opponent1.is_winner2:
            winner2 = "Opponent 1"
            opponent1.is_winner1 = False
        elif opponent2.is_winner2:
            winner2 = "Opponent 2"
            opponent2.is_winner1 = False


        return dict(
            opponent1=opponent1,
            opponent1_bid=opponent1.bid,
            opponent2=opponent2,
            opponent2_bid=opponent2.bid,
            winner1=winner1,
            winner2=winner2,            
        )



page_sequence = [PairingWaitPage, Three_Player_LGN, ResultsWaitPage, Results]
