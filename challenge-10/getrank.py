#! -*-coding:utf-8-*-
import sys
from pymongo import MongoClient
from collections import OrderedDict 
def get_rank(user_id):
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests

    sort_dict = OrderedDict()
    sort_dict['score']=-1
    sort_dict['stime']=1
    ret =  contests.aggregate([
        {'$group':{
            '_id':'$user_id',
            'score':{'$sum':'$score'},
            'stime':{'$sum':'$submit_time'}
            }},
        {'$sort':sort_dict}
        ])
    for i,data in enumerate(ret):
        if data['_id'] == user_id:
            return (i+1,data['score'],data['stime'])

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1].isalnum():
        ret = get_rank(int(sys.argv[1]))
        print(ret)
    else:
        print('Parameter Error')
