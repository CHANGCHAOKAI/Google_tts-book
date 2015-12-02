import os
import wave#**
import xml.etree.ElementTree#**
import codecs
import re
from LGO import *

#
# 這支程式 myHtkTwEdu.py 是運用Htk
# 來為一批台灣教育部製作的台語朗讀語音資料庫(TwEdu)
# 作自動音標對位(Phonetic Alignment)的工作 
#
#	語音資料庫是由2位台語老師錄製，原有台文文字稿，採漢羅文，
#	我們找人為其聽音轉寫成音標符號，並人工切音至句子的層次。
#	
#	採用Transcriber 的格式存放切音及音標，Combine001.trs
#	並以Microsoft .wav的格式存放語音，Combine001.wav
#		 
#	Combine001.trs,  Combine001.wav ---> [ myHtkTwEdu.py ] ---> Combine001_aligned.trs
#

def 此句過關(s): # 這個函數主要是要過濾文字資料中一些「不太好」的句子。

	def 此句全是ASCII(s):
	
		if len(s)==0: return False
	
		ans=True
		for n in range(len(s)):
			c=s[n]
			if ord(c) >= 128:
				ans=False
				break
		return ans

	def 此句全是字母數字(s):
	
		if len(s)==0: return False
	
		ans=True
		for n in range(len(s)):
			c=s[n]
			if not c.isalnum():
				ans=False
				break
		return ans
	
	ans = True
	#if not 此句全是ASCII(s):
	if 此句全是ASCII(s) is not True:
		ans = False
		return ans
	for syl in s.split('_'):
		#if not 此句全是字母數字(syl):
		if 此句全是字母數字(syl) is not True:
			ans = False
			return ans
	return ans

def 把一個trs轉換成多個lab檔(trsFn='Combine001.trs'):

    #trsDir='../ryAudioBook/'  #'c:/TwEdu/'

    trs=xml.etree.ElementTree.parse(trsFn)

    root=trs.getroot()

    audio_filename= root.attrib['audio_filename']+'.wav'
    print('audio_filename=',audio_filename)

    endTime=root[0][0].attrib['endTime']
    print('endTime=',endTime)

    audio_time_in_sec = float(endTime)
    t_endTime = int(audio_time_in_sec*1e7)
    
    S=[]
    T=[]
    for a in root.getchildren():
        for b in a.getchildren():
            for c in b.getchildren():
                for d in c.getchildren():

                    if d.tag=='Sync':

                        t=d.attrib['time']

                        t = int(float(t)*1e7)
                        s=d.tail
                        if s.find('//')>=0:
                            s=s.split('//')[-1].rstrip('\n').rstrip(' ').rstrip('\n')
                        else:
                            continue
                        T.append(t)
                        S.append(s)
                        #print(t,s,file=f)
    T.append(t_endTime)
    #print(T)
    '''
    labFn = trsFn.replace('.trs','.lab')
    badFn = trsFn.replace('.trs','.bad')
    '''
    labFn = trsFn.split('/')[-1].replace('.trs','.lab')
    badFn = trsFn.split('/')[-1].replace('.trs','.bad')
    
    f_lab=open(labFn,mode='w',encoding='utf-8')
    f_bad=open(badFn,'w',encoding='utf8')

    
    S0=[]
    for s in S:
        #if s=='': continue

        s=s.rstrip('\n').rstrip('-')
        s=s.replace('-,-','_sil_')
        s=s.replace('-,','_sil_')
        s=s.replace(',-','_sil_')
        s=s.replace(',','_sil_')
        s=s.replace('-','_')
        s=s.replace(' ','_')
        s=s.replace('!','')
        s=s.replace('.','_')
        #s=s.replace('__','_')
        s=s.replace('Ā','ā')
        s=s.replace('È','è')
        s=s.replace('Ě','ě')
        s=s.replace('ā','a1')
        s=s.replace('á','a2')
        s=s.replace('ǎ','a3')
        s=s.replace('à','a4')
        s=s.replace('ē','e1')
        s=s.replace('é','e2')
        s=s.replace('ě','e3')
        s=s.replace('è','e4')
        s=s.replace('ī','i1')
        s=s.replace('í','i2')
        s=s.replace('ǐ','i3')
        s=s.replace('ì','i4')
        s=s.replace('ō','o1')
        s=s.replace('ó','o2')
        s=s.replace('ǒ','o3')
        s=s.replace('ò','o4')
        s=s.replace('ū','u1')
        s=s.replace('ú','u2')
        s=s.replace('ǔ','u3')
        s=s.replace('ù','u4')
        s=s.replace('ǚ','u')
        if s!='':
                s='sil_'+s+'_sil'
        for i in range(10):
            s=s.replace(str(i),'')
        s=s.replace('__','_')
        S0.append(s)
    S=S0
    #print(len(T),len(S))
    for n in range(len(S)):
        s=S[n].lower()
        if s!='':
            print(T[n],' ',T[n+1],' ',s, file=f_lab)
        '''
        if 此句過關(s):
            print(T[n],' ',T[n+1],' ',s, file=f_lab)
        else:
            print(T[n],' ',T[n+1],' ',s, file=f_bad)
        '''    
    f_lab.close()
    f_bad.close()
    return audio_time_in_sec

def 把長語音檔切割成短語音檔(wavFn):
	
   #global	語音總時間
	
   #fnIn='Combine001.wav'
   #fnOut='Combine001_00.wav'
	
    fnIn=wavFn#trsFn.replace('.trs','.wav')
    #語音總時間=audio_time_in_sec
    #fnLab=fnIn.replace('.wav','.lab').replace('C:/TwEdu/','')
    fnLab=fnIn.replace('.wav','.lab').replace('cgualign_lite/Input/','')
    #print(fnLab)
    #f=open(fnLab)
    f=open(fnLab,'r',encoding='utf8')
    #f=open(fnLab,'r',encoding='utf-8')
    lines=f.readlines()
    f.close()
    #print(lines[0])
    #lines[0]=lines[0].replace('\ufeff','')
	
    #for i in range(len(lines)):
    #    lines[i]=lines[i].replace('\ufeff','')
    #    lines[i]=lines[i].replace('\r','\n')
    #print(lines)
    T=[]
    for l in lines:
        #print(l)
        t=l.split()
	#print(len(t),t)
        t0=int(t[0])/1e7
        t1=int(t[1])/1e7
        s=t[2].rstrip('\n')
        T.append([t0,t1,s])

    #wavDir='' # '../ryAudioBook/' #C:/TwEdu/'
    wavIn = wave.open (fnIn, "rb")
    #wavOut = wave.open (fnOut, "wb")
    params=wavIn.getparams()
    (nChannels, sampWidth, frameRate, nFrames, compType, compName) = params
    語音總時間 = nFrames/frameRate
    print('語音總時間=', 語音總時間)
    #exit(0)
    #dirName=trsFn.replace('.trs','')
    dirName = wavFn.split('/')[-1].rstrip('.wav')
    os.system('mkdir '+dirName)
    fnOut = dirName+'/SN'
    n=0
    for t in T:
        pos0 = int(frameRate * t[0])## 起始點
        nFrames = int(frameRate * (t[1]-t[0]))## 持續時間
        wavIn.setpos(pos0)
        data = wavIn.readframes (nFrames * nChannels)
        pos1 = wavIn.tell()##讀完後停在此處。
        #print(nFrames, pos0,pos1)
        wavOut = wave.open (fnOut+str(n)+'.wav', "wb");
        params=(nChannels, sampWidth, frameRate, nFrames, compType, compName)
        wavOut.setparams(params)
        wavOut.writeframes(data)
        wavOut.close()
        labOut =open(fnOut+str(n)+'.lab',"w",encoding='utf-8');
        #labOut =open(fnOut+str(n)+'.lab',"w",encoding='utf8');
        labOut.write('0 '+ str(int(1e7*nFrames/frameRate))+' '+t[2]+'\n')  ### This is HTK Lab format
        labOut.close()
        n+=1
    wavIn.close()
    n=0
    spWav_scp=''
    spLab_scp=''
    spWav2Mfc_scp=''
    spMfc_scp=''
    for t in T:
        spWav_scp += fnOut+str(n)+'.wav' +'\n'
        spLab_scp += fnOut+str(n)+'.lab' +'\n'
        spWav2Mfc_scp +=  fnOut+str(n)+'.wav' +'\t' + fnOut+str(n)+'.mfc'+'\n'
        spMfc_scp +=  fnOut+str(n)+'.mfc'+'\n'
        n+=1
    
    f=open('spWav.scp','a')
    f.write(spWav_scp)
    f.close()
    f=open('spLab.scp','a')
    f.write(spLab_scp)
    f.close()
    f=open('spWav2Mfc.scp','a')
    f.write(spWav2Mfc_scp)
    f.close()
    f=open('spMfc.scp','a')
    f.write(spMfc_scp)
    f.close()
    '''
    f=open('spWav.scp','a',encoding='utf-8-sig')
    f.write(spWav_scp)
    f.close()
    f=open('spLab.scp','a',encoding='utf-8-sig')
    f.write(spLab_scp)
    f.close()
    f=open('spWav2Mfc.scp','a',encoding='utf-8-sig')
    f.write(spWav2Mfc_scp)
    f.close()
    f=open('spMfc.scp','a',encoding='utf-8-sig')
    f.write(spMfc_scp)
    f.close()
    '''
