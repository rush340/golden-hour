import schema
import yaml
from yaml import CLoader as Loader

from golden_hour import tweet, location


GOLDENHOUR_CONFIGURATION_SCHEMA = schema.Schema({
    'location': location.LOCATION_CONFIG_SCHEMA,
    schema.Optional('twitter'): tweet.TWITTER_CONFIG_SCHEMA,
    schema.Optional('darksky_key'): str,
})


def load_configuration(config_file_path):
    with open(config_file_path) as config_file:
        config = yaml.load_all(config_file.read(), Loader=Loader)

    return GOLDENHOUR_CONFIGURATION_SCHEMA.validate(config)
