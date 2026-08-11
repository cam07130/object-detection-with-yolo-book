# 第15章 YOLOモデルのWebアプリ化

画像をアップロードし、検出結果をブラウザ上に描画するWebアプリです。FastAPIのAPI、HTMLとJavaScriptの画面、Dockerfileを1つの構成にまとめています。

## ファイル

- [main.py](main.py): モデルの読み込みと検出API
- [static/index.html](static/index.html): 操作画面
- [static/app.js](static/app.js): API呼び出しと検出結果の描画
- [Dockerfile](Dockerfile): Dockerイメージ
- [requirements-web.txt](requirements-web.txt): Webアプリで追加するパッケージ

## ローカルでの実行

リポジトリ直下で共通の環境を準備したあと、Webアプリ用のパッケージを追加します。

```bash
pip install -r chapter15/requirements-web.txt
cd chapter15
uvicorn main:app --reload
```

起動後、`http://127.0.0.1:8000/static/index.html`を開きます。APIの仕様は`http://127.0.0.1:8000/docs`に表示されます。

初回起動時にはYOLO26nのモデルがダウンロードされます。画面で別のモデルサイズを選んだ場合も、初回の検出時に対応するモデルがダウンロードされます。

## Dockerでの実行

第15章のディレクトリで次のコマンドを実行します。

```bash
cd chapter15
docker build -t yolo-book-app .
docker run --rm -p 8000:8000 yolo-book-app
```

Dockerfileは、Ultralyticsの最新公式イメージを使用します。

## 制限

このアプリはローカルで仕組みを学ぶためのサンプルです。認証、複数ワーカーでの運用、外部公開に必要なセキュリティ設定は含みません。アップロードできる画像は10MBまでです。

共通の動作確認環境は、[リポジトリ直下のREADME](../README.md)を参照してください。