def 建立Hmm原型(N=1,M=1,D=39,fileName=''):
	
	#global hmm原型檔名
	hmm原型檔名='myHmmPro'   #  這一行是在此新加的，原先是設定為global變數
	
	if fileName=='':	fileName=hmm原型檔名
	dotPosition=fileName.find('.')
	if dotPosition>=0:	fileName=fileName[0:dotPosition]
	
	print ('\n\nCreateHProto....\n',fileName,'\nN = ',N,'M = ',M,'\n\n')
	hProto= '~h '+ '"'+fileName +'"'+'\n' \
			+ '~o <VecSize> '+str(D) +'\n' \
			+'<MFCC_0_D_A> <StreamInfo> 1 '+ str(D)+'\n' \
			+'\n<BeginHMM>'+'\n'

	
	hProto += '<NumStates> '+ str(N+2) +'\n'
	
	for state in range(2,N+2): # 2...(N+1)
		hProto +='\n'
		hProto += ' <State> '+ str(state) +' '+' <NumMixes> '+str(M) +' <Stream> 1 '+'\n'
		
		for mixture in range(1, M+1): # 1...M
			hProto += '  <Mixture> '+str(mixture) + ' ' +str(1.0/M) +'\n'
			
			hProto += '   <Mean> '+str(D) +'\n'
			hProto += '    '
			for i in range(D):
				hProto += str(0)+' '
			hProto += '\n'
			
			hProto += '   <Variance> '+str(D) +'\n'
			hProto += '    '
			for i in range(D):
				hProto += str(1)+' '
			hProto += '\n'
	
	hProto += '\n<TransP> '+str(N+2) +'\n'

	
	for i in range(0,1):
		hProto +=' '
		for j in range(0,N+2):
			if j==1: aij=1.0
			else: aij=0.0
			hProto += str(aij)+' '
		hProto += '\n'
	for i in range(1,N+1):
		hProto +=' '
		for j in range(0,N+2):
			if j==i: aij=0.6
			elif j==(i+1): aij=0.4
			else: aij=0.0
			hProto += str(aij)+' '
		hProto += '\n'
	for i in range(N+1,N+2):
		hProto +=' '
		for j in range(0,N+2):
			aij=0.0
			hProto += str(aij)+' '
		hProto += '\n'
	
	hProto += '\n'+'<EndHMM>'+'\n'

   
	#fileName= 'hProto.hmm' 檔名似乎得和 ~h "..." 中一致，否則會出錯, .hmm 沒關係 
	f=open(fileName,'w')
	#f=open(fileName,'w',encoding='utf-8-sig')
	f.write(hProto)
	f.close()
	
	return hProto

def htk00_製造各個HtkTool所需的參數檔():

	hLed_led='''
	#### hLed.led
	EX    # expand word into phone
	'''
	
	hLed00_led='''
	#### hLed00.led
	#EX    # expand word into phone
	'''
	
	hCopy_conf='''
	 SOURCEKIND     = WAVEFORM
	 TARGETKIND     = MFCC_0 	#12d(MFCC)+1d(E) = 13d
	 SOURCEFORMAT   = WAV #NIST	#TIMIT
	 SOURCERATE     = 625    	# T=625e-7 sec ==> Fs = 16KHz
	 TARGETRATE     = 100000  	# 10 ms
	 
	 ENORMALISE=F   # for realtime test
		
	'''
	
	hInit_conf='''

	TARGETKIND = MFCC_0_D_A
	SAVEGLOBOPTS = TRUE
	
	KEEPDISTINCT=F
		
	'''
	
	hRest_conf='''

	TARGETKIND = MFCC_0_D_A
	SAVEGLOBOPTS = TRUE
	
	KEEPDISTINCT=F
		
	'''
	
	hErest_conf='''

	TARGETKIND = MFCC_0_D_A
	SAVEGLOBOPTS = TRUE
	
	KEEPDISTINCT=T
	BINARYACCFORMAT=T
		
	'''
	
	hVite_conf='''

	TARGETKIND = MFCC_0_D_A
	SAVEGLOBOPTS = TRUE
	
	KEEPDISTINCT=F
	BINARYACCFORMAT=F
		
	'''

	f=open('hLed.led','w')
	f.write(hLed_led)
	f.close()
	
	f=open('hLed00.led','w')
	f.write(hLed00_led)
	f.close()
	
	f=open('hCopy.conf','w')
	f.write(hCopy_conf)
	f.close()

	f=open('hInit.conf','w')
	f.write(hInit_conf)
	f.close()

	f=open('hRest.conf','w')
	f.write(hRest_conf)
	f.close()
	
	f=open('hErest.conf','w')
	f.write(hErest_conf)
	f.close()
	
	f=open('hVite.conf','w')
	f.write(hVite_conf)
	f.close()
	
	
	建立Hmm原型(N=3,M=6)  ###<<<<<<<<<<<<<<<<<<<<<<<

def htk01_處裡語音標籤及詞典():

        os.system('hled -A -i spLab00.mlf -n spLab00.lst -S spLab.scp  hLed00.led')

        os.system('hled -A -i spLab.mlf -n spLab.lst -S spLab.scp  hLed.led')

        lst2dic()

        os.system('hled -A -i spLab_p.mlf -n spLab_p.lst -S spLab.scp -I spLab.mlf -d spLab_p.dic hLed.led')

def lst2dic():

	f=open('spLab.lst',encoding='utf-8')
	lines=f.readlines()
	f.close()

	lines.sort()  ## htk.dic 需要 sort
	
	f=open('spLab.lst','w',encoding='utf-8')
	for l in lines:
		f.write(l)
	f.close()

	#global mList
	#mList=[]
	D=''
	Dp=''
	for l in lines:
		d=l.rstrip('\n')
		D += d+' '+d+'\n'
		
		if d=='sil' or len(d)<2:
			ps=d
		else: #(len(d))>=2:
			ps=''
			for n in range(len(d)-1):
				ps += d[n]+d[n+1]+' '
			
		Dp += d+' '+ps+'\n'
		
		#mList.append(d)
	f=open('spLab.dic','w',encoding='utf-8')
	f.write(D)
	f.close()

	f=open('spLab_p.dic','w',encoding='utf-8')
	f.write(Dp)
	f.close()

