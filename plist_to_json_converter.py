#Author: matant
#FileName: plist_to_json_converter
#Date: 28:03:2017
import argparse
import base64
import collections
import datetime
import os
import json
import subprocess
import biplist


def sanitize(obj):
    """Sanitize loaded plist object to a JSON-serializable one.
    Convert datetime.datetime (<date> tag) to an ISO 8601-formatted
    string, and bytes to base64 representation.
    """
    if isinstance(obj, bytes):
        return base64.b64encode(obj).decode('utf-8')
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, list):
        return [sanitize(elem) for elem in obj]
    elif isinstance(obj, dict):
        return collections.OrderedDict((key, sanitize(val)) for key, val in obj.items())
    else:
        return obj
def PlistToJson(fileName):
    """
    Convert Plist file to json by converting the binary plist data to XML and then to pretty json
    :param fileName: full path to file
    :return:
    """
    res = subprocess.check_output(['plistutil','-i',fileName])
    plist_data = biplist.readPlistFromString(res)
    converted_string = json.dumps(plist_data, sort_keys=True, indent=4)
    with open(os.path.basename(fileName).split(".")[0]+".json", 'a') as my_file:
        my_file.write(converted_string)


def argsPars():
    parser = argparse.ArgumentParser(
        description='Convert Plist file to json')
    parser.add_argument('--f', type=str, help='Path to file', metavar='',
                        required=True)
    args = parser.parse_args()
    return args

def main():
    args = argsPars()
    if args.f:
        PlistToJson(args.f)


if __name__ == '__main__':
    main()
