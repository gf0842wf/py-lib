# -*- coding: utf-8 -*-

import cPickle as pickle


class M2M(object):
    """多对多关系对象
    : 例如存放好友关系结构: {userid1:{"public":set([userid2, userid3]), "private":set([userid4, userid5])}, ...}, 可以存放多对多关系数据,很明显,数据冗余性较大
    userid1的public好友有[userid2, userid3], userid1的私有好友有[userid4, userid5]
    """

    def __init__(self, m2m={}):
        self.m2m = m2m
    
    def add(self, obj_id, key, value):
        self.m2m.setdefault(obj_id, {})
        self.m2m[obj_id].setdefault(key, set())
        self.m2m[obj_id][key].add(value)
            
    def update(self, obj_id, key, s):
        self.m2m.setdefault(obj_id, {})
        self.m2m[obj_id].setdefault(key, set())
        self.m2m[obj_id][key].update(s)
            

    def remove(self, obj_id, key, value):
        try:
            self.m2m[obj_id][key].remove(value)
            return True
        except KeyError:
            return False

    def remove_set(self, obj_id, key):
        """删除obj_id->key下的所有值"""
        try:
            self.m2m[obj_id][key] = set()
            return True
        except KeyError:
            return False
                
    def isInKey(self, obj_id, key, value):
        try:
            return value in self.m2m[obj_id][key]
        except KeyError:
            return None
                
    def isInAny(self, obj_id, value):
        try:
            o2m = self.m2m[obj_id]
            ks = [k for k, v in o2m.iteritem() if value in v]
            return ks if ks else False
        except KeyError:
            return None

    def dumps(self):
        return pickle.dumps(self.m2m)

    def loads(self, s):
        self.m2m = pickle.loads(s)


if __name__ == "__main__":
    mm = M2M()
    mm.add(1001, "public", 1002)
    mm.update(1001, "private", [1003, 1004, 1005])
    print mm.m2m
    print mm.remove(1001, "public", 1002)


__all__ = ["M2M"]