def htk02_擷取語音特徵及訓練語音模型():

	os.system('hcopy -A -C hCopy.conf -S spWav2Mfc.scp')
	
	
	os.system('mkdir hmms_p')

	
	f=open('spLab_p.lst',encoding='utf-8')
	lines=f.readlines()
	f.close()
	
	mList=[]
	for l in lines:
		m = l.strip('\n')
		mList.append(m)
	m = 'myHCompV'
	os.system('HCompV -A -C hInit.conf  -S spMfc.scp -m -I spLab_p.mlf -M hmms_p/ -o '+m+' myHmmPro')
	
	f=open('hmms_p/'+m)
	myHCompV=f.read()
	f.close()
	
	for m in mList:
		myModel=myHCompV.replace('myHCompV',m)
		f=open('hmms_p/'+m,'w',encoding='utf-8')
		f.write(myModel)
		f.close()
	'''
	for m in mList:
		os.system('HInit -A -C hInit.conf  -S spMfc.scp  -I spLab_p.mlf -m 1 -i 10 -l '+m+' -M hmms_p/ -o '+m+' hmms_p/'+m)

	for m in mList:	
		os.system('HRest -A -C hRest.conf   -S spMfc.scp -I spLab_p.mlf -m 1 -i 10 -u tmvw -w 3 -v 0.05 -l '+m+' -M hmms_p/ hmms_p/'+m)
	'''
	for i in range(5):
		print('[%d]HERest '%i)
		os.system('HERest -A -C hErest.conf  -S spMfc.scp -p 1 -t 2000.0 -w 3 -v 0.05 -I spLab_p.mlf -M hmms_p -d hmms_p/ spLab_p.lst')
		os.system('HERest -A -C hErest.conf -p 0 -t 2000.0 -w 3 -v 0.05 -I spLab_p.mlf -M hmms_p/ -d hmms_p/ spLab_p.lst hmms_p/HER1.acc')

def htk03_語音文字對齊():

	os.system('HVite -A -C hVite.conf  -S spMfc.scp  -a -d hmms_p/ -i spLab_aligned.mlf -I spLab.mlf spLab_p.dic spLab_p.lst')
	

def toTrs(trsFn,語音總時間長度): # 仍有待改進
	print("-----\n"+trsFn+"\n------\n")
	fileName = trsFn.split('/')[-1].rstrip('.trs')
	fileName=trsFn.split('/')[-1][0:len(trsFn.split('/')[-1])-4]
	print("-----\n"+fileName+"\n------\n")
	總時間=str(語音總時間長度)
	
	f=open('spLab_aligned.mlf',encoding='utf-8')
	lines=f.readlines()
	f.close()
	syls=lines
	
	f=open(fileName+'.lab',encoding='utf-8')
	lines=f.readlines()
	f.close()
	sens=lines
	
	n=0
	B=[]
	E=[]
	#for n in range(len(syls)):
	while n<len(syls):
		s=syls[n]
		if s.find('"'+fileName)>=0:
			B.append(n+1)
			n+=1
			s=syls[n]
			while(s[0]!='.'):
				n+=1
				s=syls[n]
			E.append(n-1)
		n+=1
	trsFile = open(fileName+'_aligned.trs',mode='w',encoding='utf-8')
	labFile = open(fileName+'_aligned.lab',mode='w',encoding='utf-8')
	
	
	####
	#### 這個trs檔頭，和檔尾，我只是從  Combine001.trs copy過來，
	#### 還有待自動化，特別是在這裡不分Turn了，那裏會出包，小心一下 
	####	主要是時間總長度的欄位要小心一下

	#global 語音總時間  		## 從Combine001.wav 那裏挖出來的，
	
	#總時間 = 語音總時間 #2613.577
	
	dirFnName=fileName

	file_head='''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Trans SYSTEM "trans-14.dtd">
<Trans scribe="wjLabtoTrs" audio_filename="'''+dirFnName+'''">
<Episode>
<Section type="report" startTime="0" endTime="'''+總時間+'''">
<Turn startTime="0" endTime="'''+總時間+'''">'''
	file_tail='''</Turn>
</Section>
</Episode>
</Trans>'''
	print(file_head,file=trsFile)
	s0_pre=0.0
	s1_pre=0.0
	
	#for i in range(len(B)):
	for i in range(len(sens)):
		#print(sens[i])
		t0=int(sens[i].split()[0])
		
		#print(i,B[i],E[i])
		print(len(B),len(E),len(syls))
		
		for n in range(B[i],E[i]+1):
			#print(syls[n])
			syl=syls[n].split()
			
			
			s0=t0+int(syl[0])
			s1=t0+int(syl[1])
			s2=syl[2].rstrip('\n')
			#print(s0,s1,s2,file=labFile)
			
			
			s0 /= 1e7
			s1 /= 1e7
			#print(s0,s1,s2)
			print('%.3f'%s0,'%.3f'%s1,s2,file=labFile)
			if s0 != s1_pre:
				print('<Sync time="%.3f"/>'%s0,file=trsFile)
			print(s2,file=trsFile)
			print('<Sync time="%.3f"/>'%s1,file=trsFile)
			
			s0_pre = s0
			s1_pre = s1
		labFile.write('\n')
	

	print(file_tail,file=trsFile)
	trsFile.close()
	labFile.close()
	#print(fileName)
	os.system('copy %s %s'
                  %(fileName
                    +'_aligned.trs','cgualign_lite\\Output\\切到字的trs檔\\'
                    +fileName
                    +'_aligned.trs'))
	os.system('copy %s %s'
                  %(fileName
                    +'_aligned.lab','cgualign_lite\\Output\\切到字的lab檔\\'
                    +fileName
                    +'_aligned.lab'))

def 主程式():

	# @Mac
	#trsFn='../ryAudioBook/TwEduCombine001.trs'
	#wavFn='../ryAudioBook/TwEduCombine001.wav'
	
	# @Windows
	trsFn='Combine001.trs'
	wavFn='Combine001.wav'

	語音總時間長度=把一個trs轉換成多個lab檔(trsFn)
		
	把長語音檔切割成短語音檔(wavFn)
	htk00_製造各個HtkTool所需的參數檔()
	htk01_處裡語音標籤及詞典()
	htk02_擷取語音特徵及訓練語音模型()
	htk03_語音文字對齊()
			
	toTrs(trsFn,語音總時間長度)
	
#################################################
## wj
#################################################
def 建立資料夾():

    os.makedirs('cgualign_lite/Output')
    os.makedirs('cgualign_lite/Output/切到句的srt檔')
    os.makedirs('cgualign_lite/Output/切到字的trs檔')
    os.makedirs('cgualign_lite/Output/切到字的lab檔')
    os.makedirs('cgualign_lite/Output/切到字的lrc檔')
    os.makedirs('cgualign_lite/Output/切到字的sbv檔')
	
def 讀取檔案(檔案名稱):
    f=open(檔案名稱,'r',encoding='utf-8')
    T=f.read()
    f.close()
    檔案內容=T
    return(檔案內容)
	
def 將字串內容存成一行(檔案內容):
    檔案內容=檔案內容.split('\n')
    所有時間=[]
    所有字串=[]
    累積字串=''
    for i in range(len(檔案內容)):
        if 檔案內容[i].count(':')==4:
            所有時間.append(檔案內容[i])
        else:
            if 檔案內容[i]!='':
                累積字串=累積字串+檔案內容[i]+' '
            else:
                所有字串.append(累積字串)
                累積字串=''
    #所有字串.remove('')
    #print(len(所有時間),len(所有字串))
    #print(所有字串[0])
    return(所有時間,所有字串)
	
