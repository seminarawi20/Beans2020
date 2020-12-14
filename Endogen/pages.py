from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

# Pages are responsible for retrieving and passing back data from models to templates and vice versa.
# If you need to show something to a participant or to get his/her input, you need to indicate this in pages.py

#If you want to display something other than text (e.g. a variable) you need to use the function
#vars_for_template and make it return a dictionary. The index of the dictionary can then be used to display it on the page with {{ index }}.
# it is key that you indicate from which model you return a variable, here our treatment is defined on the subsession level while the pool is defined in the constants
class Welcome(Page):
    timeout_seconds = 60

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_welcome = True

class gendertreatment(Page):

    form_model = 'player'
    form_fields = ['gender']

    def is_displayed(self):
        return self.subsession.treatment == 1

    timeout_seconds = 60

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_gendertreatment = True



def is_displayed(self):
    return self.player.id_in_group == 2

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



# I split the Pages for the comprehension tests since the structure looks nicer. Does not have a practical meaning.
# For each Question and Answer pair i created a new page. You can decide if you want to show the page by the
# id _displayed line.

## a form field is something the participant can interact with. Since we defined it on a player level, we must specify it in the form_model section.

class Test1(Page):
    form_model = 'player'
    form_fields = ['test1']

    timeout_seconds = 60

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_test1 = True

class Test2(Page):
    form_model = 'player'
    form_fields = ['test2']

    timeout_seconds = 60

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_test2 = True

class Results_Test1(Page):
    def vars_for_template(self):
        return {'test1': self.player.test1,
                'base': Constants.base*100,
                'addition_per_take': Constants.addition_per_take*100}

    timeout_seconds = 60

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_results_test1 = True

class Results_Test2(Page):
    def vars_for_template(self):
        return {'test2': self.player.test2}

    timeout_seconds = 60

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_results_test2 = True

# Now we create a page for the player to decide what to take.
class Take(Page):

    form_model = 'player'
    form_fields = ['take']
    def vars_for_template(self):
        return {'max': Constants.max,
                'treatment': self.subsession.treatment,
                'base': Constants.base*100,
                }

    timeout_seconds = 60

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_take = True

class Belief(Page):
    # New page in which players state their belief, how much the other players took
    form_model = 'player'
    form_fields = ['belief']

    timeout_seconds = 60

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_belief = True

class ResultsWaitPage(WaitPage):

    # We use after_all_players_arrive to make sure we only start our calculation after every participant made their choice.
    # First we need to set the tipping point, then we check if the pool breaks down and the last step is to calculate the payoffs.
    #This is done by calling the functions be defined on our group level.
    # We order is important, since the tipping point is an input for the breakdown, which is an input for the payoff

    def after_all_players_arrive(self):
        self.group.set_tipping_point()
        self.group.set_breakdown()
        self.group.set_payoffs()

class Results(Page):
    def vars_for_template(self):
        # here the dict() is used to convert our list to a dictionary. dict() and {} are equivalent, but use a different notation. Please be aware.

        return dict(
            payoff = self.player.payoff,
            take = self.player.take,
            total_points_left = self.group.total_points_left,
            points_taken = Constants.pool - self.group.total_points_left,
            pool_mult = self.group.total_points_left * Constants.efficiency_factor,
            breakdown = self.group.breakdown,
            treatment = self.subsession.treatment,
            share = self.group.resource_share,
            tipping_point = round(self.group.tipping_point*100,1),
            completion_code= self.player.completion_code,
            belief = self.player.belief,
            correct_belief = self.player.correct_belief
        )


class Genderrole(Page):
    form_model = 'player'
    form_fields = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10']

class Genderrole2(Page):
    form_model = 'player'
    form_fields = ['G11', 'G12', 'G13', 'G14', 'G15', 'G16', 'G17', 'G18', 'G19', 'G20']

class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'experience']

    def is_displayed(self):
        return self.subsession.treatment == 0

class Demographicstreatment(Page):
    form_model = 'player'
    form_fields = ['age', 'education', 'experience']

    def vars_for_template(self):
        return dict(
            treatment=self.subsession.treatment,
        )

    def is_displayed(self):
        return self.subsession.treatment == 1

class End(Page):

    def vars_for_template(self):
        # here the dict() is used to convert our list to a dictionary. dict() and {} are equivalent, but use a different notation. Please be aware.

        return dict(
            payoff = self.player.payoff,
            completion_code= self.player.completion_code,
        )

# here we indicate in which sequence we want the pages to the played. You can repeat pages as well.
page_sequence = [Welcome,
                 gendertreatment,
                 Instructions,
                 Test1,
                 Results_Test1,
                 Test2,
                 Results_Test2,
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
