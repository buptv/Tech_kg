from grest import GRest
from models import User

class UsersView(GRest):
    __model__ = {"primary": User}
    __selection_field__ = {"primary": "id"}