def 轉換時間格式(時間):
    開始時間=[]#取出,前的時間
    for i in range(len(時間)):
        x=時間[i].split(',')[0]
        x=x.split(':')
        x[0]=float(x[0])
        x[1]=float(x[1])
        x[2]=float(x[2])
        y=x[0]*3600+x[1]*60+x[2]
        y='%.3f'%y
        開始時間.append(y)
    #print(開始時間[201])
    return(開始時間)

def 轉成切到句的trs檔(檔名,時間,字串):
    waveFile='cgualign_lite/Input/'+檔名+'.wav'
    wavIn=wave.open(waveFile,'rb')
    params=wavIn.getparams()
    (nChannels, sampWidth, frameRate, nFrames, compType, compName)=params
    語音總時間=nFrames/frameRate
    總時間=str(語音總時間)
    trsFile=open('cgualign_lite/Input/'+檔名+'.trs',mode='w',encoding='utf8')
    head_str='''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Trans SYSTEM "trans-14.dtd">
<Trans scribe="wjLabtoTrs" audio_filename="'''+waveFile+'''">
<Episode>
<Section type="report" startTime="0" endTime="'''+總時間+'''">
<Turn startTime="0" endTime="'''+總時間+'''">'''
    tail_str='''</Turn>
</Section>
</Episode>
</Trans>'''
    print(head_str,file=trsFile)
    for i in range(len(時間)):
        print('<Sync time="'+時間[i]+'"/>',file=trsFile)
        trsFile.write(字串[i].replace('&','and')+'//')
        字串[i]=字串[i].replace('`','')
        字串[i]=字串[i].replace(',','')
        字串[i]=字串[i].replace('?','')
        字串[i]=字串[i].replace('.','')
        字串[i]=字串[i].replace('%','')
        字串[i]=字串[i].replace('^','')
        字串[i]=字串[i].replace('*','')
        字串[i]=字串[i].replace('(','')
        字串[i]=字串[i].replace(')','')
        字串[i]=字串[i].replace('[','')
        字串[i]=字串[i].replace(']','')
        字串[i]=字串[i].replace('\'','')
        字串[i]=字串[i].replace('\"','')
        字串[i]=字串[i].replace(':','')
        字串[i]=字串[i].replace(';','')
        字串[i]=字串[i].replace('!','')
        字串[i]=字串[i].replace('-','')
        字串[i]=字串[i].replace('--','')
        ######Han 2015 0615#####
        字串[i]=字串[i].replace('「',' ')
        字串[i]=字串[i].replace('」',' ')
		######Han 2015 0615#####
        字串[i]=字串[i].replace('&','and')
        print(字串[i],file=trsFile)
    print(tail_str,file=trsFile)
    trsFile.close()

def 轉成切到句的srt檔(音標檔案名稱,對齊後時間,對齊後字串):
    s=[]
    for i in range(len(對齊後時間)):
        s.append(對齊後時間[i].replace(',','-->'))
    srtFile=open('cgualign_lite/Output/切到句的srt檔/'+音標檔案名稱+'.srt',mode='w',encoding='UTF-8-sig')
    for i in range(len(s)-1):
        print(i+1,file=srtFile)
        print(s[i],file=srtFile)
        print(對齊後字串[i]+'\n',file=srtFile)
    srtFile.close()
	
def 將trs檔的時間與對應字串轉成多個lab檔(trsFn):
    語音總時間長度=把一個trs轉換成多個lab檔(trsFn)
    return(語音總時間長度)
	
def 將長語音檔依照lab檔所對應的時間來切割成多個短語音檔(wavFn):
    把長語音檔切割成短語音檔(wavFn)
	
def 製造各個HtkTool所需的參數檔():
    htk00_製造各個HtkTool所需的參數檔()
	
def 處裡語音標籤及詞典():
    htk01_處裡語音標籤及詞典()
	
def 擷取語音特徵及訓練語音模型():
    htk02_擷取語音特徵及訓練語音模型()
	
def 將語音文字做對齊():
    htk03_語音文字對齊()
	
def 轉成切到字的trs檔(trsFn,語音總時間長度):
    toTrs(trsFn,語音總時間長度)

def 小數點進位(時間):
    
    for i in range(len(時間)):
        時間[i]=float(時間[i])
        時間[i]='%.3f'%時間[i]
    return(時間)

def 將sil接到上一個音標(音標內容):
    
    一行的字串=音標內容.split('\n')
    #print(type(一行的字串))
    以空白分割一行字串=[]
    所有開始時間=[]
    開始時間們=[]
    所有結束時間=[]
    所有音標=[]
    累積字串=''
    for i in range(len(一行的字串)-1):
        一行的字串[i]=一行的字串[i].replace('\r','')
        以空白分割一行字串.append(一行的字串[i].split(' '))
        分割時間與音標=以空白分割一行字串[i]
        if 分割時間與音標[0]!='':
            分割時間與音標[0]=float(分割時間與音標[0])
            分割時間與音標[1]=float(分割時間與音標[1])
            分割時間與音標[0]='%.3f'%分割時間與音標[0]
            分割時間與音標[1]='%.3f'%分割時間與音標[1]
        if len(以空白分割一行字串[i])!=1: 
            if 分割時間與音標[2]=='sil':
                if i!=0:
                    累積字串=累積字串+分割時間與音標[2]+'_'
                    累積字串=累積字串.replace(' sil_','_sil ')
                    累積字串=累積字串.replace('@_sil','@')
            else:
                累積字串=累積字串+分割時間與音標[2]+' '
                if 以空白分割一行字串[i-1][2]=='sil':
                    所有開始時間.append(以空白分割一行字串[i-1][0])
                else:
                    所有開始時間.append(分割時間與音標[0])
                #所有開始時間.append(分割時間與音標[0])
            開始時間們.append(分割時間與音標[0])
            所有結束時間.append(分割時間與音標[1])
            '''    
            s1=分割時間與音標[0]
            s2=分割時間與音標[1]
            t=分割時間與音標[2]
            '''     
        else:
            '''
            t1='@'
            #t2='@'
            s='@'
            '''
            所有開始時間.append('@')
            累積字串=累積字串+'@ '
    所有音標=累積字串.split(' ')
    所有音標.remove('')
    #print(len(開始時間們),len(所有結束時間))
    d=dict(zip(開始時間們,所有結束時間))
    #d=dict(zip(所有開始時間,所有音標))
    #print(以空白分割一行字串[1][2])
    #print(len(所有開始時間),len(所有音標),所有開始時間[7517],所有音標[7517])
    '''
    wjFile=open('01.txt',mode='w',encoding='utf-8')
    for i in range(len(所有開始時間)):
        if 所有開始時間[i]!='':
            print(所有開始時間[i]+' '+所有音標[i],file=wjFile)
    wjFile.close()
    '''
    return(所有開始時間,所有音標,d)

