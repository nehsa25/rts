import random

class Names:
    def generate_name(self):
        names = []
        names.append("Ley")
        names.append("Sirius")
        names.append("Capella")
        names.append("Regulus")
        names.append("Stride")
        names.append("Betelgeuse")
        names.append("Holo")
        name_choice = random.randint(0, len(names) -1)

        # title list
        titles = []
        titles.append("the Brave")
        titles.append("the Cowardly")
        titles.append("the Fool")
        titles.append("the greedy")
        titles.append("the Prideful")
        titles.append("the Wise")
        title_choice = random.randint(0, len(titles) -1)

        # combine name and title
        name = f"{names[name_choice]} {titles[title_choice]}"

        return name