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


import settings

authors = '(Moritz Sommerlad), Julius Gross, Emeli Röttgers, Linda Aldehoff'

doc = """
This is the second out of two experiments for the Seminar on Experimental Economics in the WS 2021 at the AWI Heidelberg
"""


class Constants(BaseConstants):

    # Here we define the different values that are valid in every form of the game.

    name_in_url = 'Endogen'#The name can be set to whatever you want it to be. It will show in the URL.
    players_per_group = 3 #Players per group can be set here. In our case the we play a one-shot three person game. You can change this to any INT. Just make sure you change it in the settings tab as well.
    id_in_group = ()
    num_rounds = 1 # You can play more than one round, but in our case we play one.
    pool = 30 #This defines how big the pool is. You can use any INT or String here
    efficiency_factor = 2 # This is a INT that indicates how the resource increases the leftover points. You can use any INT or String here
    base= 0/100 #This is the baseline for the tipping point. The first number indicates the percentage, which you can adjust.
    addition_per_take = 2/100 #This is the percentage the tipping point will increase per point taken. The first number indicates the percentage, which you can adjust.
    max = int(np.floor(pool / players_per_group)) #The max value is calculated by the point available and the number of players.
    # np.floor rounds it down and int converts it to an integer. The last step is not necessary, but it looks better.
    completion_code = 112021 # Please change this number in your live version. This is just a random code all participants in the live version get
    #after they complete the experiment.
    base_payment = 0.5  # The amount of money (in $) the player gets just for participating
    money_per_point = 0.05
    maxmoney = int(np.floor(money_per_point*23.33+base_payment))


class Subsession(BaseSubsession): # Ideally you do not need to change anything here.
    # Here we define the different treatments that are available in the different subversions.

    # This is done by having a Boolean (either TRUE or FALSE) for the Treatment.
    treatment = models.BooleanField()

    # We then create a session. Here we need to specify if the session should have any special properties. In this case we choose that we
    #want a treatment based on our Boolean in line 35. If we wanted another treatment, like different tipping points, we need to add a bool here.
    def creating_session(self):
        self.treatment = self.session.config.get('treatment')
        self.session.vars['treatment'] = self.session.config.get('treatment')
        # This gives the player the completion code for the payout. Do not worry about this, since it does not effect the functionality
        for player in self.get_players():
            player.completion_code = Constants.completion_code
            self.session.vars['code'] = Constants.completion_code

            if self.session.vars['treatment'] == 1:
                if player.id_in_group % 3 == 0:
                    player.participant.vars['category'] = 'B'
                else:
                    player.participant.vars['category'] = 'A'

            else:
                player.participant.vars['category'] = 'A'

            player.category = player.participant.vars['category']


class Group(BaseGroup):
    pass

    #The group-level is used to define values that are the same for every player in the group and to aggregate over the players.
    # To set a variable you need to define it in as a model field. If you the value is not fixed (e.g. the payoff), you can leave the field empty and
    #define a function which sets the value later on

    #First we need to define the tipping point. It consists of the base plus the additional percentage based on the the number of points taken.



    # The Player-level is used to define var on the player level. In otree this means everything that involves a players direct choice.
    # In our case it is the amount he takes.
    # We give the field a label which is then displayed on our html page without any further action.

    #the max a player can take is the third of the pool, rounded down. e.g. pool = 40 --> 40/3 = 13,33.
    #The decimal places can be avoided by picking a number that is divisible by 3. To round down we use the numpy (np) function floor.
    #The way we set up the choices here is by adding a valiation function. This can be done by jst writing fieldname_choices.
    #This will yield a dropdown the player can choose from. We use the function range. The issue here is that it excludes the max value.
    #This is we add +1 to the range

class Player(BasePlayer):

    category = models.StringField()

    completion_code = models.IntegerField() # Do not worry about this. it does not effect the functionality

    #Now we implement the test questions. For this we use radioselect and a couple of choices.


    test_control = models.IntegerField(choices=[0, 5 , 15, 20], widget=widgets.RadioSelect(), label = "How many points would you earn in total when the <b>pool breaks down</b>?")
    test_control2 = models.IntegerField(choices=[0, 5, 15, 20], widget=widgets.RadioSelect(), label = "How many points would you earn in total? This time the <b>pool does not break down</b>?")

    test1 = models.IntegerField(choices=[0, 5, 15, 20], widget=widgets.RadioSelect() , label=" How many points would you earn in total if the <b>pool breaks down</b>?")
    test2 = models.IntegerField(choices=[0, 5, 15, 20], widget=widgets.RadioSelect() , label=" How many points would you earn in total if the <b>pool does not break down</b>?")

    timeout_preview = models.BooleanField(initial=False)
    timeout_intro = models.BooleanField(initial=False)
    timeout_welcome = models.BooleanField(initial=False)
    timeout_ctest1 = models.BooleanField(initial=False)
    timeout_ctest_result1 = models.BooleanField(initial=False)
    timeout_ctest2 = models.BooleanField(initial=False)
    timeout_ctest_result2 = models.BooleanField(initial=False)
    timeout_test1 = models.BooleanField(initial=False)
    timeout_test2 = models.BooleanField(initial=False)
    timeout_test_result1 = models.BooleanField(initial=False)
    timeout_test_result2 = models.BooleanField(initial=False)