def 將trs檔時間與文字存成字典(檔名):
    
    trs=xml.etree.ElementTree.parse(檔名)
    root=trs.getroot()
    #audio_filename= root.attrib['audio_filename']+'.wav'
    #endTime=root[0][0].attrib['endTime']
    X=[]
    Y=[]
    T=[]
    S=[]
    for a in root.getchildren():
        for b in a.getchildren():
            for c in b.getchildren():
                for d in c.getchildren():
                    if d.tag=='Sync':
                        t=d.attrib['time']
                        if 檔名=='Combine011':
                            t=float(t)
                            if t >= 1586.784:#Combine011
                                t=t+46
                            if t >= 1950.855:#Combine011
                                t=t+50
                            t=str(t)
                        else:
                            s=d.tail
                            if s.find('//')>=0:
                                #x=s.split('//')[0].replace('\n','')
                                #y=s.split('//')[-1].rstrip('\n').rstrip(' ').rstrip('\n')
                                s=s.replace('\n','')
                                s=re.sub(r'\（.*?\）|','',s)
                                x=s.split('//')[0].replace('\n','')
                                if x=='':
                                    #print(s)
                                    x=s.split('//')[-1].replace('\n','')
                                y=s.split('//')[-1].rstrip('\n').rstrip(' ').rstrip('\n')
                            else:
                                x=s
                                y=s
                                #continue
                            if x.find('\n')<0 and x!='':
                                T.append(t)#Time
                                X.append(x)#漢字
                                Y.append(y)#音標
                                S.append(s)#漢字&音標
    #d=dict(zip(T,X))
    #print(d['598.3610625'])
    #print(len(T),len(X))
    T=小數點進位(T)
    #print(T[0],S[0])
    #print(X[0],Y[0])
    d=dict(zip(T,X))
    #print(d['603.0960625'])
    '''
    #檔名=檔名.replace('原文trs(句)/','中間過程測試/').replace('.trs','.txt')
    wjFile=open('02.txt',mode='w',encoding='utf-8')
    for i in range(len(T)):
        print(T[i]+' '+X[i],file=wjFile)
    wjFile.close()
    '''
    #print(len(T))
    return(T,X)

def 原文句字對齊音標(音標時間,音標字串,句子時間,句子字串,開始時間對應結束時間字典):
    
    S=[]#字數們
    t=[]#一句開頭時間
    c=0#紀錄一句的字數
    a=0#少的句子數
    音標字典=dict(zip(音標時間,音標字串))
    trs字典=dict(zip(句子時間,句子字串))
    for i in range(len(音標時間)):
        if 音標時間[i]!='@':
            if c==0:
                t.append(音標時間[i])
            c=c+1
        else:
            S.append(c)
            c=0
    d=dict(zip(t,S))#一句開頭時間對應一句的字數
    #print(len(S),len(t))
    #print(len(句子時間))
    s1=set(句子時間)
    s2=set(t)
    #比較兩個時間list
    #print(s2.difference(s1))#檢查音標在原文無出現的時間點
    #print(s1.difference(s2))
    沒有的時間=s1.difference(s2)
    沒有的時間=list(沒有的時間)
    for i in range(len(沒有的時間)):
        沒有的時間[i]=float(沒有的時間[i])
    list.sort(沒有的時間)
    沒有的時間=小數點進位(沒有的時間)
    沒有的時間字串=[]
    for i in range(len(沒有的時間)):
        沒有的時間[i]=str(沒有的時間[i])
        沒有的時間字串.append(trs字典[沒有的時間[i]])
    沒有的時間對應字串字典=dict(zip(沒有的時間,沒有的時間字串))
    #print(沒有的時間)
    #print(len(沒有的時間),len(沒有的時間字串))
    '''
    for i in range(len(句子時間)-len(沒有的時間)-1):
        for j in range(len(沒有的時間)):
            if 句子時間[i+1]==沒有的時間[j]:
                句子字串[i]=句子字串[i]+句子字串[i+1]
                句子字串[i+1]=''
                句子字串.remove(句子字串[i+1])
                句子時間.remove(沒有的時間[j])
                #句子字串.remove(句子字串[i+1])
                #print(i,j)

    '''
    for i in range(len(句子時間)-len(沒有的時間)-1):
        for j in range(len(沒有的時間)):
            if 句子時間[i+1]==沒有的時間[j]:
                #句子字串[i]=句子字串[i]+句子字串[i+1]
                #句子字串[i+1]=''
                句子字串.remove(句子字串[i+1])
                句子時間.remove(沒有的時間[j])
                #句子字串.remove(句子字串[i+1])
                #print(i,j)
    #print(len(句子時間))
    
    原文字典=dict(zip(句子時間,句子字串))
    A1=[]#LGO.py分漢羅
    A2=[]
    for i in range(len(句子時間)):
        if 句子時間[i]!='':
            A=原文字典[句子時間[i]]
            B=LGO.hunHLX(A)
            D=[]
            for j in range(len(B)):
                if B[j].isdigit():
                    C=LGO.hunHL(B[j])
                    for k in range(len(C)):
                        D.append(C[k])
                else:
                    if re.match("[\u4e00-\u9fa5]",B[j]):
                        E=LGO.hunHL(B[j])
                        for l in range(len(E)):
                            D.append(E[l])
                    else:
                        if B[j]!='':
                            D.append(B[j])
            A1.append(D)
            D=[]
    #去除空白字串
    for i in range(len(A1)):
        a1=A1[i]
        a2=[]
        for j in range(len(a1)):
            if a1[j]!=' ':
                a2.append(a1[j])
        A2.append(a2)
        a2=[]
    C=[]
    
    #處理標點符號(僅限於教育部閩南語朗讀)如run其他data要在此增加標點符號處理
    for i in range(len(A2)):
        B=A2[i]
        x=''
        for j in range(len(B)):
            if B[j]=='﹐' or B[j]=='~' or B[j]==',' or B[j]=='?' or B[j]=='!' or B[j]=='，' or B[j]=='『' or B[j]=='』' or B[j]=='？' or B[j]=='、' or B[j]=='…' or B[j]=='。' or B[j]=='「' or B[j]=='」' or B[j]=='？' or B[j]=='-' or B[j]=='！' or B[j]=='：' or B[j]=='—'or B[j]=='；' or B[j]=='﹐'or B[j]=='…' or B[j]=='.' or B[j]=='*' or B[j]=='--' or B[j]=='"' or B[j]=='[*' or B[j]=='?' or B[j]=='-' or B[j]=='-' or B[j]==']' or B[j]=='\'' or B[j]=='\'"' or B[j]=='"]' or B[j]==',' or B[j]=='"--' or B[j]=='.' or B[j]=='"':
                x=x+B[j]
                x=x.replace(' ~','~ ')
                x=x.replace(' ,',', ')
                x=x.replace(' ?','? ')
                x=x.replace(' !','! ')
                x=x.replace(' ，','， ')
                x=x.replace(' 『','『 ')
                x=x.replace(' 』','』 ')
                x=x.replace(' ？','？ ')
                x=x.replace(' 、','、 ')
                x=x.replace(' …','… ')
                x=x.replace(' 。','。 ')
                x=x.replace(' 「','「 ')
                x=x.replace(' 」','」 ')
                x=x.replace(' -','- ')
                x=x.replace(' ！','！ ')
                x=x.replace(' ：','： ')
                x=x.replace(' —','— ')
                x=x.replace(' ；','； ')
                x=x.replace(' .','. ')
                x=x.replace(' ﹐','﹐ ')
                x=x.replace(' ,',', ')
                x=x.replace(' ?','? ')
                x=x.replace(' .','. ')
                x=x.replace(' %','% ')
                x=x.replace(' ^','^ ')
                x=x.replace(' *','* ')
                x=x.replace(' (','( ')
                x=x.replace(' )',') ')
                x=x.replace(' [','[ ')
                x=x.replace(' ]','] ')
                x=x.replace(' \'','\' ')
                x=x.replace(' \"','\" ')
                x=x.replace(' :',': ')
                x=x.replace(' ;','; ')
                x=x.replace(' !','! ')
                x=x.replace(' -','- ')
            else:
                x=x+B[j]+' '
        x=x.split(' ')
        for k in range(len(x)):
            if x[k]=='':
                c+=1#統計空字串個數
        for k in range(c):
            x.remove('')
        c=0
        C.append(x)
        #print()
        x=''
    句子個數=[]
    for i in range(len(句子時間)):
        個數=len(C[i])
        句子個數.append(個數)
    #print(len(句子時間),len(句子個數))
    D=dict(zip(句子時間,句子個數))#原句時間對應個數字典
    對齊後時間=[]
    對齊後字串=[]
    音標時間去除區隔符號=[]
    音標字串去除區隔符號=[]
    for i in range(len(音標時間)):
        if 音標時間[i]!='@':
            音標時間去除區隔符號.append(音標時間[i])
            音標字串去除區隔符號.append(音標字串[i])
            #print(音標時間[i])
    #print(len(音標時間))
    q=0
    #print(len(t),len(句子時間))
    '''
    for i in range(len(t)):
        if t[i]==句子時間[i]:
            #print(i)
            if d[t[i]]==D[句子時間[i]]:
                for j in range(d[t[i]]):
                    if q==0:
                        對齊後時間.append(音標時間去除區隔符號[q])
                        q=q+1
                    else:
                        對齊後時間.append(音標時間去除區隔符號[q])
                        q=q+1
                    對齊後字串.append(C[i][j])
                    #print(音標時間去除區隔符號[i+j],C[i][j])
            else:
                q+=d[t[i]]
                對齊後時間.append(句子時間[i])
                對齊後字串.append(句子字串[i])
                #print(句子時間[i],句子字串[i])
    '''
    
    for i in range(len(t)):
        if t[i]==句子時間[i]:
            #print(i)
            if d[t[i]]==D[句子時間[i]]:
                for j in range(d[t[i]]):
                    if q==0:
                        if j==0:
                            對齊後時間.append(開始時間對應結束時間字典[音標時間去除區隔符號[q]])
                        q=q+1
                    else:
                        if j==0:
                            對齊後時間.append(開始時間對應結束時間字典[音標時間去除區隔符號[q]])
                        else:
                            對齊後時間.append(音標時間去除區隔符號[q])
                        q=q+1
                    對齊後字串.append(C[i][j])
                    #print(音標時間去除區隔符號[i+j],C[i][j])
            else:
                q+=d[t[i]]
                對齊後時間.append(句子時間[i])
                對齊後字串.append(句子字串[i])
    #print(len(對齊後時間))
    for i in range(len(沒有的時間)):
        對齊後時間.append(沒有的時間[i])
    for i in range(len(對齊後時間)):
        對齊後時間[i]=float(對齊後時間[i])
    list.sort(對齊後時間)
    對齊後時間=小數點進位(對齊後時間)
    #print(len(對齊後時間),len(對齊後字串))
    for i in range(len(對齊後時間)):
        對齊後時間[i]=str(對齊後時間[i])
    #print(沒有的時間)
    for i in range(len(對齊後時間)):
        for j in range(len(沒有的時間)):
            if 對齊後時間[i]==沒有的時間[j]:
                對齊後字串.insert(i,沒有的時間對應字串字典[沒有的時間[j]])
    #print(len(對齊後時間),len(對齊後字串))

    '''
    for k in range(len(沒有的時間)):
        for i in range(len(t)):
            if t[i]!=沒有的時間[k]:
                if t[i]==句子時間[i]:
                    #print(i)
                    if d[t[i]]==D[句子時間[i]]:
                        for j in range(d[t[i]]):
                            if q==0:
                                if j==0:
                                    對齊後時間.append(開始時間對應結束時間字典[音標時間去除區隔符號[q]])
                                q=q+1
                            else:
                                if j==0:
                                    對齊後時間.append(開始時間對應結束時間字典[音標時間去除區隔符號[q]])
                                else:
                                    對齊後時間.append(音標時間去除區隔符號[q])
                                q=q+1
                            對齊後字串.append(C[i][j])
                            #print(開始時間對應結束時間字典[音標時間去除區隔符號[q]],C[i][j])
                    else:
                        q+=d[t[i]]
                        對齊後時間.append(句子時間[i])
                        對齊後字串.append(句子字串[i])
            else:
                對齊後時間.append(沒有的時間[k])
                對齊後字串.append(沒有的時間對應字串字典[沒有的時間[k]])
    '''
    #print(q)
    #wjFile=open('wjTest0514A2.txt',mode='w',encoding='utf-8-sig')
    #for i in range(len(句子時間)):
    #    wjFile.write(句子時間[i]+' ')
    #    print(句子個數[i],file=wjFile)
    #print(A2,file=wjFile)
    #wjFile.close()
    return(對齊後時間,對齊後字串)
    #return(A1)
