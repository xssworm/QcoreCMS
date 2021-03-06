#coding=utf-8
import YooYo.db.mySql
import types

class Base:
    # 表名
    table = False
    # YooYo.db.mySql.use 别名
    use = YooYo.db.mySql.use
    # 主键
    primaryKey = 'id'

    def __init__(self):
        self.use   = YooYo.db.mySql.use
    
    # 查询
    def find(self,condition=False, *arguments):
        self.query = self.use( self.__class__.table )
        self.query.Meta = self.meta
        if condition == False:
            return self.query
        return self.query.where(condition,*arguments)

    # 通过主键取得值
    def get(self,id):
        return self.find().where( self.__class__.primaryKey + ' = ?' , id ).get()

    # 扩展元数据
    def meta(self,attr):
        return attr


class Meta:

    def __init__(self, ar, attr):
        self.ar = ar
        self.attr = attr
  
    def __setitem__(self, key, val):
        self.attr[key] = val

    def __delitem__(self,key):
        del self.attr[key]

  
    def __iter__(self): 
        return iter(self.attr)

    def __len__(self): 
        return len(self.attr)

    def __contains__(self, value): 
        return value in self.attr

    def __getitem__(self, key):
        if self.attr.has_key(key):
            return self.attr[key]
 
        if type(key) != types.IntType:
            key = 'attr_' + key
            if hasattr(self,key):
                val = getattr(self,key)()
                self.attr[key] = val
                return val
        return None

