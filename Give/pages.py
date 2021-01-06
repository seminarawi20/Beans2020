from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time


class Grouping(WaitPage):
    group_by_arrival_time = True

    body_text = "Waiting for two other participants to begin the real task.\
      This wait should be fairly short, though in some cases it could last a couple of minutes (max 3 min)."



class Give(Page):

    form_model = 'player'
    form_fields = ['give']
    def vars_for_template(self):
        return {'max': Constants.max,
               'alone': self.player.give}

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_give = True



class ResultsWaitPage(WaitPage):
    body_text = "Waiting for two other participants to make their decision.\
    This wait should be fairly short, though in some cases it could last a couple of minutes (max 2 min)."

    def after_all_players_arrive(self):
        self.group.set_up_otherplayer()
        self.group.set_tipping_point()
        self.group.set_breakdown()
        self.group.set_payoffs()

class Questions(Page):

    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10']

    timeout_seconds = 240

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_questions = True


class Results(Page):
    def vars_for_template(self):
        # here the dict() is used to convert our list to a dictionary. dict() and {} are equivalent, but use a different notation. Please be aware.

        return dict(
            payoff = self.player.payoff,
            give = self.player.give,
            total_points_given = self.group.total_points_given,
            breakdown = self.group.breakdown,
            treatment = self.session.vars['treatment'],
            share = self.group.resource_share,
            tipping_point = round(self.group.tipping_point*100,1),
            completion_code= self.session.vars['code'],
            total = self.participant.payoff_plus_participation_fee()
        )

page_sequence = [Grouping,
                 Give,
                 ResultsWaitPage,
                 Questions,
                 Results]
