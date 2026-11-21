from build_common import *

def build_assets(out):
    amap = {}
    metadata = json.loads((ROOT / 'assets-src/dimensions.json').read_text(encoding='utf-8'))
    for f in sorted((ROOT / 'assets-src').rglob('*')):
        if not f.is_file() or f.name == 'dimensions.json':
            continue
        rel = f.relative_to(ROOT / 'assets-src').as_posix()
        d = f.read_bytes()
        if rel in ['favicon.ico', 'apple-touch-icon.png']:
            name = rel
        else:
            name = 'assets/' + str(Path(rel).with_name(f.stem + '.' + digest(d)[:12] + f.suffix)).replace('\\', '/')
        dest = out / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(d)
        amap['assets/' + rel] = '/' + name
        if f.suffix == '.webp' and 'images/' in rel:
            with Image.open(io.BytesIO(d)) as im:
                if im.width > 400:
                    resized = im.copy()
                    resized.thumbnail((400, 10000))
                    buf = io.BytesIO()
                    resized.save(buf, 'WEBP', quality=82, method=6)
                    bd = buf.getvalue()
                    vr = str(Path(rel).with_name(f.stem + '-responsive-400.webp'))
                    vn = 'assets/' + str(Path(vr).with_name(Path(vr).stem + '.' + digest(bd)[:12] + '.webp'))
                    (out / vn).parent.mkdir(parents=True, exist_ok=True)
                    (out / vn).write_bytes(bd)
                    amap['assets/' + vr] = '/' + vn
    for source, key, width in [('brand/lca-wordmark-v17-transparent-640.webp', 'header-wordmark', 400), ('brand/lca-icon-lc-aircraft-v26b-transparent-128.png', 'header-icon', 96)]:
        with Image.open(ROOT / 'assets-src' / source) as im:
            im.thumbnail((width, width), Image.Resampling.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, 'WEBP', method=6, **{'lossless': True} if key == 'header-icon' else {'quality': 85})
            data = buf.getvalue()
            name = 'assets/brand/' + key + '.' + digest(data)[:12] + '.webp'
            (out / name).write_bytes(data)
            amap[key] = '/' + name
    for f, key in [('site.css', 'css'), ('site.js', 'js')]:
        d = (ROOT / 'templates' / f).read_bytes()
        name = 'assets/' + Path(f).stem + '.' + digest(d)[:12] + Path(f).suffix
        (out / name).write_bytes(d)
        amap[key] = '/' + name
    return (amap, metadata)
