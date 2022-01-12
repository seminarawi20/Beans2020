from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time

# Pages are responsible for retrieving and passing back data from models to templates and vice versa.
# If you need to show something to a participant or to get his/her input, you need to indicate this in pages.py

#If you want to display something other than text (e.g. a variable) you need to use the function
#vars_for_template and make it return a dictionary. The index of the dictionary can then be used to display it on the page with {{ index }}.
# it is key that you indicate from which model you return a variable, here our treatment is defined on the subsession level while the pool is defined in the constants

class Preview(Page):

    # def vars_for_template(self):
    #    return {'base_payment': Constants.base_payment}

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_preview = True

class Introduction(Page):

    def vars_for_template(self):
        return dict( base =Constants.base_payment,
                     rate=Constants.money_per_point,
                     maxmoney=Constants.maxmoney
                    )

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_intro = True

class Welcome(Page):

    def vars_for_template(self):
        return {'pool': Constants.pool,
                'players': Constants.players_per_group,
                'factor': Constants.efficiency_factor,
                'max': Constants.max,
                'treatment': self.subsession.treatment,
                'base': Constants.base*100,
                'addition_per_take': Constants.addition_per_take*100,
                'id_in_group': self.player.id_in_group,
                'category': self.participant.category
                }

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_welcome = True

# I split the Pages for the comprehension tests since the structure looks nicer. Does not have a practical meaning.
# For each Question and Answer pair i created a new page. You can decide if you want to show the page by the
# id _displayed line.

## a form field is something the participant can interact with. Since we defined it on a player level, we must specify it in the form_model section.


class Test_Control(Page):
    form_model = 'player'
    form_fields = ['test_control']

    def is_displayed(self):
        return self.subsession.treatment == 0

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_ctest1 = True

class Results_Control(Page):

    def vars_for_template(self):
        return {'test_control': self.player.test_control}

    def is_displayed(self):
        return self.subsession.treatment == 0

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_ctest_result1 = True

    ## DIESE SEITE IST NEU: FRAGT DIEJEINIGEN, DIE ERSTE FRAGE FALSCH BEANTWORTET HABEN NOCHEINMAL MIT NEUEM BSP:##
class Test_Control2(Page):
    form_model = 'player'
    form_fields = ['test_control2']

    def is_displayed(self):
        return self.subsession.treatment == 0

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_ctest2 = True

    ## DIESE SEITE IST NEU: GIBT DENJENIGEN, DIE ERSTE FRAGE FALSCH BEANTWORTET HABEN, ERGEBNISSE DER 2. FRAGE: ##
class Results_Control2(Page):

    def vars_for_template(self):
        return {'test_control2': self.player.test_control2}

    def is_displayed(self):
        return self.subsession.treatment == 0 and self.player.test_control != 15

    timeout_seconds = 120

    def before_next_page(self):
        self.participant.vars['wait_page_arrival'] = time.time()
        if self.timeout_happened:
            self.player.timeout_ctest_result2 = True

class Test1(Page):
    form_model = 'player'
    form_fields = ['test1']

    def is_displayed(self):
        return self.subsession.treatment == 1

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_test1 = True


class Test2(Page):
    form_model = 'player'
    form_fields = ['test2']

    def is_displayed(self):
        return self.subsession.treatment == 1

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_test2 = True

class Results_Test1(Page):
    def vars_for_template(self):
        return {'test1': self.player.test1,
                'id_in_group': self.player.id_in_group
                }

    def is_displayed(self):
        return self.subsession.treatment == 1

    timeout_seconds = 120

    def before_next_page(self):
        if self.timeout_happened:
            self.player.timeout_test_result1 = True

class Results_Test2(Page):
    def vars_for_template(self):
        return {'test2': self.player.test2}

    def is_displayed(self):
        return self.subsession.treatment == 1

    timeout_seconds = 120

    def before_next_page(self):
        self.participant.vars['wait_page_arrival'] = time.time()
        if self.timeout_happened:
            self.player.timeout_test_result2 = True


# here we indicate in which sequence we want the pages to be played. You can repeat pages as well.
page_sequence = [Preview,
                 Introduction,
                 Welcome,
                 Test_Control,
                 Results_Control,
                 Test_Control2,
                 Results_Control2,
                 Test1,
                 Results_Test1,
                 Test2,
                 Results_Test2,
                 ]
