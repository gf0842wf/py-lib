# -*- coding: utf-8 -*-
from collections import defaultdict
def tree():
    """数结构
    
    >>> t = tree()
    >>> t["person"]["name"] = "fk"
    >>> t["person"]["age"] = 24
    >>> t["person"]
    defaultdict(<function tree at ...>, {'age': 24, 'name': 'fk'})
    >>> t["person"]["name"]
    'fk'
    """
    return defaultdict(tree)


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
    # 注意,由于每次defaultdict的工厂函数地址不一样,所以doctest测试会报错,所以要使用省略号
    # 同时测试时要这样:doctest.testmod(optionflags=doctest.ELLIPSIS)