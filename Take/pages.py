from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time





class Grouping(WaitPage):
    group_by_arrival_time = True

    body_text = "Waiting for two other participants to begin the real task.\
      This wait should be fairly short, though in some cases it could last a couple of minutes (max 3 min)."


class Take(Page):

    form_model = 'player'
    form_fields = ['take']

    def vars_for_template(self):
        # here the dict() is used to convert our list to a dictionary. dict() and {} are equivalent, but use a different notation. Please be aware.

        return dict(
            alone=self.player.alone )

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True

class Belief(Page):
    # New page in which players state their belief, how much the other players took
    form_model = 'player'
    form_fields = ['belief']

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_belief = True

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_up_otherplayer()
        self.group.set_tipping_point()
        self.group.set_breakdown()
        self.group.set_payoffs()

class Results(Page):
    def vars_for_template(self):
        # here the dict() is used to convert our list to a dictionary. dict() and {} are equivalent, but use a different notation. Please be aware.

        return dict(
            payoff = self.player.payoff,
            payoff_real =self.player.payoff.to_real_world_currency(self.session),
            take = self.player.take,
            total_points_left = self.group.total_points_left,
            points_taken = Constants.pool - self.group.total_points_left,
            pool_mult = self.group.total_points_left * Constants.efficiency_factor,
            breakdown = self.group.breakdown,
            share = self.group.resource_share,
            tipping_point = round(self.group.tipping_point*100,1),
            belief = self.player.belief,
            correct_belief = self.player.correct_belief
        )

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_results = True


class Genderrole(Page):
    form_model = 'player'
    form_fields = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10']

    timeout_seconds = 180

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_genderrole = True


class Genderrole2(Page):
    form_model = 'player'
    form_fields = ['G11', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17', 'G18', 'G19', 'G20']

    timeout_seconds = 180

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_genderrole2 = True


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'experience']

    def is_displayed(self):
        return self.session.vars['treatment'] == 0

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_demographics = True


class Demographicstreatment(Page):
    form_model = 'player'
    form_fields = ['age', 'education', 'experience']

    def is_displayed(self):
        return self.session.vars['treatment'] == 1

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_demographicstreatment = True

class End(Page):

    def vars_for_template(self):
        return dict(
            payoff = self.player.payoff,
            completion_code= self.session.vars['code'],
            total = self.participant.payoff_plus_participation_fee()

        )

# here we indicate in which sequence we want the pages to the played. You can repeat pages as well.
page_sequence = [Grouping,
                 Take,
                 Belief,
                 ResultsWaitPage,
                 Results,
                 Genderrole,
                 Genderrole2,
                 Demographics,
                 Demographicstreatment,
                 End,
                 ]
