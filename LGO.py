# -*- coding: utf-8 -*-

#############################################################

##def isUnicodeFile(fname):
##    """ binary read 2 bytes and check for b'\xff\xfe' """
##    fhand=open(fname, 'rb');    a=fhand.read(2);    fhand.close()
##    if a==b'\xff\xfe':  return True
##    return False
##
##def openUA(fname):
##    """ open text file in unicode file or in ansi(big5) file
##        by checking for b'\xff\xfe' """
##    fhand=open(fname, 'rb');    a=fhand.read(2);    fhand.close()
##    if a==b'\xff\xfe':
##        fhand = open(fname,encoding='utf16')
##        fhand.read(1)       ## skip uchar '\ufffe'
##    else:
##        fhand = open(fname)
##    return fhand
##
##def open8UA(fname):
##    return openR(fname)

def openR(fname):
    """ open text file in unicode file or in ansi(big5) file or utf8/BOM
        by checking for b'\xff\xfe' """
    f=open(fname, 'rb');  a=f.read(3);  f.close()
    if a==b'\xef\xbb\xbf': f=open(fname,'r', encoding='utf-8'); f.read(1);
    elif a[:2]==b'\xff\xfe' or a[:2]==b'\xfe\xff': f = open(fname,'r',encoding='utf16')
    else : f = open(fname,'r')
    return f

def openW(fname, encoding='utf-8'):
    """ open for write, default to utf8-BOM """
    f=open(fname, 'w', encoding=encoding)
    return f

import imp
import string
import re
import unicodedata
import collections
import os
import glob

#############################################################
def eachfilename(dir2list, printfname=0):
    """
    iput a string, a list, a tuple, or a flist.txt
    ouput an iterable of file names that match filename pattern
    example: use case
    for fname in eachfilename(dir2list):
        pass
    where
    1.  dir2list= 'c:/a/*.txt'
    2.  dir2list=['c:/a/*.txt',  'c:/b/*.cpp']
    3.  dir2list=('c:/a/*.txt',  'c:/b/*.cpp')
    4.  dir2list= 'c:/a/flist.txt';
        and that flist.txt consists of the following lines
            aa/*.txt
            bb/*.cpp
    """
    if printfname: print('eachfilename is matching for \n' + dir2list);
    if isinstance(dir2list,str):
        if not os.path.exists(dir2list): # if not a valid (single) filename
            dir2list=[dir2list]          # try it as a list
    if isinstance(dir2list,list) or isinstance(dir2list,tuple):
        for line in dir2list:
            for fname in glob.iglob(line):
                fname = fname.replace('\\','/')
                if printfname: print(fname)
                yield fname
    elif isinstance(dir2list,str):
        pp, ff = os.path.split(dir2list); pp+='/';
        for line in open(dir2list):
            line = line.strip()
            if line.startswith('##') : continue ## skip those lines
            for fname in glob.iglob( pp + line ):
                fname=fname.replace('\\','/')
                if printfname: print(fname)
                yield fname

def xmpfilelist():
    a='C:/c2k/bcb/dqs34/*.h'
    ##a=['C:/c2k/bcb/dqs34/*.h','C:/c2k/bcb/dqs34/*.cpp','C:/c2k/bcb/dqs34/*.exe']
    ##a=('C:/c2k/bcb/dqs34/*.h','C:/c2k/bcb/dqs34/*.cpp','C:/c2k/bcb/dqs34/*.exe')
    ##a='C:/c2k/2008tmp台華對譯資料/flist2.txt'
    for fname in eachfilename(a):
        print(fname)
#############################################################
class xmplcls():
    """ note: in 2.5, one cannot call xmplcls.xmpl(1,2)
        but ok in 3.0
    """
    def xmpl(a,b):
        print(a,b)


class DirLister():
    def ls1(dirpat=None):
        if not dirpat : dirpat='*.*'
        print('現在目錄 (os.getcwd() => )', os.getcwd())
        print('listing ',dirpat); print()
        for f in eachfilename(dirpat):
            print(f)
    def ls(self, dirpat=None):
        if not dirpat : dirpat='*.*'
        print('\n現在目錄 (os.getcwd() => )', os.getcwd())
        print('listing ',"'"+dirpat+"'", ':\n');
        i=1
        for f in eachfilename(dirpat):
            print('{0:3}  '.format(i), f); i+=1
        print()
    @property
    def txt(self):
        self.ls('*.txt')
    ##old
    ## def txt():
    ##     DirLister.ls('*.txt')
    ## need () when use
    @property
    def py(self):
        self.ls('*.py')
    @property
    def pys(self):
        self.ls('*.py*')
    @property
    def all(self):
        self.ls()
        ## dynamic adding a method?
        ## dynamic adding a property?
    @property
    def pkl(self):
        self.ls('*.pkl')

ls =DirLister()

##def ls(dirpat=None):
##    if not dirpat : dirpat='*.*'
##    print('現在目錄 (os.getcwd() => )', os.getcwd())
##    for f in eachfilename(dirpat):
##        print(f)
##class Pat:
##    def __init__(self):
##        self.txt='*.txt'
##        self.py ='*.py'
##
##pat =Pat()
##def lstxt():
##    ls('*.txt')

#############################################################
#### keep it a while
##punctsome0 = '\u2010-\u301E\uFE50-\uFF6B\uFF01-\uFF0F\uFF1A-\uFF20\uFF3B-\uFF40'
##punctsome0=punctsome0 + string.punctuation
##punctsome = '([' + punctsome0 + '])'
##sentpunct0= '，。？！：；,.?!:;'
##sentpunct= '([' + sentpunct0 + '])'
##############################################################


class unicodecat:
    def sentpunct():   return '，。？！：；,.?!:;'
    def catcount(printit=0):
        dic = collections.defaultdict(int)
        for i in range(1,2**16-1):
            c = chr(i)
            k=unicodedata.category(c)
            dic[k]+=1
        if printit:
            for k,v in dic.items(): print(k,v)
        return dic
    
    def charclass(*cats, ucoded=0):
        if isinstance(cats,str): cats = (cats,)
        rr=''
        for i in range(1,2**16-1):
            c=chr(i)
            k=unicodedata.category(c)
            if k in cats: rr += c
        if ucoded:   rr=unicodecat.str2rangesUC(rr)
        else:        rr=unicodecat.str2ranges  (rr)
        rr=rr.replace('[','\[')
        rr=rr.replace(']','\]')
        ##rr='[' + rr + ']'
        return rr

    def HL_LL():
        excludeCat='NPSZC'  ##num/punct/symb/sep/others
        rr=''
        H=ord('一')
        for i in range(1,H):
            c=chr(i)
            k=unicodedata.category(c)
            if k[0] in excludeCat: continue
            rr += c
        return unicodecat.str2ranges(rr)

    def HL_LN():
        ##xcld='NPSZC'  ##num/punct/symb/sep/others
        rr=''
        H=ord('一')
        for i in range(1,H):
            c=chr(i)
            k=unicodedata.category(c)
            if k[0] != 'N': continue
            rr += c
        return unicodecat.str2ranges(rr)
        
    def str2ranges(s):
        """ convert, say, 'abcdz' to 'a-dz' """
        def pair2range(be):
            if be[1]-be[0]  ==0: tt = chr(be[0])
            elif be[1]-be[0]==1: tt = chr(be[0])       + chr(be[1])
            else:                tt = chr(be[0]) + '-' + chr(be[1])
            return tt
        lenn=len(s);
        if lenn==0 : return s
        d = ord(s[0])
        be = [d,d]; tt = ''
        for ii in range(1,lenn):
            d = ord(s[ii])
            if d-be[1]==1: be[1]=d
            else:
                tt += pair2range(be)
                be = [d,d]
        tt += pair2range(be)
        return tt

    def str2rangesUC(s):
        """ convert, say, 'abcdz' to '\u0061-\u0064\u007a' """
        def i2uhex(i):
            s=hex(i);
            if s[:2]=='0x': s=s[2:]
            s='\\u'+s.rjust(4,'0')
            return s
        def pair2ucode(be):
            if be[1]-be[0]  ==0: tt = i2uhex(be[0])
            elif be[1]-be[0]==1: tt = i2uhex(be[0])       + i2uhex(be[1])
            else:                tt = i2uhex(be[0]) + '-' + i2uhex(be[1])
            return tt
        lenn=len(s)
        if lenn==0 : return s
        d = ord(s[0])
        be = [d,d]; tt = ''
        for ii in range(1,lenn):
            d = ord(s[ii])
            if d-be[1]==1: be[1]=d
            else:
                tt += pair2ucode(be)
                be = [d,d]
        tt += pair2ucode(be)
        return tt

##PsPe = '\u0028\u0029\u005b\u005d\u007b\u007d\u0f3a-\u0f3d\u169b\u169c\u201a\u201e\u2045\u2046\u207d\u207e\u208d\u208e\u2329\u232a\u2768-\u2775\u27c5\u27c6\u27e6-\u27ef\u2983-\u2998\u29d8-\u29db\u29fc\u29fd\u2e22-\u2e29\u3008-\u3011\u3014-\u301b\u301d-\u301f\ufd3e\ufd3f\ufe17\ufe18\ufe35-\ufe44\ufe47\ufe48\ufe59-\ufe5e\uff08\uff09\uff3b\uff3d\uff5b\uff5d\uff5f\uff60\uff62\uff63'
##PsPe = PsPe.replace('[','\[')
##PsPe = PsPe.replace(']','\]')
_HeadPUNCTS =  unicodecat.charclass('Ps','Pe')
_TailPUNCTS =  _HeadPUNCTS + '，。？！：；,.?!:;'
_MidPUNCTS  =  '。，？！：；'
import re

class toSPH:
    def split(line, skipspace=0):
        """ return iterator of punct/sph/space strings """
        a = re.sub('\s+',' ', line.strip()) ##normalize white's -> 1 space
        a = re.split('(\s)', a)             ##split/keep space
        for aa in a:    ## for each PPH, convert it to SPH
            if aa==' ':
                if skipspace == 0: yield aa
            else:
                for aaa in toSPH.pph2sph(aa):  yield aaa

    def pph2sph(pph):
        """ return a list in lead-puncts , sph, trail-puncts """
        rr=[]

        ### split/keep HeadPUNCTS
        a = re.split('(^['+ _HeadPUNCTS +']+)',pph) ## for head-punct
        a = [aa for aa in a if len(aa)>0 ]  ## del empty string
        if len(a)>1:                ## have head-puncts, and not sole punct
            rr += a[0]              ## append head puncts 1X1
            pph=a[1]                ## remaining part

        ### split/keep TailPUNCTS
        a = re.split('(['+ _TailPUNCTS+']+$)',pph) ## for tail-punct
        a = [aa for aa in a if len(aa)>0 ]  ## del empty string

        ### split/keep MidPUNCTS
        if len(a)>0:
            m = re.split('([' + _MidPUNCTS + ']+)', a[0]);
            m=[aa for aa in m if len(aa)>0]   ## del empty string
            rr += m                     ## append the sph
        if len(a)>1 : rr += a[1]    ## append tail-puncts 1X1

        return rr

    def pph2sphYield(pph):
        """ another way to sph using yield """
        a = re.split('(^['+ _HeadPUNCTS +']+)',pph)
        a = [aa for aa in a if len(aa)>0 ]  ##there may have empty string
        if len(a)>1:        ## so there are punct at the begin
            for aa in a[0]:    yield aa
            pph=pph[len(a[0]) : ]
        a = re.split('(['+_TailPUNCTS+']+$)',pph)
        a = [aa for aa in a if len(aa)>0 ]  ##there may have empty string
        if len(a)<=1: ## split and yied if middle-puncts
            mm = re.split('([' + _MidPUNCTS + ']+)', a[0]); mm=[aa for aa in mm if len(aa)>0]
            for aa in mm: yield aa
        else:        ## so there are punct at the end
            yield a[0]
            for aa in a[1]:    yield aa

