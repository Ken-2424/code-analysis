#!/usr/bin/env python3
"""
YAMLテンプレート生成スクリプト
CSVから学籍番号を抽出し、ユーザーIDマッピングのテンプレートを生成します。
"""

import pandas as pd
import yaml
import sys
from pathlib import Path


def generate_template(csv_path: str, output_path: str):
    """
    CSVから学籍番号を抽出し、YAMLテンプレートを生成
    
    Args:
        csv_path: 入力CSVファイルのパス
        output_path: 出力YAMLファイルのパス
    """
    try:
        # CSVを読み込み
        print(f"📖 CSVファイルを読み込み中: {csv_path}")
        df = pd.read_csv(csv_path)
        
        # 学籍番号と氏名を抽出(空白削除)
        df['学籍番号'] = df['学籍番号'].astype(str).str.strip()
        students = df[['学籍番号', '氏名']].drop_duplicates()
        
        # 学籍番号でソート
        students = students.sort_values('学籍番号').reset_index(drop=True)
        
        print(f"✅ {len(students)}件の学籍番号を抽出しました")
        
        # ユーザーIDマッピングを作成(学籍番号順に1~18を仮設定)
        user_mapping = {}
        for idx, row in students.iterrows():
            student_id = row['学籍番号']
            name = row['氏名']
            user_id = idx + 1  # 1から開始
            
            # コメント付きで保存
            user_mapping[student_id] = {
                'user_id': user_id,
                'name': name  # 参考情報として氏名を含める
            }
        
        # 出力ディレクトリを作成
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # YAMLファイルに書き込み
        print(f"💾 YAMLテンプレートを生成中: {output_path}")
        with open(output_path, 'w', encoding='utf-8') as f:
            # ヘッダーコメント
            f.write("# ユーザーIDマッピング設定ファイル\n")
            f.write("# 各学籍番号に対して1~18のユーザーIDを設定してください\n")
            f.write("# user_id: 1~18の範囲で一意な整数値を設定\n")
            f.write("# name: 参考情報(編集不要)\n\n")
            
            # YAMLデータを書き込み
            yaml.dump(
                user_mapping,
                f,
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False
            )
        
        print(f"✨ テンプレート生成完了!")
        print(f"\n📝 次のステップ:")
        print(f"   1. {output_path} を編集してユーザーIDを調整")
        print(f"   2. ./run.sh process を実行してCSVを生成")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ エラー: ファイルが見つかりません: {csv_path}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ エラー: {e}", file=sys.stderr)
        return False


def main():
    """メイン処理"""
    csv_path = "/app/システムアンケート回答.csv"
    output_path = "/app/config/user_mapping.yaml"
    
    success = generate_template(csv_path, output_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
