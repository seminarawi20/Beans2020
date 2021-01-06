from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time


class Welcome(Page):

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_welcome = True

class gendertreatment(Page):

    form_model = 'player'
    form_fields = ['gender']

    def is_displayed(self):
        return self.subsession.treatment == 1

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_gendertreatment = True



class Instructions(Page):

    def vars_for_template(self):
        return {'pool': Constants.pool,
                'players': Constants.players_per_group,
                'factor': Constants.efficiency_factor,
                'max': Constants.max,
                'treatment': self.subsession.treatment,
                'base': Constants.base*100,
                'addition_per_take': Constants.addition_per_take*100}

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_instructions = True


class Test1(Page):
    form_model = 'player'
    form_fields = ['test1']

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_test1 = True

class Test2(Page):
    form_model = 'player'
    form_fields = ['test2']

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_test2 = True

class Results_Test1(Page):
    def vars_for_template(self):
        return {'test1': self.player.test1,
                'base': Constants.base*100,
                'addition_per_take': Constants.addition_per_take*100}

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_results_test1 = True

class Results_Test2(Page):
    def vars_for_template(self):
        return {'test2': self.player.test2}

    timeout_seconds = 120

    def before_next_page(self):
        self.participant.vars['wait_page_arrival'] = time.time()
        if self.timeout_happened:
            self.player.timeout_results_test2 = True

page_sequence = [Welcome,
                 gendertreatment,
                 Instructions,
                 Test1,
                 Results_Test1,
                 Test2,
                 Results_Test2]