##############################################################
##############################################################
examples = [
    '」   「「阮  足肯定  這m是 耶誕。老人，」 警局副局長 Ken．Garner講。 。',
    '一個 頭戴 耶誕帽ｅ 查甫人， 因為 ho人發現 di Hollywood  中國戲院 外口 戴著 一頂假頭毛、 閣 穿著一領 紅色蕾絲 無袖ｅ女人 穿乳胚仔 gah 一領紫色 丁字褲， suah-di 禮拜日 暗時  hong掠起來， 接受 食酒駛車 調查， 警方講。',
    'zit名 嫌疑犯 因為 血液 酒精含量 檢測 du好超過.08．ｅ 州法定 限制， 而且 hong登記 入監牢， 警方講。 伊 後來 用5000美元 交保釋放。'
    ]


def main_toSPH():
##    unicodecat.catcount(1)
##    PsPe=unicodecat.charclass('Ps','Pe', ucoded=0); print(PsPe)
    ss=examples[0]; print(ss,'\n',  '**'*20)
    for t in toSPH.split(ss, 1): print(t); 

##def __each21d(filelist):
##    import re
##    for fn in eachfilename(filelist):
##        ll, dic=[], {}
##        beged, ended=0,0
##        for line in openR(fn):
##            if re.match('^[.][.]\s',line):# \n is at the end of line
##                beged=1;
##                continue
##            if not beged:
##                continue
##            if re.match('^[.]\s',line):
##                ended=1
##            if ended:
##                yield(ll)
##                ll,beged,ended=[],0,0
##                continue
##            ll.append(line.rstrip())

class LGC():
    @classmethod
    def each21d_cls(cls, filelist):
        import re
        for fn in eachfilename(filelist):
            ll, beged, ended=[],0,0
            for line in openR(fn):
                line=line.rstrip()
                if not line: continue
                if line=='..' or re.match('^[.][.]\s',line): beged=1; continue
                if not beged: continue
                if line=='.' or re.match('^[.]\s',line):     ended=1
                if ended:
                    yield(ll)
                    ll,beged,ended=[],0,0
                    continue
                ll.append(line)
    def each21d(filelist):
        import re
        for fn in eachfilename(filelist):
            rr, beged, ended=[],0,0
            for line in openR(fn):
                line=line.rstrip()
                if line.startswith('..') or line.startswith('…') : beged=1; continue
                # why …? Since word will replace ... with … automatically.
                if not beged: continue
                if line=='.' or re.match('^[.]\s',line): ended=1  #[.] for a single dot
                if ended:
                    yield(rr)
                    rr,beged,ended=[],0,0
                    continue
                # append everything else
                rr.append(line)

    def each21ddic(filelist):
        for rr in LGC.each21d(filelist):
            dic ={}
            for r in rr:
                if not r: continue
                ll=re.split('(^[.][-\w]+[.])', r);
                if len(ll)!=3: continue
                dic[ll[1]]=ll[2] # split(..) gives blank first field
            yield(dic)

    def eachdm(filelist):
        for dic in LGC.each21ddic(filelist):
            yield(dic.get('.d.',''), dic.get('.m.',''))

    def eachdama(filelist):
        for dic in LGC.each21ddic(filelist):
            yield(dic.get('.da.',''), dic.get('.ma.',''))
            
    def eachssp(LGgu):
        pass
    
def main_LGC(flisttxt):
##    for ll in LGC.each21d(flisttxt):
##        print(ll)
    
##    i=1
##    for d,m in LGC.eachdm(flisttxt):
##        print(i,d);  i+=1
    import collections
    dic=collections.Counter()
    for d,_ in LGC.eachdm(flisttxt):
        for t in d.split():
            dic[t]+=1
    for k,v in dic.items():
        print(v,k)

##    dic = collections.defaultdict(int)
##    for fname in eachfilename(flisttxt):
##        fname = fname.strip();
##        print(fname)
##        for para in openR(fname):
##            para = para.strip()
##            if not para.startswith('.d.'): continue
##            para = para[3:]
##            for word in toSPH.split(para,1):
##                dic[word]+=1
##    sortedlist=sorted([(v,k) for k,v in dic.items() if v>2 ])
##    for (v,k) in sortedlist : print(v,k)
##    print(len(sortedlist), len(dic))

def countwords(flisttxt):
    dic = collections.defaultdict(int)
    for fname in eachfilename(flisttxt):
        fname = fname.strip();
        print(fname)
        for para in openR(fname):
            para = para.strip()
            if not para.startswith('.d.'): continue
            para = para[3:]
            for word in toSPH.split(para,1):
                dic[word]+=1
    sortedlist=sorted([(v,k) for k,v in dic.items() if v>2 ])
    for (v,k) in sortedlist : print(v,k)
    print(len(sortedlist), len(dic))
    

class stredit:    
    """ Levenstein edit-distance """
    def dp(hh,vv, subcost=1):
        """ dynamic programming for Levenstein edit-distance """
        C,R=len(hh),len(vv);
        # Initialize the Best-so-far table
        B=[ [0]*(C+1) for r in range(R+1) ] ## matrix[R}[C}
        for r in range(R+1): B[r][0] = r
        for c in range(C+1): B[0][c] = c
        # dynamic programming
        for r in range(1,R+1):
            for c in range(1,C+1):
                cost = 0 if hh[c-1]==vv[r-1] else subcost
                B[r][c] = min(1+B[r][c-1],   1+B[r-1][c],   cost+B[r-1][c-1])
                ###           via insertion, via deletion,  via sub/copy
        return B

    def backtrack(B):
        """ backtrack for Levenstein edit-distance """
        trac=[]; 
        lenR, lenC = len(B)-1, len(B[0])-1
        R,C=lenR,lenC;
        while R>0 and C>0:
            LL,TT,LT=B[R][C-1], B[R-1][C], B[R-1][C-1]; ## Left,Top,LeftTop
            min3=min(LL, TT, LT)
            if min3==LT and LT == B[R][C]:
                trac.append((R,C,'0'));       R-=1; C-=1 #mov2 LT, 0-cost
            elif min3==TT : trac.append((R,C,'T')); R-=1 #mov2 Top, 
            elif min3==LL : trac.append((R,C,'L')); C-=1 #mov2 Left
            else: trac.append((R,C,'S'));     R-=1; C-=1 #mov2 LT, sub-cost
        if   R>0: trac += [ (r,0,'T') for r in range(R,0,-1) ]
        elif C>0: trac += [ (0,c,'L') for c in range(C,0,-1) ]
        trac.reverse()
        return trac

class LCS:
    """ Longest Common Subsequence """

    def lcs(hh, vv):
        """ return list of the common-subseq """
        B=LCS.getB(hh,vv)
        trac=LCS.backtrack(B);
        cs=[ hh[h-1] for v,h,k in trac if k=='1' ]
        return cs

    def indexesLCS(hh, vv):
        return ndxLCS(hh,vv)

    def ndxLCS(hh, vv):
        """ 
        return two lists of indexes of the common-subseq
        hh='sfdre'      or   ['s','f','d','r','e']
        vv='asdfgr'     or   ['a','s','d','f','g','r']
        return
        ([0, 1, 3], [1, 3, 5])
        that are the indexes of the LCS into the 2 sequences
        """
        B=LCS.getB(hh,vv)
        return LCS.backtrack2(B);

    def lcslen(hh, vv):
        B=LCS.getB(hh,vv)
        return B[-1][-1]
    
    def cidslen(hh,vv) ->tuple :
        """ cdis: common, insert, delete, subsitution view from HH seq"""
        B=LCS.getB(hh,vv); trac=LCS.backtrack(B);
        return LCS.btrack2cidslen(trac)

    def all3(hh,vv, printB=0, printtrack=0):
        """ return 3 lists : common-subseq, hh-remains, vv-remains """
        B=LCS.getB(hh,vv)
        trac=LCS.backtrack(B);
        if printB:
            print('Best-so-far B = ')
            for row in B : print(row)
        if printtrack:
            print('backtrack = ')
            for t in trac: print(t)

        ndxh = [ h-1 for v,h,k in trac if k=='1' ]
        ndxv = [ v-1 for v,h,k in trac if k=='1' ]
        cs=[ hh[h] for h in ndxh ]
        hr=LCS.__exclude(hh,ndxh)
        vr=LCS.__exclude(vv,ndxv)
        return cs,hr,vr

    def __exclude(seq, ndx):
        """ helper: return list of items in seq that is not in ndx """
        leng=len(seq); mask=[1]*leng;
        for n in ndx: mask[n]=0
        remain=[seq[n] for n in range(leng) if mask[n]==1]
        return remain

    def getB(hh,vv):
        """ return Best-so-far using dynamic programming """
        C,R=len(hh),len(vv);
        B=[ [0]*(C+1) for r in range(R+1) ] ## matrix[R+1}[C+1}
        for r in range(1,R+1):
            for c in range(1,C+1):
                gain = 1 if hh[c-1]==vv[r-1] else 0
                B[r][c] = max(B[r][c-1],   B[r-1][c],   gain + B[r-1][c-1])
        return B

    def backtrack2(B):
        """ backtrack for Longest Common Subsequence
            return 2 lists of indexes into hh and vv that are LCS
            better to further processing
        """
        tracH, tracV=[],[]
        lenR, lenC = len(B)-1, len(B[0])-1
        R,C =lenR,lenC;
        while R>0 and C>0:
            LL,TT,LT = B[R][C-1], B[R-1][C], B[R-1][C-1] ## Left,Top,LeftTop
            max3=max(LL, TT, LT)
            if max3==LT:
                if LT==B[R][C]-1: ## otherwise, it is a subsitution
                    tracH.append(R-1); tracV.append(C-1)
                R-=1; C-=1
            elif max3==TT:   R-=1
            else : C-=1
        tracV.reverse(); tracH.reverse()
        return tracH,  tracV

    def backtrack(B):
        """ backtrack for Longest Common Subsequence
            indexes of returned track is B's indexes
        """
        trac=[]; 
        lenR, lenC = len(B)-1, len(B[0])-1
        R,C =lenR,lenC;
        while R>0 and C>0:
            LL,TT,LT = B[R][C-1], B[R-1][C], B[R-1][C-1] ## Left,Top,LeftTop
            max3=max(LL, TT, LT)
            if max3==LT :
                tt=(R,C,'1') if LT==B[R][C]-1 else (R,C,'S')
                trac.append(tt); R-=1; C-=1; ## mov2 LT, 1-gain or 0-gain
            elif max3==TT : trac.append((R,C,'T')); R-=1 #mov2 Top, 
            elif max3==LL : trac.append((R,C,'L')); C-=1 #mov2 Left
        if   R>0: trac += [ (r,0, 'T') for r in range(R,0,-1) ]
        elif C>0: trac += [ (0,c, 'L') for c in range(C,0,-1) ]
        trac.reverse()
        return trac
    
    def btrack2cidslen(track):
        """ cdis: common, insert, delete, subsitution view from HH seq"""
        cids=[0,0,0,0];
        for h,v,k in track:
            if   k=='1': cids[0]+=1     # c (common subsequence)
            elif k=='L': cids[1]+=1     # i (insertion)
            elif k=='T': cids[2]+=1     # d (deletion)
            else :       cids[3]+=1     # s (substitution)
        return cids



