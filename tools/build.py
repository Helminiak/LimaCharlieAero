from build_common import *
from build_assets import build_assets, presentation_assets
from cases import select_cases
from editorial import select_editorial
from render_site import render_site

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output')
    ap.add_argument('--preview', action='store_true')
    ap.add_argument('--as-of')
    args = ap.parse_args()
    site = json.loads((ROOT / 'content/site.json').read_text(encoding='utf-8'))
    asof = date.fromisoformat(args.as_of or site['date'])
    pages = json.loads((ROOT / 'content/pages.json').read_text(encoding='utf-8'))
    records = json.loads((ROOT / 'content/updates.json').read_text(encoding='utf-8'))
    public, published, warnings = select_editorial(records, pages, asof)
    out = ROOT / (args.output or ('dist-preview' if args.preview else 'dist'))
    if args.preview != (out == ROOT/'dist-preview'):
        raise ValueError('Private preview requires its own dist-preview output')
    registry = {a['id']:a for a in json.loads((ROOT/'content/proof-assets.json').read_text())}
    records = json.loads((ROOT/'content/cases.json').read_text())
    cases = select_cases(records,set(registry),args.preview)
    case_images = {i for c in cases for stage in c['stages'] for i in stage['evidence']}
    excluded = {r['asset'].removeprefix('assets/') for r in registry.values() if r.get('case_only') and r['id'] not in case_images}
    if out not in [ROOT / 'dist', ROOT / 'dist-preview', ROOT / 'repro-dist'] or out.is_symlink():
        raise ValueError('Choose dist, dist-preview or repro-dist')
    out.mkdir(exist_ok=True)
    for f in out.iterdir():
        if f.is_symlink() or f.is_file():
            f.unlink()
        else:
            shutil.rmtree(f)
    amap, metadata = build_assets(out, excluded)
    presentation_assets(out, amap, registry)
    routes = render_site(out, site, pages, public, published, amap, metadata, registry, cases, args.preview)

    def asset(src):
        return amap[src]
    redirect = '/e-props-usa-dealer-support /e-props-dealer-support 301\n/e-props-usa-dealer-support.html /e-props-dealer-support 301\n/rotax-912-rubber-replacement /rotax-rubber-hose-replacement-fluid-leaks 301\n/rotax-912-rubber-replacement.html /rotax-rubber-hose-replacement-fluid-leaks 301\n/prebuy /light-sport-prebuy-evaluation 301\n/prebuy.html /light-sport-prebuy-evaluation 301\n'
    redirect += '/e-props-usa-dealer-support/ /e-props-dealer-support 301\n/rotax-912-rubber-replacement/ /rotax-rubber-hose-replacement-fluid-leaks 301\n/prebuy/ /light-sport-prebuy-evaluation 301\n'
    redirect += '/_headers /__missing-config-resource 302\n/_redirects /__missing-config-resource 302\n'
    (out / '_redirects').write_text(redirect, encoding='utf-8', newline='\n')
    headers = '/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: geolocation=(), microphone=(), camera=()\n  X-Frame-Options: SAMEORIGIN\n\n/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n\n/*.html\n  Cache-Control: public, max-age=0, must-revalidate\n\n/site.webmanifest\n  Cache-Control: public, max-age=0, must-revalidate\n\n/favicon.ico\n  Cache-Control: public, max-age=0, must-revalidate\n\n/apple-touch-icon.png\n  Cache-Control: public, max-age=0, must-revalidate\n\n' + asset('assets/downloads/joseph-helminiak-lima-charlie-aero.vcf') + '\n  Content-Type: text/vcard; charset=utf-8\n  Content-Disposition: attachment; filename="Joseph-Helminiak-Lima-Charlie-Aero.vcf"\n'
    headers += '\nhttps://limacharlieaero.com/*\n  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload\n  Content-Security-Policy: upgrade-insecure-requests\n'
    (out / '_headers').write_text(headers, encoding='utf-8', newline='\n')
    manifest = {'name': site['company'], 'short_name': 'LCAero', 'start_url': '/', 'display': 'standalone', 'background_color': '#092a44', 'theme_color': '#092a44', 'icons': [{'src': asset(f'assets/brand/lca-icon-lc-aircraft-v26b-transparent-{sz}.png'), 'sizes': f'{sz}x{sz}', 'type': 'image/png'} for sz in [192, 512]]}
    (out / 'site.webmanifest').write_text(json.dumps(manifest, indent=2), encoding='utf-8', newline='\n')
    (out / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: ' + site['domain'] + '/sitemap.xml\n', encoding='utf-8', newline='\n')
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(('<url><loc>' + E(site['domain'] + r['route']) + '</loc><lastmod>' + r['last_modified'] + '</lastmod></url>' for r in routes if r['indexed'])) + '</urlset>\n'
    (out / 'sitemap.xml').write_text(xml, encoding='utf-8', newline='\n')
    for f in ['security.txt', '.well-known/security.txt']:
        dest = out / f
        dest.parent.mkdir(exist_ok=True)
        dest.write_text(f"Contact: mailto:{site['email']}\nExpires: 2027-04-04T00:00:00Z\nCanonical: {site['domain']}/.well-known/security.txt\nPolicy: {site['domain']}/security-disclosure\nPreferred-Languages: en\n", encoding='utf-8', newline='\n')
    evidence = ROOT / '.build-evidence' / out.name
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / 'asset-map.json').write_text(json.dumps(amap, indent=2), encoding='utf-8', newline='\n')
    (evidence / 'routes.json').write_text(json.dumps(routes, indent=2), encoding='utf-8', newline='\n')
    (evidence / 'review-warnings.json').write_text(json.dumps(warnings, indent=2), encoding='utf-8', newline='\n')
    files = {f.relative_to(out).as_posix(): digest(f.read_bytes()) for f in sorted(out.rglob('*')) if f.is_file()}
    (evidence / 'deployment-manifest.json').write_text(json.dumps(files, indent=2), encoding='utf-8', newline='\n')
    print(json.dumps({'output': str(out), 'release': site['release'], 'html_pages': len(routes), 'files': len(files), 'bytes': sum((f.stat().st_size for f in out.rglob('*') if f.is_file())), 'review_warnings': warnings}))
if __name__ == '__main__':
    main()