def 英原文句字對齊音標(音標時間,音標字串,句子時間,句子字串,開始時間對應結束時間字典):
    
    S=[]#字數們
    t=[]#一句開頭時間
    c=0#紀錄一句的字數
    a=0#少的句子數
    音標字典=dict(zip(音標時間,音標字串))
    trs字典=dict(zip(句子時間,句子字串))
    for i in range(len(音標時間)):
        if 音標時間[i]!='@':
            if c==0:
                t.append(音標時間[i])
            c=c+1
        else:
            S.append(c)
            c=0
    d=dict(zip(t,S))#一句開頭時間對應一句的字數
    #print(len(S),len(t))
    #print(len(句子時間))
    s1=set(句子時間)
    s2=set(t)
    #比較兩個時間list
    #print(s2.difference(s1))#檢查音標在原文無出現的時間點
    #print(s1.difference(s2))
    沒有的時間=s1.difference(s2)
    沒有的時間=list(沒有的時間)
    for i in range(len(沒有的時間)):
        沒有的時間[i]=float(沒有的時間[i])
    list.sort(沒有的時間)
    沒有的時間=小數點進位(沒有的時間)
    沒有的時間字串=[]
    for i in range(len(沒有的時間)):
        沒有的時間[i]=str(沒有的時間[i])
        沒有的時間字串.append(trs字典[沒有的時間[i]])
    沒有的時間對應字串字典=dict(zip(沒有的時間,沒有的時間字串))
    #print(沒有的時間)
    #print(len(沒有的時間),len(沒有的時間字串))
    '''
    for i in range(len(句子時間)-len(沒有的時間)-1):
        for j in range(len(沒有的時間)):
            if 句子時間[i+1]==沒有的時間[j]:
                句子字串[i]=句子字串[i]+句子字串[i+1]
                句子字串[i+1]=''
                句子字串.remove(句子字串[i+1])
                句子時間.remove(沒有的時間[j])
                #句子字串.remove(句子字串[i+1])
                #print(i,j)

    '''
    for i in range(len(句子時間)-len(沒有的時間)-1):
        for j in range(len(沒有的時間)):
            if 句子時間[i+1]==沒有的時間[j]:
                #句子字串[i]=句子字串[i]+句子字串[i+1]
                #句子字串[i+1]=''
                句子字串.remove(句子字串[i+1])
                句子時間.remove(沒有的時間[j])
                #句子字串.remove(句子字串[i+1])
                #print(i,j)
    #print(len(句子時間))
    
    原文字典=dict(zip(句子時間,句子字串))
    A1=[]#LGO.py分漢羅
    A2=[]
    for i in range(len(句子時間)):
        if 句子時間[i]!='':
            A=原文字典[句子時間[i]]
            B=LGO.hunHLX(A)
            D=[]
            for j in range(len(B)):
                if B[j].isdigit():
                    C=LGO.hunHL(B[j])
                    for k in range(len(C)):
                        D.append(C[k])
                else:
                    if re.match("[\u4e00-\u9fa5]",B[j]):
                        E=LGO.hunHL(B[j])
                        for l in range(len(E)):
                            D.append(E[l])
                    else:
                        if B[j]!='':
                            D.append(B[j])
            A1.append(D)
            D=[]
    #去除空白字串
    for i in range(len(A1)):
        a1=A1[i]
        a2=[]
        for j in range(len(a1)):
            if a1[j]!=' ':
                a2.append(a1[j])
        A2.append(a2)
        a2=[]
    C=[]
    
    #處理標點符號(僅限於教育部閩南語朗讀)如run其他data要在此增加標點符號處理
    for i in range(len(A2)):
        B=A2[i]
        x=''
        for j in range(len(B)):
            if B[j]=='﹐' or B[j]=='~' or B[j]==',' or B[j]=='?' or B[j]=='!' or B[j]=='，' or B[j]=='『' or B[j]=='』' or B[j]=='？' or B[j]=='、' or B[j]=='…' or B[j]=='。' or B[j]=='「' or B[j]=='」' or B[j]=='？' or B[j]=='-' or B[j]=='！' or B[j]=='：' or B[j]=='—'or B[j]=='；' or B[j]=='﹐'or B[j]=='…' or B[j]=='.' or B[j]=='*' or B[j]=='--' or B[j]=='"' or B[j]=='[*' or B[j]=='?' or B[j]=='-' or B[j]=='-' or B[j]==']' or B[j]=='\'' or B[j]=='\'"' or B[j]=='"]' or B[j]==',' or B[j]=='"--' or B[j]=='.' or B[j]=='"':
                x=x+B[j]
                x=x.replace(' ~','~ ')
                x=x.replace(' ,',', ')
                x=x.replace(' ?','? ')
                x=x.replace(' !','! ')
                x=x.replace(' ，','， ')
                x=x.replace(' 『','『 ')
                x=x.replace(' 』','』 ')
                x=x.replace(' ？','？ ')
                x=x.replace(' 、','、 ')
                x=x.replace(' …','… ')
                x=x.replace(' 。','。 ')
                x=x.replace(' 「','「 ')
                x=x.replace(' 」','」 ')
                x=x.replace(' -','-')
                x=x.replace(' ！','！ ')
                x=x.replace(' ：','： ')
                x=x.replace(' —','—')
                x=x.replace(' ；','； ')
                x=x.replace(' .','. ')
                x=x.replace(' ﹐','﹐ ')
                x=x.replace(' ,',', ')
                x=x.replace(' ?','? ')
                x=x.replace(' .','. ')
                x=x.replace(' %','% ')
                x=x.replace(' ^','^ ')
                x=x.replace(' *','* ')
                x=x.replace(' (','( ')
                x=x.replace(' )',') ')
                x=x.replace(' [','[ ')
                x=x.replace(' ]','] ')
                x=x.replace(' \'','\'')
                x=x.replace(' \"','\" ')
                x=x.replace(' :',': ')
                x=x.replace(' ;','; ')
                x=x.replace(' !','! ')
                x=x.replace(' -','-')
            else:
                x=x+B[j]+' '
                x=x.replace(' ~','~')
                x=x.replace(' ,',',')
                x=x.replace(' ?','?')
                x=x.replace(' !','!')
                x=x.replace(' ，','，')
                x=x.replace(' 『','『')
                x=x.replace(' 』','』')
                x=x.replace(' ？','？')
                x=x.replace(' 、','、')
                x=x.replace(' …','…')
                x=x.replace(' 。','。')
                x=x.replace(' 「','「')
                x=x.replace(' 」','」')
                x=x.replace(' - ','-')
                x=x.replace(' ！','！')
                x=x.replace(' ：','：')
                x=x.replace(' — ','—')
                x=x.replace(' ；','；')
                x=x.replace(' .','.')
                x=x.replace(' ﹐','﹐')
                x=x.replace(' ,',',')
                x=x.replace(' ?','?')
                x=x.replace(' .','.')
                x=x.replace(' %','%')
                x=x.replace(' ^','^')
                x=x.replace(' *','*')
                x=x.replace(' (','(')
                x=x.replace(' )',')')
                x=x.replace(' [','[')
                x=x.replace(' ]',']')
                x=x.replace(' \'','\'')
                x=x.replace(' \"','\"')
                x=x.replace(' :',':')
                x=x.replace(' ;',';')
                x=x.replace(' !','!')
                x=x.replace(' - ','-')
        x=x.split(' ')
        for k in range(len(x)):
            if x[k]=='':
                c+=1#統計空字串個數
        for k in range(c):
            x.remove('')
        c=0
        C.append(x)
        #print()
        x=''
    句子個數=[]
    for i in range(len(句子時間)):
        個數=len(C[i])
        句子個數.append(個數)
    #print(len(句子時間),len(句子個數))
    D=dict(zip(句子時間,句子個數))#原句時間對應個數字典
    對齊後時間=[]
    對齊後字串=[]
    音標時間去除區隔符號=[]
    音標字串去除區隔符號=[]
    for i in range(len(音標時間)):
        if 音標時間[i]!='@':
            音標時間去除區隔符號.append(音標時間[i])
            音標字串去除區隔符號.append(音標字串[i])
            #print(音標時間[i])
    #print(len(音標時間))
    q=0
    #print(len(t),len(句子時間))
    '''
    for i in range(len(t)):
        if t[i]==句子時間[i]:
            #print(i)
            if d[t[i]]==D[句子時間[i]]:
                for j in range(d[t[i]]):
                    if q==0:
                        對齊後時間.append(音標時間去除區隔符號[q])
                        q=q+1
                    else:
                        對齊後時間.append(音標時間去除區隔符號[q])
                        q=q+1
                    對齊後字串.append(C[i][j])
                    #print(音標時間去除區隔符號[i+j],C[i][j])
            else:
                q+=d[t[i]]
                對齊後時間.append(句子時間[i])
                對齊後字串.append(句子字串[i])
                #print(句子時間[i],句子字串[i])
    '''
    
    for i in range(len(t)):
        if t[i]==句子時間[i]:
            #print(i)
            if d[t[i]]==D[句子時間[i]]:
                for j in range(d[t[i]]):
                    if q==0:
                        if j==0:
                            對齊後時間.append(開始時間對應結束時間字典[音標時間去除區隔符號[q]])
                        q=q+1
                    else:
                        if j==0:
                            對齊後時間.append(開始時間對應結束時間字典[音標時間去除區隔符號[q]])
                        else:
                            對齊後時間.append(音標時間去除區隔符號[q])
                        q=q+1
                    對齊後字串.append(C[i][j])
                    #print(音標時間去除區隔符號[i+j],C[i][j])
            else:
                q+=d[t[i]]
                對齊後時間.append(句子時間[i])
                對齊後字串.append(句子字串[i])
    #print(len(對齊後時間))
    for i in range(len(沒有的時間)):
        對齊後時間.append(沒有的時間[i])
    for i in range(len(對齊後時間)):
        對齊後時間[i]=float(對齊後時間[i])
    list.sort(對齊後時間)
    對齊後時間=小數點進位(對齊後時間)
    #print(len(對齊後時間),len(對齊後字串))
    for i in range(len(對齊後時間)):
        對齊後時間[i]=str(對齊後時間[i])
    #print(沒有的時間)
    for i in range(len(對齊後時間)):
        for j in range(len(沒有的時間)):
            if 對齊後時間[i]==沒有的時間[j]:
                對齊後字串.insert(i,沒有的時間對應字串字典[沒有的時間[j]])
    #print(len(對齊後時間),len(對齊後字串))

    '''
    for k in range(len(沒有的時間)):
        for i in range(len(t)):
            if t[i]!=沒有的時間[k]:
                if t[i]==句子時間[i]:
                    #print(i)
                    if d[t[i]]==D[句子時間[i]]:
                        for j in range(d[t[i]]):
                            if q==0:
                                if j==0:
                                    對齊後時間.append(開始時間對應結束時間字典[音標時間去除區隔符號[q]])
                                q=q+1
                            else:
                                if j==0:
                                    對齊後時間.append(開始時間對應結束時間字典[音標時間去除區隔符號[q]])
                                else:
                                    對齊後時間.append(音標時間去除區隔符號[q])
                                q=q+1
                            對齊後字串.append(C[i][j])
                            #print(開始時間對應結束時間字典[音標時間去除區隔符號[q]],C[i][j])
                    else:
                        q+=d[t[i]]
                        對齊後時間.append(句子時間[i])
                        對齊後字串.append(句子字串[i])
            else:
                對齊後時間.append(沒有的時間[k])
                對齊後字串.append(沒有的時間對應字串字典[沒有的時間[k]])
    '''
    #print(q)
    #wjFile=open('wjTest0514A2.txt',mode='w',encoding='utf-8-sig')
    #for i in range(len(句子時間)):
    #    wjFile.write(句子時間[i]+' ')
    #    print(句子個數[i],file=wjFile)
    #print(C,file=wjFile)
    #wjFile.close()
    return(對齊後時間,對齊後字串)
    #return(A1)

