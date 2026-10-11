"""Atalho para a prévia baseada no layout revisado do PBIP."""
import runpy
from pathlib import Path
if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).with_name("gerar_previa_bi.py")), run_name="__main__")
