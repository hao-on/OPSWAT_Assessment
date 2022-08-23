import os
import sys

from function import API
from hash import hash_file


def scan_file(api_key, filename):
    """
    This function performs all the necessary functions
        :param api_key: the API key
        :param filename: filename can be either filename relative to directory or a whole file path
        :return: display the scanning result
    """

    # get the real path of the file
    filepath = os.path.realpath(filename)

    # create an API object with an initialized API key
    api = API(api_key)

    # validate the API key
    if not api.valid_key():
        return

    # 1: calculate the Hash value using SHA-1 algorithm
    hash_value = hash_file(filepath=filepath)

    # 2: perform a hash lookup
    result = api.lookup(hash=hash_value)

    # 3: if results are found --> # 6
    # 4: if results are not found
    if len(result.json().keys()) <= 1:  # results with a single key --> not found
        dataId = api.upload_file(filepath)  # upload and retrieve the dataId
        result = api.get_results(dataId=dataId)

        # While scan_details are empty then call get result by dataId until scan details are ready
        while len(result.json()["scan_results"]["scan_details"].keys()) == 0:
            # 5: repeatedly pull result with dataId
            result = api.get_results(dataId=dataId)

    # 6: Display results
    API.display(result, filename)


def main():
    """
        Command line: python main.py 'api: <API_KEY>' 'file: <FILENAME or FILEPATH>'
    """
    if len(sys.argv) < 3:
        print("Invalid number of arguments")
        return
    else:
        api_key = sys.argv[1].partition('api: ')[2]
        filename = sys.argv[2].partition('file: ')[2]

        # check if file exists
        if os.path.exists(filename):
            try:
                scan_file(api_key, filename)
            except Exception as e:
                print(e.message, end="\n")
        else:
            print("File does not exists")


if __name__ == '__main__':
    main()
