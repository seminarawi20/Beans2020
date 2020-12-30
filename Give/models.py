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

    # Here we define the different values that are valid in every form of the game.

    name_in_url = 'Give'#The name can be set to whatever you want it to be. It will show in the URL.
    players_per_group = 3 #Players per group can be set here. In our case the we play a one-shot three person game. You can change this to any INT. Just make sure you change it in the settings tab as well.
    num_rounds = 1 # You can play more than one round, but in our case we play one.
    pool = 30 #This defines how big the pool is. You can use any INT or String here
    efficiency_factor = 2 # This is a INT that indicates how the resource increases the leftover points. You can use any INT or String here
    base= 30/100 #This is the baseline for the tipping point. The first number indicates the percentage, which you can adjust.
    addition_per_give = 2/100 #This is the percentage the tipping point will increase per point taken. The first number indicates the percentage, which you can adjust.
    fee = 1 # Show up fee in USD
    per_point = 1 # Amount of USD players get for every point
    max = 10
    # np.floor rounds it down and int converts it to an integer. The last step is not necessary, but it looks better.
    completion_code = 142675 # Please change this number in your live version. This is just a random code all participants in the live version get
    #after they complete the experiment.

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

    otherplayer1_give = models.IntegerField()
    otherplayer2_give = models.IntegerField()

    def set_up_otherplayer(self):
        self.otherplayer1_give = np.random.randint(4, 11)
        self.otherplayer2_give = np.random.randint(4, 11)

    def set_tipping_point(self):
        if sum([p.alone for p in self.get_players()]) > 0:
            self.tipping_point = np.round(Constants.base + ((sum([p.give for p in self.get_players()]) + self.otherplayer1_give + self.otherplayer2_give) * Constants.addition_per_give), 4)
        else:
            self.tipping_point = np.round(
                Constants.base + (sum([p.give for p in self.get_players()]) * Constants.addition_per_give), 4)


    breakdown = models.BooleanField(initial=False)

    def set_breakdown(self):
        self.breakdown = self.tipping_point < (2 / 3)


    total_points_given = models.IntegerField()
    resource_share = models.IntegerField()


    def set_payoffs(self):


        if sum([p.alone for p in self.get_players()]) > 0:
                self.total_points_given = sum([p.give for p in self.get_players()]) + self.otherplayer1_give + self.otherplayer2_give
                self.resource_share = np.round(self.total_points_given * Constants.efficiency_factor / Constants.players_per_group, 0)
        else:
                self.total_points_given =  sum([p.give for p in self.get_players()])
                self.resource_share = np.round(self.total_points_given * Constants.efficiency_factor / Constants.players_per_group, 0)

        if self.breakdown == True:
            for p in self.get_players():
                p.payoff = (Constants.max - p.give)
        else:
            for p in self.get_players():
                p.payoff = sum([+ (Constants.max - p.give),
                                + self.resource_share,
                                ])

class Player(BasePlayer):


    give = models.IntegerField(label="How many points do you want to give?")

    def give_choices(self):
        return range(11)

    def waiting_too_long(self):
        import time
        return time.time() - self.participant.vars['wait_page_arrival'] > 1 * 60

    timeout_give = models.BooleanField(initial=False)
    timeout_questions = models.BooleanField(initial=False)

    alone = models.BooleanField(initial=False)


    q1 = models.StringField(choices=["Alabama", "Alaska", "Arizona", "Arkansas", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois",
                                      "Indiana", "Iowa", "California", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
                                      "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina",
                                      "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
                                      "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"], label="Which state are you from?")

    q2 = models.StringField(choices=["Democratic Party", "Republican Party", "None"], widget=widgets.RadioSelect() , label="With party do you feel closer to?")

    q3 = models.StringField(choices=["Very opposed", "Rather opposed", "Impartial", "Rather in favour", "Very in favour", "No answer"], widget=widgets.RadioSelect() , label=
                            "Are you opposed or in favour of Anti-COVID-19 measures in your state?")

    q4 = models.StringField(choices=["Yes", "No", "No answer"], widget=widgets.RadioSelect() , label="Do you have health insurance?")

    q5 = models.StringField(choices=["High School", "Undergraduate", "Graduate", "None", "No answer"], widget=widgets.RadioSelect() , label="What is your educational qualification?")

    q6 = models.StringField(choices=["0-30", "30-60", "60-80", "80-100", "100+", "No answer"], widget=widgets.RadioSelect() , label="What is your annual income in thousand US Dollars?")

    q7 = models.StringField(choices=["Single", "Long-term relationship", "Married", "Divorced", "Widowed", "No answer"], widget=widgets.RadioSelect() , label=
                            "What is your relationship status?")

    q8 = models.StringField(choices=["0", "1", "2", "3", "4+", "No answer"], widget=widgets.RadioSelect() , label="How many children do you have?")

    q9 = models.StringField(choices=["Male", "Female", "Diverse", "No answer"], widget=widgets.RadioSelect() , label="What is your gender?")

    q10 = models.StringField(choices=["18-24", "25-30", "31-40", "41-50", "51-60", "61-70", "71-80", "80+", "No answer"], widget=widgets.RadioSelect() , label=
                             "How old are you?")

