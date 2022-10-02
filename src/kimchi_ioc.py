from src.kimchi_io import print_line
from src.kimchi_object.environment import SelfLikeObjEnvironment, Environment
from src.kimchi_object.integer import IntegerBuilder


class IOC():
    def __init__(self, self_like=False):
        self.set_self_like(self_like)
        self.IntegerBuilder = IntegerBuilder(False)

    def set_self_like(self, self_like):
        self.self_like = self_like

    def print_config(self):
        print_line('[Kimchi Config]: self_like: ' + str(self.self_like))

    def create_env(self, outer=None):
        return SelfLikeObjEnvironment(outer)
        # if self.self_like:
        #     return SelfLikeObjEnvironment(outer)
        # else:
        #     return Environment(outer)
    