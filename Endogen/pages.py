from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

# Pages are responsible for retrieving and passing back data from models to templates and vice versa.
# If you need to show something to a participant or to get his/her input, you need to indicate this in pages.py

#If you want to display something other than text (e.g. a variable) you need to use the function
#vars_for_template and make it return a dictionary. The index of the dictionary can then be used to display it on the page with {{ index }}.
# it is key that you indicate from which model you return a variable, here our treatment is defined on the subsession level while the pool is defined in the constants

class Preview(Page):

    def vars_for_template(self):
        return {'base_payment': Constants.base_payment}

class Introduction(Page):

    def vars_for_template(self):
        return

class Welcome(Page):

    def vars_for_template(self):
        return {'pool': Constants.pool,
                'players': Constants.players_per_group,
                'factor': Constants.efficiency_factor,
                'max': Constants.max,
                'treatment': self.subsession.treatment,
                'base': Constants.base*100,
                'addition_per_take': Constants.addition_per_take*100,
                'id_in_group': self.player.id_in_group
                }

# I split the Pages for the comprehension tests since the structure looks nicer. Does not have a practical meaning.
# For each Question and Answer pair i created a new page. You can decide if you want to show the page by the
# id _displayed line.

## a form field is something the participant can interact with. Since we defined it on a player level, we must specify it in the form_model section.


class Test_Control(Page):
    form_model = 'player'
    form_fields = ['test_control']

    def is_displayed(self):
        return self.subsession.treatment == 0

class Results_Control(Page):

    def vars_for_template(self):
        return {'test_control': self.player.test_control}

    def is_displayed(self):
        return self.subsession.treatment == 0

    ## DIESE SEITE IST NEU: FRAGT DIEJEINIGEN, DIE ERSTE FRAGE FALSCH BEANTWORTET HABEN NOCHEINMAL MIT NEUEM BSP:##
class Test_Control2(Page):
    form_model = 'player'
    form_fields = ['test_control2']

    def is_displayed(self):
        return self.subsession.treatment == 0
    ## DIESE SEITE IST NEU: GIBT DENJENIGEN, DIE ERSTE FRAGE FALSCH BEANTWORTET HABEN, ERGEBNISSE DER 2. FRAGE: ##
class Results_Control2(Page):

    def vars_for_template(self):
        return {'test_control2': self.player.test_control2}

    def is_displayed(self):
        return self.subsession.treatment == 0 and self.player.test_control != 15

class Test1(Page):
    form_model = 'player'
    form_fields = ['test1']

    def is_displayed(self):
        return self.subsession.treatment == 1


class Test2(Page):
    form_model = 'player'
    form_fields = ['test2']

    def is_displayed(self):
        return self.subsession.treatment == 1

class Results_Test1(Page):
    def vars_for_template(self):
        return {'test1': self.player.test1,
                'id_in_group': self.player.id_in_group
                }

    def is_displayed(self):
        return self.subsession.treatment == 1

class Results_Test2(Page):
    def vars_for_template(self):
        return {'test2': self.player.test2}

    def is_displayed(self):
        return self.subsession.treatment == 1



# Now we create a page for the player to decide what to take.
class Take(Page):

    form_model = 'player'
    form_fields = ['take']
    def vars_for_template(self):
        return {'max': Constants.max}



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
            completion_code= self.player.completion_code
        )

class Survey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'employment', 'environment', 'answer_same']

    def vars_for_template(self):
        return dict(
            completion_code=self.player.completion_code
        )
    #def vars_for_template(self):
        #age = player.age
        #gender = player.gender

    #def vars_for_template(self):
        #return dict(
            #age = self.player.age,
            #gender = self.player.gender
        #)

#das müssen wir noch löschen, aber ertsmal als Hilfe stehen lassen

class End(Page):
    def vars_for_template(self):
        return dict(
            completion_code=self.player.completion_code
        )
# here we indicate in which sequence we want the pages to be played. You can repeat pages as well.
page_sequence = [Survey,
                 Preview,
                 Introduction,
                 Welcome,
                 Test_Control,
                 Results_Control,
                 Test_Control2,
                 Results_Control2,
                 Test1,
                 Results_Test1,
                 Test2,
                 Results_Test2,
                 Take,
                 ResultsWaitPage,
                 Results,
                 End,
                 ]
