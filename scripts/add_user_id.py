#!/usr/bin/env python3
"""
ユーザーID追加・ソートスクリプト
YAMLマッピングファイルを読み込み、CSVにユーザー番号列を追加してソートします。
"""

import pandas as pd
import yaml
import sys
from pathlib import Path
from typing import Dict, Any


def load_user_mapping(yaml_path: str) -> Dict[str, int]:
    """
    YAMLファイルからユーザーIDマッピングを読み込む
    
    Args:
        yaml_path: YAMLファイルのパス
        
    Returns:
        学籍番号 -> ユーザーID の辞書
        
    Raises:
        FileNotFoundError: ファイルが存在しない
        ValueError: バリデーションエラー
    """
    print(f"📖 YAMLファイルを読み込み中: {yaml_path}")
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    if not data:
        raise ValueError("YAMLファイルが空です")
    
    # user_idを抽出してバリデーション
    user_mapping = {}
    errors = []
    
    for student_id, info in data.items():
        # 学籍番号の空白を削除
        student_id = str(student_id).strip()
        
        # user_idを取得
        if not isinstance(info, dict):
            errors.append(f"  ❌ {student_id}: 不正なデータ形式です")
            continue
            
        user_id = info.get('user_id')
        
        # null チェック
        if user_id is None:
            errors.append(f"  ❌ {student_id}: user_idが設定されていません")
            continue
        
        # 型チェック
        if not isinstance(user_id, int):
            errors.append(f"  ❌ {student_id}: user_idは整数である必要があります (現在: {type(user_id).__name__})")
            continue
        
        # 範囲チェック
        if user_id < 1 or user_id > 18:
            errors.append(f"  ❌ {student_id}: user_idは1~18の範囲である必要があります (現在: {user_id})")
            continue
        
        user_mapping[student_id] = user_id
    
    # エラーがあれば表示して終了
    if errors:
        print("\n⚠️  バリデーションエラーが見つかりました:\n")
        for error in errors:
            print(error)
        raise ValueError(f"{len(errors)}件のエラーがあります")
    
    # 重複チェック
    user_ids = list(user_mapping.values())
    duplicates = [uid for uid in set(user_ids) if user_ids.count(uid) > 1]
    
    if duplicates:
        print("\n⚠️  user_idの重複が見つかりました:\n")
        for uid in duplicates:
            students = [sid for sid, u in user_mapping.items() if u == uid]
            print(f"  ❌ user_id={uid}: {', '.join(students)}")
        raise ValueError(f"{len(duplicates)}件の重複があります")
    
    # 欠損チェック(1~18がすべて存在するか)
    expected_ids = set(range(1, 19))
    actual_ids = set(user_ids)
    missing_ids = expected_ids - actual_ids
    
    if missing_ids:
        print(f"\n⚠️  未使用のuser_idがあります: {sorted(missing_ids)}")
        print("   すべての1~18のIDを使用することを推奨します")
    
    print(f"✅ {len(user_mapping)}件のマッピングを読み込みました")
    return user_mapping


def add_user_id_and_sort(csv_path: str, user_mapping: Dict[str, int], output_path: str):
    """
    CSVにユーザー番号列を追加し、ユーザーID順にソート
    
    Args:
        csv_path: 入力CSVファイルのパス
        user_mapping: 学籍番号 -> ユーザーID の辞書
        output_path: 出力CSVファイルのパス
    """
    print(f"\n📖 CSVファイルを読み込み中: {csv_path}")
    df = pd.read_csv(csv_path)
    
    # 学籍番号の空白を削除
    df['学籍番号'] = df['学籍番号'].astype(str).str.strip()
    
    # ユーザー番号を追加
    print("🔢 ユーザー番号を追加中...")
    df['ユーザー番号'] = df['学籍番号'].map(user_mapping)
    
    # マッピングできなかった行をチェック
    unmapped = df[df['ユーザー番号'].isna()]
    if len(unmapped) > 0:
        print("\n⚠️  以下の学籍番号がYAMLファイルに存在しません:")
        for _, row in unmapped.iterrows():
            print(f"  ❌ {row['学籍番号']} ({row['氏名']})")
        raise ValueError(f"{len(unmapped)}件の学籍番号がマッピングされていません")
    
    # ユーザー番号を整数型に変換
    df['ユーザー番号'] = df['ユーザー番号'].astype(int)
    
    # ユーザー番号順にソート
    print("📊 ユーザー番号順にソート中...")
    df = df.sort_values('ユーザー番号').reset_index(drop=True)
    
    # 列の順序を変更(ユーザー番号を1列目に)
    cols = ['ユーザー番号'] + [col for col in df.columns if col != 'ユーザー番号']
    df = df[cols]
    
    # 出力ディレクトリを作成
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # CSVに書き込み
    print(f"\n💾 出力ファイルを保存中: {output_path}")
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"✨ 処理完了!")
    print(f"\n📊 統計情報:")
    print(f"   総行数: {len(df)}行")
    print(f"   ユーザー番号範囲: {df['ユーザー番号'].min()} ~ {df['ユーザー番号'].max()}")
    print(f"   出力列数: {len(df.columns)}列")


def main():
    """メイン処理"""
    yaml_path = "/app/config/user_mapping.yaml"
    csv_path = "/app/システムアンケート回答.csv"
    output_path = "/app/output/システムアンケート回答_ユーザー番号付き.csv"
    
    try:
        # YAMLを読み込み
        user_mapping = load_user_mapping(yaml_path)
        
        # CSVを処理
        add_user_id_and_sort(csv_path, user_mapping, output_path)
        
        sys.exit(0)
        
    except FileNotFoundError as e:
        print(f"\n❌ エラー: ファイルが見つかりません: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"\n❌ エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 予期しないエラー: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
