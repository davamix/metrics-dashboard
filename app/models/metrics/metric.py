# class Metric():
#     def __init__(self):
#         self.values = {}
#         self.merged_with = []

#     def add(self, name, value):
#         if name in self.values:
#             self.values[name].append(value)
#         else:
#             self.values[name] = []
#             self.values[name].append(value)

#     def get(self, name):
#         if name in self.values:
#             return self.values[name]

#     def add_merge(self, name, merge_with):
#         self.values[name]


class Metric():
    def __init__(self, metric_name):
        self.name = metric_name
        self.__values = []
        self.__merged_with = []

    # def add(self, name, value):
    #     if name in self.values:
    #         self.values[name].append(value)
    #     else:
    #         self.values[name] = []
    #         self.values[name].append(value)
    def add_value(self, value):
        self.__values.append(value)

    def get_values(self):
        return self.__values
    
    def merge_with(self, metric_name):
        self.__merged_with.append(metric_name)

    def get_merges(self):
        return self.__merged_with


