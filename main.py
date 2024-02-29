import csv
from dataclasses import dataclass

from bs4 import BeautifulSoup

from crawler import crawl

crawl()

print("Parsing source HTML...")

with open('index.html', 'r') as f:
    content = f.read()

soup = BeautifulSoup(content, features="html.parser")


@dataclass
class FlightInfo:
    departure_time: str
    arrival_time: str
    price: int
    cabin_class: str
    operator: str


# Find all divs with the class of nrc6
divs = soup.find_all('div', class_='nrc6')

dataset = []
for div in divs:
    price = div.find_all('div', class_='f8F1')[0].get_text(strip=True)
    price = price.split('\xa0')[1]
    price = int("".join(price.split(',')))

    cabin_class = div.find_all('div',
                               class_='aC3z-name')[0].get_text(strip=True)

    operator = div.find_all(
        'div', class_='J0g6-operator-text')[0].get_text(strip=True)

    timings = div.find_all(
        'div', class_='vmXl-mod-variant-large')[0].get_text(strip=True)

    departure_time = timings.split('–')[0]
    arrival_time = timings.split('–')[1]

    flight_info = FlightInfo(departure_time=departure_time,
                             arrival_time=arrival_time,
                             price=price,
                             cabin_class=cabin_class,
                             operator=operator)

    dataset.append(flight_info)


def dump_to_csv(dataset):
    print("Dumping to csv...")
    with open('flight_info.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "DEPARTURE_TIME", "ARRIVAL_TIME", "PRICE", "CABIN_CLASS",
            "OPERATOR"
        ])
        for flight in dataset:
            writer.writerow([
                flight.departure_time, flight.arrival_time, flight.price,
                flight.cabin_class, flight.operator
            ])


dump_to_csv(dataset)
print("CSV dataset generated")
