import requests


class API:
    """ API class connects to the OPSWAT's Metadefender Cloud API v4 to perform the following methods """
    #API_KEY = "971cb89b59412aadc278c23f956cfe6b"
    #headers = {}

    def __init__(self, api_key):
        """
        :param api_key: the API key
        """
        self.API_KEY = api_key
        self.headers = {
            "apikey": api_key
        }

    def valid_key(self):
        """
        Validate the given API key
            :rtype: bool
            :return: False if there is an error in the response
        """
        response = requests.request("GET", "https://api.metadefender.com/v4/apikey/", headers=self.headers)
        response = response.json()
        if "error" in response:
            print("error: " + str(response["error"]["messages"]))
            return False
        else:
            return True

    def lookup(self, hash):
        """
        Retrieve scan reports using a data hash
            :param hash: the hash value of a given file
            :return: response
        """
        url = "https://api.metadefender.com/v4/hash/" + hash
        response = requests.request("GET", url, headers=self.headers)
        return response

    def upload_file(self, filepath):
        """
        Upload a file and get the data_id
            :param filepath: the real path of a file
            :rtype: string
            :return: data_id
        """
        byteFile = ""
        # open file for reading in binary mode
        with open(filepath, 'rb') as file:
            # loop till the end of the file
            chunk = 0
            while chunk != b'':
                # read only 1024 bytes at a time
                chunk = file.read(1024)
                byteFile += chunk

        files = {'file': byteFile}
        url = "https://api.metadefender.com/v4/file"
        response = requests.request("POST", url, headers=self.headers, data=files)
        return response.json()["data_id"]

    def get_results(self, dataId):
        """
        Retrieve the file using data_id
            :param dataId: the data_id of a file
            :return: response
        """
        url = "https://api.metadefender.com/v4/file" + dataId
        response = requests.request("GET", url, headers=self.headers)
        return response

    @staticmethod
    def display(response, filename):
        """
        Display results in the given format
            :param response: the response of the request
            :param filename: filename can be either filename relative to directory or a whole file path
        """
        scan_result = response.json()["scan_results"]
        scan_details = scan_result["scan_details"]

        print("filename: " + filename, end="\n")
        status = "Clean" if (scan_result["scan_all_result_a"] == "") or (
                scan_result["scan_all_result_a"] == "No Threat Detected") else scan_result["scan_all_result_a"]
        print("overall status: " + status, end="\n")

        for engine in scan_details:
            print("engine : " + engine, end="\n")
            threat = "Clean" if scan_details[engine]["threat_found"] == "" else scan_details[engine]["threat_found"]
            print("threat_found: " + threat, end="\n")
            print("scan_result: " + str(scan_details[engine]["scan_result_i"]), end="\n")
            print("def_time: " + scan_details[engine]["def_time"], end="\n")
