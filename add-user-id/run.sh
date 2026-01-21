#!/usr/bin/env bash
# CSVアンケートデータにユーザーIDを追加するスクリプト

set -e

# ヘルプメッセージを表示
show_help() {
    cat << EOF
使い方: ./run.sh <command> [options]

コマンド:
    generate           YAMLテンプレートを生成 (config/user_mapping.yaml)
    process            ユーザーIDを追加してCSVを生成 (output/システムアンケート回答_ユーザー番号付き.csv)
    query <user_id>    指定したユーザー番号のE1~E3回答を表示
    help               このヘルプを表示

例:
    ./run.sh generate        # 最初にテンプレートを生成
    ./run.sh process         # config/user_mapping.yamlを編集後に実行
    ./run.sh query 1         # ユーザー番号1のE1~E3回答を表示
    ./run.sh query 5         # ユーザー番号5のE1~E3回答を表示

EOF
}

# 引数チェック
if [ $# -eq 0 ]; then
    echo "❌ エラー: コマンドを指定してください"
    echo ""
    show_help
    exit 1
fi

# コマンドを処理
case "$1" in
    generate)
        echo "🚀 YAMLテンプレートを生成します..."
        docker compose run --rm generate
        ;;
    process)
        echo "🚀 ユーザーIDを追加してCSVを生成します..."
        docker compose run --rm process
        ;;
    query)
        if [ $# -lt 2 ]; then
            echo "❌ エラー: ユーザー番号を指定してください"
            echo "例: ./run.sh query 1"
            exit 1
        fi
        echo "🔍 ユーザー番号 $2 のE1~E3回答を取得します..."
        docker compose run --rm query python3 /app/scripts/query_responses.py "$2"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ エラー: 不明なコマンド '$1'"
        echo ""
        show_help
        exit 1
        ;;
esac
