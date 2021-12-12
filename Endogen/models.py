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

authors = 'Moritz Sommerlad, Julius Gross, Emeli Röttgers, Linda Aldehoff'

doc = """
This is the second out of two experiments for the Seminar on Experimental Economics in the WS 2021 at the AWI Heidelberg
"""


class Constants(BaseConstants):

    # Here we define the different values that are valid in every form of the game.

    name_in_url = 'Endogen'#The name can be set to whatever you want it to be. It will show in the URL.
    players_per_group = 3 #Players per group can be set here. In our case the we play a one-shot three person game. You can change this to any INT. Just make sure you change it in the settings tab as well.
    id_in_group = () #Selbst hinzugefügt könnte sein, dass wir es löschen müssen
    num_rounds = 1 # You can play more than one round, but in our case we play one.
    pool = 30 #This defines how big the pool is. You can use any INT or String here
    efficiency_factor = 2 # This is a INT that indicates how the resource increases the leftover points. You can use any INT or String here
    base= 0/100 #This is the baseline for the tipping point. The first number indicates the percentage, which you can adjust.
    addition_per_take = 2/100 #This is the percentage the tipping point will increase per point taken. The first number indicates the percentage, which you can adjust.
    max = int(np.floor(pool / players_per_group)) #The max value is calculated by the point available and the number of players.
    # np.floor rounds it down and int converts it to an integer. The last step is not necessary, but it looks better.
    completion_code = 112021 # Please change this number in your live version. This is just a random code all participants in the live version get
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
        self.tipping_point = np.round(Constants.base + (sum([p.take for p in self.get_players()]) * Constants.addition_per_take),4)



    # To determine if a groups pool breaks down, we create a random number that takes values between 0 and 1.
    # If the tipping point is higher than the random number, breakdown will be TRUE.
    # We set this breakdown as a function that can be called during the experiment.
    # Since we only evaluate it if we are playing the treatment, we condition it by an if statement.

    breakdown = models.BooleanField(initial=False)


    def set_breakdown(self):
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
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)

        # to calculate the points left we need the sum of all points the players took.
        # This is done with sum([p.take for p in self.get_players()]). Take is defined in the player class.
        self.total_points_left = Constants.pool - sum([p.take for p in self.get_players()])

        # the resource_share is the amount every player gets back from the pool.
        # to calculate the resource_share we need to know how much remained in the pool , multiply it by the factor and devide it by the number of players.
        # Here we use np.round(number, number of decimals) to aviod getting a number like 13,33333333333
        self.resource_share = np.round(
            self.total_points_left * Constants.efficiency_factor / Constants.players_per_group, 0)


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

        if self.subsession.treatment == 1:
            if self.breakdown == True:
                p1.payoff = 0
                p2.payoff = 0
                p3.payoff = p3.take


            else:
            # The payoff for each player is determined by the the amount he took and what his share of the common resource is.
            # We do not need to check for the treatment or anything else, since we added the if statement. in case it breaks down.
                for p in self.get_players():
                    p.payoff = sum([+ p.take,
                                    + self.resource_share,
                                    ])

        else:
            if self.breakdown == True:
                for p in self.get_players():
                    p.payoff = 0
            else:
            # The payoff for each player is determined by the the amount he took and what his share of the common resource is.
             # We do not need to check for the treatment or anything else, since we added the if statement. in case it breaks down.
                for p in self.get_players():
                    p.payoff = sum([+ p.take,
                                    + self.resource_share,
                                    ])



class Player(BasePlayer):

    # The Player-level is used to define var on the player level. In otree this means everything that involves a players direct choice.
    # In our case it is the amount he takes.
    # We give the field a label which is then displayed on our html page without any further action.

    take = models.IntegerField(label="How many points do you want to take ?")

    #the max a player can take is the third of the pool, rounded down. e.g. pool = 40 --> 40/3 = 13,33.
    #The decimal places can be avoided by picking a number that is divisible by 3. To round down we use the numpy (np) function floor.
    #The way we set up the choices here is by adding a valiation function. This can be done by jst writing fieldname_choices.
    #This will yield a dropdown the player can choose from. We use the function range. The issue here is that it excludes the max value.
    #This is we add +1 to the range

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
    occupation = models.StringField(label='What is your occupation?')
    environment = models.StringField(
        label='Do you care about the environment?',
        choices=[['yes', 'yes'], ['no', 'no'], ['a little', 'a little']],
        widget=widgets.RadioSelect,
    )

    def take_choices(self):
        return range(int(np.floor(Constants.pool/Constants.players_per_group))+1)

    completion_code = models.IntegerField() # Do not worry about this. it does not effect the functionality

    #Now we implement the test questions. For this we use radioselect and a couple of choices.


    test_control = models.IntegerField(choices=[5 , 10, 15, 20], widget=widgets.RadioSelect(), label = "How many points would you earn in total?")
    test_control2 = models.IntegerField(choices=[6, 13, 17, 22], widget=widgets.RadioSelect(), label = "How many points would you earn in total?")

    test1 = models.IntegerField(choices=[0, 5, 15, 20], widget=widgets.RadioSelect() , label=" How many points would you earn in total if the pool breaks down?")
    test2 = models.IntegerField(choices=[0, 5, 15, 20], widget=widgets.RadioSelect() , label=" How many points would you earn in total if the pool does not break down?")

