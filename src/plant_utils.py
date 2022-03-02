import file_utils as fu
import pandas


class Plants:
    def __init__(self):
        with open(fu.get_plantlist_path(), 'r') as f:
            self.plant_list = f.read().split(",\n")
        self.plant_names = pandas.read_csv(fu.get_plantname_path(), index_col="sci")

    def get_plant_sci_name(self, result_arr):
        plant_index = list(result_arr).index(1)
        return self.plant_list[plant_index]

    def get_plant_common_name(self, sci_name, lang='ta'):
        return self.plant_names[lang][sci_name]

