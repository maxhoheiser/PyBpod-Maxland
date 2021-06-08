from psychopy import visual, core, monitors #import some libraries from PsychoPy
import multiprocessing
import time
import threading
import os
import sys

class Stimulus():
    def __init__(self, settings, rotary_encoder, correct_stim_side):
        """[summary]

        Args:
            settings (TrialParameterHandler object):  the object for all the session parameters from TrialPArameterHandler
            rotary_encoder (RotaryEncoder object): object handeling rotary encoder module
        """         
        self.settings = settings    
        self.trials = settings.trial_number

        # set gain
        self.FPS = settings.FPS
        self.SCREEN_WIDTH = settings.SCREEN_WIDTH
        self.SCREEN_HEIGHT = settings.SCREEN_HEIGHT
        self.SCREEN_SIZE = (settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT)
        # stimulus    
        self.rotary_encoder = rotary_encoder
        self.correct_stim_side = correct_stim_side
        #self.gain = self.get_gain()
        self.gain_left,self.gain_right  =  [round(abs(y/x),2) for x in settings.thresholds[0:1] for y in settings.stim_end_pos]
        self.gain = self.gain_left
        # monitor configuration
        self.monitor = monitors.Monitor('testMonitor', width=self.SCREEN_WIDTH, distance=self.SCREEN_HEIGHT)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
        self.monitor.setSizePix(self.SCREEN_SIZE)
        # create window
        #create a window
        self.win = visual.Window(
            size=(self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 
            fullscr=True, 
            screen=2, 
            monitor=self.monitor,
            winType='pyglet', allowGUI=False, allowStencil=False,
            color=self.settings.bg_color, colorSpace='rgb',
            blendMode='avg', useFBO=True, 
            units='height')
        self.win.winHandle.maximize() # fix black bar bottom
        self.win.flip()
        # get frame rate of monitor
        expInfo = {}
        expInfo['frameRate'] = self.win.getActualFrameRate()
        if expInfo['frameRate'] != None:
            frameDur = 1.0 / round(expInfo['frameRate'])
        else:
            frameDur = 1.0 / 60.0  # could not measure, so guess
        


    # helper functions ===============================================================
    def keep_on_scrren(self, position_x):
        """keep the stimulus postition in user defined boundaries

        Args:
            position_x (int): current stimulus screen positition in pixel

        Returns:
            int: updated stimulus position
        """        
        return max(min(self.stim_end_pos_right, position_x), self.stim_end_pos_left)
        

    def get_gain(self):
        clicks = 1024/365 * abs(self.settings.thresholds[0]) #each full rotation = 1024 clicks
        gain = abs(self.settings.stim_end_pos[0]) / clicks
        return round(gain,2)

    def ceil(self,num):
        if num > 20:
            return 20
        else:
            return num

    # stimulus functions =============================================================
    def gen_grating(self, grating_sf, grating_or, pos):
        grating = visual.GratingStim(
            win=self.win,
            tex = 'sin', # texture used
            pos = (pos,0),
            units='pix',
            size=500,
            sf = grating_sf, 
            ori = grating_or,
            phase= (0.0,0.0),
            contrast = 1, # unchanged contrast (from 1 to -1)
            #units="deg",
            #pos = (0.0, 0.0), #in the middle of the screen. It is convertes internally in a numpy array
            #sf = 5.0 / 200.0, # set the spatial frequency 5 cycles/ 150 pixels. 
            #mask='raisedCos',
            mask = 'raisedCos'
        )
        return grating

    def gen_stim(self):
        circle = visual.Circle(
            win=self.win,
            name='cicle',
            radius=self.settings.stimulus_rad,
            units='pix',
            edges=128,
            #units='pix',
            fillColor= self.settings.stimulus_col,
            pos=(0,0),
            )
        return circle

    # Main psychpy loop ==============================================================
    def run_game(self,run_closed_loop,run_open_loop, display_stim_event, still_show_event):
        # initialize variables
        display_stim_event.clear()
        still_show_event.clear()
        run_open_loop.value = True
        run_closed_loop.value = True
        # get right grating
        if self.correct_stim_side["right"]:
            right_sf = self.settings.stimulus_correct["grating_sf"]
            right_or = self.settings.stimulus_correct["grating_ori"]
            right_ps = self.settings.stimulus_correct["phase_speed"]
            left_sf = self.settings.stimulus_wrong["grating_sf"]
            left_or = self.settings.stimulus_wrong["grating_ori"]
            left_ps = self.settings.stimulus_correct["phase_speed"]
        elif self.correct_stim_side["left"]:
            left_sf = self.settings.stimulus_correct["grating_sf"]
            left_or = self.settings.stimulus_correct["grating_ori"]
            left_ps = self.settings.stimulus_correct["phase_speed"]
            right_sf = self.settings.stimulus_wrong["grating_sf"]
            right_or = self.settings.stimulus_wrong["grating_ori"]
            right_ps = self.settings.stimulus_correct["phase_speed"]
        # generate gratings and stimuli
        grating_left = self.gen_grating(left_sf,left_or,self.settings.stim_end_pos[0])
        grating_right = self.gen_grating(right_sf,right_or,self.settings.stim_end_pos[1])
        stim = self.gen_stim()
        #-----------------------------------------------------------------------------
        # on soft code of state 1
        #-----------------------------------------------------------------------------
        # present initial stimulus
        display_stim_event.wait()
        while run_closed_loop.value:#self.run_closed_loop: 
            # dram moving gratings
            grating_left.setPhase(left_ps, '+')#advance phase by 0.05 of a cycle
            grating_right.setPhase(right_ps, '+')
            grating_left.draw()
            grating_right.draw()
            #stim.draw()
            self.win.flip()
        #-------------------------------------------------------------------------
        # on soft code of state 2
        #-------------------------------------------------------------------------
        # reset rotary encoder
        self.rotary_encoder.rotary_encoder.set_zero_position()
        self.rotary_encoder.rotary_encoder.enable_stream()
        # open loop
        print("open loop")
        pos=0
        while run_open_loop.value:
            # dram moving gratings
            grating_left.setPhase(left_ps, '+')#advance phase by 0.05 of a cycle
            grating_right.setPhase(right_ps, '+')
            grating_left.draw()
            grating_right.draw()
            # get rotary encoder change position
            stream = self.rotary_encoder.rotary_encoder.read_stream()
            if len(stream)>0:
                print((pos - stream[-1][2])*self.gain)
                change = (pos - stream[-1][2])*self.gain #self.ceil((pos - stream[-1][2])*self.gain) # if ceil -> if very fast rotation still threshold, but stimulus not therer
                pos = stream[-1][2]
                #move stimulus with mouse
                stim.pos+=(change,0)    
            stim.draw()
            self.win.flip()
        #-------------------------------------------------------------------------
        # on soft code of state 3 freez movement
        #-------------------------------------------------------------------------
        still_show_event.wait()
        print("end")
        self.win.flip()



