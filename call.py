from pprint import pformat
from PythonSDK.facepp import API, File
import os


def print_result(hit, result):
    print(hit)
    print('\n'.join("  " + i for i in pformat(result, width=75).split('\n')))


def printFuctionTitle(title):
    return "\n" + "-" * 60 + title + "-" * 60;


api = API()

res={}
def add(faceSet_img,path):
    faceResStr = ""
    res = api.detect(image_file=File(faceSet_img))
    faceList = res["faces"]
    for index in range(len(faceList)):
        if (index == 0):
            faceResStr = faceResStr + faceList[index]["face_token"]
        else:
            res[faceList[index]["face_token"]] = path
            faceResStr = faceResStr + "," + faceList[index]["face_token"]
    #
    api.faceset.addface(outer_id='faceplusplus', face_tokens=faceResStr)


api.faceset.delete(outer_id='faceplusplus', check_empty=0)
ret = api.faceset.create(outer_id='faceplusplus')

for root, dirs, files in os.walk("dataset"):
    for f in files:
        add(os.path.join(root, f), f)

for root, dirs, files in os.walk("unknown"):
    for f in files:
        search_result = api.search(image_file=File(os.path.join(root, f)), outer_id='faceplusplus')
        print(res[search_result['results']['face_token']])
