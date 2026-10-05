"""Local-only authoring/preview; models static Pages routes, not the live edge."""
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlsplit, parse_qs, unquote
from datetime import date, timedelta
import argparse, mimetypes, json, html, secrets, subprocess, sys, fnmatch, hashlib
ROOT=Path(__file__).resolve().parents[1]
TOKEN=secrets.token_urlsafe(32)
def editor(slug=''):
 records=json.loads((ROOT/'content/updates.json').read_text(encoding="utf-8"))
 today=date.today().isoformat()
 r=next((r for r in records if r['slug']==slug),{'slug':'','type':'answer','title':'','owner_question':'','summary':'','body':[],'sources':[],'state':'draft','published':today,'last_modified':today,'last_review':today,'next_review':(date.today()+timedelta(days=30)).isoformat(),'reviewer':'','document':'','issue_date':today,'supersedes':'','replaced_by':''})
 e=lambda v:html.escape(str(v),quote=True)
 fields=''
 for key in ['slug','type','title','owner_question','summary','body','sources','document','issue_date','supersedes','state','published','last_modified','last_review','next_review','reviewer','replaced_by']:
  value=r.get(key,'');value='\n\n'.join(value) if key=='body' else '\n'.join(value) if key=='sources' else value
  if key in ['type','state']:
   values=['answer','notice','work-note'] if key=='type' else ['draft','published','superseded','archived']
   control='<select name="'+key+'">'+''.join('<option '+('selected ' if v==value else '')+'>'+v+'</option>' for v in values)+'</select>'
  elif key in ['body','sources','summary']:control='<textarea rows="'+('7' if key=='body' else '3')+'" name="'+key+'">'+e(value)+'</textarea>'
  else:control='<input name="'+key+'" value="'+e(value)+'" '+('type="date"' if key in ['issue_date','published','last_modified','last_review','next_review'] else '')+'>'
  fields+='<label>'+key.replace('_',' ').title()+control+'</label>'
 links='<a href="/__editor">New draft</a> · '+ ' · '.join('<a href="/__editor?slug='+e(i['slug'])+'">'+e(i['title'])+'</a>' for i in records)
 return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>LCA local content editor</title><style>body{font:17px/1.5 system-ui;max-width:850px;margin:25px auto;padding:20px;color:#132d40}label{display:block;margin:18px 0;font-weight:650}input,textarea,select{display:block;width:100%;font:inherit;padding:10px;box-sizing:border-box}button{font:inherit;padding:12px;background:#092a44;color:white}a{color:#174d74}fieldset{margin-top:25px}</style><h1>Local owner content editor</h1><p>This interface runs only on this computer. The deployable ZIP contains no editor or admin endpoint.</p><p>'+links+'</p><p>Write body paragraphs separated by a blank line; one verified source URL per line. Use your real reviewer identity. A draft is never public. Dates are explicit; saving does not invent historical publication dates.</p><form method="POST" action="/__editor"><input type="hidden" name="token" value="'+TOKEN+'"><input type="hidden" name="original_slug" value="'+e(slug)+'">'+fields+'<label>Build as of<input type="date" name="asof" value="'+today+'" required></label><button name="operation" value="save">Save and rebuild preview</button> <button name="operation" value="delete">Delete selected item</button></form><p><a href="/">Open preview homepage</a> · <a href="/updates">Preview updates</a></p></html>'
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def reply(self,status,data=b'',headers=None):
  self.send_response(status)
  for k,v in (headers or {}).items():self.send_header(k,v)
  self.send_header('Content-Length',str(len(data)));self.end_headers()
  if self.command!='HEAD':self.wfile.write(data)
 def do_POST(self):
  if not self.server.editor_enabled or urlsplit(self.path).path!='/__editor':return self.reply(405)
  size=int(self.headers.get('Content-Length','0'))
  if size>100000:return self.reply(413)
  q={k:v[0] for k,v in parse_qs(self.rfile.read(size).decode(),keep_blank_values=True).items()}
  if not secrets.compare_digest(q.get('token',''),TOKEN):return self.reply(403)
  content=ROOT/'content/updates.json';old=content.read_bytes()
  try:
   records=json.loads(old);original=q.get('original_slug','')
   if q.get('operation')=='delete':
    if not original:raise ValueError('Select an existing item before deleting')
    if any(r['slug']==original and r['state']!='draft' for r in records):raise ValueError('Archive a published item to preserve its URL. Only drafts can be deleted.')
    records=[r for r in records if r['slug']!=original]
   else:
    if original and q['slug']!=original:raise ValueError('Published slugs are stable. Create a new record and retain the old URL with a replacement link.')
    row={k:q.get(k,'').strip() for k in ['slug','type','title','owner_question','summary','document','issue_date','supersedes','state','published','last_modified','last_review','next_review','reviewer','replaced_by']}
    row['body']=[s.strip() for s in q.get('body','').replace('\r','').split('\n\n') if s.strip()];row['sources']=[s.strip() for s in q.get('sources','').splitlines() if s.strip()];row['topic']='notice' if row['type']=='notice' else 'unsure'
    if not original and any(r['slug']==row['slug'] for r in records):raise ValueError('Choose a unique slug')
    records=[r for r in records if r['slug']!=original]+[row]
   content.write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n', encoding="utf-8", newline="\n")
   result=subprocess.run([sys.executable,str(ROOT/'tools/build.py'),'--output',str(self.server.root),'--as-of',q['asof']],capture_output=True,text=True)
   if result.returncode:raise ValueError(result.stderr)
  except Exception as exc:
   content.write_bytes(old);return self.reply(400,('Save rejected: '+html.escape(str(exc))).encode(),{'Content-Type':'text/plain; charset=utf-8'})
  return self.reply(303,headers={'Location':'/__editor?slug='+q.get('slug','')})
 def do_HEAD(self):self.do_GET()
 def do_GET(self):
  parsed=urlsplit(self.path);path=unquote(parsed.path);query=('?'+parsed.query if parsed.query else '')
  root=self.server.root
  if self.server.root_file:root=Path(self.server.root_file.read_text(encoding="utf-8").strip()).resolve()
  if self.server.editor_enabled and path=='/__editor':return self.reply(200,editor(parse_qs(parsed.query).get('slug',[''])[0]).encode(),{'Content-Type':'text/html; charset=utf-8','Cache-Control':'no-store'})
  rules=(root/'_redirects').read_text(encoding="utf-8").splitlines() if (root/'_redirects').exists() else []
  for line in rules:
   if not line.strip() or line.lstrip().startswith('#'):continue
   parts=line.split()
   if len(parts)!=3 or path!=parts[0]:continue
   target,status=parts[1],int(parts[2])
   if status!=200:return self.reply(status,headers={'Location':target+query})
   path=target
   break
  if path.endswith('.html') and (root/path.lstrip('/')).is_file():return self.reply(301,headers={'Location':path[:-5]+query if path!='/index.html' else '/'+query})
  if path!='/':
   clean=path.rstrip('/')
   if (root/(clean.lstrip('/')+'.html')).is_file() and path.endswith('/'):return self.reply(301,headers={'Location':clean+query})
  if '..' in Path(path).parts:return self.reply(400)
  file=root/path.lstrip('/')
  if path=='/':file=root/'index.html'
  elif not file.is_file() and Path(path).suffix=='':file=root/(path.lstrip('/')+'.html')
  status=200
  if path in ['/_headers','/_redirects'] or not file.is_file():file=root/'404.html';status=404
  if not file.is_file():return self.reply(404,b'Not found')
  data=file.read_bytes();headers={'Content-Type':mimetypes.guess_type(file.name)[0] or 'application/octet-stream','Cache-Control':'public, max-age=0, must-revalidate','ETag':'"'+hashlib.sha256(data).hexdigest()+'"'}
  header_file=root/'_headers'
  if header_file.exists():
   pattern=None
   for line in header_file.read_text(encoding="utf-8").splitlines():
    if not line.strip() or line.lstrip().startswith('#'):continue
    if not line[0].isspace():pattern=line.strip()
    elif pattern and fnmatch.fnmatchcase(parsed.path,pattern):
     k,v=line.strip().split(':',1);headers[k]=v.strip()
  if self.headers.get('If-None-Match')==headers['ETag']:return self.reply(304,headers=headers)
  self.reply(status,data,headers)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',default='dist');ap.add_argument('--port',type=int,default=9000);ap.add_argument('--editor',action='store_true');ap.add_argument('--root-file');args=ap.parse_args()
 root=Path(args.root).resolve()
 server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler);server.root=root;server.editor_enabled=args.editor;server.root_file=Path(args.root_file).resolve() if args.root_file else None
 print(f'Local preview: http://127.0.0.1:{args.port}/'+(' — editor at /__editor' if args.editor else ''),flush=True);server.serve_forever()
