import itchat
import json
# itchat.login()
# friends = itchat.get_friends(update=True)[0:]
# json.dump(friends,open("wetchat",'w'),indent=4,ensure_ascii=False)
friends = json.load(open("wetchat",'r'))
print(len(friends))
female = 0
male = 0
location = {}
for friend in friends:
    if friend["Sex"] == 2:
        female += 1
    elif friend["Sex"] == 1:
        male += 1

    if friend["Province"] is "":
        print(friend["NickName"])
    if friend["Province"] in location:
        location[friend["Province"]] += 1
    else:
        location[friend["Province"]] = 1

print("female:" + str(female))
print("male:"+str(male))
print(json.dumps(location,indent=4,ensure_ascii=False))
