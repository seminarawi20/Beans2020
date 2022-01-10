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
        return self.player.id_in_group <= 2

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
        return self.player.id_in_group > 2

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
        return self.player.id_in_group <= 2

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True

class Test_B(Page):
    form_model = 'player'
    form_fields = ['test_control']

    def is_displayed(self):
        return self.player.id_in_group > 2

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True

class Results_Test_A(Page):
    def vars_for_template(self):
        return {'test_control': self.player.test_control}

    def is_displayed(self):
        return self.player.id_in_group <= 2

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True

class Results_Test_B(Page):
    def vars_for_template(self):
        return {'test_control': self.player.test_control}

    def is_displayed(self):
        return self.player.id_in_group > 2

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True


class Test2A(Page):
    form_model = 'player'
    form_fields = ['test2']

    def is_displayed(self):
        return self.player.id_in_group <= 2

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True

class Test2B(Page):
    form_model = 'player'
    form_fields = ['test2']

    def is_displayed(self):
        return self.player.id_in_group > 2

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True

class Results_Test2A(Page):
    def vars_for_template(self):
        return {'test2': self.player.test2}

    def is_displayed(self):
        return self.player.id_in_group <= 2

    timeout_seconds = 120

    def before_next_page(self):
        self.participant.vars['wait_page_arrival'] = time.time()
        if self.timeout_happened:
            self.player.timeout_results_test2 = True

class Results_Test2B(Page):
    def vars_for_template(self):
        return {'test2': self.player.test2}

    def is_displayed(self):
        return self.player.id_in_group > 2

    timeout_seconds = 120

    def before_next_page(self):
        self.participant.vars['wait_page_arrival'] = time.time()
        if self.timeout_happened:
            self.player.timeout_results_test2 = True


class Grouping(WaitPage):
    group_by_arrival_time = True

    body_text = "Waiting for two other participants to begin the real task.\
      This wait should be fairly short, though in some cases it could last a couple of minutes (max 3 min)."

# Now we create a page for the player to decide what to take.

class TakeA(Page):

    form_model = 'player'
    form_fields = ['take']
    def vars_for_template(self):
        return {'max': Constants.max}

    def is_displayed(self):
        return self.player.id_in_group <= 2

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True

class TakeB(Page):

    form_model = 'player'
    form_fields = ['take']
    def vars_for_template(self):
        return {'max': Constants.max}

    def is_displayed(self):
        return self.player.id_in_group > 2

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True

class ExitSurvey(Page):

    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'education', 'mothertongue', 'mturkmoney', 'coplayerA', 'coplayerB']

    def is_displayed(self):
        return self.player.id_in_group <= 3

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True

class ResultsWaitPage(WaitPage):

    # We use after_all_players_arrive to make sure we only start our calculation after every participant made their choice.
    # First we need to set the tipping point, then we check if the pool breaks down and the last step is to calculate the payoffs.
    #This is done by calling the functions be defined on our group level.
    # We order is important, since the tipping point is an input for the breakdown, which is an input for the payoff

    def after_all_players_arrive(self):
        self.group.set_up_otherplayer()
        self.group.set_tipping_point()
        self.group.set_breakdown()
        self.group.set_payoffs()



class ResultsA(Page):
    def vars_for_template(self):
        # here the dict() is used to convert our list to a dictionary. dict() and {} are equivalent, but use a different notation. Please be aware.

        return dict(
            payoff = self.player.payoff,
            take = self.player.take,
            total_points_left = self.group.total_points_left,
            points_taken = Constants.pool - self.group.total_points_left,
            pool_mult = self.group.total_points_left * Constants.efficiency_factor,
            breakdown = self.group.breakdown,
            share = self.group.resource_share,
            tipping_point = round(self.group.tipping_point*100,1),
            completion_code = self.player.completion_code
        )
    def is_displayed(self):
        return self.player.id_in_group <= 2

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_results = True


class ResultsB(Page):
    def vars_for_template(self):
        # here the dict() is used to convert our list to a dictionary. dict() and {} are equivalent, but use a different notation. Please be aware.

        return dict(
            payoff = self.player.payoff,
            take = self.player.take,
            total_points_left = self.group.total_points_left,
            points_taken = Constants.pool - self.group.total_points_left,
            pool_mult = self.group.total_points_left * Constants.efficiency_factor,
            breakdown = self.group.breakdown,
            share = self.group.resource_share,
            tipping_point = round(self.group.tipping_point*100,1),
            completion_code = self.player.completion_code
        )

    def is_displayed(self):
        return self.player.id_in_group > 2

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_results = True


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
                 Grouping,
                 TakeA,
                 TakeB,
                 ExitSurvey,
                 ResultsWaitPage,
                 ResultsA,
                 ResultsB]
