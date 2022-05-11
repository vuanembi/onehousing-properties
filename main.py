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

        buildings = iterate(client, 'buildings', projects)
        floors = iterate(client, 'floors', buildings)
        properties = iterate(client, 'properties', floors)

    return properties


def get_valuations():
    with open("properties.json") as f:
        properties = json.load(f)

    size = 5000

    properties_group = [properties[i: i + size] for i in range(0, len(properties), size)]

    for i, group in enumerate(properties_group):
        with open(f"properties/properties.{i}.json", 'w') as f:
            json.dump(group, f)

    # with get_client() as client:
    #     valuations = [
    #         get_resource(client, "apartment-valuation", property_)
    #         for property_ in tqdm(properties)
    #     ]

    #     with open("data.json", "w") as f:
    #         json.dump(valuations, f)



if __name__ == "__main__":
    get_valuations()
