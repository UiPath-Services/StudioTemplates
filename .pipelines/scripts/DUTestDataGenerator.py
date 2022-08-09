import yaml, json

data = yaml.safe_load((open("DocumentUnderstandingTestData.yaml", 'r')))

config_json = {"dataVariationFileInfo": []}

i = 0
"""
Nu merge asa, trebuie sa vad dimensiunea cheilor si pe baza la aia sa imi dimensionez dictionarul dinamic. 
"""
config_json["dataVariationFileInfo"] = dict.fromkeys(data["TestCaseDataGeneration"])
# for testcase in data["TestCaseDataGeneration"]:
#     config_json["dataVariationFileInfo"][i].update({"filePath": testcase + ".json"})
#     config_json["dataVariationFileInfo"][i].
#     config_json["dataVariationFileInfo"][i].update({"dataVariationType": "File"})
#     i += 1

    # print(testcase)
# print(data)