class PCC:
    def resetdic(self):
        self.dicCommon=collections.defaultdict(int)
        self.dicRemain=collections.defaultdict(int)
        self.dcnt=0
        
    def allpairs(seq1, seq2):
        for w1 in seq1:
            for w2 in seq2:
                yield (w1,w2)

    def linepro1(self, dline, mline):
        ds=toSPH.split(dline,1); ds=[t for t in ds if unicodedata.category(t[0])[0]!='P']
        ms=toSPH.split(mline,1); ms=[t for t in ms if unicodedata.category(t[0])[0]!='P']
        self.dcnt+=len(ds)
        cs, dd, mm = LCS.all3(ds,ms)
        for t in cs: self.dicCommon[t]+=1
        for t1, t2 in PCC.allpairs(dd,mm):
            self.dicRemain[t1+' '+t2]+=1

    def linepro2(self, dlines, mlines):
        dss = re.split('[。，；！？]',dlines); dss=[t for t in dss if t!='']
        mss = re.split('[。，；！？]',mlines); mss=[t for t in mss if t!='']
        for dline, mline in zip(dss,mss):
            dline, mline = dline.strip(), mline.strip()
            self.linepro1(dline,mline)

    def doPCC(self, flist, linepro):
        self.resetdic()
        for fname in eachfilename(flist):
            print(fname)
            dline, mline ="", ""
            for line in openUA(fname):
                line.strip()
                if line.startswith('.d.'): dline=line[3:]
                elif line.startswith('.m.'): mline=line[3:]
                if dline=="" or mline=="": continue
                linepro(dline,mline)
                dline, mline="",""
    def excersise(self):
        flist='C:/c2k/2008tmp台華對譯資料/flist2.txt'
        self.doPCC(flist, self.linepro2)


def mainPCC():
    pcc = PCC()
    pcc.excersise()
    dic=pcc.dicCommon
    for k,v in dic.items():
        if v>10: print(k,v)
    cnt=0;
    for k,v in dic.items(): cnt+=v
    print(cnt)
    print(len(pcc.dicCommon))
    print(pcc.dcnt)
    dic=pcc.dicRemain
    print(len(dic))
##    for k,v in dic.items():
##        if v>3: print(k,v)
    crp=sorted([(v,k) for k,v in dic.items() if v>3])
    for v,k in crp: print(v,k)


def main_allpairs():
    s1=list(toSPH.split(examples[0]))
    s2=list(toSPH.split(examples[1]))
    for t in allpairs(s1,s2):
        print(' '.join(t))


def main_StrEdit():
    hh,vv='drake','park'
##    hh,vv='xbadz','abcd'
    B=stredit.dp(hh,vv)
    for b in B: print(b)
    btrac=stredit.backtrack(B)
    for t in btrac: print(t)

    
def main_LCS():
    hh,vv='drake','park'
##    hh,vv='xbadz','abcd'
##    hh,vv="zu gui gong ng ging ing", "su gui hor gong ging"; hh,vv=hh.split(),vv.split()
    print('hh =' ,hh); print('vv =', vv)
    t=LCS.lcs(hh,vv);    print(t)
    t=LCS.lcslen(hh,vv);    print(t)
    t=LCS.cidslen(hh,vv);    print(t)
    chv= LCS.all3(hh,vv,1,1); print(chv)
    for t in chv: print(t)

class DAIQI():
    def vowel_add_nn(imso):
        if imso in 'aeiou': imso=imso+'nn'
        if imso=='or': imso = 'ornn'
        return imso

    def syl2imso(syl):
        """ mono-syllable to phoneme"""
        pp=re.split('(ngh|mh|nnh|orh|[aeiou]h|nn|ng|m|n|or|[aeiou][ptk])$',syl)
        qq=re.split('([aeiou])',pp[0])
        qq+=pp[1:]
        u=[it for it in qq if it]
        frst, last = u[0], u[-1]
        if frst==frst=='m' or frst=='n' or frst=='ng':
            u=[DAIQI.vowel_add_nn(it) for it in u]
        if last=='nnh' or last=='nn':
            u=[DAIQI.vowel_add_nn(it) for it in u[:-1]]
        if last == 'nnh':
            u[-1]=u[-1]+'h'
        return u
    def syl2sipi(syl):
        """ sipi: siang pin"""
        ll=DAIQI.syl2imso(syl)
        vv=re.findall('[aeiou]',syl)
        if len(vv)==0:
            return [syl]
        if len(vv)==1:
            if len(ll)<=2:
                return [syl]
            else:
                return [''.join(ll[:2]), ''.join(ll[1:])]
        else: ## len(ll)>1:
            return  [''.join(ll[:2]), ''.join(ll[2:])]

    def syl2synsipi(syl):
        """ sipi: siang pin"""
        if re.search('[aeiou]',syl):
            ll=DAIQI.syl2imso(syl)
            if len(ll)>=3:
                return  [''.join(ll[:2]), ''.join(ll[1:])]
        return [syl]



import xml.etree.ElementTree as xet
##dq1=xet.parse(open('C:/c2k/LGO/2give2/rd5a-5x.tcpml'))

class DZB:
    def __init__(self):
        self.dic={}
    def reset():
        self.dic={}
    def split_tcpml(entry):
        ###<!-- //0!!01  檔案： danri9a.txt -->
        e=entry.strip()
        if e.startswith('<!--'): return []
        elem = xet.fromstring(e)
        return elem.attrib
    def linein(self, entry):
        e=entry; e=e.strip()
        if e.startswith('<!-- '): return 0  ## this is comment line
        g=DZB.split_tcpml(entry)
        print(g)

def main_DZB():
    dzb=DZB()
    e='<sud v="十"	i= "sip6"	kqdzf= "970"	vbv="0"/>'
#    print(e);    dzb.linein(e)
    e='<sud v="也"	i="ia2"	kqdzf="275"	vbv="0"/>'
#    print(e);    dzb.linein(e)
    e='<sud v="性情"	i="sing3-zing5"	kqdzf="3"	hqzg=""/>'
    print(e);    print(DZB.split_tcpml(e))
    e='<sud v="入"	i="(rip6|lip6|qip6)"	kqdzf="288"	vbv="1"/>'
    print(e);    print(DZB.split_tcpml(e))
    dic=dzb.dic
    for k,v in dic.items():
        print(k,v)

