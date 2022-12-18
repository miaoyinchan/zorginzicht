from suggest import suggest


def main():

    # Unit test with 100% decision coverage.
    available_insurances = {
        'Fysio': [{'costs': 10,
                    'id': 4,
                    'insuranceType': None,
                    'insuranceTypeId': 2,
                    'max_coverage': 250,
                    'name': 'Fysio 1',
                    'policies': None},
                {'costs': 20,
                    'id': 5,
                    'insuranceType': None,
                    'insuranceTypeId': 2,
                    'max_coverage': 500,
                    'name': 'Fysio 2',
                    'policies': None},
                {'costs': 30,
                    'id': 6,
                    'insuranceType': None,
                    'insuranceTypeId': 2,
                    'max_coverage': 750,
                    'name': 'Fysio 3',
                    'policies': None}],
        'Tand': [{'costs': 10,
                'id': 1,
                'insuranceType': None,
                'insuranceTypeId': 1,
                'max_coverage': 250,
                'name': 'Tand 1',
                'policies': None},
                {'costs': 20,
                'id': 2,
                'insuranceType': None,
                'insuranceTypeId': 1,
                'max_coverage': 500,
                'name': 'Tand 2',
                'policies': None},
                {'costs': 30,
                'id': 3,
                'insuranceType': None,
                'insuranceTypeId': 1,
                'max_coverage': 750,
                'name': 'Tand 3',
                'policies': None}],
    }

    testcases = [
        {
            "current_insurance": "none",
            "usage": 0,
            "coverage": 0,
        }, # No suggestion.
        {
            "current_insurance": "Tand 1",
            "usage": 0,
            "coverage": 250,
        }, # Maybe you don't need Tand 1.
        {
            "current_insurance": "Tand 2",
            "usage": 0,
            "coverage": 500,
        }, # Maybe you don't need Tand 2.
        {
            "current_insurance": "Tand 3",
            "usage": 0,
            "coverage": 750,
        }, # Maybe you don't need Tand 3.
        {
            "current_insurance": "Tand 1",
            "usage": 249,
            "coverage": 250,
        }, # Please keep using Tand 1.
        {
            "current_insurance": "Tand 2",
            "usage": 499,
            "coverage": 500,
        }, # Please keep using Tand 2.
        {
            "current_insurance": "Tand 3",
            "usage": 749,
            "coverage": 750,
        }, # Please keep using Tand 3.
        {
            "current_insurance": "Tand 1",
            "usage": 251,
            "coverage": 250,
        }, # T2
        {
            "current_insurance": "Tand 2",
            "usage": 501,
            "coverage": 500,
        }, # T3
        {
            "current_insurance": "Tand 3",
            "usage": 751,
            "coverage": 750,
        }, # Please contact us for advice.
        {
            "current_insurance": "Tand 1",
            "usage": 751,
            "coverage": 250,
        }, # Please contact us for advice.
        {
            "current_insurance": "Tand 2",
            "usage": 751,
            "coverage": 500,
        }, # Please contact us for advice.
    ]

    for kwargs in testcases:
        available_insurance = available_insurances["Tand"]
        print(suggest(**kwargs, available_insurances=available_insurance))


if __name__ == '__main__':
    main()
