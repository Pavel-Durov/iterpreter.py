from src.kimchi_object.environment import SelfLikeObjEnvironment, Environment
from src.kimchi_io import print_line


class IOC():
    def __init__(self):
        self.self_like = False
        
    def set_self_like(self, self_like):
        print_line('[Kimchi Config]: self_like: ' + str(self_like))
        self.self_like = self_like
    
    def create_env(self, outer=None):
        if self.self_like:
            return SelfLikeObjEnvironment(outer)
        else:
            return Environment(outer)

