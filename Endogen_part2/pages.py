from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time


# Pages are responsible for retrieving and passing back data from models to templates and vice versa.
# If you need to show something to a participant or to get his/her input, you need to indicate this in pages.py

# If you want to display something other than text (e.g. a variable) you need to use the function
# vars_for_template and make it return a dictionary. The index of the dictionary can then be used to display it on the page with {{ index }}.
# it is key that you indicate from which model you return a variable, here our treatment is defined on the subsession level while the pool is defined in the constants


class Grouping(WaitPage):
    group_by_arrival_time = True
    #get_player_by_id = True
    body_text = "Waiting for two other participants to reach this task.\
      This wait should be fairly short, though in some cases it could last a couple of minutes (max 3 min).\
                <b>It is very important that you do not close this window!<b\>"

    def vars_for_template(self):
        self.player.category = self.player.participant.vars['category']

    def before_next_page(self):
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        p3 = self.group.get_player_by_id(3)
        #self.player.session.vars['ids_finished'] = self.player.session.ids_finishedid_in_subsession
        #self.player.participant.vars['group.id_in_subsession'] = self.player.group.id_in_subsession
        #self.player.participant.vars['p1'] = p1
        #self.player.participant.vars['p2'] = p2
        #self.player.participant.vars['p3'] = p3
        if self.player == self.group.set_up_otherplayer():
            self.player.participant.vars['otherplayer1_take'] = self.group.otherplayer1_take

    def after_all_players_arrive(self):
        for player in self.group.get_players():
            participant = player.participant
            group = player.group
            participant.past_group_id = group.id
            participant.past_id_in_group = player.id_in_group
            #participant.vars['group_id'] = group.id_in_subsession



# Now we create a page for the player to decide what to take.
class Take(Page):
    form_model = 'player'
    form_fields = ['take']

    def vars_for_template(self):
        # here the dict() is used to convert our list to a dictionary. dict() and {} are equivalent, but use a different notation. Please be aware.

        return dict(
            max=Constants.max,
            alone=self.player.alone)


    timeout_seconds = 120



    def before_next_page(self):
        self.player.participant.vars['alone'] = self.player.alone
        if self.player.alone == False:
            self.p1 = self.group.get_player_by_id(1)
            self.p2 = self.group.get_player_by_id(2)
            self.p3 = self.group.get_player_by_id(3)
            if self.player == self.p1:
                self.player.participant.vars['take'] = self.p1.take
            if self.player == self.p2:
                self.player.participant.vars['take'] = self.p2.take
            if self.player == self.p3:
                self.player.participant.vars['take'] = self.p3.take
        else:
            if self.player == self.group.set_up_otherplayer():
                self.player.participant.vars['otherplayer1_take'] = self.group.otherplayer1_take
            #self.player.participant.

        if self.timeout_happened:

            self.player.timeout_take = True

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
            tipping_point=round(self.group.tipping_point * 100, 1)
        )

    def before_next_page(self):
        self.player.participant.vars['wait_page_arrival'] = time.time()

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_endresults = True

class Expectations(Page):

    get_player_by_id = True

    def vars_for_template(self):
        return {'id_in_group': self.player.id_in_group}

    def is_displayed(self):
        return self.player.treatment == 1

    form_model = 'player'

    def get_form_fields(self):
        player = self.player
        if player.id_in_group == 3:
            return ['expectations1T', 'expectations2tb']
        else:
            return ['expectations1T', 'expectations2T']

    def before_next_page(self):
        player = self.player
        if player.id_in_group == 3:
            self.player.participant.vars['expectations2tb'] = self.player.expectations2tb
            self.player.participant.vars['expectations1T'] = self.player.expectations1T
        else:
            self.player.participant.vars['expectations1T'] = self.player.expectations1T
            self.player.participant.vars['expectations2T'] = self.player.expectations2T

    timeout_seconds = 120

class Expectations_Control(Page):

    def vars_for_template(self):
        return {'id_in_group': self.player.id_in_group}

    def is_displayed(self):
        return self.player.treatment == 0

    form_model = 'player'
    form_fields = ['expectations1C', 'expectations2C']

    def before_next_page(self):
        self.player.participant.vars['expectations1C'] = self.player.expectations1C
        self.player.participant.vars['expectations2C'] = self.player.expectations2C
        #if self.player.timout_happened:
            #self.player.timeout_expectations_control = True

    timeout_seconds = 120

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
page_sequence = [Grouping,
                 Take,
                 ResultsWaitPage,
                 Expectations,
                 Expectations_Control,
                 Results,
                 ]
