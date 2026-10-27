import json
with open("search_response.json", "r", encoding="utf-8") as search_response:
    search_data=json.load(search_response) # process of deserialization: where json.load reads data directly froma file and converts it into a native pytgon object
for item in search_data["items"]:
    print(item["snippet"]["title"], item["snippet"]["channelTitle"],item["id"]["videoId"]) #getting title,channelname and videoId from the items list from the search_response.json file