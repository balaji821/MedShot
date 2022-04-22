import configparser as cfg


def get_resource_dir():
    return "resources/"


def get_test_images_dir():
    return get_resource_dir() + "test_images/"


def get_plant_images_dir():
    return get_resource_dir() + "plant_images/"


def get_info_dir():
    return get_resource_dir() + "info/"


def get_log_directory():
    return "logs/"


def get_model_path():
    return get_resource_dir()+"model.h5"


def get_language_resource_path():
    return get_resource_dir()+"LanguageResources.properties"


def get_plantlist_path():
    return get_resource_dir()+"scientific_names.txt"


def get_plantname_path():
    return get_resource_dir()+"plant_names.csv"


def get_audio_path():
    return get_resource_dir()+"audio/"


def save_image(image_bytes, path):
    with open(path, "wb") as image:
        image.write(image_bytes)


def load_language_resources():
    config = cfg.ConfigParser()
    config.read(get_language_resource_path())
    return config


def update_language_resources(config: cfg.ConfigParser):
    with open(get_language_resource_path(), 'w') as config_file:
        config.write(config_file)


def load_plant_props(path):
    config = cfg.ConfigParser()
    config.read(path)
    return config