#########################################
##    L = unicodecat.HL_LL();    print(L)
##    L = unicodecat.HL_LN();    print(L)
##_HL_LL='A-Za-zªµºÀ-ÖØ-öø-ˁˆ-ˑˠ-ˤˬˮ̀-ʹͶͷͺ-ͽΆΈ-ΊΌΎ-ΡΣ-ϵϷ-ҁ҃-ԣԱ-Ֆՙա-և֑-ׇֽֿׁׂׅׄא-תװ-ײؐ-ؚء-ٞٮ-ۓە-ۜ۞-۪ۨ-ۯۺ-ۼۿܐ-݊ݍ-ޱߊ-ߵߺँ-ह़-्ॐ-॔क़-ॣॱॲॻ-ॿঁ-ঃঅ-ঌএঐও-নপ-রলশ-হ়-ৄেৈো-ৎৗড়ঢ়য়-ৣৰৱਁ-ਃਅ-ਊਏਐਓ-ਨਪ-ਰਲਲ਼ਵਸ਼ਸਹ਼ਾ-ੂੇੈੋ-੍ੑਖ਼-ੜਫ਼ੰ-ੵઁ-ઃઅ-ઍએ-ઑઓ-નપ-રલળવ-હ઼-ૅે-ૉો-્ૐૠ-ૣଁ-ଃଅ-ଌଏଐଓ-ନପ-ରଲଳଵ-ହ଼-ୄେୈୋ-୍ୖୗଡ଼ଢ଼ୟ-ୣୱஂஃஅ-ஊஎ-ஐஒ-கஙசஜஞடணதந-பம-ஹா-ூெ-ைொ-்ௐௗఁ-ఃఅ-ఌఎ-ఐఒ-నప-ళవ-హఽ-ౄె-ైొ-్ౕౖౘౙౠ-ౣಂಃಅ-ಌಎ-ಐಒ-ನಪ-ಳವ-ಹ಼-ೄೆ-ೈೊ-್ೕೖೞೠ-ೣംഃഅ-ഌഎ-ഐഒ-നപ-ഹഽ-ൄെ-ൈൊ-്ൗൠ-ൣൺ-ൿංඃඅ-ඖක-නඳ-රලව-ෆ්ා-ුූෘ-ෟෲෳก-ฺเ-๎ກຂຄງຈຊຍດ-ທນ-ຟມ-ຣລວສຫອ-ູົ-ຽເ-ໄໆ່-ໍໜໝༀ༹༘༙༵༷༾-ཇཉ-ཬཱ-྄྆-ྋྐ-ྗྙ-ྼ࿆က-ဿၐ-ႏႠ-Ⴥა-ჺჼᄀ-ᅙᅟ-ᆢᆨ-ᇹሀ-ቈቊ-ቍቐ-ቖቘቚ-ቝበ-ኈኊ-ኍነ-ኰኲ-ኵኸ-ኾዀዂ-ዅወ-ዖዘ-ጐጒ-ጕጘ-ፚ፟ᎀ-ᎏᎠ-Ᏼᐁ-ᙬᙯ-ᙶᚁ-ᚚᚠ-ᛪᜀ-ᜌᜎ-᜔ᜠ-᜴ᝀ-ᝓᝠ-ᝬᝮ-ᝰᝲᝳក-ឳា-៓ៗៜ៝᠋-᠍ᠠ-ᡷᢀ-ᢪᤀ-ᤜᤠ-ᤫᤰ-᤻ᥐ-ᥭᥰ-ᥴᦀ-ᦩᦰ-ᧉᨀ-ᨛᬀ-ᭋ᭫-᭳ᮀ-᮪ᮮᮯᰀ-᰷ᱍ-ᱏᱚ-ᱽᴀ-ᷦ᷾-ἕἘ-Ἕἠ-ὅὈ-Ὅὐ-ὗὙὛὝὟ-ώᾀ-ᾴᾶ-ᾼιῂ-ῄῆ-ῌῐ-ΐῖ-Ίῠ-Ῥῲ-ῴῶ-ῼⁱⁿₐ-ₔ⃐-⃰ℂℇℊ-ℓℕℙ-ℝℤΩℨK-ℭℯ-ℹℼ-ℿⅅ-ⅉⅎↃↄⰀ-Ⱞⰰ-ⱞⱠ-Ɐⱱ-ⱽⲀ-ⳤⴀ-ⴥⴰ-ⵥⵯⶀ-ⶖⶠ-ⶦⶨ-ⶮⶰ-ⶶⶸ-ⶾⷀ-ⷆⷈ-ⷎⷐ-ⷖⷘ-ⷞⷠ-ⷿⸯ々〆〪-〯〱-〵〻〼ぁ-ゖ゙゚ゝ-ゟァ-ヺー-ヿㄅ-ㄭㄱ-ㆎㆠ-ㆷㇰ-ㇿ㐀-䶵'
_LL='A-Za-zªµºÀ-ÖØ-öø-ˁˆ-ˑˠ-ˤˬˮ̀-ʹͶͷͺ-ͽΆΈ-ΊΌΎ-ΡΣ-ϵϷ-ҁ҃-ԣԱ-Ֆՙա-և֑-ׇֽֿׁׂׅׄא-תװ-ײؐ-ؚء-ٞٮ-ۓە-ۜ۞-۪ۨ-ۯۺ-ۼۿܐ-݊ݍ-ޱߊ-ߵߺँ-ह़-्ॐ-॔क़-ॣॱॲॻ-ॿঁ-ঃঅ-ঌএঐও-নপ-রলশ-হ়-ৄেৈো-ৎৗড়ঢ়য়-ৣৰৱਁ-ਃਅ-ਊਏਐਓ-ਨਪ-ਰਲਲ਼ਵਸ਼ਸਹ਼ਾ-ੂੇੈੋ-੍ੑਖ਼-ੜਫ਼ੰ-ੵઁ-ઃઅ-ઍએ-ઑઓ-નપ-રલળવ-હ઼-ૅે-ૉો-્ૐૠ-ૣଁ-ଃଅ-ଌଏଐଓ-ନପ-ରଲଳଵ-ହ଼-ୄେୈୋ-୍ୖୗଡ଼ଢ଼ୟ-ୣୱஂஃஅ-ஊஎ-ஐஒ-கஙசஜஞடணதந-பம-ஹா-ூெ-ைொ-்ௐௗఁ-ఃఅ-ఌఎ-ఐఒ-నప-ళవ-హఽ-ౄె-ైొ-్ౕౖౘౙౠ-ౣಂಃಅ-ಌಎ-ಐಒ-ನಪ-ಳವ-ಹ಼-ೄೆ-ೈೊ-್ೕೖೞೠ-ೣംഃഅ-ഌഎ-ഐഒ-നപ-ഹഽ-ൄെ-ൈൊ-്ൗൠ-ൣൺ-ൿංඃඅ-ඖක-නඳ-රලව-ෆ්ා-ුූෘ-ෟෲෳก-ฺเ-๎ກຂຄງຈຊຍດ-ທນ-ຟມ-ຣລວສຫອ-ູົ-ຽເ-ໄໆ່-ໍໜໝༀ༹༘༙༵༷༾-ཇཉ-ཬཱ-྄྆-ྋྐ-ྗྙ-ྼ࿆က-ဿၐ-ႏႠ-Ⴥა-ჺჼᄀ-ᅙᅟ-ᆢᆨ-ᇹሀ-ቈቊ-ቍቐ-ቖቘቚ-ቝበ-ኈኊ-ኍነ-ኰኲ-ኵኸ-ኾዀዂ-ዅወ-ዖዘ-ጐጒ-ጕጘ-ፚ፟ᎀ-ᎏᎠ-Ᏼᐁ-ᙬᙯ-ᙶᚁ-ᚚᚠ-ᛪᜀ-ᜌᜎ-᜔ᜠ-᜴ᝀ-ᝓᝠ-ᝬᝮ-ᝰᝲᝳក-ឳា-៓ៗៜ៝᠋-᠍ᠠ-ᡷᢀ-ᢪᤀ-ᤜᤠ-ᤫᤰ-᤻ᥐ-ᥭᥰ-ᥴᦀ-ᦩᦰ-ᧉᨀ-ᨛᬀ-ᭋ᭫-᭳ᮀ-᮪ᮮᮯᰀ-᰷ᱍ-ᱏᱚ-ᱽᴀ-ᷦ᷾-ἕἘ-Ἕἠ-ὅὈ-Ὅὐ-ὗὙὛὝὟ-ώᾀ-ᾴᾶ-ᾼιῂ-ῄῆ-ῌῐ-ΐῖ-Ίῠ-Ῥῲ-ῴῶ-ῼⁱⁿₐ-ₔ⃐-⃰ℂℇℊ-ℓℕℙ-ℝℤΩℨK-ℭℯ-ℹℼ-ℿⅅ-ⅉⅎↃↄⰀ-Ⱞⰰ-ⱞⱠ-Ɐⱱ-ⱽⲀ-ⳤⴀ-ⴥⴰ-ⵥⵯⶀ-ⶖⶠ-ⶦⶨ-ⶮⶰ-ⶶⶸ-ⶾⷀ-ⷆⷈ-ⷎⷐ-ⷖⷘ-ⷞⷠ-ⷿⸯ々〆〪-〯' #####〱-〵〻〼ぁ-ゖ゙゚ゝ-ゟァ-ヺー-ヿㄅ-ㄭㄱ-ㆎㆠ-ㆷㇰ-ㇿ㐀-䶵'
_LN='0-9²³¹¼-¾٠-٩۰-۹߀-߉०-९০-৯৴-৹੦-੯૦-૯୦-୯௦-௲౦-౯౸-౾೦-೯൦-൵๐-๙໐-໙༠-༳၀-၉႐-႙፩-፼ᛮ-ᛰ០-៩៰-៹᠐-᠙᥆-᥏᧐-᧙᭐-᭙᮰-᮹᱀-᱉᱐-᱙⁰⁴-⁹₀-₉⅓-ↂↅ-ↈ①-⒛⓪-⓿❶-➓⳽〇〡-〩〸-〺㆒-㆕㈠-㈩㉑-㉟㊀-㊉㊱-㊿'
_LN='一二三四五六七八九十０百仟萬億兆佰千' + _LN
_LLN = _LL + _LN
_HLXpattern    = '([{2}]+(?:[.,][{2}]+)*%?)|([^{0}\s])|([{1}]*[{2}]*)|([\s]*)'.format(_LLN, _LL, _LN)
_HLXpattern1   = '([{2}]+([.,]?[{2}]*)*%?)|([^{0}\s])|([{1}]*[{2}]*)|([\s]*)'.format(_LLN, _LL, _LN)
_HLxpattern    = '([^{0}\s])|([{1}]*[{2}]*)|([\s]*)'.format(_LLN, _LL, _LN)
_HLpatternOLD  = '^(['+_LL+']*['+_LN+']*-?)'
_HLpattern1    = '(['+_LL+']*['+_LN+']*-?)'
_HLpattern2    = '(['+_LL+']+['+_LN+']*-?)'+'|([\s])|([^'+_LL+_LN+']{1})'
#####                          ^ : why won't work if use * instead of + ???
####### Isn't this nice?!!!!  ##########
########################################


import pickle

class LGO:
##    def bpm22a():
##        for k in bpm2abc.keys():
##            a=[]; rmn=k;
##            if re.match('[ㄅ-ㄙ]',rmn):
##                a.append(rmn[0]); rmn=rmn[1:]
##
##    def bpm2SU(bpm):
##        a= re.split('([^ㄅ-ㄙ]+)',bpm)
##        if len(a)==3 and a[2]=='': a.pop()
##        if len(a)==1 : a.append('')
##        if not len(a)==2: print(bpm + ' : err input to bpm2SU ?')
##        return a
##    def bpm2SU2abc(bpm):
##        if bpm=='ㄈㄥ': return 'fong'
##        a=LGO.bpm2SU(bpm)
##        if a[1]=='ㄨㄥ' and a[0]!='':
##            r=bpmSiannvor[a[0]]+'ong'
##        else:
##            r=bpmSiannvor[a[0]]+bpmUnvor[a[1]]
##            if a[1]=='': r+='ih'  ## for zhih chih shih rih zih cih sih
##        return r
##
##    def bpm22():
##        count=0
##        for k,v in bpm2abc.items():
##            if k=='' and v=='': continue
##            r=LGO.bpm2SU2abc(k)
##            if r!=v :   print(k,v, r, a); count+=1
##        if count<=0: print ('done. no err')
##        return
##
##    def bpm22c():
##        aset=set()
##        for k in bpm2abc.keys():
##            a=LGO.bpm2SU(k)
##            ##print(k,a)
##            for t in a :
##                if t!='': aset.add(t)
##        a=sorted([ t for t in aset])
##        for t in a:     print("'{0}':'',".format(t))
##        ##return aset
##    def bpm22b():
##        aset={}
##        for k in bpm2abc.keys():
##            a=LGO.bpm2SU(k)
##            print(k,a)
            
    def hunHLiterative(s, keepdash=0):
        """ split Hanri from Lormari in ascii """
        n,nlen = 0,len(s);
        aa=[]
        while n<nlen:
            t=s[n:]
            tt=re.split('^([a-zA-Z]+[0-9]*-?)',t)
            if tt[0]=='':
                n +=len(tt[1]);
                if not keepdash: tt[1]=tt[1].rstrip('-')
                aa.append(tt[1]);
            else: aa.append(t[0]); n+=1
        return aa
    def hunHLXiterative(s, keepdash=0):
        """ split Hanri from extened Lormari """
        n,nlen = 0,len(s);
        aa=[]
        ##HLpattern='(['+HL_LL+']+['+HL_LN+']*-?)'
        while n<nlen:
            t=s[n:]
            tt=re.split( _HLpattern1, t )
            if tt[0]=='':
                n +=len(tt[1]);
                if not keepdash: tt[1]=tt[1].rstrip('-')
                aa.append(tt[1]);
            else: aa.append(t[0]); n+=1
        return aa
    def hunHL(s, keepdash=0):
        """ split Hanri from Lormari in ascii """
        tt=re.split( '([a-zA-Z]+[0-9]*-?)|([^a-zA-Z])', s )
        tt = [ t for t in tt if (t!=None and t!='')]
        return tt
    def hunHLX(s, keepdash=0):
        """ split Hanri from extened Lormari """
        #LGO.hunHLX('abc台灣123.12%1,200,394.abc台灣123abc123')
        #['abc', '台', '灣', '123.12%', '1,200,394', '.', 'abc', '台', '灣', '123', 'abc123']
        tt=re.split( _HLXpattern, s )
        tt = [ t for t in tt if (t!=None and t!='')]
        return tt
    def splitabc(s):
        """ split data line s in abc format"""
        a=re.split('\s*(<::[^<>:]*::>)\s*', s)
        if a[0]=='': a.pop(0)
        return a
    def splitabc1(s):
        """ split data line s in abc format"""
        a=re.split('\s*(<:[^<>:]*:>)\s*', s)
        if a[0]=='': a.pop(0)
        return a
    def splitkv(s):
        """ split line s in key-value pairs"""
        a=re.split('(\w*)\s*=\s*"([^="]*)"\s*', s)
        a=[ t for t in a if t!='']
        return a
    def splitetag(s):
        """ split data line s in empty tag of xml """
        if s.lstrip().startswith('<!--'): return {}
        return xet.fromstring(s).attrib
    
    def pickleto(object, fname):
        fob = open(fname,'wb')
        pickle.dump(object,fob)
        fob.close()
        print('done pickle2', fname)
    def unpickle(fname):
        fob = open(fname,'rb')
        o = pickle.load(fob)
        fob.close()
        return o

    def ckipdic_countbpm(flist=''):
        if flist=='':
            flist='C:/Documents and Settings/aa/桌面/ckip2004/1Dic/*.3bpm.txt'
        dic=collections.defaultdict(int)
        tone = 'ˇˊˋ˙'
        ##print(flist)
        for fname in eachfilename(flist,1):
            print(fname)
            for line in openUA(fname):
                aa=list(line.strip().split())
                for tt in aa[2:]:
                    dic[tt.rstrip(tone)]+=1
        return dic

    def ckipdic2vi(flist=''):
        if flist=='':
            flist='C:/Documents and Settings/aa/桌面/ckip2004/1Dic/*.3bpm.txt'
        ##dic={}
        dic = collections.defaultdict(list)
        ##print(flist)
        for fname in eachfilename(flist,1):
            print(fname)
            for line in openUA(fname):
                aa=list(line.strip().split())
                abc=[ BPM.bpm12SU2abc(tt) for tt in aa[2:]]
                dic[aa[0]].append(' '.join(abc))
                ##dic[aa[0]]=' '.join(aa[2:])
        return dic

    def tcpml2vi(flist=''):
        if flist=='':
            flist='c:/c2k/LGO/2give2/*x.tcpml'
        dic = collections.defaultdict(list)
        ##dic={}
        for fname in eachfilename(flist):
            print(fname)
            for line in openUA(fname):
                if line.lstrip().startswith('<sud '):
                    a=xet.fromstring(line)
                    ##dic[a.attrib['v']]=a.attrib['i']
                    dic[a.attrib['v']].append(a.attrib['i'])
        return dic

    def tcpml2set(flist=''):
        if flist=='':
            flist='c:/c2k/LGO/2give2/*x.tcpml'
        dset=set()
        for fname in eachfilename(flist):
            print(fname)
            for line in openUA(fname):
                if line.lstrip().startswith('<sud '):
                    a=xet.fromstring(line)
                    dset.add(a.attrib['v'])
        return dset

    def ckipdic2vi2pickle(fname='ckiprd_vi.pkl'):
        dic = LGO.ckipdic2vi()
        dic['<<::note::>>']=['ckip詞典2004?']
        dic=dict(dic)
        LGO.pickleto(dic, fname)
        return dic

    def tcpml2vi2pickle(fname='dird6vi.pkl'):
        dic = LGO.tcpml2vi()
        dic['<<::note::>>']=['台音字典 6?']
        dic=dict(dic)
        print(fname)
        LGO.pickleto(dic, fname)
        return dic
    def tcpml2set2pickle():
        dset = LGO.tcpml2set()
        fname = 'dird6set.pkl'
        LGO.pickleto(dset, fname)
        return dset
