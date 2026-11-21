from build_common import *

RESPONSIVE_WIDTHS = (160, 352, 400, 640, 800, 1200)

def build_assets(out, excluded):
    amap = {}
    metadata = json.loads((ROOT / 'assets-src/dimensions.json').read_text(encoding='utf-8'))
    for f in sorted((ROOT / 'assets-src').rglob('*')):
        if not f.is_file() or f.name == 'dimensions.json' or f.relative_to(ROOT/'assets-src').as_posix() in excluded:
            continue
        rel = f.relative_to(ROOT / 'assets-src').as_posix()
        d = f.read_bytes()
        if rel == 'brand/lca-icon-lc-aircraft-v26b-transparent-192.png':
            # Preserve the original icon dimensions and alpha with an indexed PNG.
            with Image.open(f) as icon:
                buf = io.BytesIO()
                icon.convert('RGBA').quantize(colors=256).save(buf, 'PNG', optimize=True)
                d = buf.getvalue()
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
                for width in RESPONSIVE_WIDTHS:
                    if width >= im.width: continue
                    resized = im.copy()
                    resized.thumbnail((width, 10000))
                    buf = io.BytesIO()
                    resized.save(buf, 'WEBP', quality=60 if width <= 352 else 72 if width <= 640 else 82, method=6)
                    bd = buf.getvalue()
                    vr = str(Path(rel).with_name(f.stem + f'-responsive-{width}.webp'))
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
        if key=='css':
            d = d.replace(b'ARCHIVO_LOCAL',amap['assets/fonts/archivo-latin.woff2'].removeprefix('/assets/').encode())
        name = 'assets/' + Path(f).stem + '.' + digest(d)[:12] + Path(f).suffix
        (out / name).write_bytes(d)
        amap[key] = '/' + name
    return (amap, metadata)

def presentation_assets(out, amap, registry):
    from PIL import ImageOps
    def save(key, image, fmt, quality):
        data = io.BytesIO()
        image.save(data, fmt, quality=quality, **({'method':6} if fmt=='WEBP' else {}))
        content = data.getvalue()
        path = Path('assets/media') / (Path(key).stem+'.'+digest(content)[:12]+Path(key).suffix)
        (out/path).parent.mkdir(exist_ok=True)
        (out/path).write_bytes(content)
        amap[key] = '/'+path.as_posix()

    def source(subject):
        return Image.open(ROOT/'assets-src'/registry[subject]['asset'].removeprefix('assets/')).convert('RGB')
    engine = source('rotax-support-hero-original-photo')
    for width,height in [(640,760),(1024,720),(1600,900)]:
        crop = ImageOps.fit(engine,(width,height),centering=(0.8,0.5))
        for fmt,quality in [('WEBP',78),('AVIF',48 if width == 640 else 63)]:
            save(f'hero-{width}.{fmt.lower()}',crop,fmt,quality)
    for family, subject in SOCIAL.items():
        photo = source(subject)
        # Keep the complete subject on a navy field when an enlargement would be needed.
        if photo.width>=1200 and photo.height>=630:
            card = ImageOps.fit(photo,(1200,630))
        else:
            card = Image.new('RGB',(1200,630),'#08182a')
            photo.thumbnail(card.size)
            card.paste(photo,((1200-photo.width)//2,(630-photo.height)//2))
        save(f'social-{family}.jpg',card,'JPEG',83)

SOCIAL = {'shop':'rotax-support-hero-original-photo','rotax':'rotax-installed-hoses-overview',
          'propeller':'eprops-aircraft-closeup-sky-ranger-1200','records':'aircraft-open-cowling-under-canopy-800',
          'avionics':'garmin-g5-installed-panel-wide','work':'engine-cage-weld-repair-detail-800'}
