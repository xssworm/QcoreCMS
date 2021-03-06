#coding=utf-8
import types
import re
import time
import hashlib

from tornado import escape

def md5(s):
    m = hashlib.md5(str(s))
    m.digest()
    return m.hexdigest()

class json:
    
    @staticmethod
    def decode(s,default=[]):
        s = filters.trim(str(s))
        if '' == s:
            return default

        try:
            return escape.json_decode(s)
        except Exception, e:
            return default


    @staticmethod
    def encode(json):
        return escape.json_encode(json)
    
            
        

class date:
    # 将字符格式化成时间
    @staticmethod
    def strToTime(s , f='%Y-%m-%d %X'):
        f = f.replace('Y-m-d' , '%Y-%m-%d')
        f = f.replace('H:i:s' , '%X')
        return int(time.mktime(time.strptime( s, f )))

    # 将时间格式化成字符
    @staticmethod
    def timeToStr(f='%Y-%m-%d %X' ,t=False):
        f = f.replace('Y-m-d' , '%Y-%m-%d')
        f = f.replace('H:i:s' , '%X')
        t = t and t or time.mktime(time.localtime())
        return time.strftime( f , time.localtime( float( t ) ) )

    @staticmethod
    def time():
        return time.mktime(time.localtime())



class filters:
    """
    过滤字符 
    =============

    #### 方法:

     - trim 去除两边空格
     - toNumber 转换成数字
     - toText 转换成纯文本
     - toLowerCase 转小写
     - toUpperCase 转大写

    """

    @staticmethod
    def trim(s):
        return str(s).strip()

    @staticmethod
    def toNumber(s):
        if validators.isNumber(s):
            return int(s)
        return 0

    #转小写
    @staticmethod
    def toLowerCase(s):
        return str(s).lower()
        
    #转大写
    @staticmethod
    def toUpperCase(s):
        return str(s).upper()

    @staticmethod
    def toText(s):
        if None == s : return None
        #先过滤CDATA
        re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
        re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
        re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
        re_br=re.compile('<br\s*?/?>')#处理换行
        re_h=re.compile('</?\w+[^>]*>')#HTML标签
        re_comment=re.compile('<!--[^>]*-->')#HTML注释
        s=re_cdata.sub('',s)#去掉CDATA
        s=re_script.sub('',s) #去掉SCRIPT
        s=re_style.sub('',s)#去掉style
        s=re_br.sub('\n',s)#将br转换为换行
        s=re_h.sub('',s) #去掉HTML 标签
        s=re_comment.sub('',s)#去掉HTML注释
        #去掉多余的空行
        blank_line=re.compile('\n+')
        s=blank_line.sub('\n',s)
        s=filters.replaceCharEntity(s)#替换实体
        return s

    ##替换常用HTML字符实体.
    #使用正常的字符替换HTML中特殊的字符实体.
    #你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
    #@param htmlstr HTML字符串.
    @staticmethod
    def replaceCharEntity(s):
        CHAR_ENTITIES={
            'nbsp':' ',
            '160':' ',
            'lt':'<',
            '60':'<',
            'gt':'>',
            '62':'>',
            'amp':'&',
            '38':'&',
            'quot':'"',
            '34':'"',
        }
        re_charEntity=re.compile(r'&#?(?P<name>\w+);')
        sz=re_charEntity.search(s)
        while sz:
            entity=sz.group()#entity全称，如&gt;
            key=sz.group('name')#去除&;后entity,如&gt;为gt
            try:
                s=re_charEntity.sub(CHAR_ENTITIES[key],s,1)
                sz=re_charEntity.search(s)
            except KeyError:
                #以空串代替
                s=re_charEntity.sub('',s,1)
                sz=re_charEntity.search(s)
        return s


class validators:
    '''
    验证类
    =============

    #### 方法:

     - isString 是否字符
     - isNumber 是否数字
     - isFloat 是否浮点数
     - isDict 是否字典
     - isArray 是否数组
     - isEmpty 是否为空(含None)
     - isDate 是否符合日历规则 2010-01-31
     - isEmail 是否邮件地址
     - isChineseCharString 是否为中文字符串
     - isLegalAccounts 是否合法 字母开头，允许4-16字节，允许字母数字下划线
     - isIpAddr 是否ip地址

    '''

    @staticmethod
    def isString(x):
        return type(x) is types.StringType

    @staticmethod
    def isNumber(x):
        rule = '[+-]?\d+$'
        return re.match(rule, str(x))
            
    #判断是否为浮点数 1.324
    @staticmethod
    def isFloat(x):
        return type(x) is types.FloatType

    #判断是否为字典 {'a1':'1','a2':'2'}
    @staticmethod
    def isDict(x):
        return type(x) is types.DictType

    @staticmethod
    def isArray(x):
        return type(x) is types.ListType

    @staticmethod
    def isEmpty(x):
        if type(x) is types.NoneType:
            return True
        if validators.isNumber(x): 
            return False
        return len(x) == 0

    #判断是否为日期格式,并且是否符合日历规则 2010-01-31
    @staticmethod
    def isDate(x):
        x = str(x)
        if len(x) == 10:
            rule = '(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)$/'
            match = re.match( rule , x )
            if match:
                return True
            return False
        return False

    #判断是否为邮件地址
    @staticmethod
    def isEmail(x):
        x = str(x)
        rule = '[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$'
        match = re.match( rule , x )

        if match:
            return True
        return False

    #判断是否为中文字符串
    @staticmethod
    def isChineseCharString(x):
        x = str(x)
        for v in x:
            if (v >= u"\u4e00" and v<=u"\u9fa5") or (v >= u'\u0041' and v<=u'\u005a') or (v >= u'\u0061' and v<=u'\u007a'):
                continue
            else:
                return False
        return True

    #判断帐号是否合法 字母开头，允许4-16字节，允许字母数字下划线
    @staticmethod
    def isLegalAccounts(x):
        x = str(x)
        rule = '[a-zA-Z][a-zA-Z0-9_]{3,15}$'
        match = re.match( rule , x )

        if match:
            return True
        return False

    #匹配IP地址
    @staticmethod
    def isIpAddr(x):
        x = str(x)
        #rule = '\d+\.\d+\.\d+\.\d+'
        rule = '((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)'
        match = re.match( rule , x )

        if match:
            return True
        return False
