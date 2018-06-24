from flask import Flask, jsonify
from flask_classful import route
import markupsafe
import neomodel
from neomodel import (StructuredNode, StringProperty, IntegerProperty,
                      UniqueIdProperty, RelationshipFrom, RelationshipTo,
                      StructuredRel)
from webargs import fields
from grest import GRest, utils, models, global_config
import logging
import logging.handlers
import os


class PetInfo(StructuredRel, models.Relation):
    """Pet Information Model (for relationship)"""
    adopted_since = IntegerProperty()


class Pet(StructuredNode, models.Node):
    """Pet model"""
    pet_id = UniqueIdProperty()
    name = StringProperty()
    owner = RelationshipFrom("Person", "HAS_PET")


class Person(StructuredNode, models.Node):
    """Person model"""
    __validation_rules__ = {
        "first_name": fields.Str(),
        "last_name": fields.Str(),
        "phone_number": fields.Str(required=True)
    }

    __filtered_fields__ = ["secret_field"]

    uid = UniqueIdProperty()
    first_name = StringProperty()
    last_name = StringProperty()
    phone_number = StringProperty(unique_index=True, required=True)

    secret_field = StringProperty(default="secret", required=False)

    pets = RelationshipTo(Pet, "HAS_PET", model=PetInfo)


class PersonsView(GRest):
    """Person's View (/persons)"""
    __model__ = {"primary": Person,
                 "secondary": {
                     "pets": Pet
                 }}
    __selection_field__ = {"primary": "uid",
                           "secondary": {
                               "pets": "pet_id"
                           }}


class PetsView(GRest):
    """Pet's View (/pets)"""
    __model__ = {"primary": Pet}
    __selection_field__ = {"primary": "pet_id"}

    @route("/<pet_id>/owner", methods=["GET"])
    def owner(self, pet_id):
        try:
            pet = Pet.nodes.get(**{self.__selection_field__.get("primary"):
                                   str(markupsafe.escape(pet_id))})

            if (pet):
                current_owner = pet.owner.get()
                if (current_owner):
                    return jsonify(owner=current_owner.to_dict()), 200
                else:
                    return jsonify(errors=["Selected pet has not been adopted yet!"]), 404
            else:
                return jsonify(errors=["Selected pet does not exists!"]), 404
        except:
            return jsonify(errors=["An error occurred while processing your request."]), 500


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return "Hello World"

    neomodel.config.DATABASE_URL = global_config.DB_URL
    neomodel.config.AUTO_INSTALL_LABELS = True
    neomodel.config.FORCE_TIMEZONE = True  # default False

    if (global_config.LOG_ENABLED):
        logging.basicConfig(filename=os.path.abspath(os.path.join(
            global_config.LOG_LOCATION, global_config.LOG_FILENAME)), format=global_config.LOG_FORMAT)
        app.ext_logger = logging.getLogger()
        app.ext_logger.setLevel(global_config.LOG_LEVEL)
        handler = logging.handlers.RotatingFileHandler(
            os.path.abspath(os.path.join(
                global_config.LOG_LOCATION, global_config.LOG_FILENAME)),
            maxBytes=global_config.LOG_MAX_BYTES,
            backupCount=global_config.LOG_BACKUP_COUNT)
        app.ext_logger.addHandler(handler)
    else:
        app.ext_logger = app.logger

    PersonsView.register(app, route_base="/persons", trailing_slash=False)
    PetsView.register(app, route_base="/pets", trailing_slash=False)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run('0.0.0.0',port=5001,debug=True, threaded=True)