def 轉成lrc檔(音標檔案名稱,對齊後時間,對齊後字串):

    字串=[]
    lrcFile=open('cgualign_lite/Output/切到字的lrc檔/'+音標檔案名稱+'.lrc',mode='w',encoding='UTF-8')#-sig')
    for i in range(len(對齊後時間)):
        if 對齊後時間[i]!='' or 對齊後字串[i]!='':
            字串.append(對齊後字串[i])
            字串[i]=字串[i].replace('.','.<br/><br/>')
            字串[i]=字串[i].replace('.<br/><br/>"','."<br/><br/>')
            字串[i]=字串[i].replace('。','。<br/><br/>')
            字串[i]=字串[i].replace('。<br/><br/>」','。」<br/><br/>')
            字串[i]=字串[i].replace('。<br/><br/>』','。』<br/><br/>')
            字串[i]=字串[i].replace('1-','<sub><sub>1</sub></sub>-')
            字串[i]=字串[i].replace('2-','<sub><sub>2</sub></sub>-')
            字串[i]=字串[i].replace('3-','<sub><sub>3</sub></sub>-')
            字串[i]=字串[i].replace('4-','<sub><sub>4</sub></sub>-')
            字串[i]=字串[i].replace('5-','<sub><sub>5</sub></sub>-')
            字串[i]=字串[i].replace('6-','<sub><sub>6</sub></sub>-')
            字串[i]=字串[i].replace('7-','<sub><sub>7</sub></sub>-')
            字串[i]=字串[i].replace('8-','<sub><sub>8</sub></sub>-')
            字串[i]=字串[i].replace('9-','<sub><sub>9</sub></sub>-')
            字串[i]=字串[i].replace('1,','<sub><sub>1</sub></sub>,')
            字串[i]=字串[i].replace('2,','<sub><sub>2</sub></sub>,')
            字串[i]=字串[i].replace('3,','<sub><sub>3</sub></sub>,')
            字串[i]=字串[i].replace('4,','<sub><sub>4</sub></sub>,')
            字串[i]=字串[i].replace('5,','<sub><sub>5</sub></sub>,')
            字串[i]=字串[i].replace('6,','<sub><sub>6</sub></sub>,')
            字串[i]=字串[i].replace('7,','<sub><sub>7</sub></sub>,')
            字串[i]=字串[i].replace('8,','<sub><sub>8</sub></sub>,')
            字串[i]=字串[i].replace('9,','<sub><sub>9</sub></sub>,')
            if i==0:
                lrcFile.write('['+對齊後時間[i]+']'+字串[i])
            else:
                lrcFile.write('\n['+對齊後時間[i]+']'+字串[i])
    lrcFile.close()

