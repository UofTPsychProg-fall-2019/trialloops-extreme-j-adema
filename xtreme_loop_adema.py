#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a trial loop Step 2
Use this template to turn Step 1 into a loop
@author: katherineduncan
"""
#%% Required set up
# this imports everything you might need and opens a full screen window
# when you are developing your script you might want to make a smaller window
# so that you can still see your console
import numpy as np
import pandas as pd
import os, sys
from psychopy import visual, core, event, gui, logging
from psychopy.hardware import keyboard

#gui
theGui = gui.Dlg()
theGui.addText('Welcome :) The stimulus will be shown and you will respond, then you will get feedback.')
theGui.show()

# open a white full screen window
win = visual.Window(fullscr=True, allowGUI=False, color='white', unit='height')
win.recordFrameIntervals = True
win.refreshThreshold = 1/60 + 0.004
logging.console.setLevel(logging.WARNING)
event.globalKeys.add(key='q',func=core.quit)

# make a list or a pd.DataFrame that contains trial-specific info (stimulus, etc)
# e.g. stim = ['1.jpg','2.jpg','3.jpg']
trialInfo = pd.read_csv('pics.csv')
trialInfo = trialInfo.sample(frac=1)
trialInfo = trialInfo.reset_index()
nTrials = len(trialInfo)

#logging
out = pd.DataFrame(columns=['trial','response','rt','acc'])
logFile = 'data/log.csv'
outputFileName = logFile
out.to_csv(outputFileName,index=False)

# make your loop
#clocks
expClock = core.Clock()
trialClock = core.Clock()
stimClock = core.Clock()
respClock = core.Clock()
fbClock = core.Clock()
#empty lists
rt=[]
alright=[]
#loop
for thisTrial in np.arange(0,nTrials):
    stimDur = 1
    respDur = 0.2 #these timings seemed to work best for the trials
    thePic = visual.ImageStim(win, image=trialInfo.loc[thisTrial,'img'],pos=(0,0),units='pix',size=(800,600))
    theText = visual.TextStim(win,color='white',text='Z or M?',
        alignHoriz='center',pos=(0,-0.5))
    thePic.draw()
    theText.draw()
    win.flip()
    event.clearEvents()
    stimClock.reset()
    respClock.reset()
    keys = []
    while len(keys)==0 and respClock.getTime()<respDur:
        if stimClock.getTime()<stimDur:
            thePic.draw()
            theText.draw()
            win.flip()
        else:
            win.flip()
    keys = event.waitKeys(keyList=['z','m'],timeStamped=respClock)

    alrightText = visual.TextStim(win, text='alright',color='black')
    okayText = visual.TextStim(win, text='okay',color='black')
    if keys[0][0]=='z':
        alrightText.draw()
        win.flip()
        core.wait(2.0) #required to show the feedback at all
        alright.append(0)
        out.loc[thisTrial,'acc']=1 #'acc' in outfile saved as
    elif keys[0][0]=='m':
        okayText.draw()
        win.flip()
        core.wait(2.0)
        alright.append(0)
        out.loc[thisTrial,'acc']=0 #'acc' in outfile saved as
    win.flip()

#what info is recorded for each trial?
    out.loc[thisTrial,'trial'] = thisTrial
    out.loc[thisTrial,'response'] = keys[0][0]
    out.loc[thisTrial,'rt'] = keys[0][1]
    rt.append(keys[0][1])
    out.loc[[thisTrial]].to_csv(logFile,mode='a',header=False,index=False)

win.flip()
core.wait(1)

win.close()
#put summaries here to come up after 'warnings'
print('your accuracy for each trial:', alright)
print('your RTs for each trial:',rt)
print('See log.csv for more specific info')
core.quit()