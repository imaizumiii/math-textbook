"""
テスト共通フィクスチャ
"""

import pytest
from pdf_generator.builder.document_builder import DocumentBuilder


@pytest.fixture
def builder():
    """基本的な DocumentBuilder インスタンスを返すフィクスチャ"""
    return DocumentBuilder()
