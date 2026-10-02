import argparse,json
from pathlib import Path
from .demo import create_fixture
from .grounding import quote_boxes
from .render import render

def main():
    p=argparse.ArgumentParser(description='Source-first paper videos; no hosted service is called by default.')
    sub=p.add_subparsers(dest='cmd',required=True)
    d=sub.add_parser('demo',help='Render an original, silent fixture with no API keys');d.add_argument('--out',default='out/demo');d.add_argument('--font')
    r=sub.add_parser('render',help='Render a grounded config');r.add_argument('--config',required=True);r.add_argument('--out',required=True);r.add_argument('--font');r.add_argument('--native',help='Native speech manifest with real word timings and audio hash')
    q=sub.add_parser('quote',help='Find one unique phrase in an actual PDF');q.add_argument('--pdf',required=True);q.add_argument('--page',type=int,required=True);q.add_argument('--text',required=True)
    args=p.parse_args()
    if args.cmd=='demo':
        out=Path(args.out);cfg=create_fixture(out/'input');result=render(cfg,out/'render',args.font)
        print(json.dumps({'output':str(out/'render/video.mp4'),**result},indent=2))
    elif args.cmd=='render':print(json.dumps(render(args.config,args.out,args.font,args.native),indent=2))
    else:print(json.dumps(quote_boxes(args.pdf,args.page,args.text),indent=2))

if __name__=='__main__':main()
