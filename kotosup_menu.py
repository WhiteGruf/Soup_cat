import pandas

class Food():
    def __init__(self,sheet:str) -> None:

        self.sheet = sheet
        a = pandas.read_excel("Меню.xlsx",sheet_name=sheet, index_col = False)

        self.name = a["Название"]
        self.weight = a["Вес"]
        self.price = a["Цена"]
        self.compound = a["Описание"]

    def get_sections(self) -> list:
        sections = []
        for i in range(len(self.name)):
            section = []
            section.append(self.name[i])
            section.append(self.weight[i])
            section.append(self.price[i])
            section.append(self.compound[i])
            sections.append(section)
        return sections
    
    def get_food(self, choice):
        for i in self.get_sections():
            #print(i, choice)
            if choice in i[0]:
                if "nan"== str(i[-1]):
                    i.remove(i[-1])

                return i

    

# print(Food("Горячие напитки").get_food("Американо"))