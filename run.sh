#!/usr/bin/env bash
# CSVアンケートデータにユーザーIDを追加するスクリプト

set -e

# ヘルプメッセージを表示
show_help() {
    cat << EOF
使い方: ./run.sh <command>

コマンド:
    generate    YAMLテンプレートを生成 (config/user_mapping.yaml)
    process     ユーザーIDを追加してCSVを生成 (output/システムアンケート回答_ユーザー番号付き.csv)
    help        このヘルプを表示

例:
    ./run.sh generate     # 最初にテンプレートを生成
    ./run.sh process      # config/user_mapping.yamlを編集後に実行

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