##    def loaddirdvi0():
##        dic={'台灣':'daiuan', '是':'si', '寶島':'bordor'}
##        return dic
##    def loaddirdvi(pickledfname='dird6vi.pkl'):
##        return LGO.unpickle(pickledfname)
##    def loadckipdic_vi(pickledfname='ckiprd_vi.pkl'):
##        return LGO.unpickle(pickledfname)
##    def loaddirdset(pickledfname='dird6set.pkl'):
##        return LGO.unpickle(pickledfname)


def main_hunHL():
##    L = unicodecat.HL_LL();    print(L)
##    L = unicodecat.HL_LN();    print(L)
##    s='εὲέ ə  ə́  ə̌  ə̀	<:ziq:>		ㄜˊ  ㄜˇ  ㄜˋ  ㄜ˙		 ə  ə́  ə̌  ə̀	 ₀₁₂₃₄₅₆₇₈₉ '
    s='dai52-uan55台灣si3     si23是 寶島bor41-dor44 e使'; print(); print(s)
    s=re.sub('\s+',' ',s); aa=LGO.hunHL         (s,keepdash=1); print(aa)
    s=re.sub('\s+',' ',s); aa=LGO.hunHLiterative(s,keepdash=1); print(aa)

    s='   dε₉sə₅tə12sə34₆     dε0₉隨tə12意sə34₆  '; print(); print(s)
    s=re.sub('\s+',' ',s); aa=LGO.hunHLx         (s,keepdash=1); print(aa)
    s=re.sub('\s+',' ',s); aa=LGO.hunHLXiterative(s); print(aa)

    s='  dε0₉隨意tə12意sə34₆。 1984 隨意1984  1984隨意'; print(); print(s)
    s=re.sub('\s+',' ',s); aa=LGO.hunHLx         (s,keepdash=1); print(aa)
    s=re.sub('\s+',' ',s); aa=LGO.hunHLXiterative(s); print(aa)


class sudenIO():
    """ import dictionary in .pyc(.py) : faster than pickle"""
    def di6vi():
        import dic4di6
        return dic4di6.dic
    def ckipvi():
        import dic4ckip
        return dic4ckip.dic
    def LGOWSO():
        import dic4LGOWSO
        return dic4LGOWSO.dic

class segdict():
    def __init__(self, qiqen=None):
        if qiqen=='d' or qiqen=='t'  : self.loadd()
        elif qiqen=='h' or qiqen=='m': self.loadh()
        else:    self.load0()
    def load0(self):
        self.dic={'台灣':'daiuan', '是':'si', '寶島':'bordor'}
        
    def load(self, pickledfname):
        self.dic = LGO.unpickle(pickledfname)
        
    def loadd(self, pickledfname='dird6vi.pkl'):
        self.dic = LGO.unpickle(pickledfname)
        
    def loadh(self, pickledfname='ckiprd_vi.pkl'):
        self.dic = LGO.unpickle(pickledfname)

    def pickledq(self, fname2pickle='dird6vi.pkl'):
        LGO.tcpml2vi2pickle(fname2pickle)

    def picklehq(self, fname2pickle='ckiprd_vi.pkl'):
        LGO.ckipdic2vi2pickle(fname2pickle)

    def note(self):
        return self.dic.get('<<::note::>>','no notes')

    def fmm(self,string, maxEntrylen=5, trace=0):
        aa=LGO.hunHLx(string)
        return fmmList(self.dic,aa,maxEntrylen,trace)
    def bmm(self, string, maxEntrylen=5, trace=0):
        aa=LGO.hunHLx(string)
        return bmmList(self.dic,aa,maxEntrylen,trace)
    def rmm(self, string, maxEntrylen=5, trace=0):
        aa=LGO.hunHLx(string)
        return rmmList(self.dic,aa,maxEntrylen,trace)

def fmm(dic,string, maxEntrylen=5, trace=0):
    aa=LGO.hunHLx(string)
    return fmmList(dic,aa,maxEntrylen,trace)
def bmm(dic, string, maxEntrylen=5, trace=0):
    aa=LGO.hunHLx(string)
    return bmmList(dic,aa,maxEntrylen,trace)
def rmm(dic, string, maxEntrylen=5, trace=0):
    aa=LGO.hunHLx(string)
    return rmmList(dic,aa,maxEntrylen,trace)

def fmmList(dic, arr, maxEntrylen=5, trace=0):
    if dic==None:
        print('no dic'); return []
    rr=[]
    alen=len(arr);
    LEN= min(maxEntrylen, alen)
    B,E=0,LEN
    while True:
        if LEN>1:
            E = B + LEN;
            if E>alen: E=alen; LEN=E-B;
            t=''.join(arr[B:E]);
            if trace>0: print(t)
            if dic.get(t,'')!='':
                rr.append(t)
                B=E
                LEN=min(maxEntrylen,alen-B)
            else:
                LEN-=1
        else:
            if B>=alen: break
            ##rr.append(''.join(arr[B:B+1]))
            ##if trace>0: print(''.join(arr[B:B+1]))
            rr.append(arr[B])
            if trace>0: print(arr[B])
            B=B+1
            LEN=min(maxEntrylen, alen-B)
            if B<alen: continue
            break;
    return rr

def bmmList(dic, arr, maxEntrylen=5, trace=0):
    if dic==None:
        print('no dic'); return []
    rr=[]
    alen=len(arr);
    LEN= min(maxEntrylen, alen)
    E,B=alen,alen-LEN
    while True:
        if LEN>1:
            B = E - LEN;
            if B <0 : B=0; LEN=E-B;
            t=''.join(arr[B:E]);
            if trace>0: print(t)
            if dic.get(t,'')!='':
                rr.insert(0,t)
                E=B
                if E<=0: break;
                LEN=min(maxEntrylen,E)
            else:
                LEN-=1
        else:
            if E<=0 : break
            rr.insert(0,''.join(arr[E-1:E]));
            if trace>0: print(''.join(arr[E-1:E]))
            E-=1; 
            LEN=min(maxEntrylen, E);
            if 0 < E: continue
            break;
    return rr

def rmmList(dic, arr, maxEntrylen=5, trace=0):
    if dic==None:
        print('no dic'); return []
    alen=len(arr);
    LEN= min(maxEntrylen, alen)
    found=False
    B,E=0,LEN
    while not found :
        if LEN<=1: break
        for i in range(alen-LEN+1):
            BB = B+i; EE = BB+LEN;  t=''.join(arr[BB:EE])
            if trace>0: print(t)
            if dic.get(t,'')!='':
                found=True
                B,E=BB,EE
                break
        if found: break
        else : LEN-=1
    rr=[]
    if found:
        rr+=rmmList(dic,arr[:B],maxEntrylen)
        rr.append(''.join(arr[B:E]))
        rr+=rmmList(dic,arr[E:],maxEntrylen)
    else:
        rr+=arr
    return rr


"""
import pickle

data1 = {'a': [1, 2.0, 3, 4+6j],
         'b': ("string", "string using Unicode features \u0394"),
         'c': None}

selfref_list = [1, 2, 3]
selfref_list.append(selfref_list)

output = open('data.pkl', 'wb')

# Pickle dictionary using protocol 2.
pickle.dump(data1, output, 2)

# Pickle the list using the highest protocol available.
pickle.dump(selfref_list, output, -1)

output.close()



import pprint, pickle

pkl_file = open('data.pkl', 'rb')

data1 = pickle.load(pkl_file)
pprint.pprint(data1)

data2 = pickle.load(pkl_file)
pprint.pprint(data2)

pkl_file.close()

"""

class ABC:
    def ordiMethod(a,b,c):
        print(a)
    # 如同 普通函數
    # 使用法：
    #    ABC.ordimethod(aval,bval,cval)
    def clsMethod(cls, a,b,c):
        print(b)
    # class method
    # 使用法：
    #    ABC.clsmethod(aval,bval,cval)
    # 此時 Python 會di 頭前 自動 加入 class-object
    # 可以 方便調用 class data member
    def instMethod(self,a,b,c):
        print(c)
    # instance method
    # 使用法：
    #    abc=ABC()  # 此時 abc 叫做 ABC的 一個object
    #    abc.instMethod(aval,bval,cval)
    # 此時 Python 會di 頭前 自動 加入 instance-object

