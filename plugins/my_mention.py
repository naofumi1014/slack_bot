from keras.models import load_model
import numpy as np
from keras.preprocessing.image import img_to_array, load_img
from PIL import Image
import os
import glob
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
import requests
import codecs
import slackbot_settings
import pathlib
import glob




class DownloadFile:
    



    def __init__(self, file_types, save_directly):
        # 引数が省略された場合は、デフォルトのタイプを指定
        self.file_types = file_types
        self.save_directly = save_directly
 
 
    def exe_download(self, file_info):
 
        file_name = file_info['name']
        url_private = file_info['url_private_download']
 
        # 保存対象のファイルかチェックする
        if file_info['filetype'] in self.file_types:
            # ファイルをダウンロード
            self.file_download(url_private, self.save_directly + file_name)
            return 'ok'
        else:
            # 保存対象外ファイル
            return 'file type is not applicable.'
 
    def file_download(self, download_url, save_path):
        content = requests.get(
            download_url,
            allow_redirects=True,
            headers={'Authorization': 'Bearer %s' % slackbot_settings.API_TOKEN}, stream=True
        ).content
        # 保存する
        target_file = codecs.open(save_path, 'wb')
        target_file.write(content)
        target_file.close()

    def predict(self):
        #ファイル探索
        files = glob.glob(r"C:\Users\naofumi\slackbot\photo\*.")
        for file in files:
            print(file)
        #学習済みモデルを入力
        model = load_model(r"C:\Users\naofumi\slackbot\plugins\model_mnist.h5")

        #画像入力
        X = np.asarray(Image.open(file).convert('L'))
        X = 255.0 - X
        #float型に変換
        X = X.astype('float32')
        #1次元にする
        X = X.reshape(1,784)
        pred = model.predict(X, batch_size=1, verbose=0)
        #prediction = np.argmax(pred[0])
        
        #予測
        return np.argmax(pred[0]),file



    
@respond_to('^予測$')
def file_download(message):
    # ダウンロードするファイルタイプを指定する
    file_types = ['png', 'gif', 'jpg']
    # ファイルの保存ディレクトリ
    save_path = r'C:\Users\naofumi\slackbot\photo\gazo'
    download_file = DownloadFile(file_types, save_path)
    result = download_file.exe_download(message._body['files'][0])
    yosoku,path = download_file.predict()
    yosoku = str(yosoku)
    text = "予測結果は" + yosoku + "です。"
    os.remove(path)
    if result == 'ok':
        message.send('ファイルをダウンロードしました')
        message.send(text)
    elif result == 'file type is not applicable.':
        message.send('ファイルのタイプがダウンロード対象外です')
    else:
        message.send('ファイルのダウンロードに失敗しました')    


