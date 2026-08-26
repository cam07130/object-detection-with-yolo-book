# 『（仮）深層学習による物体検出入門：YOLOから学ぶ』サンプルコード

本リポジトリは、書籍『（仮）深層学習による物体検出入門：YOLOから学ぶ』で使用するサンプルコードを公開するためのリポジトリです。

## 動作確認環境

本書のサンプルコードは、次の環境で動作を確認しています。

- Python 3.12.13
- Ultralytics 8.4.116
- PyTorch 2.11.0+cu128

PyTorchの導入方法は、OS、GPU、CUDA環境によって異なります。GPUを利用する場合は、使用する環境に合ったPyTorchを先にインストールしてください。

## セットアップ

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Windowsでは、仮想環境の有効化に次のコマンドを使用します。

```powershell
.venv\Scripts\activate
```

## 章別サンプル

| 章 | サンプル |
| --- | --- |
| 第10章 | [開発環境の構築](chapter10/01_environment_setup.ipynb) |
| 第11章 | [基本的な推論](chapter11/01_basic_inference.ipynb)、[検出結果の取得と保存](chapter11/02_results_and_export.ipynb)、[バッチ処理と推論速度](chapter11/03_batch_and_speed.ipynb) |
| 第12章 | [基本的な学習](chapter12/01_basic_training.ipynb)、[学習オプション](chapter12/02_training_options.ipynb)、[学習の再開と実験管理](chapter12/03_resume_and_results.ipynb) |
| 第13章 | [カスタムデータセットの学習](chapter13/01_custom_dataset_training.ipynb)、[data.yaml](chapter13/data.yaml) |
| 第14章 | [ベンチマーク](chapter14/01_benchmark.ipynb)、[ONNXとOpenVINO](chapter14/02_onnx_and_openvino.ipynb)、[TensorRT](chapter14/03_tensorrt.ipynb) |
| 第15章 | [Webアプリ](chapter15/) |

## Notebookの使い方

Notebookには、第11〜14章のコード例と、各章の代表的なCLI例を掲載順に収録しています。先頭からすべて一括実行するのではなく、書籍の説明を確認しながら必要なセルを実行してください。

- モデルの学習には時間がかかるため、GPUを利用できる環境を推奨します。
- カスタムデータセットを使う例では、Notebook内のパスを実際のデータセットに合わせて変更してください。
- TensorRTの実行には、CUDAに対応したNVIDIA GPUとTensorRT環境が必要です。
- エクスポートに必要なパッケージは、選択した形式に応じて追加でインストールされる場合があります。

## モデルとデータセット

学習済みモデル、大規模なデータセット、学習結果はリポジトリに含めません。Ultralyticsの学習済みモデルは、各サンプルの初回実行時にダウンロードされます。

## ライセンス

本リポジトリのサンプルコードは、[GNU Affero General Public License v3.0](LICENSE)のもとで公開します。

本リポジトリは、オープンソース版の[Ultralytics](https://github.com/ultralytics/ultralytics)を依存関係として利用します。Ultralyticsには、GNU Affero General Public License v3.0または契約に基づくEnterprise Licenseが適用されます。詳しくは[Ultralyticsのライセンス情報](https://www.ultralytics.com/license)を確認してください。

Ultralyticsのソースコード、学習済みモデル、データセット、画像は本リポジトリに同梱していません。これらを利用する場合は、それぞれの利用条件を確認してください。
