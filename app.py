from flask import Flask, request, render_template, send_file
from PIL import Image
import os

app = Flask(__name__, static_url_path='/static', static_folder='static')

# アップロードされたファイルの保存先
UPLOAD_FOLDER = 'file/'

@app.route('/', methods=['GET', 'POST'])
def convert_image():
    if request.method == 'POST':
        # アップロードされたファイルを取得
        files = request.files.getlist('file')
        save_paths = []

        for file in files:
            # ファイルが選択されているかチェック
            if file.filename == '':
                return 'ファイルが選択されていません'

            # 画像ファイルであるかチェック
            if not allowed_file(file.filename):
                return '画像ファイルを選択してください'

            # 画像をPillow Imageオブジェクトに変換
            image = Image.open(file).convert('RGBA')
            background = Image.new('RGBA', image.size, (255, 255, 255))
            converted_image = Image.alpha_composite(background, image).convert('RGB')

            # ファイル名と拡張子を取得
            filename, file_extension = os.path.splitext(file.filename)

            # 保存パスを生成
            save_path = os.path.join(UPLOAD_FOLDER, f'{filename}_converted.png')
            converted_image.save(save_path, format='PNG')
            save_paths.append(save_path)

        return render_template('complete.html', save_paths=save_paths)

    return render_template('index.html')  # アップロードフォームを表示するHTMLテンプレート

@app.route('/delete', methods=['POST'])
def delete_file():
    save_path = request.form.get('save_path', '')
    if save_path:
        try:
            os.remove(save_path)
            return 'ファイルを削除しました'
        except Exception as e:
            return f'ファイルの削除中にエラーが発生しました: {str(e)}'
    else:
        return 'ファイルが見つかりません'

@app.route('/download')
def download():
    filename = request.args.get('filename', '')
    if filename:
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        return send_file(save_path, as_attachment=True)
    else:
        return 'ファイルが見つかりません'

# 画像ファイルの拡張子を許可するリスト
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# ファイルの拡張子をチェックする関数
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    # グローバルIPアドレスからのアクセスを許可するために、host='0.0.0.0' を指定してアプリを起動する
    app.run(host='0.0.0.0')
