FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
RUN pip install --no-cache-dir pandas pyyaml

# スクリプトをコピー
COPY scripts/ /app/scripts/

# デフォルトコマンド
CMD ["python3"]
