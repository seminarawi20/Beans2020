from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

# Numpy is a mathematical python library which is used from more complex calculations. When we want to call it we can use np.
import numpy as np

author = 'Moritz Sommerlad'

doc = """
This is the first out of three experiments for the Seminar on Experimental Economics in the WS 2020 at the AWI Heidelberg
"""


class Constants(BaseConstants):
    name_in_url = 'Study'#The name can be set to whatever you want it to be. It will show in the URL.
    players_per_group = 3 #Players per group can be set here. In our case the we play a one-shot three person game. You can change this to any INT. Just make sure you change it in the settings tab as well.
    num_rounds = 1 # You can play more than one round, but in our case we play one.
    pool = 30
    efficiency_factor = 2 # This is a INT that indicates how the resource increases the leftover points. You can use any INT or String here
    base = 20/100 #This is the baseline for the tipping point. The first number indicates the percentage, which you can adjust.
    addition_per_take = 1/100 #This is the percentage the tipping point will increase per point taken. The first number indicates the percentage, which you can adjust.
    max = 10
    completion_code = 142675

class Subsession(BaseSubsession):

    def group_by_arrival_time_method(self, waiting_players):
        if len(waiting_players) >= 3:
            return waiting_players[:3]
        for p in waiting_players:
            if p.waiting_too_long():
                p.alone = 1
                return [p]

class Group(BaseGroup):

    tipping_point = models.FloatField()
    otherplayer1_take = models.IntegerField()
    otherplayer2_take = models.IntegerField()
    chance = models.FloatField()

    def set_up_otherplayer(self):
        self.otherplayer1_take = np.random.randint(0, 6)
        self.otherplayer2_take = np.random.randint(0, 6)


    def set_tipping_point(self):
        if sum([p.alone for p in self.get_players()]) > 0:
            self.tipping_point = np.round(Constants.base + ((sum([p.take for p in
                                                                  self.get_players()]) + self.otherplayer1_take + self.otherplayer2_take) * Constants.addition_per_take),4)
        else:
            self.tipping_point = np.round(Constants.base + (sum([p.take for p in self.get_players()]) * Constants.addition_per_take), 4)

    breakdown = models.BooleanField(initial=False)


    def set_breakdown(self):
        self.chance = round(np.random.rand(),2)
        self.breakdown = self.tipping_point > self.chance

    total_points_left = models.IntegerField()
    resource_share = models.IntegerField()

    def set_payoffs(self):

            if sum([p.alone for p in self.get_players()]) > 0:
                self.total_points_left = Constants.pool - sum([p.take for p in self.get_players()]) - self.otherplayer1_take - self.otherplayer2_take
                self.resource_share = np.round(self.total_points_left * Constants.efficiency_factor / Constants.players_per_group, 0)
            else:
                self.total_points_left = Constants.pool - sum([p.take for p in self.get_players()])
                self.resource_share = np.round(self.total_points_left * Constants.efficiency_factor / Constants.players_per_group, 0)

            for p in self.get_players():
                p.correct_belief = 1 if self.total_points_left - 2 <= p.belief <= self.total_points_left + 2 else 0

            if self.breakdown == True:
                for p in self.get_players():
                    p.payoff = p.correct_belief
            else:
                for p in self.get_players():
                    p.payoff = sum([+ p.take,
                                    + self.resource_share,
                                    + p.correct_belief,
                                    ])

class Player(BasePlayer):



    take = models.IntegerField(label="How many points do you want to take ?")



    def take_choices(self):
        return range(11)


    def waiting_too_long(self):
        import time
        return time.time() - self.participant.vars['wait_page_arrival'] > 180


    alone = models.BooleanField(initial=False)


    belief = models.IntegerField(min=0, max=30, label="How many points are left in the pool?")
    correct_belief = models.IntegerField()


    timeout_take = models.BooleanField(initial=False)
    timeout_belief = models.BooleanField(initial=False)
    timeout_results = models.BooleanField(initial=False)
    timeout_genderrole = models.BooleanField(initial=False)
    timeout_genderrole2 = models.BooleanField(initial=False)
    timeout_demographics = models.BooleanField(initial=False)
    timeout_demographicstreatment = models.BooleanField(initial=False)


