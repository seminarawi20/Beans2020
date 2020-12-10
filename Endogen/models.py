from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
)

# Numpy is a mathematical python library which is used from more complex calculations. When we want to call it we can use np.
import numpy as np

author = 'Moritz Sommerlad'

doc = """
This is the second out of three experiments for the Seminar on Experimental Economics in the WS 2020 at the AWI Heidelberg
"""


class Constants(BaseConstants):

    # Here we define the different values that are valid in every form of the game.

    name_in_url = 'Endogen'#The name can be set to whatever you want it to be. It will show in the URL.
    players_per_group = 3 #Players per group can be set here. In our case the we play a one-shot three person game. You can change this to any INT. Just make sure you change it in the settings tab as well.
    num_rounds = 1 # You can play more than one round, but in our case we play one.
    pool = 30 #This defines how big the pool is. You can use any INT or String here
    efficiency_factor = 2 # This is a INT that indicates how the resource increases the leftover points. You can use any INT or String here
    base= 30/100 #This is the baseline for the tipping point. The first number indicates the percentage, which you can adjust.
    addition_per_give = 2/100 #This is the percentage the tipping point will increase per point taken. The first number indicates the percentage, which you can adjust.
    common_pool = 0 #This is the common pool that is empty at the beginning
    max = int(np.floor(pool / players_per_group)) #The max value is calculated by the point available and the number of players.
    # np.floor rounds it down and int converts it to an integer. The last step is not necessary, but it looks better.
    completion_code = 142675 # Please change this number in your live version. This is just a random code all participants in the live version get
    #after they complete the experiment.

class Subsession(BaseSubsession): # Ideally you do not need to change anything here.

    # Here we define the different treatments that are available in the different subversions.

    # This is done by having a Boolean (either TRUE or FALSE) for the Treatment.
    treatment = models.BooleanField()

    # We then create a session. Here we need to specify if the session should have any special properties. In this case we choose that we
    #want a treatment based on our Boolean in line 35. If we wanted another treatment, like different tipping points, we need to add a bool here.
    def creating_session(self):
        self.treatment = self.session.config.get('treatment')
        # This gives the player the completion code for the payout. Do not worry about this, since it does not effect the functionality
        for player in self.get_players():
            player.completion_code = Constants.completion_code



class Group(BaseGroup):

    #The group-level is used to define values that are the same for every player in the group and to aggregate over the players.
    # To set a variable you need to define it in as a model field. If you the value is not fixed (e.g. the payoff), you can leave the field empty and
    #define a function which sets the value later on

    #First we need to define the tipping point. It consists of the base plus the additional percentage based on the the number of points taken.

    tipping_point = models.FloatField()
    def set_tipping_point(self):
        self.tipping_point = np.round(Constants.base + (sum([p.give for p in self.get_players()]) * Constants.addition_per_give),4)



    # To determine if a groups pool breaks down, we create a random number that takes values between 0 and 1.
    # If the tipping point is lower than the random number, breakdown will be TRUE.
    # We set this breakdown as a function that can be called during the experiment.

    # To determine if the common pool breaks down we check whether the tipping point is higher
    breakdown = models.BooleanField(initial=False)

    # If tipping point is higher than 2/3 there still is some chance that the common pool breaks down, which can be
    # slimmed by putting more balls in the common pool.
    def set_breakdown(self):
        self.breakdown = self.tipping_point < (2/3)


    # Alternative (still to be decided):
    # def set_breakdown(self):
    #     self.breakdown = self.tipping_point < np.random.rand()


    # total_points_given is the number of points that are given.
    # resource share is the share each player receives from the resource.
    total_points_given = models.IntegerField()
    resource_share = models.IntegerField()
    # We could define functions here to fill the fields, but we will do it in the payoff function, since it speeds up the programm and
    # keeps the code a little "cleaner"

    #Now we need to set the payoff.
    # If we want the player we need to use player. or for p in self get._players()
    def set_payoffs(self):

        # to calculate the points given we need the sum of all points the players gave.
        # This is done with sum([p.give for p in self.get_players()]). Give is defined in the player class.

        # We calculate total points given to the common pool by adding up all given balls from every player
        self.total_points_given = Constants.common_pool + sum([p.give for p in self.get_players()])

        # the resource_share is the amount every player gets back from the pool.
        # to calculate the resource_share we need to know how much was given to the common pool , multiply it by the
        # factor and divide it by the number of players.
        # Here we use np.round(number, number of decimals) to aviod getting a number like 13,33333333333
        self.resource_share = np.round(
            self.total_points_given * Constants.efficiency_factor / Constants.players_per_group, 0)

        # we need to add an if statement for when the pool breaks down.
        # If that is the case the players only receive the balls they have not put in the common pool.

        if self.breakdown == True:
            for p in self.get_players():
                p.payoff = (Constants.max - p.give)

                # Alternative:
                # p.payoff = 0

        else:
            # The payoff for each player is determined by the the amount he gave and what his share of the common resource is.
            for p in self.get_players():
                p.payoff = sum([+ p.give,
                                + self.resource_share,
                                ])


class Player(BasePlayer):

    # The Player-level is used to define var on the player level. In otree this means everything that involves a players direct choice.
    # In our case it is the amount he takes.
    # We give the field a label which is then displayed on our html page without any further action.

    give = models.IntegerField(label="How many balls do you want to give?")

    #the max a player can take is the third of the pool, rounded down. e.g. pool = 40 --> 40/3 = 13,33.
    #The decimal places can be avoided by picking a number that is divisible by 3. To round down we use the numpy (np) function floor.
    #The way we set up the choices here is by adding a valiation function. This can be done by jst writing fieldname_choices.
    #This will yield a dropdown the player can choose from. We use the function range. The issue here is that it excludes the max value.
    #This is we add +1 to the range

    def give_choices(self):
        return range(int(np.floor(Constants.pool/Constants.players_per_group))+1)

    completion_code = models.IntegerField() # Do not worry about this. it does not effect the functionality

    #Now we implement the test questions. For this we use radioselect and a couple of choices.

    test1 = models.IntegerField(choices=[0, 5, 15], widget=widgets.RadioSelect() , label=" How many balls would you have in total if the pool breaks down?")
    test2 = models.IntegerField(choices=[0, 5, 15], widget=widgets.RadioSelect() , label=" How many balls would you have in total if the pool does not break down?")

    #In the following we implement the questions from the questionnaire.

    q1 = models.StringField(choices=["Alabama", "Alaska", "Arizona", "Arkansas", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois",
                                      "Indiana", "Iowa", "California", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
                                      "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina",
                                      "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
                                      "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"], label="Which state are you from?")

    q2 = models.StringField(choices=["Democratic Party", "Republican Party", "Other", "None"], widget=widgets.RadioSelect() , label="With party do you feel closer to?")

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

