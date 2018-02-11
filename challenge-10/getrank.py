#! -*-coding:utf-8-*-
import sys
from pymongo import MongoClient

def get_rank(user_id):
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests
    uid = 'user_id'
    cid = 'challenge_id'
    score = 'score'
    stime = 'submit_time'

    user_list ={}
    for data in contests.find():
        if user_list.get(data[uid]) is None:
            user_list[data[uid]] = [data[score],data[stime]]
        else:
            user_list[data[uid]][0]+=data[score]
            user_list[data[uid]][1]+=data[stime]

    ret = sorted(user_list.items(),reverse=True,key=lambda x : (x[1][0],-x[1][1]))
    

    for i in ret :
        if i[0] == user_id:
            return (ret.index(i)+1,i[1][0],i[1][1])
    return 'NOTFOUND'

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1].isalnum():
        ret = get_rank(int(sys.argv[1]))
        print(ret)
    else:
        print('Parameter Error')

