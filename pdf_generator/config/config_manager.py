"""
設定ファイルの読み込み、検証、管理を担当するモジュール
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from jsonschema import validate, ValidationError, SchemaError
from jsonschema.exceptions import best_match


class ConfigManager:
    """
    設定ファイルの読み込み、検証、管理を担当
    
    機能:
    - JSON設定ファイルの読み込み
    - JSON Schemaによるバリデーション
    - 設定値の取得とマージ
    - デフォルト値の提供
    """
    
    def __init__(self, config_path: Optional[str] = None, 
                 schema_path: str = "config/schema.json"):
        """
        Args:
            config_path: 設定ファイルのパス（Noneの場合はデフォルト）
            schema_path: JSON Schemaファイルのパス
        """
        # デフォルトパスの設定
        if config_path is None:
            config_path = "config/default.json"
        
        # 相対パスの場合は絶対パスに変換
        config_path_obj = Path(config_path)
        if not config_path_obj.is_absolute():
            # カレントディレクトリから探す
            if config_path_obj.exists():
                self.config_path = config_path_obj.resolve()
            else:
                # スクリプトのディレクトリから探す
                script_dir = Path(__file__).parent.parent.parent
                candidate = script_dir / config_path
                if candidate.exists():
                    self.config_path = candidate.resolve()
                else:
                    self.config_path = config_path_obj
        else:
            self.config_path = config_path_obj
        
        schema_path_obj = Path(schema_path)
        if not schema_path_obj.is_absolute():
            # カレントディレクトリから探す
            if schema_path_obj.exists():
                self.schema_path = schema_path_obj.resolve()
            else:
                # config_pathと同じディレクトリから探す
                candidate = self.config_path.parent / schema_path
                if candidate.exists():
                    self.schema_path = candidate.resolve()
                else:
                    self.schema_path = schema_path_obj
        else:
            self.schema_path = schema_path_obj
        
        self.config: Dict[str, Any] = {}
        self.schema: Dict[str, Any] = {}
        
    def load_config(self) -> Dict[str, Any]:
        """設定ファイルを読み込む"""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"設定ファイルが見つかりません: {self.config_path}"
            )
        
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        
        return self.config
    
    def load_schema(self) -> Dict[str, Any]:
        """JSON Schemaを読み込む"""
        if not self.schema_path.exists():
            raise FileNotFoundError(
                f"スキーマファイルが見つかりません: {self.schema_path}"
            )
        
        with open(self.schema_path, "r", encoding="utf-8") as f:
            self.schema = json.load(f)
        
        return self.schema
    
    def validate_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        設定をバリデーション
        
        Args:
            config: 検証する設定辞書（Noneの場合はself.configを使用）
        
        Returns:
            bool: バリデーション成功時True
        
        Raises:
            ValidationError: バリデーションエラー時
            SchemaError: スキーマエラー時
        """
        if config is None:
            config = self.config
        
        # スキーマファイルが存在しない場合はスキップ
        if not self.schema_path.exists():
            return True
        
        if not self.schema:
            try:
                self.load_schema()
            except FileNotFoundError:
                # スキーマファイルが見つからない場合はスキップ
                return True
        
        try:
            validate(instance=config, schema=self.schema)
            return True
        except ValidationError as e:
            # より詳細なエラーメッセージを提供
            best_error = best_match([e])
            error_path = " -> ".join(str(p) for p in e.absolute_path)
            raise ValidationError(
                f"設定ファイルのバリデーションエラー:\n"
                f"  パス: {error_path}\n"
                f"  エラー: {best_error.message}\n"
                f"  値: {e.instance}"
            ) from e
        except SchemaError as e:
            raise SchemaError(f"スキーマファイルのエラー: {e.message}") from e
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        設定値を取得（ドット記法対応）
        
        Args:
            key_path: 設定キーのパス（例: "directories.template_dir"）
            default: デフォルト値
        
        Returns:
            設定値
        """
        keys = key_path.split(".")
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def merge(self, override_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        設定をマージ（上書き）
        
        Args:
            override_config: 上書きする設定
        
        Returns:
            マージされた設定辞書
        """
        def deep_merge(base: Dict, override: Dict) -> Dict:
            result = base.copy()
            for key, value in override.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = deep_merge(result[key], value)
                else:
                    result[key] = value
            return result
        
        return deep_merge(self.config, override_config)
    
    def validate_template_config(self, template_name: str, 
                                 variables: Dict[str, Any]) -> bool:
        """
        テンプレート用の変数が設定と一致するか検証
        
        Args:
            template_name: テンプレート名
            variables: 提供された変数
        
        Returns:
            bool: 検証成功時True
        
        Raises:
            ValueError: 必須変数が不足している場合
        """
        template_config = self.get(f"templates.{template_name}")
        if not template_config:
            raise ValueError(f"テンプレート '{template_name}' の設定が見つかりません")
        
        required = template_config.get("required_variables", [])
        missing = [var for var in required if var not in variables]
        
        if missing:
            raise ValueError(
                f"テンプレート '{template_name}' に必須変数が不足しています: {missing}"
            )
        
        return True
    
    def get_default_variables(self, template_name: str) -> Dict[str, Any]:
        """テンプレートのデフォルト変数を取得"""
        template_config = self.get(f"templates.{template_name}")
        if template_config:
            return template_config.get("default_variables", {})
        return {}

