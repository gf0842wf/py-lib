# -*- coding: utf-8 -*-

from operator import add
import random

def prob_choice_i(probs, seq):
    """按照概率来选取一个, 概率只保留整数位
    @param probs: 存放概率的list, sum(probs)=100 形如[40, 1, 49, 10]
    @param seq: 存放元素的list, 形如[2,3,2,5]
    @return: (idx, e), i-来自seq第几个元素, e-元素值
    """
#     TODO: 可以不等于100
#     可以probs=[449, 1, 500, 50]这样, 来提高精确度
#     assert sum(probs) == 100
    seq_ = reduce(add, [ps[0] * [ps[1]] for ps in zip(probs, seq)])
    idx_ = random.choice(xrange(len(seq_)))
    e = seq_[idx_]
    for i, p in enumerate(probs):
        if idx_ <= p - 1:
            idx = i
            break
        else:
            idx_ -= p
    return (idx, e)

def prob_choice(probs, seq):
    """和上面一样,只是不返回idx了, 只返回结果值"""
    seq_ = reduce(add, [ps[0] * [ps[1]] for ps in zip(probs, seq)])
    return random.choice(seq_)


if __name__ == "__main__":
    i = 1
    while True:
        _, e = prob_choice_i([449, 1, 500, 50], [2,3,2,5])
        if e == 3:
            print "WOW, 中大奖了"
            print i
        i += 1
        
__all__ = ["prob_choice", "prob_choice_i"]
