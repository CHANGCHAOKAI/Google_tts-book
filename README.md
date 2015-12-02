# Google_tts-book
此系統是利用python結合google_tts所製作而成的語音同步有聲書系統

主要是究利用雲端的文字轉語音(Text-to-speech)技術，結合語音辨識(Speech Recognition)技術，設計一個方便處理的音文同步有聲書系統，
讓使用者能夠針對中、英、日三種語言中自己喜愛的文章來製作自己的的學習素材，針對不同的語言做文章內容的斷句處理、拼音轉換、
製作句子的拼音內容、搭配上從文字轉語音中取得的時間點經由運用Python包裝語音辨識技術HTK(Hidden Markov Model Toolkit)的CGUAlign，
製作出達到詞層級(Word-level) 時間點文字檔案，再將文章中的每個句子及文字進行位置的搜尋取出其畫面的位置，
最後再將每個句子、單字、播放時間、畫面位置整理成tlt(text_location_time)檔案作存取，製作出音文同步的有聲書檔案。

使用軟體:
ffmpeg:對mp3檔案進行轉檔將檔案轉成wav檔。
來源:http://ffmpeg.zeranoe.com/builds/

mecab:對日文內容做斷詞及日文段詞拼音。
來源:http://taku910.github.io/mecab/

HTK:語音辨識軟體將句子等級的時文檔與WAV檔做辨識產稱字等級的時文檔。
詳細介紹請參考http://ryresearch.blogspot.tw/2015/09/htk.html

PYTHON使用模組:
requests
來源:http://docs.python-requests.org/en/latest/

inflect
來源:https://pypi.python.org/pypi/inflect

pygame
來源:https://www.pygame.org/docs/ref/music.html

romkan
來源:https://pypi.python.org/pypi/romkan

系統詳細介紹:
http://changchaokai.blogspot.tw/
