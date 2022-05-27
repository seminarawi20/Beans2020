from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time


# Pages are responsible for retrieving and passing back data from models to templates and vice versa.
# If you need to show something to a participant or to get his/her input, you need to indicate this in pages.py

# If you want to display something other than text (e.g. a variable) you need to use the function
# vars_for_template and make it return a dictionary. The index of the dictionary can then be used to display it on the page with {{ index }}.
# it is key that you indicate from which model you return a variable, here our treatment is defined on the subsession level while the pool is defined in the constants




class ResultsWaitPage(WaitPage):

    # We use after_all_players_arrive to make sure we only start our calculation after every participant made their choice.
    # First we need to set the tipping point, then we check if the pool breaks down and the last step is to calculate the payoffs.
    # This is done by calling the functions be defined on our group level.
    # We order is important, since the tipping point is an input for the breakdown, which is an input for the payoff




    def after_all_players_arrive(self):
        self.group.set_up_otherplayer()
        self.group.set_tipping_point()
        self.group.set_breakdown()
        self.group.set_payoffs()

class ResultsWaitPage2(WaitPage):


    #get_player_by_id = True
    def vars_for_template(self):
        self.player.alone = self.player.participant.vars['alone']
        if self.player.alone == 0:
            if self.subsession.treatment == 0:
                self.player.expectations1C = self.player.participant.vars['expectations1C']
                self.player.expectations2C = self.player.participant.vars['expectations2C']
            else:
                if self.player.id_in_group == 3:
                    self.player.expectations2tb = self.player.participant.vars['expectations2tb']
                    self.player.expectations1T = self.player.participant.vars['expectations1T']
                else:
                    self.player.expectations1T = self.player.participant.vars['expectations1T']
                    self.player.expectations2T = self.player.participant.vars['expectations2T']
            self.p1 = self.group.get_player_by_id(1)
            self.p2 = self.group.get_player_by_id(2)
            self.p3 = self.group.get_player_by_id(3)
            if self.player == self.p1:
                self.p1.take = self.player.participant.vars['take']
            if self.player == self.p2:
                self.p2.take = self.player.participant.vars['take']
            if self.player == self.p3:
                self.p3.take = self.player.participant.vars['take']
        else:
            if self.player == self.group.set_up_otherplayer():
                self.group.otherplayer1_take = self.player.participant.vars['otherplayer1_take']
            if self.subsession.treatment == 0:
                self.player.expectations1C = self.player.participant.vars['expectations1C']
                self.player.expectations2C = self.player.participant.vars['expectations2C']
            else:
                    self.player.expectations1T = self.player.participant.vars['expectations1T']
                    self.player.expectations2T = self.player.participant.vars['expectations2T']


    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def get_timeout_seconds(self):
        import time
        self.player.alone = self.player.participant.vars['alone']
        if self.player.alone == 1:
            print('hallo')
            self.timeout_seconds = time.time() - self.player.participant.wait_page_arrival


class Results(Page):
    def vars_for_template(self):
        # here the dict() is used to convert our list to a dictionary. dict() and {} are equivalent, but use a different notation. Please be aware.
        return dict(
            money=(Constants.money_per_point * self.player.payoff + Constants.base_payment),
            payoff=self.player.payoff,
            rate=Constants.money_per_point,
            base=Constants.base_payment,
            take=self.player.take,
            total_points_left=self.group.total_points_left,
            points_taken=Constants.pool - self.group.total_points_left,
            pool_mult=self.group.total_points_left * Constants.efficiency_factor,
            breakdown=self.group.breakdown,
            treatment=self.player.treatment,
            share=self.group.resource_share,
            tipping_point=round(self.group.tipping_point * 100, 1),
        )

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_endresults = True

class Expectations(Page):


    get_player_by_id = True

    def vars_for_template(self):
        return {'id_in_group': self.player.id_in_group}

    def is_displayed(self):
        return self.subsession.treatment == 1

    form_model = 'player'

    def get_form_fields(self):
        player = self.player
        if player.id_in_group == 3:
            return ['expectations1T', 'expectations2tb']
        else:
            return ['expectations1T', 'expectations2T']

    timeout_seconds = 120


class Expectations_Control(Page):

    def is_displayed(self):
        return self.subsession.treatment == 0

    form_model = 'player'
    form_fields = ['expectations1C', 'expectations2C']

    timeout_seconds = 120

class Results_Expectations(Page):

    def vars_for_template(self):
        if self.player.alone == False:
            self.p1 = self.group.get_player_by_id(1)
            self.p2 = self.group.get_player_by_id(2)
            self.p3 = self.group.get_player_by_id(3)
        #if self.player == self.p1:
            self.p1.take = self.player.participant.vars['take']
            self.p2.take = self.player.participant.vars['take']
            self.p3.take = self.player.participant.vars['take']
        else:
            if self.player == self.group.set_up_otherplayer():
                self.group.otherplayer1_take = self.player.participant.vars['otherplayer1_take']

        #self.take = self.player.participant.vars['take']
        return dict(
            payoff=self.player.payoff,
            money=Constants.money_per_point * self.player.payoff,
            rate=Constants.money_per_point,

        )

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_expectationsresults = True

class Survey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', 'children', 'environment', 'answer_same']

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_survey = True


class End(Page):
    def vars_for_template(self):
        return dict(
            completion_code=self.session.vars['code']
        )


# here we indicate in which sequence we want the pages to be played. You can repeat pages as well.
page_sequence = [ResultsWaitPage2,
                 Results_Expectations,
                 Survey,
                 End,
                 ]
