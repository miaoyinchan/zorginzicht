

available_insurances = [
    {"name": "tand1", "coverage": 250, "cost": 10},
    {"name": "tand2", "coverage": 500, "cost": 20},
    {"name": "tand3", "coverage": 750, "cost": 30},
    {"name": "fysio1", "coverage": 750, "cost": 30},
    {"name": "fysio2", "coverage": 750, "cost": 30},
    {"name": "fysio3", "coverage": 750, "cost": 30},
]

# TODO: total usage of each care type & the covering of
# current insurance of that care type have to be query
# from the 2 databases

# TODO: create an endpoint
# TODO: integrate with frontend
# TODO: write test cases to guarantee 100% coverage

# TODO: also show the price of the suggested package.

def suggest_tand(usage, current_insurance):
    costs = {
        "tand1": 10,
        "tand2": 20,
        "tand3": 30,
    }

    suggestion = []
    usage_amount = [e for e in usage.values()][0]


    if current_insurance is None:
        if usage_amount == 0:
            suggestion.append("No suggestion")

    else:
        # if current_ins not NONE, it will be,
        # current_ins = {"caretype": covering}, e.g., {"tand1": 250 }
        current_covering = [e for e in current_insurance.values()][0]
        current_ins_name = [e for e in current_insurance.keys()][0]
        difference = usage_amount - current_covering

        if usage_amount == 0 and current_covering > 0:
            suggestion.append("You may not need this additional insurance.")

        if usage_amount != 0:
            if current_covering == 0:
                if usage_amount <= 250:
                    suggestion.append({"tand1": 250, "costs": costs["tand1"]})
                elif usage_amount > 250 and usage_amount <= 500:
                    suggestion.append({"tand2": 500, "costs": costs["tand2"]})
                elif usage_amount > 500 and usage_amount <= 750:
                    suggestion.append({"tand3": 750, "costs": costs["tand3"]})
                elif usage_amount > 750:
                    suggestion.append("For advice, pls contact us.")

            else:
                if difference <= 0:
                    suggestion.append("No suggestion")
                else:
                    if difference > 250 and difference <= 500:
                        suggestion.append({"tand3": 750, "costs": costs["tand3"]})
                    elif difference > 500:
                        suggestion.append("For advice, pls contact us.")
                    elif difference <= 250:
                        if current_ins_name == "tand1":
                            suggestion.append({"tand2": 500, "costs": costs["tand2"]})
                        elif current_ins_name == "tand2":
                            suggestion.append({"tand3": 750, "costs": costs["tand3"]})

    return suggestion

def suggest_fysio(usage, current_insurance):
    costs = {
        "fysio1": 10,
        "fysio2": 20,
        "fysio3": 30,
    }

    suggestion = []
    usage_amount = [e for e in usage.values()][0]


    if current_insurance is None:
        if usage_amount == 0:
            suggestion.append("No suggestion")

    else:
        # if current_ins not NONE, it will be,
        # current_ins = {"caretype": covering}, e.g., {"tand1": 250 }
        current_covering = [e for e in current_insurance.values()][0]
        current_ins_name = [e for e in current_insurance.keys()][0]
        difference = usage_amount - current_covering

        if usage_amount == 0 and current_covering > 0:
            suggestion.append("You may not need this additional insurance.")

        if usage_amount != 0:
            if current_covering == 0:
                if usage_amount <= 250:
                    suggestion.append({"fysio1": 250, "costs": costs["fysio1"]})
                elif usage_amount > 250 and usage_amount <= 500:
                    suggestion.append({"fysio2": 500, "costs": costs["fysio2"]})
                elif usage_amount > 500 and usage_amount <= 750:
                    suggestion.append({"fysio3": 750, "costs": costs["fysio3"]})
                elif usage_amount > 750:
                    suggestion.append("For advice, pls contact us.")

            else:
                if difference <= 0:
                    suggestion.append("No suggestion")
                else:
                    if difference > 250 and difference <= 500:
                        suggestion.append({"fysio3": 750, "costs": costs["fysio3"]})
                    elif difference > 500:
                        suggestion.append("For advice, pls contact us.")
                    elif difference <= 250:
                        if current_ins_name == "fysio1":
                            suggestion.append({"fysio2": 500, "costs": costs["fysio2"]})
                        elif current_ins_name == "fysio2":
                            suggestion.append({"fysio3": 750, "costs": costs["fysio3"]})

    return suggestion

def calculate_suggestion(usage, coverage, current_insurance, available_insurances):
    if not usage:
        return "nope"
    if usage <= coverage:
        return f"keep using {current_insurance}"

    for insurance in available_insurances:
        if usage <= insurance["coverage"]:
            return insurance

    return "too much"


def main():
    available_insurances = [
        {"name": "tand1", "coverage": 250, "cost": 10},
        {"name": "tand2", "coverage": 500, "cost": 20},
        {"name": "tand3", "coverage": 750, "cost": 30},
    ]

    testcases = [
        {
            "current_insurance": "tand1",
            "usage": 325,
            "coverage": 250,
        },
        {
            "current_insurance": "tand1",
            "usage": 500,
            "coverage": 250,
        },
        {
            "current_insurance": "tand1",
            "usage": 750,
            "coverage": 250,
        },
        {
            "current_insurance": "tand1",
            "usage": 0,
            "coverage": 250,
        },
        {
            "current_insurance": "none",
            "usage": 0,
            "coverage": 0,
        },
        {
            "current_insurance": "none",
            "usage": 100,
            "coverage": 0,
        },
        {
            "current_insurance": "tand1",
            "usage": 10000,
            "coverage": 250,
        },
    ]

    for kwargs in testcases:
        print(calculate_suggestion(**kwargs, available_insurances=available_insurances))

    return

    testcases_tand = [
        [{"tand": 500}, {"tand1": 250}],
        [{"tand": 0}, {"tand1": 250}],
        [{"tand": 300}, {"tand1": 250}],
        [{"tand": 700}, {"tand1": 250}],
        [{"tand": 250}, {"tand1": 250}],
        [{"tand": 0}, None],
    ]

    testcases_fysio = [
        [{"fysio": 500}, {"fysio1": 250}],
        [{"fysio": 0}, {"fysio1": 250}],
        [{"fysio": 300}, {"fysio1": 250}],
        [{"fysio": 700}, {"fysio1": 250}],
        [{"fysio": 0}, None],
    ]

    for tc in testcases_tand:
        usage = tc[0]
        current_ins = tc[1]
        print(suggest_tand(usage, current_ins))

    for tc in testcases_fysio:
        usage = tc[0]
        current_ins = tc[1]
        print(suggest_fysio(usage, current_ins))


if __name__ == '__main__':
    main()
