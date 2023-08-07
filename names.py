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
        names.append("Roswaal")
        names.append("Roz")
        names.append("Maximus")
        names.append("Candie")
        names.append("Jesse")
        names.append("Ethan")
        names.append("Pinf")
        names.append("Logoc")
        name_choice = random.randint(0, len(names) -1)

        # title list
        titles = []
        titles.append("the Brave")
        titles.append("the Cowardly")
        titles.append("the Fool")
        titles.append("the Greedy")
        titles.append("the Prideful")
        titles.append("the Wise")
        titles.append("the Magnificent")
        titles.append("the Professor")
        titles.append("the Scholar")
        titles.append("the Loyal")
        titles.append("Stone")      

        title_choice = random.randint(0, len(titles) -1)

        # combine name and title
        name = f"{names[name_choice]} {titles[title_choice]}"

        return name