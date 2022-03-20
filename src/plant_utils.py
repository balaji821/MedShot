import file_utils as fu
import pandas
# import model_utils as mu
# import os
# import shutil


class Plants:
    def __init__(self):
        with open(fu.get_plantlist_path(), 'r') as f:
            self.plant_list = f.read().split(",\n")
        self.plant_names = pandas.read_csv(fu.get_plantname_path(), index_col="sci")

    def get_plant_sci_name_with_common_name(self, common_name):
        return list(self.plant_names['ta']).index(common_name)

    def get_plant_sci_name(self, result_arr):
        result_arr = list(result_arr)
        plant_index = result_arr.index(max(result_arr))
        return self.plant_list[plant_index]

    def get_plant_common_name(self, sci_name, lang='ta'):
        return self.plant_names[lang][sci_name]


# p = Plants()
# mu.load_model()
# dataset = "E:/Files/sem8/Dataset/plantdisease"
# target_dir = "E:/Files/sem8/Dataset/plantdisease/test"
# for plant in os.listdir(dataset):
#     # print(plant)
#     plant_dir = dataset+"/"+plant
#     # print(plant_dir)
#     for image in os.listdir(plant_dir):
#         # print(image)
#         f = plant_dir+"/"+image
#         res = mu.make_prediction(f)
#         pred_sci_name = p.get_plant_sci_name(res[0])
#         predicted_name = p.get_plant_common_name(pred_sci_name)
#         original_name = plant
#         print(predicted_name, original_name)
#         if predicted_name.lower() == original_name.lower():
#             shutil.copyfile()
