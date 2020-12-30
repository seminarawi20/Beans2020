from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time

# Pages are responsible for retrieving and passing back data from models to templates and vice versa.
# If you need to show something to a participant or to get his/her input, you need to indicate this in pages.py

#If you want to display something other than text (e.g. a variable) you need to use the function
#vars_for_template and make it return a dictionary. The index of the dictionary can then be used to display it on the page with {{ index }}.
# it is key that you indicate from which model you return a variable, here our treatment is defined on the subsession level while the pool is defined in the constants
class Welcome(Page):

    def vars_for_template(self):
        return {'pool': Constants.pool,
                'players': 3,
                'factor': Constants.efficiency_factor,
                'max': Constants.max,
                'treatment': self.subsession.treatment,
                'base': Constants.base*100,
                'addition_per_give': Constants.addition_per_give*100,
                'show_up_fee': Constants.fee,
                'per_point': Constants.per_point}

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_welcome = True

# I split the Pages for the comprehension tests since the structure looks nicer. Does not have a practical meaning.
# For each Question and Answer pair i created a new page. You can decide if you want to show the page by the
# id _displayed line.

## a form field is something the participant can interact with. Since we defined it on a player level, we must specify it in the form_model section.

class Test1_init(Page):
    form_model = 'player'

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_test1_init = True

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
        return {'test1': self.player.test1}

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_result1 = True

class Results_Test2(Page):
    def vars_for_template(self):
        return {'test2': self.player.test2}

    timeout_seconds = 120

    def before_next_page(self):
        self.participant.vars['wait_page_arrival'] = time.time()
        if self.timeout_happened:
            self.player.timeout_result2 = True





# Page for Framing.
class Framing(Page):

    form_model = 'player'
    def is_displayed(self):
        return self.subsession.treatment == 1

    def vars_for_template(self):
        return {'show_up_fee': Constants.fee,
                'per_point': Constants.per_point}

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_framing = True

class Welcome2(Page):

    form_model = 'player'

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_welcome2 = True




class Results(Page):
    def vars_for_template(self):
        # here the dict() is used to convert our list to a dictionary. dict() and {} are equivalent, but use a different notation. Please be aware.

        return dict(
            payoff = self.player.payoff,
            give = self.player.give,
            total_points_given = self.group.total_points_given,
            points_given = Constants.common_pool + self.group.total_points_given,
            pool_mult = self.group.total_points_given * Constants.efficiency_factor,
            breakdown = self.group.breakdown,
            treatment = self.subsession.treatment,
            share = self.group.resource_share,
            tipping_point = round(self.group.tipping_point*100,1),
            completion_code= self.player.completion_code
        )

# here we indicate in which sequence we want the pages to the played. You can repeat pages as well.
page_sequence = [Framing,
                 Welcome,
                 Test1_init,
                 Test1,
                 Results_Test1,
                 Test2,
                 Results_Test2
                 ]
