import argparse
import json
from pathlib import Path
from .generate import generate
from .db import Database
from .etl import load_batch
from .analyze import export


def main():
    p=argparse.ArgumentParser(description="Produtividade: dados 100% sintéticos")
    p.add_argument("command",choices=["generate","load","export","demo"])
    p.add_argument("--batch",help="Arquivo JSON para load")
    p.add_argument("--postgres",action="store_true",help="Usa DATABASE_URL e psycopg")
    p.add_argument("--db",default="data/warehouse.sqlite")
    args=p.parse_args()
    if args.command in ("generate","demo"):
        print(json.dumps(generate("data/raw"),ensure_ascii=False))
    if args.command=="generate":
        return
    db=Database(args.db,args.postgres)
    try:
        if args.command=="load":
            if not args.batch:
                p.error("load requer --batch")
            print(json.dumps(load_batch(db,args.batch)))
        if args.command=="demo":
            for batch in sorted(Path("data/raw").glob("*.json")):
                print(json.dumps(load_batch(db,batch)))
        if args.command in ("demo","export"):
            result=export(db)
            print(f"Exportados {len(result['monthly'])} agregados para reports/ e site/data.js")
    finally:
        db.close()


if __name__=="__main__":
    main()
