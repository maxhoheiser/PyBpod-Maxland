
import random

class ProbabilityConstuctor():
    def __init__(self, settings):
        """object to calculate and handle stimulus sides
        Args:
            settings (TrialParameterHandler object): the object for all the session parameters from TrialPArameterHandler
        """        
        self.settings = settings
        self.stim_side_dict =  {}
        # initialize random sides
        self.stim_side_dict = dict()
        # insist mode tracking
        self.chosen_sides_li = []
        self.insist_mode_chosen_side_li = []
        self.insist_range_trigger = settings.insist_range_trigger #range to check for same side
        self.insist_range_deactivate = settings.insist_range_deactivate # range in which number of correct choices have to occure to deactivate insit mode
        self.insist_correct_deactivate = settings.insist_correct_deactivate # number of correct choice to deactivate insist mode
        self.insist_mode_active = False
        self.inisist_side = None
        
        

    def get_random_side(self):
        # check insist mode
        if self.insist_mode_active:
            if self.insist_side == "left":
                random_right = False
            elif self.insist_side == "right":
                random_right = True
        else:
            random_right = bool(random.getrandbits(1))
        # asign sides to dict
        self.stim_side_dict["right"]=random_right
        self.stim_side_dict["left"]= not(random_right)


    def insist_mode_check(self,trial):
        # get chosen side
        if trial:
            current_side = "left"
        elif trial:
            current_side = "right"
        self.chosen_sides_li.append(current_side)
        # check for insist mode activate 
        if not self.insist_mode_activte:
            if len(self.chosen_sides_li) >= self.insist_range_trigger:
                slice = self.chosen_sides_li[-self.insist_range_trigger:]
            else:
                slice = self.chosen_sides_li
            left_num_chosen = sum(map(lambda x: x=="left", slice))
            right_num_chosen = sum(map(lambda x: x=="right", slice))
            if left_num_chosen >= self.insist_range_trigger:
                self.insist_mode_active = True
                self.insist_side = "left"
            if right_num_chosen >= self.insist_range_trigger:
                self.insist_mode_active = True
                self.insist_side = "right"
            print("\n--------------------------------\n")
            print("INSISTE MODE ACTIVATED: ",self.insist_side)
            print("\n--------------------------------")
        # deactivate insist mode
        if self.insist_mode_active:
            self.insist_mode_chosen_side_li.append(current_side)
            # get insist mode slice
            if len(self.insist_mode_chosen_side_li) >= self.insist_range_deactivate:
                slice = self.insist_mode_chosen_side_li[-self.insist_correct_deactivate:]
            else:
                slice = self.insist_mode_chosen_side_li
            # check range if correct
            insist_correct_choice = sum(map(lambda x: x==self.insist_side, slice))
            if insist_correct_choice >= self.insist_correct_deactivate:
                self.insist_mode_active = False
                self.insist_side = "right"
                self.inist_mode_chosen_sde = [] #clear last insist mode list
                print("\n--------------------------------\n")
                print("INSISTE MODE DEACTIVATED")
                print("\n--------------------------------")