# ab hier die Items zu Demografie

    age = models.IntegerField(min=14, max=120)

    gender = models.IntegerField(
        choices=[
            [1, 'female'],
            [2, 'male'],
            [3, 'non-binary'],
            [9, 'prefer not to say'],
        ]
        , label="What gender do you identify with?")

    education = models.IntegerField(
        choices=[
            [1, 'no diploma'],
            [2, 'high school diploma'],
            [3, 'university degree'],
            [9, 'prefer not to say'],
        ]
        , label="What is the highest level of education you have completed?")

    experience = models.IntegerField(
        choices=[
            [1, 'none'],
            [2, 'a few times'],
            [3, 'more than 10'],
        ], widget=widgets.RadioSelect()
        , label="How much experience with experiments like this have you had so far?")

# G1-G20 sind die Items zu Genderroles

    G1 = models.IntegerField(label="compassionate",
        choices=[
            [1, 'Never'],
            [2, 'Very Rarely'],
            [3, 'Rarely'],
            [4, 'Occasionally'],
            [5, 'Often'],
            [6, 'Very Often'],
            [7, 'Always'],
        ], widget=widgets.RadioSelectHorizontal())

    G2 = models.IntegerField(label="tender",
                             choices=[
                                 [1, 'Never'],
                                 [2, 'Very Rarely'],
                                 [3, 'Rarely'],
                                 [4, 'Occasionally'],
                                 [5, 'Often'],
                                 [6, 'Very Often'],
                                 [7, 'Always'],
                             ], widget=widgets.RadioSelectHorizontal())

    G3 = models.IntegerField(label="dominant",
                             choices=[
                                 [1, 'Never'],
                                 [2, 'Very Rarely'],
                                 [3, 'Rarely'],
                                 [4, 'Occasionally'],
                                 [5, 'Often'],
                                 [6, 'Very Often'],
                                 [7, 'Always'],
                             ], widget=widgets.RadioSelectHorizontal())

    G4 = models.IntegerField(label="brave",
                             choices=[
                                 [1, 'Never'],
                                 [2, 'Very Rarely'],
                                 [3, 'Rarely'],
                                 [4, 'Occasionally'],
                                 [5, 'Often'],
                                 [6, 'Very Often'],
                                 [7, 'Always'],
                             ], widget=widgets.RadioSelectHorizontal())

    G5 = models.IntegerField(label="loving",
                             choices=[
                                 [1, 'Never'],
                                 [2, 'Very Rarely'],
                                 [3, 'Rarely'],
                                 [4, 'Occasionally'],
                                 [5, 'Often'],
                                 [6, 'Very Often'],
                                 [7, 'Always'],
                             ], widget=widgets.RadioSelectHorizontal())

    G6 = models.IntegerField(label="controlling",
                             choices=[
                                 [1, 'Never'],
                                 [2, 'Very Rarely'],
                                 [3, 'Rarely'],
                                 [4, 'Occasionally'],
                                 [5, 'Often'],
                                 [6, 'Very Often'],
                                 [7, 'Always'],
                             ], widget=widgets.RadioSelectHorizontal())

    G7 = models.IntegerField(label="analytical",
                             choices=[
                                 [1, 'Never'],
                                 [2, 'Very Rarely'],
                                 [3, 'Rarely'],
                                 [4, 'Occasionally'],
                                 [5, 'Often'],
                                 [6, 'Very Often'],
                                 [7, 'Always'],
                             ], widget=widgets.RadioSelectHorizontal())

    G8 = models.IntegerField(label="careful",
                             choices=[
                                 [1, 'Never'],
                                 [2, 'Very Rarely'],
                                 [3, 'Rarely'],
                                 [4, 'Occasionally'],
                                 [5, 'Often'],
                                 [6, 'Very Often'],
                                 [7, 'Always'],
                             ], widget=widgets.RadioSelectHorizontal())

    G9 = models.IntegerField(label="boastful",
                             choices=[
                                 [1, 'Never'],
                                 [2, 'Very Rarely'],
                                 [3, 'Rarely'],
                                 [4, 'Occasionally'],
                                 [5, 'Often'],
                                 [6, 'Very Often'],
                                 [7, 'Always'],
                             ], widget=widgets.RadioSelectHorizontal())

    G10 = models.IntegerField(label="willing to take risks",
                             choices=[
                                 [1, 'Never'],
                                 [2, 'Very Rarely'],
                                 [3, 'Rarely'],
                                 [4, 'Occasionally'],
                                 [5, 'Often'],
                                 [6, 'Very Often'],
                                 [7, 'Always'],
                             ], widget=widgets.RadioSelectHorizontal())

    G11 = models.IntegerField(label="caring",
                             choices=[
                                 [1, 'Never'],
                                 [2, 'Very Rarely'],
                                 [3, 'Rarely'],
                                 [4, 'Occasionally'],
                                 [5, 'Often'],
                                 [6, 'Very Often'],
                                 [7, 'Always'],
                             ], widget=widgets.RadioSelectHorizontal())

    G12 = models.IntegerField(label="sensitive",
                             choices=[
                                 [1, 'Never'],
                                 [2, 'Very Rarely'],
                                 [3, 'Rarely'],
                                 [4, 'Occasionally'],
                                 [5, 'Often'],
                                 [6, 'Very Often'],
                                 [7, 'Always'],
                             ], widget=widgets.RadioSelectHorizontal())

    G13 = models.IntegerField(label="rational",
                             choices=[
                                 [1, 'Never'],
                                 [2, 'Very Rarely'],
                                 [3, 'Rarely'],
                                 [4, 'Occasionally'],
                                 [5, 'Often'],
                                 [6, 'Very Often'],
                                 [7, 'Always'],
                             ], widget=widgets.RadioSelectHorizontal())

    G14 = models.IntegerField(label="anxious",
                             choices=[
                                 [1, 'Never'],
                                 [2, 'Very Rarely'],
                                 [3, 'Rarely'],
                                 [4, 'Occasionally'],
                                 [5, 'Often'],
                                 [6, 'Very Often'],
                                 [7, 'Always'],
                             ], widget=widgets.RadioSelectHorizontal())

    G15 = models.IntegerField(label="familiy-oriented",
                             choices=[
                                 [1, 'Never'],
                                 [2, 'Very Rarely'],
                                 [3, 'Rarely'],
                                 [4, 'Occasionally'],
                                 [5, 'Often'],
                                 [6, 'Very Often'],
                                 [7, 'Always'],
                             ], widget=widgets.RadioSelectHorizontal())

    G16 = models.IntegerField(label="pragmatic",
                             choices=[
                                 [1, 'Never'],
                                 [2, 'Very Rarely'],
                                 [3, 'Rarely'],
                                 [4, 'Occasionally'],
                                 [5, 'Often'],
                                 [6, 'Very Often'],
                                 [7, 'Always'],
                             ], widget=widgets.RadioSelectHorizontal())

    G17 = models.IntegerField(label="reckless",
                             choices=[
                                 [1, 'Never'],
                                 [2, 'Very Rarely'],
                                 [3, 'Rarely'],
                                 [4, 'Occasionally'],
                                 [5, 'Often'],
                                 [6, 'Very Often'],
                                 [7, 'Always'],
                             ], widget=widgets.RadioSelectHorizontal())

    G18 = models.IntegerField(label="warm-hearted",
                             choices=[
                                 [1, 'Never'],
                                 [2, 'Very Rarely'],
                                 [3, 'Rarely'],
                                 [4, 'Occasionally'],
                                 [5, 'Often'],
                                 [6, 'Very Often'],
                                 [7, 'Always'],
                             ], widget=widgets.RadioSelectHorizontal())

    G19 = models.IntegerField(label="adventurous",
                             choices=[
                                 [1, 'Never'],
                                 [2, 'Very Rarely'],
                                 [3, 'Rarely'],
                                 [4, 'Occasionally'],
                                 [5, 'Often'],
                                 [6, 'Very Often'],
                                 [7, 'Always'],
                             ], widget=widgets.RadioSelectHorizontal())

    G20 = models.IntegerField(label="delicate",
                              choices=[
                                  [1, 'Never'],
                                  [2, 'Very Rarely'],
                                  [3, 'Rarely'],
                                  [4, 'Occasionally'],
                                  [5, 'Often'],
                                  [6, 'Very Often'],
                                  [7, 'Always'],
                              ], widget=widgets.RadioSelectHorizontal())