tbdata=[
'#1170:410.2.[0] S(agent:NP(Head:Nhaa:你)|reason:Dj:為什麼|negation:Dc:不|Head:VC2:養|goal:NP(DUMMY1:NP(quantifier:DM:一隻|Head:Nab:貓)|Head:Caa:或|DUMMY2:NP(quantifier:DM:一隻|Head:Nab:狗))particle:Tc:呢)#。(PERIODCATEGORY)',
'#1935:1935.[9] %(evaluation:Dbb:甚至|Head:P31:對(DUMMY:NP(Head:Nab:民族)))#。(PERIODCATEGORY)',
'#399:399.[9] S(theme:NP(property:VH11:平均|Head:Nv4:買單)|Head:VH11:劇增)condition:PP(HEad:P61:至|DUMMY:NP(Head:DM:每筆|quantifier:DM:十一張)))#，(COMMACATEGORY)',
'#2244:2243.[9] %(Head:Nca:中視|Head:P32:對於|DUMMY:S(agent:S(agent:NP(quantifier:Nes:該|Head:Nac:戲)|Head:VA4:出擊)|deontics:Dbab:能否|Head:VC31:奪得(theme:NP(property:NP‧的(head:NP(property:Nad:收視|Head:Neu:第一)|Head:DE:的)|Head:Nab:寶座))))#，(COMMACATEGORY)',
'',
'#157:157.[0] S(theme:NP(property:Nad:物價|Head:Nad:指數)|Head:VH11:居高不下)#，(COMMACATEGORY)',
'#158:158.[3] S(theme:NP(property:NP(property:Nac:家庭|Head:Naeb:消費)|Head:Nac:型態)|time:Dd:漸|Head:VJ1:呈|goal:NP(property:VH16:兩極化|Head:Nv1:發展))#，(COMMACATEGORY)',
'#159:159.[1] S(agent:NP(quantifier:NP(Head:Neqa:很多)|Head:Nab:人)|listing:Cbba:一方面|manner:VH11:拚命|Head:VE2:打聽|goal:VP(location:NP(Head:Ncdb:哪裡)|deontics:Dbab:可|Head:VC31:買|theme:NP(predication:VP‧的(head:VP(manner:Dh:更|Head:VH13:便宜)|Head:DE:的)|Head:Nab:東西)))#，(COMMACATEGORY)',
'#160:160.[2] S(listing:Cbcb:另方面|evaluation:Dbb:卻|time:Dd:又|goal:PP(Head:P31:對|DUMMY:NP(predication:S‧的(head:S(agent:NP(Head:Nab:名牌)|quantity:Dab:所|Head:VE2:標榜)|Head:DE:的)|Head:N(DUMMY1:Nv4:精緻|Head:Caa:及|DUMMY2:Nad:品質)))|Head:VI1:愛不釋手)#，(COMMACATEGORY)',
'#161:161.[1] VP(manner:DK:如此|Head:VD1:給予|goal:NP(property:Nac:中價位|Head:Ncb:市場)|theme:NP(predication:VP‧的(head:VP(degree:Dfa:極|Head:VH13:大)|Head:DE:的)|property:VC2:發展|Head:Nac:空間))#。(PERIODCATEGORY)',
'#162:162.[9] S(agent:NP(quantifier:DM:一家|property:NP(property:Nv1:進口|Head:Naeb:服飾)|property:Nv1:代理|Head:Nab:業者)|Head:VE2:表示)#，(COMMACATEGORY)',
'#163:163.[9] GP(DUMMY:VP(time:NP(Head:Ndda:過去)|theme:NP(property:Naeb:金錢|Head:Nac:遊戲)|Head:VK2:盛行)|Head:Ng:時)#，(COMMACATEGORY)',
''
]
"""
comparint ''.joind(toLGO6()) and toVGO(), there are differences
1268 你為什麼不養呢一隻貓或一隻狗 你為什麼不養呢 _Chen chou-yu.t.check
1930 甚至對民族 甚至對 _f-7910.9.t.check
395 平均買單PP至每筆十一張 平均買單PP _f-7911.9c.t.check    
2227 中視對於該戲出擊能否奪得收視第一的寶座 中視對於該戲出擊能否奪得 _f-7911.9c.t.check


'#1170:410.2.[0] S(agent:NP(Head:Nhaa:你)|reason:Dj:為什麼|negation:Dc:不|Head:VC2:養|goal:NP(DUMMY1:NP(quantifier:DM:一隻|Head:Nab:貓)|Head:Caa:或|DUMMY2:NP(quantifier:DM:一隻|Head:Nab:狗))particle:Tc:呢)#。(PERIODCATEGORY)',
'#1935:1935.[9] %(evaluation:Dbb:甚至|Head:P31:對(DUMMY:NP(Head:Nab:民族)))#。(PERIODCATEGORY)',
'#399:399.[9] S(theme:NP(property:VH11:平均|Head:Nv4:買單)|Head:VH11:劇增}condition:PP(HEad:P61:至|DUMMY:NP(Head:DM:每筆|quantifier:DM:十一張)))#，(COMMACATEGORY)',
## up 劇增} -> 劇增)
'#2244:2243.[9] %(Head:Nca:中視|Head:P32:對於|DUMMY:S(agent:S(agent:NP(quantifier:Nes:該|Head:Nac:戲)|Head:VA4:出擊)|deontics:Dbab:能否|Head:VC31:奪得(theme:NP(property:NP‧的(head:NP(property:Nad:收視|Head:Neu:第一)|Head:DE:的)|Head:Nab:寶座))))#，(COMMACATEGORY)',

"""
class ckipTBtool():
    """ ckipTBtool.parse(ckipTBline) return a tree in icgnode
        By nature, recursive function tends to be global
    """
    def rcvparse(li, ith):## reverse list item
        token=li[ith]
        if token[0]!='(': return None
        nodes=[];   nli=len(li)
        head=icgnode(token[1:])
        nodes.append(head); nownd=head; nxtit=1
        ith+=1
        while ith<nli:
            token=li[ith];
            if token[0]==':':
                if nxtit==0:##err
                    pass
                elif nxtit==1:
                    nownd.syn=token[1:]
                    nxtit+=1
                else:
                    nownd.txt=token[1:]
                    nxtit+=1
                    ## full-ed, what to do?
                ith+=1
            elif token[0]=='|':
                anode=icgnode(token[1:])
                nodes.append(anode); nownd=anode; nxtit=1
                ith+=1
            elif token[0]=='(' :
                ##ith, nds=ckipTBtool.rcvparse(li, ith)
                ##nownd.chd+=nds
                ## old code fine but tree can be err-ed like
                ##Head:P31:對(DUMMY:NP(Head:Nab:民族))
                ## fix an err like this
                ith, nds=ckipTBtool.rcvparse(li, ith)
                if nxtit<=2:
                    nownd.chd+=nds
                else:## for those case:
                    ##Head:P31:對(DUMMY:NP(Head:Nab:民族))
                    ## makes the nds (DUMMY...) sibling, rather than child
                    nodes+=nds;
                    nownd=nds[-1]
                    nxtit=0                
            elif token[0]==')':
                return ith+1, nodes
            else: ## no leading punctuation: should err, but happens once
                ##print('err************ ', ''.join(li))
                anode=icgnode(token)  
                nodes.append(anode); nownd=anode; nxtit=1
                ith+=1
        ##  else: pass ## no way this can happen
        return ith, [] ## this means coming to an end, un-ballanced ()
    def isbalanced0(line):
        prncnt=0
        for ch in line:
            if ch=='(': prncnt+=1
            elif ch==')': prncnt-=1
            else: continue
            if prncnt<0: return False
        if prncnt!=0: return False
        return True
    def isbalanced(line, trace=0, LNUM='', fname=''):
        good= ckipTBtool.isbalanced0(line)
        if trace>0 and not good:
            star='*'*20+'\n'
            print(star+'**'+LNUM+' '+fname+'\n'+'**unbalanced line :\n'+ star + line + star)
        return good
        
    def parse(ckipTBline, trace=0):
        line=ckipTBline
        if line[0]!='#' or  line.count('#')!=2:
            node =icgnode() ##print(line.count('#'))
            return node
        s1 = re.split('#', line)[1]
        s2 = re.split('\s',s1,1)[1]
        B  = s2.find('(')
        headsyn = s2[:B]
        s3 = s2[B:]
        if not ckipTBtool.isbalanced(s3, trace):
            return icgnode('err unbal','err unbal','err unbal')
        aa = [s4.group() for s4 in re.finditer('([)])|([(:|])*([^(:|)]*)',s3)]
##        aa = [s4.group() for s4 in re.finditer('([(:|)])([^(:|)]*)',s3)]
        if trace>0 :
            print(headsyn + s3);
        if trace>1 :
            print(headsyn);
            for a in aa: print(a)
        head = icgnode('',headsyn)
        ith, head.chd = ckipTBtool.rcvparse(aa,0)
        return head


class icgnode():
    """ iformation-based case grammar node: used in CKIP """
    __slots__ = ('sem', 'syn', 'txt', 'chd')  # restrict the class members
    def __init__(self, sem='', syn='', txt=''):
        self.sem, self.syn, self.txt = sem, syn, txt
        self.chd=[]
    def toWSO(self):        ## Word Separated Orthography
        s=self.txt+' '; 
        for a in self.chd: s+=a.toWSO()
        return s
    def synt(self):
        s=self.syn+' '
        for a in self.chd: s+=a.synt()
        return s
    def sema(self):
        s=self.sem+' '
        for a in self.chd: s += a.sema()
        return s
    def T3(self, trace=0):
        s = ''
        for a in self.chd: s+=a.T3()
        if trace>0: print('slf,chd = ('+self.txt+','+s+')')
        if self.txt:
            s=self.txt+'/'+self.syn+' '
        else:
            s='('+s+')/'+self.syn+' '
        ##print('to return=('+s+')') if trace>0 else ''
        return s
    def txtlen(self):
        cnt = len(self.txt)
        for a in self.chd:
            cnt+=a.txtlen()
        return cnt
    def PLChilds(self):  ## pseudo-leaf childs
        for a in self.chd:
           if len(a.chd)>0: return False
        return True

    def errBalanced(self, line, trace=0, LNUM='', fname=''):
        if not ckipTBtool.isbalanced(line,trace, LNUM, fname): return True
        return False
    def errParse(self):
        if (not self) or len(self.chd)<=0: return True
        return False
    def errLGOorSUB(self, line, trace=0, LNUM='', fname=''):
        sa=self.toVGO()
        sb=re.sub('\s*', '', ' '.join(self.toLGO()))
        if sa!=sb:
            if trace>0 : print(LNUM,'  ', sa, sb, fname)
            return True
        pat4sub = '[a-zA-Z0-9]|‧[得到之地個的]|[得到之地個的]‧|[\[\]()+%！，；、。？_#:;.,|\s]'
        sc=re.sub(pat4sub, '', line)
        sa=re.sub(pat4sub, '', sa)
        if sa!=sc:
            if trace>0:
                print(LNUM,'  ', fname+'\n'+ sa + '\n'+sc, )
            return True
        return False

    def toVGO(self):        ## VorGan Orthography
        s=self.toWSO()
        s=re.sub('\s*','',s)
        return s
    def toLGO(self):        ## LangGeh Orthography
        aa=[]; s=''
        for a in reversed(self.chd):
            if a.PLChilds():
                chdlen=len(a.chd); t=''
                if   chdlen==1: t=a.chd[0].txt
                elif chdlen==2:
                    if len(a.toVGO())<=4: t=a.toVGO();
                elif chdlen==3 and len(a.toVGO())<=5 :
                    if a.chd[1].syn[0]=='C' or a.chd[1].syn=='DE': ## coordinate or DE
                        t=a.toVGO()
                if not t: t=a.txt
            else: t=a.txt
            if t:
                tslen =len(t)+len(s)## t=a.txt+s; tlen=len(t)
                if   tslen <4: s=t+s
                elif tslen==4: aa.insert(0,t+s); s=''
                else         : aa.insert(0,  s); s=t
            else:
                if s: aa.insert(0,s); s=''
                aa=a.toLGO()+aa
        if s: aa.insert(0,s)
        if self.txt: aa.insert(0,self.txt)
        return aa


def main_treebank2():
    for sent in tbdata:
        if len(sent)<=0: break  #continue
        x=ckipTBtool.parse(sent, trace=1)
        print('SEMA  =', x.sema())
        print('SYNT  =', x.synt())
        print('TEXT  =', x.toWSO())
        print('TEXTVG=', x.toVGO())
        print('T3    =', x.T3())
##        print( x.txtlen(), x.toWSO() )
        print(' '.join(x.toLGO()))
        print()
        continue

