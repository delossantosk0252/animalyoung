import csv

# get the csv file
animals_list = 'animals_young_only.csv'

# open the csv file
with open("animals_young_only.csv", 'r',) as file:
    animals_young_collective = list(csv.reader(file, delimiter=","))
    file.close()
    # removes first entry in list (ie: the header row)
    animals_young_collective.pop(0)

    # Read the rest of the data
    for row in animals_young_collective:
        print(row)

print("Length: {}".format(len(animals_young_collective)))