def 轉成切到字的sbv檔(音標檔案名稱,對齊後時間,對齊後字串):
    
    wavIn=wave.open('cgualign_lite/Input/'+音標檔案名稱+'.wav','rb')
    params=wavIn.getparams()
    (nChannels, sampWidth, frameRate, nFrames, compType, compName)=params
    語音總時間=nFrames/frameRate
    對齊後時間.append(語音總時間)
    s=[]
    for i in range(len(對齊後時間)):
        對齊後時間[i]=float(對齊後時間[i])
        a=對齊後時間[i]//3600
        b=(對齊後時間[i]-a*3600)//60
        c=對齊後時間[i]-a*3600-b*60
        a='%01.f'%a
        b='%02.f'%b
        c='%06.3f'%c
        a=str(a)
        b=str(b)
        c=str(c)
        t=a+':'+b+':'+c
        s.append(t)
        #print(t)
    sbvFile=open('cgualign_lite/Output/切到字的sbv檔/'+音標檔案名稱+'.sbv',mode='w',encoding='UTF-8')
    for i in range(len(s)-1):
        print(s[i]+','+s[i+1],file=sbvFile)
        print(對齊後字串[i]+'\n',file=sbvFile)
    sbvFile.close()

def 將Youtube下載的sbv檔轉成切到句的trs與srt檔(檔名):
    
    檔案路徑名稱='cgualign_lite/Input/'+檔名+'.sbv'
    檔案內容=讀取檔案(檔案路徑名稱)
    (原始時間,字串)=將字串內容存成一行(檔案內容)
    轉成切到句的srt檔(檔名,原始時間,字串)
    時間=轉換時間格式(原始時間)
    轉成切到句的trs檔(檔名,時間,字串)

def 對齊原文格式並轉成切到字的lrc與sbv檔(音標檔案名稱):

    音標檔內容=讀取檔案('cgualign_lite/Output/切到字的lab檔/'+音標檔案名稱+'_aligned.lab')
    (音標時間,音標字串,開始時間對應結束時間字典)=將sil接到上一個音標(音標檔內容)
    (句子時間,句子字串)=將trs檔時間與文字存成字典('cgualign_lite/Input/'+音標檔案名稱+'.trs')
    #(對齊後時間,對齊後字串)=原文句字對齊音標(音標時間,音標字串,句子時間,句子字串,開始時間對應結束時間字典)
    (對齊後時間,對齊後字串)=英原文句字對齊音標(音標時間,音標字串,句子時間,句子字串,開始時間對應結束時間字典)
    轉成lrc檔(音標檔案名稱,對齊後時間,對齊後字串)
    轉成切到字的sbv檔(音標檔案名稱,對齊後時間,對齊後字串)
def 清理垃圾HAN():
	os.system("del *.mlf *.conf *.lst *.scp *.lab *.trs *.bad *.led *.dic")
def CguAlign主程式(原文檔名集):

    #原文檔名集=['Combine001',#]
    '''
                'Combine002',
                'Combine003',
                'Combine004',
                'Combine005',
                'Combine006',
                'Combine007',
                'Combine008',
                'Combine009',
                'Combine010',
                'Combine011',
                'Combine012',
                'Combine013',
                'Combine014']
    '''
    #原文檔名集=['laocanyouji_01_liu']
    #原文檔名集=['TSawyer_30_twain']
    #原文檔名集=['TSawyer_01-02_twain']#,#]#,
    #原文檔名集=['mlkihaveadreamgogo']#,
    #原文檔名集=['Hillary_Womens_Rights']#,
    #原文檔名集=['Temp5']#,
    #原文檔名集=['WeShallOvercome']#,
			

    #建立資料夾()
    x= 原文檔名集
    #for x in 原文檔名集:    
    trsFn = 'cgualign_lite/Input/'+ x +'.trs'
    wavFn = 'cgualign_lite/Input/'+ x +'.wav'
    
    清理垃圾HAN()
	
    將Youtube下載的sbv檔轉成切到句的trs與srt檔(x)
    
    語音總時間長度=將trs檔的時間與對應字串轉成多個lab檔(trsFn)

    將長語音檔依照lab檔所對應的時間來切割成多個短語音檔(wavFn)

    製造各個HtkTool所需的參數檔()

    處裡語音標籤及詞典()

    擷取語音特徵及訓練語音模型()

    將語音文字做對齊()

    轉成切到字的trs檔(trsFn,語音總時間長度)

    對齊原文格式並轉成切到字的lrc與sbv檔(x)
		
    清理垃圾HAN()
	
if __name__=='__main__':
	#主程式()
	import sys
	#CguAlign主程式(sys.argv[1])
	CguAlign主程式(j)
	


