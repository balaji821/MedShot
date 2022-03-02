from typing import List


class Plants:
    def __init__(self):
        self.sci_name_list = ["Phyllanthus niruri",
                              "Coccinia grandis",
                              "Ocymum pilosum",
                              "Acalypha indica",
                              "Cardiospermum halicacabum",
                              "Calotropis gigantea",
                              "Andrographis paniculata",
                              "Catharanthus roseus",
                              "Laportea interrupta",
                              "Anisomeles malabarica",
                              "Argemone mexicana",
                              "Mentha arvensis",
                              "Clitoria ternatea",
                              "Physalis philadelphica",
                              "Ocimum tenuiflorum",
                              "Datura metel",
                              "Catharanthus roseus"]
        self.common_name_list = [
            "avaram",
            "arivaalmanai poondu",
            "elantha pazham",
            "keezhanelli",
            "kovakkai",
            "krishnavalli",
            "kuppaimeni",
            "mudakathan",
            "neela erukku",
            "nilavembu",
            "pattipoo",
            "thulasi",
            "perunthumpai",
            "piramaththandu",
            "puthina",
            "sangu pushpam",
            "siru thakkali",
            "peru-n-kanchori",
            "umathai",
            "valaipaacai"
        ]

    def get_plant_sci_name(self, result_arr: List):
        plant_index = list(result_arr).index(1)
        return self.sci_name_list[plant_index]

    def get_plant_common_name(self, result_arr: List):
        plant_index = list(result_arr).index(1)
        return self.common_name_list[plant_index]
