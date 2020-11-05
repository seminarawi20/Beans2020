from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

# Pages are responsible for retrieving and passing back data from models to templates and vice versa.
# If you need to show something to a participant or to get his/her input, you need to indicate this in pages.py

#If you want to display something other than text (e.g. a variable) you need to use the function
#vars_for_template and make it return a dictionary. The index of the dictionary can then be used to display it on the page with {{ index }}.
# it is key that you indicate from which model you return a variable.
class Welcome(Page):

    def vars_for_template(self):
        return {'pool': Constants.pool,
                'players': Constants.players_per_group,
                'factor': Constants.efficiency_factor,
                'max': Constants.max,
                }


class Take(Page):
    # a form field is something the participant can interact with. Here we will asked them to pick how much they want to take
    form_model = 'player'
    form_fields = ['take']
    def vars_for_template(self):
        return {'max': Constants.max
        }

class ResultsWaitPage(WaitPage):
    # We use after_all_players_arrive to make sure we only start our calculation after every participant made their choice.

    def after_all_players_arrive(self):
        self.group.set_payoffs()



class Results(Page):
    def vars_for_template(self):
        # here the dict() is used to convert our list to a dictionary. dict() and {} are equivalent, but use a different notation. Please be aware.

        return dict(
            payoff = self.player.payoff,
            take = self.player.take,
            total_points_left = self.group.total_points_left,
            pool_mult = self.group.total_points_left * Constants.efficiency_factor,
            share = self.group.resource_share,
            completion_code=self.player.completion_code
        )


# here we indicate in which sequence we want the pages to the played. You can repeat pages as well.
page_sequence = [Welcome, Take, ResultsWaitPage, Results]
