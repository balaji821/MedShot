import logging
import src.plant_utils as pu

logger = logging.getLogger("medshot")


class Disease:

    obj = None

    @staticmethod
    def get_instance():
        if Disease.obj is None:
            Disease.obj = Disease()
        return Disease.obj

    def __init__(self):
        plant = self.plant = pu.Plants.get_instance()
        disease_to_plant_map = self.disease_to_plant_map = {}

        sci_names = list(plant.plant_names.index)
        plant_info = plant.plant_info

        for sci in sci_names:
            diseases = plant_info[sci]["uses"]
            for disease in diseases:
                if disease == "info":
                    continue
                if disease in disease_to_plant_map:
                    disease_to_plant_map[disease].append(sci)
                else:
                    disease_to_plant_map[disease] = [sci]



