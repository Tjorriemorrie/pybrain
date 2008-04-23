__author__ = 'Martin Felder, felder@in.tum.de'

from pybrain.rl.tasks import EpisodicTask
from shipsteer import ShipSteeringEnvironment
from scipy import pi, dot, array

class GoNorthwardTask(EpisodicTask):

    """ The task of balancing some pole(s) on a cart """
    def __init__(self, env = None, maxsteps = 1000):
        """
        @param env: (optional) an instance of a CartPoleEnvironment (or a subclass thereof)
        @param maxsteps: maximal number of steps (default: 1000) 
        """
        if env == None:
            env = ShipSteeringEnvironment()
        EpisodicTask.__init__(self, env) 
        self.N = maxsteps
        self.t = 0
        
        # scale sensors
        #                          [h,              hdot,           v] 
        self.sensor_limits = [(-180.0,+180.0),(-180.0,+180.0), (-10.0,+40.0)]
        
        # actions:              thrust,       rudder       
        self.actor_limits = [(-1.0,+2.0), (-90.0,+90.0)]
        
    def reset(self):
        EpisodicTask.reset(self)
        self.t = 0

    def performAction(self, action):
        self.t += 1
        EpisodicTask.performAction(self, action)
                       
    def isFinished(self):
        if self.t >= self.N:
            # maximal timesteps
            return True
        return False
        
    def getReward(self):
        if abs(self.env.getHeading())<5.: 
            return self.env.getSpeed()
        else:        
            return 0
        
    def setMaxLength(self, n):
        self.N = n    
