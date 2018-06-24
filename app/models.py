from neomodel import (StructuredNode, UniqueIdProperty, StringProperty,IntegerProperty, BooleanProperty)
from grest import models

class User(StructuredNode, models.Node):
    id = UniqueIdProperty()
    father = StringProperty()
    level = IntegerProperty()
    name = StringProperty()
    is_enabled = BooleanProperty(default=False)