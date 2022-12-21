from pprint import pprint

import requests


# CARE_TYPE_TO_INSURANCE_TYPE = {
#     "tandarts": "Tand",
#     "fysiotherapie": "Fysio",
# }


# def get_sum_per_caretype_from_api(customer_id):
#     response = requests.get(f"https://pythonbk.azurewebsites.net/api/sum_per_caretype/{customer_id}")
#     if response.status_code != 200:
#         raise ValueError(response.text)

#     data = response.json().get("results", [])

#     results = {}

#     for row in data:
#         key = CARE_TYPE_TO_INSURANCE_TYPE[row["caretype"]]
#         row["total"] = float(row["total"])
#         results[key] = row

#     return results


def get_additional_insurances_api():
    response =  requests.get("https://zi-webapp.azurewebsites.net/api/InsuranceTypes")
    if response.status_code != 200:
        raise ValueError(response.text)
    insurance_types = {i["id"]: i for i in response.json()}
    # print(insurance_types)

    response =  requests.get("https://zi-webapp.azurewebsites.net/api/AdditonalInsurrances")
    if response.status_code != 200:
        raise ValueError(response.text)

    additional_insurances = response.json()
    additional_insurances_by_type = {}
    for i in additional_insurances:
        itype = insurance_types[i["insuranceTypeId"]]["name"]
        if itype not in additional_insurances_by_type:
            additional_insurances_by_type[itype] = []
        additional_insurances_by_type[itype].append(i)

    return additional_insurances_by_type


def get_insurance_coverage_from_api(customer_id):
    response =  requests.get(f"https://zi-webapp.azurewebsites.net/api/Customers/{customer_id}")
    if response.status_code != 200:
        raise ValueError(response.text)

    data = response.json()
    results = {}

    for policy in data.get('policies', []):
        for insurance in policy.get('additional_insurances', []):
            results[insurance["insuranceType"]["name"]] = {
                "name": insurance["name"],
                "max_coverage": insurance["max_coverage"],
            }

    return results


def suggest(usage, coverage, current_insurance, available_insurances):
    if not usage and not coverage:
        return "Geen suggestie."

    if not usage and coverage:
        return f"Misschien heeft u {current_insurance} niet nodig."

    if usage <= coverage:
        return f"U kunt het beste {current_insurance} blijven gebruiken."

    for insurance in available_insurances:
        if usage <= insurance["max_coverage"]:
            return {
                "additional_insurance": insurance.get('name'),
                "coverage": insurance.get('max_coverage'),
                "price": insurance.get('costs'),
            }

    return f"Neem a.u.b. contact op over de suggestie van {current_insurance}."


def create_suggestion(customer_id, usages):
    available_insurances = get_additional_insurances_api()
    # usages = get_sum_per_caretype_from_api(customer_id)
    coverages = get_insurance_coverage_from_api(customer_id)

    suggestions = []

    for key, usage in usages.items():
        insurances = available_insurances.get(key)

        coverage = coverages.get(key)
        if not coverage:
            coverage = {'max_coverage': 0, 'name': 'none'}

        suggestions.append(suggest(
            usage["total"],
            coverage["max_coverage"],
            coverage["name"],
            insurances,
        ))

    return suggestions


def main():

    cid = 1
    # pprint(get_sum_per_caretype_from_api(cid))
    pprint(get_additional_insurances_api())
    pprint(get_insurance_coverage_from_api(cid))
    print('---------')
    pprint(create_suggestion(cid))


if __name__ == '__main__':
    main()
