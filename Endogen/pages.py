from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from .models import BasePlayer
import time

# Pages are responsible for retrieving and passing back data from models to templates and vice versa.
# If you need to show something to a participant or to get his/her input, you need to indicate this in pages.py

#If you want to display something other than text (e.g. a variable) you need to use the function
#vars_for_template and make it return a dictionary. The index of the dictionary can then be used to display it on the page with {{ index }}.
# it is key that you indicate from which model you return a variable, here our treatment is defined on the subsession level while the pool is defined in the constants

class Welcome(Page):

   # def is_displayed(self):
   #     return self.player.id_in_group <= 3

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True

class InstructionsA(Page):

    def vars_for_template(self):
        return {'pool': Constants.pool,
                'players': Constants.players_per_group,
                'factor': Constants.efficiency_factor,
                'group': BasePlayer.id_in_group,
                'max': Constants.max,
                'base': Constants.base*100,
                'addition_per_take': Constants.addition_per_take*100
                }

    def is_displayed(self):
        return self.participant.category == 'A'

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True

class InstructionsB(Page):

    def vars_for_template(self):
        return {'pool': Constants.pool,
                'players': Constants.players_per_group,
                'factor': Constants.efficiency_factor,
                'group': BasePlayer.id_in_group,
                'max': Constants.max,
                'base': Constants.base*100,
                'addition_per_take': Constants.addition_per_take*100}
    def is_displayed(self):
        return self.participant.category == 'B'

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True

# I split the Pages for the comprehension tests since the structure looks nicer. Does not have a practical meaning.
# For each Question and Answer pair i created a new page. You can decide if you want to show the page by the
# id _displayed line.

## a form field is something the participant can interact with. Since we defined it on a player level, we must specify it in the form_model section.


class Test_A(Page):
    form_model = 'player'
    form_fields = ['test_control']

    def is_displayed(self):
        return self.participant.category == 'A'

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True

class Test_B(Page):
    form_model = 'player'
    form_fields = ['test_control']

    def is_displayed(self):
        return self.participant.category == 'B'

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True

class Results_Test_A(Page):
    def vars_for_template(self):
        return {'test_control': self.player.test_control}

    def is_displayed(self):
        return self.participant.category == 'A'

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True

class Results_Test_B(Page):
    def vars_for_template(self):
        return {'test_control': self.player.test_control}

    def is_displayed(self):
        return self.participant.category == 'B'

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True


class Test2A(Page):
    form_model = 'player'
    form_fields = ['test2']

    def is_displayed(self):
        return self.participant.category == 'A'

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True

class Test2B(Page):
    form_model = 'player'
    form_fields = ['test2']

    def is_displayed(self):
        return self.participant.category == 'B'

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True

class Results_Test2A(Page):
    def vars_for_template(self):
        return {'test2': self.player.test2}

    def is_displayed(self):
        return self.participant.category == 'A'

    timeout_seconds = 120

    def before_next_page(self):
        self.participant.vars['wait_page_arrival'] = time.time()
        if self.timeout_happened:
            self.player.timeout_results_test2 = True

class Results_Test2B(Page):
    def vars_for_template(self):
        return {'test2': self.player.test2}

    def is_displayed(self):
        return self.participant.category == 'B'

    timeout_seconds = 120

    def before_next_page(self):
        self.participant.vars['wait_page_arrival'] = time.time()
        if self.timeout_happened:
            self.player.timeout_results_test2 = True





# here we indicate in which sequence we want the pages to the played. You can repeat pages as well.
page_sequence = [Welcome,
                 InstructionsA,
                 InstructionsB,
                 Test_A,
                 Test_B,
                 Results_Test_A,
                 Results_Test_B,
                 Test2A,
                 Test2B,
                 Results_Test2A,
                 Results_Test2B,
                 ]
