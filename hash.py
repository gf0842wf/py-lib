# -*- coding: utf-8 -*-
        
        
class Hash(object):
    """多对多关系对象(many to many)
    : 例如存放好友关系结构: {userid1:{"public":set([userid2, userid3]), "private":set([userid4, userid5])}, ...}, 可以存放多对多关系数据,很明显,数据冗余性较大
    userid1的public好友有[userid2, userid3], userid1的私有好友有[userid4, userid5]
    """
    
    def __init__(self, m2m={}):
        self.m2m = m2m
        
    def hset(self, key, field, values):
        """hash set
        >>> users.hset(1001, "public", 1002)
        >>> users.hset(1001, "public", [1002, 1003])
        """
        if isinstance(values, (list, set, tuple)):
            self.m2m.setdefault(key, {})
            self.m2m[key].setdefault(field, set())
            self.m2m[key][field].update(values)
        else:
            self.m2m.setdefault(key, {})
            self.m2m[key].setdefault(field, set())
            self.m2m[key][field].add(values)
    
    def hmset(self, key, fv):
        """hash muti set
        >>> users.hmset(1001, {"public":[1002,1003], "private":[1004,1005]})
        >>> users.hmset(1001, {"public":1002, "private":1004})
        """
        self.m2m.setdefault(key, {})
        for f, v in fv.iteritems():
            if isinstance(v, (list, set, tuple)):
                self.m2m[key].setdefault(f, set())
                self.m2m[key][f].update(v)
            else:
                self.m2m[key].setdefault(f, set())
                self.m2m[key][f].add(v)
                
    def hget(self, key, field):
        """hash get
        >>> users.hget(1001, "public")
        """
        try:
            return self.m2m[key][field]
        except KeyError:
            return None
        
    def hmget(self, key, fields):
        """hash muti get
        >>> user.hmget(1001, ("public", "private"))
        """
        self.m2m.setdefault(key, {})
        return [self.m2m[key].get(f, None) for f in fields]

    def remove(self, key, field, value):
        try:
            self.m2m[key][field].remove(value)
            return True
        except KeyError:
            return False
    
    def remove_field(self, key, field):
        """删除 key->field 下的所有值"""
        try:
            self.m2m[key][field] = set()
            return True
        except KeyError:
            return False
        
    def remove_from_fields(self, key, value):
        """删除该每个field中删除value
        """
        try:
            for field in self.m2m[key]:
                try:
                    self.m2m[key][field].remove(value)
                except KeyError:
                    continue
        except KeyError:
            return False
        

if __name__ == "__main__":
    users = Hash()
    users.hset(1001, "public", 1002)
    users.hset(1001, "private", [1003, 1004, 1005])
    print users.hget(1001, "private")
    print users.m2m
    print users.remove(1001, "public", 1002)


__all__ = ["Hash"]
