import folium
from haversine import haversine
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="WebMap")


def main():
    data = user_input()
    year = int(data[0])
    lat = float(data[1][:-1])
    lon = float(data[2])
    nearest_coord = find_nearest_coordinates(year, lat, lon)
    generation_map(nearest_coord)

    print("Finished. Please have look at the map webmap.html")


def user_input() -> tuple:
    year = input("Please enter a year you would like to have a map for: ")
    location = input("Please enter your location (format: lat, long): ").split()

    print("Map is generating...")
    print("Please wait...")

    return year, location[0], location[1]


def find_nearest_coordinates(year: int, lat: float, long: float) -> list:
    cities = read_file()
    coordinates = []
    
    for point in cities[year]:
        location = geolocator.geocode(point[1])

        if location != None:
            coordinates.append((point[0], float(location.latitude),
                                float(location.longitude)))
        if len(coordinates) > 100:
            break

    sorted_coordinates = sorted(coordinates, key=lambda el:
                                haversine((lat, long), (el[1], el[2])))
    return sorted_coordinates[:10]


def read_file(path_to_file = 'locations.txt') -> dict:
    films_dict = {}

    with open(path_to_file, "r") as file:
        line = file.readline().strip()
        while line != "":
            year = line[line.find("(")+1:line.find("(")+5]
            if year.isdigit():
                year = int(year)

            line = line.split(",")

            if "\t" in line[0]:
                line[0] = " ".join(line[0].strip().split("\t"))
            else:
                line[0] = " ".join(line[0].strip().split("\t"))

            if not line[0].startswith('"'):
                line[0] = ('"' + line[0][:line[0].find("(")-1] + '"'
                          + line[0][line[0].find("(")-1:])

            film = line[0][:line[0][1:].find('"')+2]
            city = line[1].strip() if len(line) != 1 else line[0].split()[-1]

            if year not in films_dict:
                films_dict[year] = [(film, city)]
            else:
                films_dict[year].append((film, city))

            line = file.readline().strip()
        return films_dict


def generation_map(coordinates: list):
    webmap = folium.Map(tiles="Stamen Terrain")
    fg = folium.FeatureGroup(name="Film map")


    for film, lt, ln, in coordinates:
        fg.add_child(folium.Marker(location=[lt, ln],
                                    popup=f'Тут було знято фільм {film}',
                                    icon=folium.Icon()))
    webmap.add_child(fg)
    webmap.save('webmap.html')


if __name__ == "__main__":
    main()