import configparser as cfg


def get_resource_dir():
    return "resources/"


def get_images_dir():
    return get_resource_dir() + "images/"


def get_log_directory():
    return "logs/"


def get_model_path():
    return get_resource_dir()+"model.h5"


def get_language_resource_path():
    return get_resource_dir()+"LanguageResources.properties"


def save_image(image_bytes, path):
    with open(path, "wb") as image:
        image.write(image_bytes)


def load_language_resources():
    config = cfg.ConfigParser()
    config.read(get_language_resource_path())
    return config


def update_language_resources(config):
    with open(get_language_resource_path()) as config_file:
        config_file.write(config)