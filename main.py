from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import time
from datetime import datetime

dir_path = r'levels'
os.makedirs(dir_path, exist_ok=True)

def config():

    #各種jsonを作成

    filename0 = 'config.json'
    if os.path.exists(filename0):
        with open(filename0, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print("config.json: ok")
    else:
        print(f"エラー: ファイル '{filename0}'が見つかりません")
        print("新たに作成しますか？")
        ans = input("Yes or No: ")
        if ans.lower() == 'yes':
            dir_path = r'ss4us'
            file_name = 'config.json'

            new_file_path = os.path.join(file_name)

            with open(new_file_path, mode='w', encoding='utf-8') as f:
                json.dump({}, f, indent=4)

            print(f"'{new_file_path}' を作成しました。")

    filename1 = 'temporary.json'
    if os.path.exists(filename1):
        with open(filename1, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print("temporary.json: ok")

    else:
        dir_path = r'ss4us'
        file_name = 'temporary.json'

        new_file_path = os.path.join(file_name)

        with open(new_file_path, mode='w', encoding='utf-8') as f:
            json.dump({}, f, indent=4)
            print(f"'{new_file_path}' を作成しました。")

    filename2 = 'sc.json'
    if os.path.exists(filename2):
        print("sc.json: ok")

    else:
        dir_path = r'ss4us'
        file_name = 'sc.json'

        new_file_path = os.path.join(file_name)

        with open(new_file_path, mode='w', encoding='utf-8') as f:
            json.dump({}, f, indent=4)
            print(f"'{new_file_path}' を作成しました。")

        sc_path = './sc.json'
        if not os.path.exists(sc_path) or os.path.getsize(sc_path) < 3:

            name = input("Enter Username: ")
            pwrd = input("Enter Password: ")
            stdata = {
                "user": {
                    "username": name,
                    "password": pwrd
                }
            }

            with open(new_file_path, 'w') as f:
                json.dump(stdata, f, indent=4)
            print("初回書き込み完了")
        else:
            print("ファイルが既に存在して中身もあるため、書き込みはスキップ")

    filename3 = 'us-charts.json'
    if os.path.exists(filename3):
        with open(filename3, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print("us-charts.json: ok")

    else:
        dir_path = r'ss4us'
        file_name = 'us-charts.json'

        new_file_path = os.path.join(file_name)

        with open(new_file_path, mode='w', encoding='utf-8') as f:
            json.dump({}, f, indent=4)
            print(f"'{new_file_path}' を作成しました。")

def levlist():
    levels_path = './levels'
        
    extension_to_category = {
        'jpg': 'jacket',
        'png': 'jacket',
        'jfif':'jacket',
        'usc': 'chart',
        'mp3': 'bgm'
    }

    special_categories = ['bgm', 'chart', 'jacket']

    json_file_path = 'temporary.json'
    filename = 'temporary.json'

    # 既存の config.json を読み込む（存在しない場合は空の辞書にする）
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as file:
            existing_config = json.load(file)
    else:
        existing_config = {}

    # levels内のサブフォルダを取得（1, 2, 3 ...）
    subdirectories = [d for d in os.listdir(levels_directory) if os.path.isdir(os.path.join(levels_directory, d))]

    # 更新後の config データ
    new_config = {}

    for subdirectory in subdirectories:
        subdirectory_path = os.path.join(levels_directory, subdirectory)
        file_names = os.listdir(subdirectory_path)

    # カテゴリに分類されたファイルデータを保存する辞書
        categorized_files = {}

        for file_name in file_names:
            name, ext = os.path.splitext(file_name)
            ext = ext.lstrip('.')
            category = extension_to_category.get(ext, 'other_files')

        # 特定カテゴリなら単一ファイルとして保存
            if category in special_categories:
                categorized_files[category] = file_name
            else:
                if category not in categorized_files:
                    categorized_files[category] = []
                categorized_files[category].append(file_name)

    # 既存のデータとマージ（title, rating, utsk-id を保持）
        existing_data = existing_config.get(subdirectory, {})
        for key in ['title', 'rating', 'utsk-id']:
            if key in existing_data:
                categorized_files[key] = existing_data[key]

        new_config[subdirectory] = categorized_files

    # JSONファイルに書き込み
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(new_config, file, ensure_ascii=False, indent=4)

    print("save success.")
    
    # 追加したいデフォルト項目
    default_fields = {
        "title": "untitle",
        "rating": 1,
        "utsk-id": "unset"
    }

    # JSONファイルを読み込む
    with open(filename, 'r', encoding='utf-8') as file:
        config = json.load(file)

    for item in config:
        for key, default_value in default_fields.items():
            # キーが存在しない場合だけ追加（上書きしない）
            if key not in config[item]:
                config[item][key] = default_value

    # 更新して保存
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False, indent=2)

    with open('temporary.json', 'r', encoding='utf-8') as file:
        levlt_data = json.load(file)

    with open('us-charts.json', 'r', encoding='utf-8') as file:
        uscht_data = json.load(file)

    # utsk_data から title: name の辞書を作成
    title_to_name = {item["title"]: item["name"] for item in uscht_data["data"]}

    # music_data の各要素の title に一致し、utsk-id が "unset" のときだけ更新
    for key, level in levlt_data.items():
        if level.get("utsk-id") == "unset":
            title = level.get("title")
            if title in title_to_name:
                level["utsk-id"] = title_to_name[title]

    with open("temporary.json", "w", encoding="utf-8") as f:
        json.dump(levlt_data, f, ensure_ascii=False, indent=4)

    # JSONを読み込む
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # titleが"untitle"のときだけ変更
    for key, value in data.items():
        if value.get('title') == 'untitle':
            # ここで新しいタイトルを決める（例：key名を使う）
            key = input(f'{key}を投稿するときの名前を入力: ')
            value['title'] = key  # 例: "air", "air1", ...

    # JSONファイルに書き戻す（上書き保存）
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    with open('temporary.json', 'r', encoding='utf-8') as f:
        data_tm = json.load(f)

    with open('sc.json', 'r', encoding='utf-8') as f:
        data_sc = json.load(f)

    file_path = r'config.json'

    # 結合
    merged_data = data_sc | data_tm

    # a.jsonに書き戻す
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)

def login():
    url = "https://us.pim4n-net.com/api/login" 
    
    c_path = './config.json'
    if not os.path.exists(c_path) or os.path.getsize(c_path) < 3:
        with open('sc.json', 'r', encoding='utf-8') as f:
            cndata = json.load(f)

    else:
        with open('config.json', 'r', encoding='utf-8') as f:
            cndata = json.load(f)
    
    namedata = cndata["user"]["username"]

    passdata = cndata["user"]["password"]

    payload = {
        "username": namedata,
        "password": passdata
    }
    """

    payload = {
        "username": username,
        "password": password
    }
    """
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            token = data.get("token")
            print("success get token")
            return token

        else:
            print(f"failed: {response.status_code}")
            return None

    except Exception as e:
        print(f"error: str{str(e)}")

    if token:
        print("Login successful!")
    else:
        print("Login failed.")

def get_chart(token):

    headers = {
        "Authorization": f"Bearer {token}",
        "isOwner" : "true"
    }
    
    c_path = './config.json'
    if not os.path.exists(c_path) or os.path.getsize(c_path) < 3:
        with open('sc.json', 'r', encoding='utf-8') as f:
            cndata = json.load(f)

    else:
        with open('config.json', 'r', encoding='utf-8') as f:
            cndata = json.load(f)
    
    username = cndata["user"]["username"]

    charts_url = f'https://us.pim4n-net.com/api/charts/user/{username}'
        
    try:
        response = requests.get(charts_url, headers=headers)
        
        if response.status_code == 200:
            charts = response.json()
            return charts
        
        else:
            return None
        
    except Exception as e:
        print(f"error: str{str(e)}")
        return None

def uschtjson():
    result = get_chart(token)

    if os.path.exists('us-charts.json'):
            with open('us-charts.json', 'w', encoding='utf-8') as file:
                json.dump(result, file, ensure_ascii=False, indent=4)
            print("writing successful")
            
    else:
        print("writing failed")
                    
        dir_path = r'ss4us'
        file_name = 'us-charts.json'
        
        new_file_path = os.path.join(file_name)

        with open(new_file_path, mode='w', encoding='utf-8') as file:
            json.dump({}, file, indent=4)
                
        with open('us-charts.json', 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=4)      
                      
        print("new jsonfile created and writing")

def ob():
    print("""observe started. \nCtrl+C to stop program""")

    last_executed = {}

    # フォルダの監視クラスを作成
    class FileUpdateHandler(FileSystemEventHandler):
        def on_modified(self, event):
            # ファイルが更新された時に呼ばれる
            if event.is_directory:
                return

            path = event.src_path
            now = datetime.now()

            # 連続イベントを0.8秒以内に発生したら無視
            if path in last_executed:
                delta = now - last_executed[path]
                if delta.total_seconds() < 2:
                    return

            # 更新
            last_executed[path] = now

            # 実際の処理
            print(f"{path} が更新されました！")

            with open('config.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # 対象のファイルパスからファイル名を取得
            postfile_path = event.src_path
            file_path = Path(f'{postfile_path}')
            file_name = file_path.name  # 'airapd.usc'

            # 対応する utsk-id を探す
            utskid = "None"
            for key, item in data.items():
                if item.get('chart') == file_name:
                    utskid = item.get('utsk-id')
                    break

            post_url = f'https://us.pim4n-net.com/api/chart/edit/{utskid}'
            
            headers = {
                "Authorization": f"Bearer {token}",
                "isOwner" : "true"
            }

            response = requests.get(url = post_url, headers = headers)

            if response.status_code != 200:

                new_token = login()
                
                headers = {
                    "Authorization": f"Bearer {new_token}",
                    "isOwner" : "true"
                }

                print("Token has expired and has been renewedToken has expired and has been renewed")
        
            ext = os.path.splitext(postfile_path)[1].lower()

            try:

                with open(postfile_path,'rb') as postfile:

                    if ext == ".sus" or ext == ".usc":
                        print("edit: chartfile")

                        files = {
                            'chart': postfile,
                        }

                    if ext == ".mp3" or ext == ".wav":
                        print("edit: bgmfile")

                        files = {
                            'bgm': postfile,
                        }

                    if ext == ".jpg" or ext == ".jpeg" or ext == ".png" or ext == ".jfif":
                        print("edit: jacketfile")

                        files = {
                            'jacket': postfile,
                        }
                    
                    response = requests.patch(post_url, headers=headers, files=files)
                        
                    if response.status_code == 200:
                        mes = response.json()
                        
                        print(mes['message'])
                            
                    else:
                        print(f"failed: {response.status_code}")
                        print(f"error: {response.text}")
                        
            except requests.exceptions.RequestException as e:
                print(f"Request failed:{e}")


    # 監視するフォルダのパス
    folder_to_watch = "levels"

    # 監視用のイベントハンドラを作成
    event_handler = FileUpdateHandler()

    # オブザーバーを作成
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=True)

    # 監視開始
    observer.start()

    try:
        while True:
            time.sleep(1)  # プログラムが終了しないように無限ループ
    except KeyboardInterrupt:
        observer.stop()  # 手動で停止した場合
    observer.join()


"""--------------------------------------------------------"""

if __name__ == "__main__":
    filename = 'config.json'
    
    config()
        
    token = login()
    
    get_chart(token)

    uschtjson()

    levels_directory = './levels'

    levlist()

    ob()
