"""
PDFGenerator の出力先制御に関するテスト
"""

import json
from pathlib import Path
from typing import Tuple

from pdf_generator import DocumentBuilder, PDFGenerator


def _create_config(tmp_path: Path) -> Tuple[Path, Path, Path]:
    default_output_dir = tmp_path / "default-output"
    temp_dir = tmp_path / "temp"
    config_path = tmp_path / "config.json"

    config = {
        "directories": {
            "output_dir": str(default_output_dir),
            "temp_dir": str(temp_dir),
        },
        "compilation": {
            "preview": False,
        },
        "file_management": {
            "cleanup": False,
        },
    }
    config_path.write_text(json.dumps(config), encoding="utf-8")
    return config_path, default_output_dir, temp_dir


def _install_fake_compile(generator: PDFGenerator, calls: dict, monkeypatch):
    def fake_compile(tex_file, output_dir):
        calls["tex_file"] = tex_file
        calls["output_dir"] = output_dir

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        compiled_pdf = output_path / f"{Path(tex_file).stem}.pdf"
        compiled_pdf.write_bytes(b"%PDF-1.4\n")
        return True, ""

    monkeypatch.setattr(generator.compiler, "compile", fake_compile)
    monkeypatch.setattr(generator.compiler, "cleanup", lambda *_args, **_kwargs: None)


def test_generate_can_override_output_dir(tmp_path, monkeypatch):
    config_path, default_output_dir, temp_dir = _create_config(tmp_path)
    custom_output_dir = tmp_path / "by-file-output"
    generator = PDFGenerator(config_path=str(config_path))
    doc = DocumentBuilder("test").build()

    calls = {}
    _install_fake_compile(generator, calls, monkeypatch)

    pdf_path = generator.generate(
        doc,
        output_name="custom.pdf",
        output_dir=str(custom_output_dir),
    )

    assert Path(pdf_path) == custom_output_dir / "custom.pdf"
    assert Path(calls["output_dir"]) == custom_output_dir
    assert Path(calls["tex_file"]) == temp_dir / "custom.tex"
    assert default_output_dir != custom_output_dir


def test_generate_uses_config_output_dir_by_default(tmp_path, monkeypatch):
    config_path, default_output_dir, _temp_dir = _create_config(tmp_path)
    generator = PDFGenerator(config_path=str(config_path))
    doc = DocumentBuilder("test").build()

    calls = {}
    _install_fake_compile(generator, calls, monkeypatch)

    pdf_path = generator.generate(doc, output_name="default.pdf")

    assert Path(pdf_path) == default_output_dir / "default.pdf"
    assert Path(calls["output_dir"]) == default_output_dir