def main_treebank1():
    ckipTBdir='C:/c2k/LGO/ckip2004/sinica treebank v1.1/*.check'
    TCNT=0
    for fname in eachfilename(ckipTBdir):
        CNT=0
        for line in openUA(fname):
            if line.lstrip()[0]=='#':   CNT+=1
        print ('lines in file', CNT); print(fname)
        TCNT+=CNT
    print('total lines', TCNT)

"""
2009.0227五 : change note to sinica tree-bank 1.1 (4 small changes, 6 remains)
This is after balance check of parathensis (51 errors)
            pat4sub = '[a-zA-Z0-9]|‧[得到之地個的]|[得到之地個的]‧|[\[\]()+%！，；、。？_#:;.,|\s]'
            sc=re.sub(pat4sub, '', line)
            sa=re.sub(pat4sub, '', sa)
            if sa!=sc: print(CNT, fname[43:]+'\n'+ sa + '\n'+sc, )
::
6482 /_f-7910.9.t.check
可是就以上幾點
可是就以上幾點來看
6482: Head:P20[+part]來看   (give up)

1939 /_f-7911.9a.t.check
其餘各項用具及黃平洋的茶壺義賣價約在四萬五十萬元之間不等
其餘各項用具及黃平洋的茶壺義賣價約在四萬五至十萬元之間不等
1939: |Caa:至 (no sematic role)

2384 /_f-7911.9a.t.check
不過這次東元球員甲組聯賽報名截止後
不過這次東元球員在甲組聯賽報名截止後
2384: |Head:P21:在Head:Nab:甲組  -->>  |Head:P21:在|Head:Nab:甲組

4120 /_f-7911.9b.t.check
躉售物價年增率自七月份的下跌
躉售物價年增率自七月份的下跌百分之五點二
4120: |Head;Neqa:百分之五點二   -->> |Head:Neqa:百分之五點二

105 /_f-7911.9c.t.check
及近數月日歐等主要貨幣對美元呈強勢
及近數月來日歐等主要貨幣對美元呈強勢
105:  (DUMMY:DM:近數月|Ng:來)  (no sematic role)

552 /_f-7911.9c.t.check
平均買單至每筆十一張
平均買單劇增}至每筆十一張
552: Head:VH11:劇增}  -->> Head:VH11:劇增|

756 /_f-7911.9c.t.check
中下級到蘇聯
中下級豬肉到蘇聯
756: Head;Naa:豬肉   -->>Head:Naa:豬肉

2716 /_f-7911.9c.t.check
蘇聯軍隊的死亡事件是因為在訓練時的疏忽與意外而不是如媒體所報導對新兵的粗野待遇
蘇聯軍隊的死亡事件是因為在訓練時的疏忽與意外而不是如媒體所報導的對新兵的粗野待遇
2716:  |DE:的  (no sematic role)

4047 /_g-trvl.1.t.check
的大口喝酒大聲高歌
來自各地的遊客大口喝酒大聲高歌
4047: missing too many sematic role

1862 /_g-trvl.3.t.check
導遊會安排你搭上該旅遊線的豪華空調巴士與來自各國或美國其它州的中國人一起去郊遊結束行程回到原點由旅行社專車送回或直接送往機場回台灣這種旅行方式最大特色是極具彈性
導遊會安排你搭上該旅遊線的豪華空調巴士與來自各國或美國其它州的中國人一起去郊遊結束行程回到原點由旅行社專車送回飯店或直接送往機場回台灣這種旅行方式最大特色是極具彈性
1862: |goal:NP(Ncb:飯店)    (no sematic role)
"""
        
def main_treebank3():
    ckipTBdir='C:/c2k/LGO/ckip2004/1sinica treebank v1.1/*.check'
    print('checking ...'); print(ckipTBdir)
    TCNT=0;
    errPCNT=0; errUCNT=0; errLGO=0; errTXTCNT=0
    for fname in eachfilename(ckipTBdir):
        CNT=0; LNUM=0
        for line in openUA(fname):
            LNUM+=1
            ##if line.lstrip()[0]=='#':   CNT+=1
            if line.lstrip()[0]!='#':
                continue
            if not ckipTBtool.isbalanced(line,1):
                errUCNT+=1
                continue
            x=ckipTBtool.parse(line)
            if (not x) or len(x.chd)<=0: 
                errPCNT+=1;
                continue
            sa=x.toVGO()
            sb=re.sub('\s*', '', ' '.join(x.toLGO()))
            if sa!=sb:
                errLGO+=1
                print(LNUM, sa, sb, fname[43:])
                continue
            ##subpat = '[\s'+_LLN+'\[\]()+%！，；、。‧？_#:;.|,得到之地個的]+'
            pat4sub = '[a-zA-Z0-9]|‧[得到之地個的]|[得到之地個的]‧|[\[\]()+%！，；、。？_#:;.,|\s]'
            sc=re.sub(pat4sub, '', line)
            sa=re.sub(pat4sub, '', sa)
            if sa!=sc:
                errTXTCNT+=1
                ##print(LNUM, fname[43:]+'\n'+ sa + '\n'+sc, )
                continue
            CNT+=1
        print('total/ok  = ',LNUM, CNT, fname[43:])
        TCNT+=CNT
    print('total/err =', TCNT, errPCNT, errUCNT, errLGO, errTXTCNT)

def main_treebank4():
    ckipTBdir='C:/c2k/LGO/ckip2004/1sinica treebank v1.1/*.check'
    print('checking ...'); print(ckipTBdir)
    trace=[0,0]
    TCNT=0;
    errPCNT=0; errBCNT=0; errLGO=0;
    for fname in eachfilename(ckipTBdir):
        CNT=0; LNUM=0; fname1=fname[42:]
        for line in openUA(fname):
            LNUM+=1
            if line.lstrip()[0]!='#':   continue
            x=ckipTBtool.parse(line)
            if x.errBalanced(line,trace[0],LNUM,fname1): errBCNT+=1; continue
            if x.errParse(): errPCNT+=1; continue
            if x.errLGOorSUB(line, trace[1], LNUM, fname1): errLGO+=1; continue
            CNT+=1
        print('total/ok  = ',LNUM, CNT, '  ', fname1)
        TCNT+=CNT
    print('total/err =', TCNT, errBCNT, errPCNT, errLGO)


def main_treebank():
##    main_treebank1()
##    main_treebank2()
##    main_treebank3()
    main_treebank4()

class segcounter():
    def __init__(self):
        self.dic=segdict('m')
        self.C1,self.H1,self.V=0,0,0
        self.C2,self.H2=0,0
    def seg2(self, lgo, refs):
        sa=[]
        for a in lgo: sa+=self.dic.bmm(a)
        sr=refs.split()
        ##print(LCS.lcslen(sa,sr), sa, sr)
        self.C1+=LCS.lcslen(sa,sr)
        self.H1+=len(sa)
        self.V+=len(sr)
        sb=''.join(sa)
        sb=self.dic.bmm(sb)
        self.C2+=LCS.lcslen(sb,sr)
        self.H2+=len(sb)
        

def main_ckip2LGO2seg():
##    dic = segdict('m')
    counter=segcounter()
    ckipTBdir='C:/c2k/LGO/ckip2004/1sinica treebank v1.1/*.check'
    TCNT=0; trace=[0,0]; CNT=0; THRSH=200000000000
    errPCNT=0; errBCNT=0; errLGO=0;
    for fname in eachfilename(ckipTBdir):
        CNT=0; LNUM=0; fname1=fname[42:]
        for line in openUA(fname):
            LNUM+=1
            if line.lstrip()[0]!='#':   continue
            x=ckipTBtool.parse(line)
            if x.errBalanced(line,trace[0],LNUM,fname1): errBCNT+=1; continue
            if x.errParse(): errPCNT+=1; continue
            if x.errLGOorSUB(line, trace[1], LNUM, fname1): errLGO+=1; continue
            CNT+=1
            sr=x.toWSO()
            sa=x.toLGO()
            counter.seg2(sa,sr)
            if CNT >THRSH: break
        print(CNT,fname1)
        if CNT >THRSH: break
    print ('lgo seg')
    print (counter.C1, counter.H1, counter.V)
    print (counter.C1/counter.H1, counter.C1/counter.V)
    print ('vgo seg')
    print (counter.C2, counter.H2, counter.V)
    print (counter.C2/counter.H2, counter.C2/counter.V)

def groupLGOVGO(lgo, wso):
    beg, end,N=0,1,len(wso)
    ret=[]
    for sf in lgo:
        while end<N and sf!=''.join(wso[beg:end]): end+=1
        ee=sf + ' '+ ' '.join(wso[beg:end]);
        ret.append(ee)
        beg,end=end, end+1
    return ret

def main_ckipLGOVGO():    
##    dic = segdict('m')
##    counter=segcounter()
    dic = collections.defaultdict(int)
    ckipTBdir='C:/c2k/LGO/ckip2004/1sinica treebank v1.1/*.check'
    TCNT=0; trace=[0,0]; CNT=0; THRSH=2000000000000
    errPCNT=0; errBCNT=0; errLGO=0;
    for fname in eachfilename(ckipTBdir):
        CNT=0; LNUM=0; fname1=fname[42:]
        for line in openUA(fname):
            LNUM+=1
            if line.lstrip()[0]!='#':   continue
            x=ckipTBtool.parse(line)
            if x.errBalanced(line,trace[0],LNUM,fname1): errBCNT+=1; continue
            if x.errParse(): errPCNT+=1; continue
            if x.errLGOorSUB(line, trace[1], LNUM, fname1): errLGO+=1; continue
            CNT+=1
            aws=x.toWSO(); aws=aws.split()
            alg=x.toLGO()
            ret=groupLGOVGO(alg,aws)
            ##print(ret)
            for it in ret: dic[it]+=1
##            counter.seg2(sa,sr)
            if CNT >THRSH: break
        print(CNT,fname1)
        if CNT >THRSH: break
    return dic
            
def main_ckipmanual():
    fname='ckipmanualseg2lgo.txt'
    a=''
    for line in openUA(fname):
        pass

class Counter():
    def __init__(self, CNT=10):
        self.CNT=CNT
        self.cnt=0
    def isout(self):
        if self.CNT>0 and self.cnt>=self.CNT: return True
        return False
    def inc(self):
        self.cnt+=1
    def inc2out(self):
        self.cnt+=1
        return self.isout()

def check_hanririsu(ifname):
    ifhand=openR(ifname)
    dline, mline='',''
    for line in ifhand:
        line = line.lstrip()
        if len(line)==0: continue
        if line.startswith('.d.'):
            if len(mline)>0 :
                print('prev M line not matched \n'+line)
                break
            dline=line
        elif line.startswith('.m.'):
            if len(dline)<=0:
                print('this M line not matched \n'+line)
                break
            mline=line
            dline,mline='',''
        elif line.startswith('.o.'):
            if dline != '' or mline!='':
                print('lines not matched: \ndline\n'+dline+'\nmline\n'+mline+'\noline\n'+line)
        else:
            print('dangling line: \n'+line)

def main_hanririsu():
    pname='C:/Documents and Settings/aa/My Documents/2009.論漢字字序問題/'
    ifname='論漢字字序問題 台華語對譯 2009-3全文.txt'
    ofname='論漢字字序問題 台華語對譯 2009-3全文-d.txt'
