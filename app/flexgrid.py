#coding:utf-8
from models import User, Score_items,Grade
"""
相应flexgrid排序和分页的函数
"""

#用于常规比较
def mycmp(a,b):
    "自定义比较函数"
    if a>b:
        return 1
    else:
        return -1


def sorter(before_sort,col,method):
    """排序函数
    args:
        before_sort:传入的待排序列表，包含一组Score_items对象（没有grade和name字段）
        col：待排序的列
        method：asc or desc
    """

    #如果待排序行为grade
    if col=="grade":
        #首先通过s.user_id获取id，再获取grade，且自定义比较函数应该使用Grade中定义的my_cmp
        after_sort=sorted(before_sort,cmp=Grade.my_cmp,key=lambda s:User.get_user_byID(s.user_id).grade,reverse=True if method=="asc" else False)
    #如果待排序行为name
    elif col=="name":
        #同样需要间接取User的字段
        after_sort=sorted(before_sort,cmp=mycmp,key=lambda s:User.get_user_byID(s.user_id).name,reverse=True if method=="asc" else False)
    else:
        after_sort=sorted(before_sort,cmp=mycmp,key=lambda s:s[col],reverse=True if method=="asc" else False)

    return after_sort


def pageslicer(page,rp,_score_items):
    """分页函数
    args:
        page:当前页数
        rp：每页结果数
        _score_items：全部条目列表
    """
    total=len(_score_items)
    jsondict={
        "page": page,#当前页
        "total": total,#总数
        "rows": []
        }
    for i in xrange((page-1)*rp,(page*rp if page*rp-1<total else total)):
        s=_score_items[i]
        #控件要求每行必须是如下结构的字典，cell中包含实际的数据
        data={
                "id": s.item_name,
                "cell": Score_items.getItemInfo(s)
            }
        jsondict["rows"].append(data)

    return jsondict
