from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer, Page, Currency as c, currency_range, WaitPage
)
import random

doc = """
2 Player Finite-Type Contest Game
"""


class C(BaseConstants):
    NAME_IN_URL = 'TwoPlayerWTA'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 15
    ENDOWMENT = 200
    COST_HIGH = 2
    COST_LOW = 1
    TWO_PLAYER_PRIZE = 100


class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
    session = subsession.session
    session.past_groups = []


def group_by_arrival_time_method(subsession: Subsession, waiting_players):
    session = subsession.session

    import itertools

    # this generates all possible pairs of waiting players
    # and checks if the group would be valid.
    for possible_group in itertools.combinations(waiting_players, 2):
        # use a set, so that we can easily compare even if order is different
        # e.g. {1, 2} == {2, 1}
        pair_ids = set(p.id_in_subsession for p in possible_group)
        # if this pair of players has not already been played
        if pair_ids not in session.past_groups:
            # mark this group as used, so we don't repeat it in the next round.
            session.past_groups.append(pair_ids)
            # in this function,
            # 'return' means we are creating a new group with this selected pair
            return possible_group    

class Group(BaseGroup):
    winning_bid = models.FloatField()


class Player(BasePlayer):
    bid = models.FloatField(
        min=0, max=C.ENDOWMENT, label="How much do you want to bid?"
    )
    is_winner = models.BooleanField()

    prev_round_player = 


# FUNCTIONS

def set_payoffs(group: Group):
    players = group.get_players()
    group.winning_bid = max([p.bid for p in players])
    winners = [p for p in players if p.bid == group.winning_bid]
    winner = random.choice(winners)
    for p in players:
        if p == winner:
            p.is_winner = True
            p.payoff = C.ENDOWMENT + C.TWO_PLAYER_PRIZE - p.bid * p.participant.COST
        else:
            p.is_winner = False
            p.payoff = C.ENDOWMENT - p.bid * p.participant.COST

def other_player(player: Player):
    return player.get_others_in_group()[0]


# PAGES

class PairingWaitPage(WaitPage):
    group_by_arrival_time = True
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
