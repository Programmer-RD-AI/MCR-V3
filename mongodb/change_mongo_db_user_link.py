import json

with open(
    "/home/ranuga/Programming/Projects/Python/Flask/Doing/My-Class-Room-V2/private/mongodb-client.json"
) as info:
    info_ = json.load(info)
    link = input(" - Link \n - ")
    ok_or_not = input(" - Is it correct ? (Y/N) \n - ")
    while ok_or_not.upper() == "N":
        link = input(" - Link \n - ")
        ok_or_not = input(" - Is it correct ? (Y/N) \n - ")
    info_["MongoDB-Client-Url"] = link
    with open(
        "/home/ranuga/Programming/Projects/Python/Flask/Doing/My-Class-Room-V2/private/mongodb-client.json",
        "w",
    ) as _info:
        json.dump(info_, _info)