##    check_hanririsu(pname+ifname);    return
    ifhand=openR(pname+ifname)
    ofhand=openW(pname+ofname)
    cnt = Counter(-1)
    cntpair=Counter(-1)
    hasD,hasM= False, False
    dline,mline='',''
    for line in ifhand:
        #print(line)
        ##if cnt.inc2out(): break
        cnt.inc()
        line = line.lstrip()
        if len(line)==0: continue
        if line.startswith('.d.'):
            if len(mline)>0 :
                print('prev mline not matched \n'+line)
                break
            dline=line
        elif line.startswith('.m.'):
            if len(dline)<=0:
                print('this mline not matched \n'+line)
                break
            mline=line
            cntpair.inc()
            ofhand.writelines(dline[3:])
            dline,mline='',''
        elif line.startswith('.o.'):
            if dline != '' or mline!='':
                print('lines not matched: \ndline\n'+dline+'\nmline\n'+mline+'\noline\n'+line)
                continue
            ofhand.writelines(line)  ## leave '.o.' mark
        else:
            print('dangling line: \n'+line)
            ofhand.writelines('***'+line)
    ofhand.close()
    ifhand.close()
    print(cnt.cnt, cntpair.cnt)


def main_4gbh():
    ifname='四角筆形rd5a-1.xml'
    from xml.etree.ElementTree import ElementTree
    tree=ElementTree()
    ee=tree.parse(ifname)
    return ee

def main_catdata():
    ifname='tmp.txt'
    ifhand=openR(ifname)
    import collections as col
    dic = col.defaultdict(int)
    for line in ifhand:
        line=line.strip()
        if not line: continue
        dic[line]+=1
    vk=sorted([(v,k) for k,v in dic.items()])
    for v,k in vk:
        print("{0}\t{1}".format(k,v))
    print(len(vk))

def main_hutging2a(dic, ipname, ifname):
    ifhand=openR(ipname+ifname)
    iline, rline='',''
    cnt=0
##    dic=collections.defaultdict(int)
    for line in ifhand:
        cnt+=1
        line=line.strip()
##        line=line.replace('。','')
##        line=line.replace('，','')
##        line=line.replace('、','')
##        line=line.replace('、','')##different char?
##        line=line.replace('（','')
##        line=line.replace('）','')
##        line=line.replace('(','')
##        line=line.replace(')','')
        line=re.sub('[。，、、（）()]','',line)
        if not line: continue
        if not iline: iline=line; continue
        if not rline: rline=line; ## continue
        ilist = iline.split()
        rlist = rline.split()
        if len(ilist)!=len(rlist):
            print(cnt-1,'\n',ilist,'\n', rlist)
            iline,rline='',''
        for i,r in zip(ilist,rlist):
            if i=='n': continue
            if i.startswith('nq'): i='ng'+i[2:]
            if i.startswith('q'): i='gh'+i[1:]
            if i.startswith('v'): i='bh'+i[1:]
            if i=='it¬6': print(ifname,'\n',cnt,iline,'\n',rline)
            dic[r+' '+i]+=1
        iline,rline='',''
        ilist,rlist=[],[]
    print('done \t', ifname)

def main_hutging2():
    ipname='C:/Documents and Settings/aa/My Documents/2009.04.佛經3種/txt/'
    ifnames=['金剛經2005.4.txt','彌陀經2005.4.txt','普門品2005.4.txt','藥師經2005.4.txt',
             '地藏經上2009.4.txt','地藏經中2009.4.txt','地藏經下2009.4.txt',
             '法華經卷第一修正2-98.12.11.txt','法華經卷第二修正2-98.12.11.txt',
             '法華經卷第三修正2-98.12.11.txt','法華經卷第四修正2-98.12.11.txt',
             '法華經卷第五修正2-98.12.11.txt','法華經卷第六修正2-98.12.11.txt',
             '法華經卷第七修正2-98.12.11.txt'
             ]
    dic = collections.defaultdict(int)
    for ifn in ifnames:
        main_hutging2a(dic, ipname, ifn)
    kv=sorted([(k,v) for k,v in dic.items()])
    ofname='2009.4.佛經14卷發音詞典.052.txt'
    ofhand=openW(ipname+ofname)
    for k,v in kv:
        ofhand.writelines(k+'   \t'+str(v)+'\t\r\n')
        ##print(k+'   \t', v, '\t')
    ofhand.close(); print('done\t', ofname)

def main_hutging3():
    ipname='C:/Documents and Settings/aa/My Documents/2009.04.佛經3種/txt/'
    ipname='C:/Documents and Settings/aa/My Documents/2009.04.佛經3種/supn/'
    ifnames=['supn金剛經2005.4.txt','supn彌陀經2005.4.txt','supn普門品2005.4.txt','supn藥師經2005.4.txt',
             'supn地藏經上2009.4.txt','supn地藏經中2009.4.txt','supn地藏經下2009.4.txt',
             'supn法華經卷第一修正2-98.12.11.txt','supn法華經卷第二修正2-98.12.11.txt',
             'supn法華經卷第三修正2-98.12.11.txt','supn法華經卷第四修正2-98.12.11.txt',
             'supn法華經卷第五修正2-98.12.11.txt','supn法華經卷第六修正2-98.12.11.txt',
             'supn法華經卷第七修正2-98.12.11.txt'
             ]
    dic = collections.defaultdict(int)
    for ifn in ifnames:
        print('doing\t', ifn)
        main_hutging2a(dic, ipname, ifn)
    kv=sorted([(k,v) for k,v in dic.items()])
    ofname='2009.4.佛經14卷發音詞典.053.txt'
    ofhand=openW(ipname+ofname)
    for k,v in kv:
        kk = k.split()
        ofhand.writelines(kk[0]+'\t'+kk[1]+'\t'+str(v)+'\t\n')
        ##ofhand.writelines(k+'   \t'+str(v)+'\t\r\n')
        ##print(k+'   \t', v, '\t')
    ofhand.close(); print('done \t', ofname)

def main_hutging1():
    ipname='C:/Documents and Settings/aa/My Documents/2009.04.佛經3種/txt/'
##    ifname='金剛經2005.4.txt'
##    ifname='彌陀經2005.4.txt'
##    ifname='普門品2005.4.txt'
##    ifname='藥師經2005.4.txt'
##    ifname='地藏經上2009.4.txt'
##    ifname='地藏經中2009.4.txt'
##    ifname='地藏經下2009.4.txt'
##    ifname='法華經卷第一修正2-98.12.11.txt'
##    ifname='法華經卷第二修正2-98.12.11.txt'
##    ifname='法華經卷第三修正2-98.12.11.txt'
##    ifname='法華經卷第四修正2-98.12.11.txt'
##    ifname='法華經卷第五修正2-98.12.11.txt'
##    ifname='法華經卷第六修正2-98.12.11.txt'
    ifname='法華經卷第七修正2-98.12.11.txt'
    ifhand=openR(ipname+ifname)
    iline, rline='',''
    cnt=0
    dic=collections.defaultdict(int)
    for line in ifhand:
        cnt+=1
        line=line.strip()
        line=line.replace('。','')
        line=line.replace('，','')
        line=line.replace('、','')
        line=line.replace('、','')##different char?
        if not line: continue
        if not iline: iline=line; continue
        if not rline: rline=line; ## continue
        ilist = iline.split()
        rlist = rline.split()
        if len(ilist)!=len(rlist):
            print(cnt-1,'\n',ilist,'\n', rlist)
            iline,rline='',''
        iline,rline='',''
        for i,r in zip(ilist,rlist):
            if i=='n': continue
            dic[r+' '+i]+=1
        ilist,rlist=[],[]
    print('done')
    return
    kv=sorted([(k,v) for k,v in dic.items()])
    for k,v in kv:
        print(k,v)

def main_hutging():
##    main_hutging2()
    main_hutging3()

def main_華語音節分類():
    ifn="華語音節表外交部2008.txt"
    ifh=openR(ifn)
    dicH={}
    dicV={}
    dicN={}
    dic1={}
    for line in ifh:
        if line.startswith('##'): continue
        items = line.split()
        if items[1][0] == '-': continue
        if items[0][-1] in "ㄢㄤㄣㄥ":
            dicN[items[0]]=items[1]
        elif len(items[0])==1:
            dic1[items[0]]=items[1]
        elif len(items[0])==2:
            if items[0][-1] in "ㄚㄛㄝㄜㄧㄨㄩㄦ":
                dicH[items[0]]=items[1]
            else:
                dicV[items[0]]=items[1]
        else:
            dicV[items[0]]=items[1]
    for k,v in sorted(dicH.items()):
        print(k+'\t'+v)
    print()
    for k,v in sorted(dicV.items()):
        print(k+'\t'+v)
    print()
    for k,v in sorted(dicN.items()):
        print(k+'\t'+v)
    print()
    for k,v in sorted(dic1.items()):
        print(k+'\t'+v)
    print()
    print( len(dic1)+len(dicH)+len(dicV)+len(dicN) )


def eachline(afilelist):
    for fname in eachfilename(afilelist):
        fhand=openR(fname)
        for line in fhand:
            yield line.rstrip()

def pickkind(dic, kind):
    if kind=="nn":
        mm=[ki for ki in dic if ki[-1] in "mng"]
        mm=[ki for ki in mm if ki.endswith("nn")]
    elif kind=="mng":
        mm=[ki for ki in dic if ki[-1] in "mng"]
        mm=[ki for ki in mm if not ki.endswith("nn")]
    elif kind=="ptkh":
        mm=[ki for ki in dic if ki[-1] in "ptkh"]
    elif kind=="ptk":
        mm=[ki for ki in dic if ki[-1] in "ptk"]
    elif kind=="h":
        mm=[ki for ki in dic if ki[-1]=='h']
    elif kind=='aeiour':
        mm=[ki for ki in dic if ki[-1] in "aeiour"]
        mm=[ki for ki in mm if len(ki)>2]
    else: mm=[]
    mm.sort()
    return mm
        

def main_台語音節():
    pat='i="([a-zA-Z]+)[0-9]+"'
    dlist="./2give2/*-1.tcpml"
    cnt=0
    dic=collections.defaultdict(int)
    for line in eachline(dlist):
        if line.startswith("<sud "):
            cnt+=1
            aaa=re.split(pat,line)
            if len(aaa)<3: continue
            ##print(len(aaa),aaa[1],"\t")
            ##print(aaa[1],end="\t")
            dic[aaa[1]]+=1
    print (cnt, len(dic))
##    for k,v in dic.items():
##        print(k,v,end="\t")
##    mm=[ki for ki in dic.keys() if ki[-1] in "mng"]
##    mm=[ki for ki in mm if not ki.endswith('nn')]
##    mm.sort()
##    mm=pickkind(dic,"aeiour")
##    mm=pickkind(dic,"mng")
##    mm=pickkind(dic,"ptk")
##    mm=pickkind(dic,"nn")
    mm=pickkind(dic,"h")
    for ii in mm : print (ii)
    print(len(mm))









if __name__ == '__main__' :
##    xmpfilelist()
##    main_toSPH()
##    countwords('C:/c2k/2008tmp台華對譯資料/flist.txt')
##    main_allpairs()
##    main_StrEdit()
##    main_LCS()
##    mainPCC()
##    main_DZB()
##    main_hunHL()
##    main_treebank()
##    main_ckip2LGO2seg()
##    main_ckipLGOVGO()
##    main_hanririsu()
##    main_4gbh()
##    main_catdata()
##    main_hutging()
##    main_華語音節分類()
##    main_台語音節()
##    beamsearch()
##    main_LGC('C:/c2k/2008tmp台華對譯資料/20080102資料庫文章/*.21d.txt')
##    xmplcls.xmpl(1,2)
    pass


