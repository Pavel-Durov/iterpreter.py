from src.kimchi_object.environment import SelfLikeObjEnvironment, Environment

SELF_LIKE_ENV = True

def createEnv(outer):
    if SELF_LIKE_ENV:
        return SelfLikeObjEnvironment(outer)
    else:
        return Environment(outer)
