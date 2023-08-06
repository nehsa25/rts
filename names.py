import random

class Names:
    def generate_name(self):
        names = []
        names.append("Jake")
        names.append("God")
        names.append("Kvothe")
        name_choice = random.randint(0, len(names) -1)

        # title list
        titles = []
        titles.append("the Brave")
        titles.append("the Fool")
        titles.append("the Strong")
        title_choice = random.randint(0, len(titles) -1)

        # combine name and title
        name = f"{names[name_choice]} {titles[title_choice]}"

        return name