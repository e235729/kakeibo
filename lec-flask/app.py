from flask import Flask, render_template

# ==================================================
# インスタンス生成
# ==================================================
app = Flask(__name__)

# ==================================================
# ルーティング
# ==================================================
# TOPページ
@app.route('/') 
def index():
    return render_template('top.html')

# 一覧
@app.route('/list') 
def item_list():
    return render_template('list.html')

# 詳細
@app.route('/detail/<int:id>')
def item_detail(id):
    return render_template('detail.html', show_id=id)

# ▼▼▼【リスト3.26】▼▼▼
# ▼▼▼▼▼ ここから【制御文】 ▼▼▼▼▼
# 「商品」クラス
class Item:
    # コンストラクタ
    def __init__(self, id, name):
        self.id = id
        self.name = name
    # 表示用関数
    def __str__(self):
        return f'商品ID：{self.id} 商品名：{self.name}'

# 繰り返し
@app.route("/for_list")
def show_for_list():
    item_list = [Item(1,"ダンゴ"), Item(2,"にくまん"), Item(3,"ドラ焼き")]
    return render_template('for_list.html', items = item_list)
# ▲▲▲【リスト3.26】▲▲▲

# 条件分岐
@app.route('/if_detail/<int:id>')
def show_if_detail(id):
    item_list = [Item(1,"ダンゴ"), Item(2,"にくまん"), Item(3,"ドラ焼き")]
    return render_template('if_detail.html', show_id=id, items = item_list)

# ==================================================
# 実行
# ==================================================
if __name__ == '__main__':
    app.run()