from numpy import take
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
This is the second out of three experiments for the Seminar on Experimental Economics in the WS 2020 at the AWI Heidelberg
"""


class Constants(BaseConstants):

    # Here we define the different values that are valid in every form of the game.

    name_in_url = 'Endogen2'#The name can be set to whatever you want it to be. It will show in the URL.
    players_per_group = 3 #Players per group can be set here. In our case the we play a one-shot three person game. You can change this to any INT. Just make sure you change it in the settings tab as well.
    num_rounds = 1 # You can play more than one round, but in our case we play one.
    pool = 30 #This defines how big the pool is. You can use any INT or String here
    efficiency_factor = 2 # This is a INT that indicates how the resource increases the leftover points. You can use any INT or String here
    base= 25/100 #This is the baseline for the tipping point. The first number indicates the percentage, which you can adjust.
    addition_per_take = 1/100 #This is the percentage the tipping point will increase per point taken. The first number indicates the percentage, which you can adjust.

    max = int(np.floor(pool / players_per_group)) #The max value is calculated by the point available and the number of players.
    # np.floor rounds it down and int converts it to an integer. The last step is not necessary, but it looks better.
    completion_code = 112021 # Please change this number in your live version. This is just a random code all participants in the live version get
    #after they complete the experiment.

class Subsession(BaseSubsession): # Ideally you do not need to change anything here.


    # Here we define the different treatments that are available in the different subversions.

    # This is done by having a Boolean (either TRUE or FALSE) for the Treatment.

    #def group_by_arrival_time_method(self, waiting_players):
    #    if len(waiting_players) >= 3:
    #        return waiting_players[:3]
    #    for p in waiting_players:
    #        if p.waiting_too_long():
    #            p.alone = 1
    #            return [p]
    def group_by_arrival_time_method(subsession, waiting_players):
        for p in waiting_players:
            p.category = p.participant.vars['category']

        print('in group_by_arrival_time_method')
        a_players = [p for p in waiting_players if p.category == 'A']
        b_players = [p for p in waiting_players if p.category == 'B']

        if len(a_players) >= 2 and len(b_players) >= 1:
            print('about to create a group')
            return [a_players[0], a_players[1], b_players[0]]
        print('not enough players yet to create a group')

        for p in waiting_players:
            p.category = p.participant.vars['category']
            if p.waiting_too_long():
                p.alone = 1
                return [p]

class Group(BaseGroup):

    #The group-level is used to define values that are the same for every player in the group and to aggregate over the players.
    # To set a variable you need to define it in as a model field. If you the value is not fixed (e.g. the payoff), you can leave the field empty and
    #define a function which sets the value later on

    #First we need to define the tipping point. It consists of the base plus the additional percentage based on the the number of points taken.

    tipping_point = models.FloatField()
    otherplayer1_take = models.IntegerField()
    otherplayer2_take = models.IntegerField()
    chance = models.FloatField()

    def set_up_otherplayer(self):
        self.otherplayer1_take = np.random.randint(0, 6)
        self.otherplayer2_take = np.random.randint(0, 6)

    def set_tipping_point(self):
        if sum([p.alone for p in self.get_players()]) > 0:
            self.tipping_point = np.round(Constants.base + ((sum([p.take for p in self.get_players()]) + self.otherplayer1_take + self.otherplayer2_take) * Constants.addition_per_take),4)
        else:
            self.tipping_point = np.round(Constants.base + (sum([p.take for p in self.get_players()]) * Constants.addition_per_take), 4)




    # To determine if a groups pool breaks down, we create a random number that takes values between 0 and 1.
    # If the tipping point is higher than the random number, breakdown will be TRUE.
    # We set this breakdown as a function that can be called during the experiment.
    # Since we only evaluate it if we are playing the treatment, we condition it by an if statement.

    breakdown = models.BooleanField(initial=False)

    def set_breakdown(self):
        self.chance = round(np.random.rand(), 2)
        self.breakdown = self.tipping_point > np.random.rand()


    # total_points_left is the number of points that do not get taken.
    # resource share is the share each player receives from the resource.
    total_points_left = models.IntegerField()
    resource_share = models.IntegerField()
    # We could define functions here to fill the fields, but we will do it in the payoff function, since it speeds up the programm and
    # keeps the code a little "cleaner"

    #Now we need to set the payoff.
    # If we want the player we need to use player. or for p in self get._players()

    def set_payoffs(self):


        if sum([p.alone for p in self.get_players()]) > 0:
            for p in self.get_players():
                p.total_points_left = Constants.pool - sum([p.take for p in self.get_players()]) - self.otherplayer1_take - self.otherplayer2_take
                p.resource_share = np.round(p.total_points_left * Constants.efficiency_factor / Constants.players_per_group, 0)

        else:
            for p in self.get_players():
                p.total_points_left = Constants.pool - sum([p.take for p in self.get_players()])
                p.resource_share = np.round(
                    p.total_points_left * Constants.efficiency_factor / Constants.efficiency_factor, 0)

        # to calculate the points left we need the sum of all points the players took.
        # This is done with sum([p.take for p in self.get_players()]). Take is defined in the player class.



        # the resource_share is the amount every player gets back from the pool.
        # to calculate the resource_share we need to know how much remained in the pool , multiply it by the factor and devide it by the number of players.
        # Here we use np.round(number, number of decimals) to aviod getting a number like 13,33333333333



        # we need to add an if statement since our payoff is 0 if the pool breaks down. Remember it can only break down if we are in the treatment version.
        # If that is the case the players do not get any money


        # HIER MÜSSEN WIR DOCH NUR DIE SPIELER UNTERSCHEIDEN. SPIELER MIT DER ID 1 UND 2 HABEN DAS AUSZAHLUNGSMUSTER:
        #WENN ZUSAMMENBRICHT BEKOMMEN SIE NICHT. FÜR SPIELER MIT DER ID 3 IST DAS AUSZAHLUNGSMUSTER ANDERS, DIE BEKOMMEN DANN IMMER VARIABLE P.TAKE ODER SO:


        #if self.breakdown == True:
            #for p in self.get_players():
                #p.payoff = 0
        #else:
            # The payoff for each player is determined by the the amount he took and what his share of the common resource is.
            # We do not need to check for the treatment or anything else, since we added the if statement. in case it breaks down.
            #for p in self.get_players():
                #p.payoff = sum([+ p.take,
                                #+ self.resource_share,
                                #])


        if self.breakdown == True:
            if sum([p.alone for p in self.get_players()]) > 0:
                for p in self.get_players():
                    p.payoff = p.take

            else:
                for p in self.get_players():
                    p.payoff = p.take


        else:
            # The payoff for each player is determined by the the amount he took and what his share of the common resource is.
            # We do not need to check for the treatment or anything else, since we added the if statement. in case it breaks down.
            if sum([p.alone for p in self.get_players()]) > 0:
                for p in self.get_players():
                    p.category = p.participant.vars['category']
                    if p.category == 'A':
                        p.payoff = sum ([+p.take,
                                    + self.resource_share,
                                    ])
                else:
                    for p in self.get_players():
                        p.payoff = p.take

            else:
                for p in self.get_players():
                    p.category = p.participant.vars['category']
                    if p.category == 'A':
                        p.payoff = sum([+p.take,
                                       + self.resource_share,
                                       ])

                else:
                    for p in self.get_players():
                        p.payoff = p.take


class Player(BasePlayer):

    category = models.StringField()

    def waiting_too_long(self):

        import time
        return time.time() - self.participant.vars['wait_page_arrival'] > 180

    alone = models.BooleanField(initial=False)

    timeout_take_a = models.BooleanField(initial=False)
    timeout_take_b = models.BooleanField(initial=False)

    timeout_survey = models.BooleanField(initial=False)

    # The Player-level is used to define var on the player level. In otree this means everything that involves a players direct choice.
    # In our case it is the amount he takes.
    # We give the field a label which is then displayed on our html page without any further action.
    age = models.IntegerField(label='What is your age?')
    gender = models.StringField(choices=('female', 'male', 'other'), widget=widgets.RadioSelect(), label= 'What is your gender?')
    education = models.StringField(choices=('High School', 'University', 'other'), widget=widgets.RadioSelect(), label='What is your educational degree?')
    mothertongue = models.StringField(label='What is your mothertongue?')
    mturkmoney = models.StringField(choices= ('0-5 Dollar', '5-10 Dollar', '10-20 Dollar', '>20 Dollar'), widget=widgets.RadioSelect(), label='What do you normally earn on Amazon MTurk per week?')
    coplayerA = models.IntegerField(choices= (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), widget=widgets.RadioSelect(), label= 'What do you think did your coplayer of type A choose?')
    coplayerB = models.IntegerField(choices= (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), widget=widgets.RadioSelect(), label= 'What do you think did your coplayer of type B choose?')


    take = models.IntegerField(label="How many points do you want to take ?")

    #the max a player can take is the third of the pool, rounded down. e.g. pool = 40 --> 40/3 = 13,33.
    #The decimal places can be avoided by picking a number that is divisible by 3. To round down we use the numpy (np) function floor.
    #The way we set up the choices here is by adding a valiation function. This can be done by jst writing fieldname_choices.
    #This will yield a dropdown the player can choose from. We use the function range. The issue here is that it excludes the max value.
    #This is we add +1 to the range

    def take_choices(self):
        return range(int(np.floor(Constants.pool/Constants.players_per_group))+1)

    #Now we implement the test questions. For this we use radioselect and a couple of choices.

