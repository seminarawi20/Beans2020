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



import numpy as np


import settings

authors = 'Linda Aldehoff based on the work of Moritz Sommerlad, Julius Gross, Emeli Röttgers'

doc = """
This is the bachelor thesis of Linda ALdehoff based on the second out of two experiments for the Seminar on Experimental Economics in the WS 2021 at the AWI Heidelberg
"""


class Constants(BaseConstants):

    # Here we define the different values that are valid in every form of the game.

    name_in_url = 'Endogen3'#The name can be set to whatever you want it to be. It will show in the URL.
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
    base_payment = 0.7  # The amount of money (in $) the player gets just for participating
    money_per_point = 0.05
    maxmoney = int(np.floor(money_per_point*23.33+base_payment))


class Subsession(BaseSubsession):
    # Here we define the different treatments that are available in the different subversions.
    # This is done by having a Boolean (either TRUE or FALSE) for the Treatment.
    treatment = models.BooleanField()
    def creating_session(self):
        self.treatment = self.session.config.get('treatment')
        #self.take = self.session.config.get('take')
        self.session.vars['treatment'] = self.session.config.get('treatment')
        #self.session.vars['take'] = self.session.config.get('take')

    def group_by_arrival_time_method(subsession, waiting_players):
        for p in waiting_players:
            p.category = p.participant.vars['category']
            p.treatment = p.session.vars['treatment']

            if p.treatment == 1:
                print('in group_by_arrival_time_method')
                a_players = [p for p in waiting_players if p.category == 'A']
                b_players = [p for p in waiting_players if p.category == 'B']
                if len(a_players) >= 2 and len(b_players) >= 1:
                    print('about to create a group')
                    return [a_players[0], a_players[1], b_players[0]]
                print('not enough players yet to create a group')
                for p in waiting_players:
                    if p.waiting_too_long():
                        p.alone = 1
                        return [p]
            else:
                if len(waiting_players) >= 3:
                    return waiting_players[:3]
                for p in waiting_players:
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


    #chance = models.FloatField()

    def set_up_otherplayer(self):
        self.otherplayer1_take = np.random.randint(0, 6)
        self.otherplayer2_take = np.random.randint(0, 6)


    def set_tipping_point(self):
        if sum([p.alone for p in self.get_players()]) > 0:
            self.tipping_point = np.round(Constants.base + ((sum([p.take for p in
                                                                  self.get_players()]) + self.otherplayer1_take + self.otherplayer2_take) * Constants.addition_per_take),
                                          4)
        else:
            self.tipping_point = np.round(Constants.base + (sum([p.take for p in self.get_players()]) * Constants.addition_per_take), 4)

    # To determine if a groups pool breaks down, we create a random number that takes values between 0 and 1.
    # If the tipping point is higher than the random number, breakdown will be TRUE.
    # We set this breakdown as a function that can be called during the experiment.
    # Since we only evaluate it if we are playing the treatment, we condition it by an if statement.

    breakdown = models.BooleanField(initial=False)


    def set_breakdown(self):
        #self.chance = round(np.random.rand(), 2)
        self.breakdown = self.tipping_point > np.random.rand()



    #def expectations2C_check(self, value):
       # self.otherplayer2_take = value['expectations2C']



 #PLAYER 3 expectations:
    expectations1C_check = models.BooleanField(initial=False)

    def set_expectations1C_check(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        self.expectations1C_check = p3.expectations1C == p1.take
        #self.expectations1C_check = p3.value['expectations1C'] == p1.participant.vars['take'].value['take']
        #if p3.value['expectations1C'] == p1.participant.vars['take'].value['take']:
            #self.expectations1C_check = True

        #winnerC2 = [p3.expectations2C == p2.take_decision]

    expectations2C_check = models.BooleanField(initial=False)
    def set_expectations2C_check(self):
        players = self.get_players()
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        self.expectations2C_check = p3.expectations2C == p2.take
        #self.expectations2C_check = p3.value['expectations2C'] == p2.participant.vars['take'].value['take']
        #if p3.value['expectations2C'] == p2.session.vars['take_choices'].value['take_choices']:
            #self.expectations2C_check = True

        #PLAYER2 expectations:

    expectations1C2_check = models.BooleanField(initial=False)
    def set_expectations1C2_check(self):
        players = self.get_players()
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        self.expectations1C2_check = p2.expectations1C == p1.take
        #self.expectations1C2_check = p2.value['expectations1C'] == p1.participant.vars['take'].value['take']
        #if p2.value['expectations1C'] == p1.session.vars['take_choices'].value['take_choices']:
            #self.expectations1C2_check = True

    expectations2C2_check =models.BooleanField(initial=False)
    def set_expectations2C2_check(self):
        players = self.get_players()
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        self.expectations2C2_check = p2.expectations2C == p3.take
        #self.expectations2C2_check = p2.value['expectations2C'] == p3.participant.vars['take'].value['take']
        #if p2.value['expectations2C'] == p3.session.vars['take_choices'].value['take_choices']:
            #self.expectations2C2_check = True


#PLAYER1 expectations:

    expectations1C1_check = models.BooleanField(initial=False)
    def set_expectations1C1_check(self):
        players = self.get_players()
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        self.expectations1C1_check = p1.expectations1C == p2.take
        #self.expectations1C1_check = p1.value['expectations1C'] == p2.participant.vars['take'].value['take']
        #if p1.value['expectations1C'] == p2.session.vars['take'].value['take']:
            #self.expectations1C1_check = True

    expectations2C1_check = models.BooleanField(initial=False)

    def set_expectations2C1_check(self):
        players = self.get_players()
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        self.expectations2C1_check = p1.expectations2C == p3.take
        #self.expectations2C1_check = p1.value['expectations2C'] == p3.participant.vars['take'].value['take']
        #if p1.value['expectations2C'] == p3.session.vars['take'].value['take']:
            #self.expectations2C1_check = True

#participant und session funktioniert beides nicht

        #PLAYER 3 expectations (treat):

    expectations1T_check = models.BooleanField(initial=False)

    def set_expectations1T_check(self):
        players = self.get_players()
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        self.expectations1T_check = p3.expectations1T == p1.take
        #self.expectations1T_check = p3.value['expectations1T'] == p1.session.vars['take'].value['take']

    expectations2T_check = models.BooleanField(initial=False)

    def set_expectations2T_check(self):
        players = self.get_players()
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        self.expectations2T_check = p3.value['expectations2T'] == p2.session.vars['take'].value['take']

#PLAYER2 expectations (treat):

    expectations1T2_check = models.BooleanField(initial=False)

    def set_expectations1T2_check(self):
        players = self.get_players()
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        self.expectations1T2_check = p2.value['expectations1T'] == p1.session.vars['take'].value['take']

    expectations2T2_check = models.BooleanField(initial=False)

    def set_expectations2T2_check(self):
        players = self.get_players()
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        self.expectations2T2_check = p2.value['expectations2T'] == p3.session.vars['take'].value['take']

#PLAYER1 expectations (treat):

    expectations1T1_check = models.BooleanField(initial=False)
    def set_expectations1T1_check(self):
        players = self.get_players()
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        self.expectations1T1_check = (p1.value['expectations1T'] == p2.session.vars['take'].value['take'])

    expectations2T1_check = models.BooleanField(initial=False)

    def set_expectations2T1_check(self, value):
        players = self.get_players()
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
       # for p1 in self.get_players():
            #p1.value.take_choices = p1.participant.vars['take_choices']
        ##for p2 in self.get_players():
            #p2.value.take_choices = p2.session.vars['take_choices']
        #for p3 in self.get_players():
            #p3.value.take_choices = p3.session.vars['take_choices']
        #self.expectations2T1_check = p1.value['expectations2tb'] == p3.session.vars['take'].value['take']
        self.expectations2T1_check = p1.expectations2tb == p3.take


    # total_points_left is the number of points that do not get taken.
    # resource share is the share each player receives from the resource.
    total_points_left = models.IntegerField()
    resource_share = models.IntegerField()
    # We could define functions here to fill the fields, but we will do it in the payoff function, since it speeds up the programm and
    # keeps the code a little "cleaner"

    #Now we need to set the payoff.
     #If we want the player we need to use player. or for p in self get._players()





    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        #id_in_group = player.id_in_group
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        for p in self.get_players():
            #p.session.config.get('take')
            #p.take = p.participant.vars['take']
            p.treatment = p.session.vars['treatment']
            #p1.take = p1.participant.vars['take']
            #p2.take = p2.participant.vars['take']
            #p3.take = p3.participant.vars['take']
            #p3.expectations1C = p3.value['expecations1C']
            #p2.expectations1C = p2.value['expecations1C']
            #p1.expectations1C = p1.value['expecations1C']
            #p3.expectations2C = p3.value['expecations2C']
            #p2.expectations2C = p2.value['expecations2C']
            #p1.expectations2C = p1.value['expecations2C']
            #p3.expectations1T = p3.value['expecations1T']
            #p2.expectations1T = p2.value['expecations1T']
            #p1.expectations1T = p1.value['expecations1T']
            #p3.expectations2tb = p3.value['expecations2tb']
            #p2.expectations2T = p2.value['expecations2T']
            #p1.expectations2T = p1.value['expecations2T']
            if p.treatment == 1:
                print('treatment')
                if p == p3:
                    print('p3')
                    if self.expectations1T_check == True:
                    #if p3.expectations1T == p1.take:
                        print('expectations1T_check')
                        if self.expectations2T_check == True:
                        #if p3.expectations2T == p2.take:
                            for p3 in self.get_players():
                                print('payoff4)')
                                p3.payoff = 4
                        else:
                            for p3 in self.get_players():
                                p3.payoff = 2
                    else:
                        if self.expectations2T_check == True:
                        #if p3.expectations2T == p2.take:
                            for p3 in self.get_players():
                                p3.payoff = 2
                        else:
                            for p3 in self.get_players():
                                p3.payoff = 0
                else:
                    if p == p2:
                        print('p2')
                        if self.expectations1T2_check == True:
                        #if p2.expectations1T == p1.take:
                            if self.expectations2T2_check == True:
                            #if p2.expectations2T == p3.take:
                                for p2 in self.get_players():
                                    p2.payoff = 4
                            else:
                                for p2 in self.get_players():
                                    p2.payoff = 2
                        else:
                            if self.expectations2T2_check == True:
                            #if p2.expectations2T == p3.take:
                                for p2 in self.get_players():
                                    p2.payoff = 2
                            else:
                                for p2 in self.get_players():
                                    p2.payoff = 0
                    else:
                        if self.expectations1T1_check == True:
                        #if p1.expectations1T == p2.take:
                            if self.expectations2T1_check == True:
                            #if p1.expectations2T == p3.take:
                                for p1 in self.get_players():
                                    p1.payoff = 4
                            else:
                                for p1 in self.get_players():
                                    p1.payoff = 2
                        else:
                            if self.expectations2T1_check == True:
                            #if p1.expectations2T == p3.take: p.take is none
                                for p1 in self.get_players():
                                    p1.payoff = 2
                            else:
                                for p1 in self.get_players():
                                    p1.payoff = 0
            else:
                #for p in player.get_player_by_id(3):
                if p == p3:
                    print('p3endo')
                    if self.expectations1C_check == True:
                        print('expetationsp3,1')
                        if self.expectations2C_check == True:
                            for p3 in self.get_players():
                                p3.payoff = 4
                        else:
                            for p3 in self.get_players():
                                p3.payoff = 2
                    else:
                        print('exp1CFalse')
                        if self.expectations2C_check == True:
                            for p3 in self.get_players():
                                p3.payoff = 2
                        else:
                            for p3 in self.get_players():
                                p3.payoff = 0
                else:
                    #for p in player.get_player_by_id(2):
                    if p == p2:
                        print('endop2')
                        if self.expectations1C2_check == True:
                            print('exp.p2')
                            if self.expectations2C2_check == True:
                                for p2 in self.get_players():
                                    p2.payoff = 4
                            else:
                                for p2 in self.get_players():
                                    p2.payoff = 2
                        else:
                            if self.expectations2C2_check == True:
                                for p2 in self.get_players():
                                    p2.payoff = 2
                            else:
                                for p2 in self.get_players():
                                    print('exp.false')
                                    p2.payoff = 0

                    else:
                        print('p1')
                        if self.expectations1C1_check == True:
                            if self.expectations2C1_check == True:
                                for p1 in self.get_players():
                                    p1.payoff = 4
                            else:
                                for p1 in self.get_players():
                                    p1.payoff = 2
                        else:
                            if self.expectations2C1_check == True:
                                for p1 in self.get_players():
                                    p1.payoff = 2
                            else:
                                for p1 in self.get_players():
                                    p1.payoff = 0



class Player(BasePlayer):

    def waiting_too_long(self):
        import time
        return time.time() - self.participant.vars['wait_page_arrival'] > 180

    category = models.StringField()
    treatment = models.BooleanField()


    alone = models.BooleanField(initial=False)

    # The Player-level is used to define var on the player level. In otree this means everything that involves a players direct choice.
    # In our case it is the amount he takes.
    # We give the field a label which is then displayed on our html page without any further action.
    take = models.IntegerField(
        label="How many points do you want to take ?",
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    )
    #the max a player can take is the third of the pool, rounded down. e.g. pool = 40 --> 40/3 = 13,33.
    #The decimal places can be avoided by picking a number that is divisible by 3. To round down we use the numpy (np) function floor.
    #The way we set up the choices here is by adding a valiation function. This can be done by jst writing fieldname_choices.
    #This will yield a dropdown the player can choose from. We use the function range. The issue here is that it excludes the max value.
    #This is we add +1 to the range

    timeout_take = models.BooleanField(initial=False)
    timeout_endresults = models.BooleanField(initial=False)
    timeout_survey = models.BooleanField(initial=False)

    expectations1C = models.IntegerField(
        label='How many points did you expect your first team member to take?',
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    )
    expectations2C = models.IntegerField(
        label='How many points did you expect your second team member to take?',
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    )

    expectations1T = models.IntegerField(
        label='How many points did you expect your first team member to take (Type A)?',
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    )

    expectations2T = models.IntegerField(
        label='How many points did you expect your second team member to take (Type B)?',
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    )

    expectations2tb = models.IntegerField(
        label='How many points did you expect your second team member to take (Type A)?',
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    )


    age = models.IntegerField(label='How old are you?', min=18, max=125)
    gender = models.StringField(
        choices=[['Male', 'Male'], ['Female', 'Female'], ['Other', 'Other']],
        label='What is your gender?',
        widget=widgets.RadioSelect,
    )
    education = models.StringField(
        choices=[['High School', 'High School'], ['Bachelor', 'Bachelor'], ['Master', 'Master'], ['PhD', 'PhD'],
                 ['None', 'None']],
        label='What is your highest level of education? (If currently enrolled highest degree received)',
        widget=widgets.RadioSelect,
    )
    children = models.StringField(
        label='Do you have children?',
        choices=[['yes', 'yes'], ['no', 'no']]
    )
    answer_same= models.IntegerField(
        label='Compared to other participants who were assigned the same role, do you think your decision was socially fair?',
        choices=[
            [1,'Not fair at all'],
            [2,'Not fair'],
            [3,'Average'],
            [4,'Fair'],
            [5,'Very fair'],
        ]
    )
    environment= models.IntegerField(
        label='How much do you agree with this sentence: "I care about the environment":',
        choices=[
            [1,'Strongly Disagree'],
            [2,'Disagree'],
            [3,'Neutral'],
            [4,'Agree'],
            [5,'Strongly Agree'],
        ]
    )

