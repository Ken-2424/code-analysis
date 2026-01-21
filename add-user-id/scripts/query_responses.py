#!/usr/bin/env python3
"""
ユーザー番号からE1~E3の質問回答を取得するスクリプト
"""

import pandas as pd
import sys
from pathlib import Path


def get_user_responses(csv_path: str, user_id: int):
    """
    指定されたユーザー番号のE1~E3の回答を取得して表示
    
    Args:
        csv_path: CSVファイルのパス
        user_id: ユーザー番号(1~18)
    """
    try:
        # CSVを読み込み
        print(f"📖 CSVファイルを読み込み中: {csv_path}")
        df = pd.read_csv(csv_path)
        
        # ユーザー番号でフィルタ
        user_data = df[df['ユーザー番号'] == user_id]
        
        if len(user_data) == 0:
            print(f"\n❌ エラー: ユーザー番号 {user_id} が見つかりません")
            print(f"有効なユーザー番号: {sorted(df['ユーザー番号'].unique().tolist())}")
            return False
        
        # 最初の行を取得
        row = user_data.iloc[0]
        
        # E1~E3の列名を取得
        e1_col = 'E1: 良かったところ（役に立った画面、助言、タイミングなど）'
        e2_col = 'E2: 困ったところ・分かりにくかったところ'
        e3_col = 'E3: 改善してほしい点・次のシステムへの期待'
        
        # 結果を表示
        print("\n" + "="*80)
        print(f"👤 ユーザー番号: {user_id}")
        print(f"👤 氏名: {row['氏名']}")
        print(f"🆔 学籍番号: {row['学籍番号']}")
        print("="*80)
        
        print(f"\n📝 {e1_col}")
        print("-"*80)
        e1_response = row[e1_col]
        if pd.isna(e1_response) or str(e1_response).strip() == '':
            print("(回答なし)")
        else:
            print(e1_response)
        
        print(f"\n📝 {e2_col}")
        print("-"*80)
        e2_response = row[e2_col]
        if pd.isna(e2_response) or str(e2_response).strip() == '':
            print("(回答なし)")
        else:
            print(e2_response)
        
        print(f"\n📝 {e3_col}")
        print("-"*80)
        e3_response = row[e3_col]
        if pd.isna(e3_response) or str(e3_response).strip() == '':
            print("(回答なし)")
        else:
            print(e3_response)
        
        print("\n" + "="*80)
        
        return True
        
    except FileNotFoundError:
        print(f"❌ エラー: ファイルが見つかりません: {csv_path}", file=sys.stderr)
        return False
    except KeyError as e:
        print(f"❌ エラー: 必要な列が見つかりません: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ エラー: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False


def main():
    """メイン処理"""
    # コマンドライン引数からユーザー番号を取得
    if len(sys.argv) < 2:
        print("❌ エラー: ユーザー番号を指定してください")
        print("\n使い方: python3 query_responses.py <ユーザー番号>")
        print("例: python3 query_responses.py 1")
        sys.exit(1)
    
    try:
        user_id = int(sys.argv[1])
    except ValueError:
        print(f"❌ エラー: ユーザー番号は整数で指定してください: {sys.argv[1]}")
        sys.exit(1)
    
    if user_id < 1 or user_id > 18:
        print(f"❌ エラー: ユーザー番号は1~18の範囲で指定してください: {user_id}")
        sys.exit(1)
    
    csv_path = "/app/output/システムアンケート回答_ユーザー番号付き.csv"
    
    success = get_user_responses(csv_path, user_id)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
