import argparse
import json

from tqdm import tqdm

from repo import get_client, get_resource


def iterate(client, resource, inputs):
    data = [
        i
        for j in [
            get_resource(client, resource, input_["id"]) for input_ in tqdm(inputs)
        ]
        for i in j
    ]
    with open(f"{resource}.json", "w") as f:
        json.dump(data, f)

    return data


def get_properties():
    with get_client() as client:
        projects = get_resource(client, "projects", "")

        buildings = iterate(client, "buildings", projects)
        floors = iterate(client, "floors", buildings)
        properties = iterate(client, "properties", floors)

    return properties


def get_valuations(file_: int):
    with open(f"properties/properties.{file_}.json", "r") as f:
        properties = json.load(f)

    with get_client() as client:
        valuations = [
            get_resource(client, "apartment-valuation", property_)
            for property_ in tqdm(properties)
        ]

        with open(f"valuations/valuations.{file_}.json", "w") as f:
            json.dump(valuations, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("file", type=int)

    args = parser.parse_args()

    get_valuations(args.file)
