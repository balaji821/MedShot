import file_utils as fu
import pandas
import os


class Plants:

    obj = None

    @staticmethod
    def get_instance():
        if Plants.obj is None:
            Plants.obj = Plants()
        return Plants.obj

    def __init__(self):
        self.plant_info = None
        with open(fu.get_plantlist_path(), 'r') as f:
            self.plant_list = f.read().split(",\n")
        self.plant_names = pandas.read_csv(fu.get_plantname_path(), index_col="sci")
        self.load_plant_info()

    def load_plant_info(self):
        self.plant_info = {}
        sci_names = list(self.plant_names.index)
        info = fu.get_info_dir()
        for sci in sci_names:
            print(sci)
            if not os.path.exists(info+sci+"/medicinal_uses.properties"):
                continue
            plant_props = dict(fu.load_plant_props(info+sci+"/medicinal_uses.properties").items("MEDICINAL-USES"))
            plant_uses = {}
            uses = []
            for key in plant_props:
                uses.append(key)
                with open("../"+plant_props[key], encoding="utf-8") as f:
                    plant_uses[key] = f.read()
            plant_uses["uses"] = uses
            self.plant_info[sci] = plant_uses
        print(self.plant_info)

    def get_lang(self, lang):
        if lang not in self.plant_names.columns:
            return 'en'
        return lang

    def get_plant_sci_name_with_common_name(self, common_name, lang):
        plant_list = self.plant_names[lang]
        return plant_list[plant_list == common_name].index[0]

    def get_plant_sci_name(self, result_arr):
        result_arr = list(result_arr)
        plant_index = result_arr.index(max(result_arr))
        print(max(result_arr))
        if max(result_arr) < 0.7:
            return "None"
        return self.plant_list[plant_index]

    def get_plant_common_name(self, sci_name, lang='en'):
        return self.plant_names[lang][sci_name]

    def get_plant_list(self, lang):
        return list(self.plant_names[lang])

    def get_info(self, common_name, lang, use_case="info"):
        sci_name = self.get_plant_sci_name_with_common_name(common_name, lang)
        return self.plant_info[sci_name][use_case]
