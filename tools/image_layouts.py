from build_common import E
from build_assets import RESPONSIVE_WIDTHS
from lxml import html

def check_engine_family_photos(root):
    excluded = {
        'rotax-915-916-turbo-ems-support': ('rotax-support-hero-original-photo', 'rotax-engine-installed-green-covers'),
        'rotax-912-carb-sync': ('rotax-airbox-focus',),
    }
    for page, subjects in excluded.items():
        doc = html.parse(root / (page + '.html'))
        references = doc.xpath('//img/@data-subject | //img/@src | //img/@srcset | //picture/source/@srcset')
        for subject in subjects:
            if any(subject in ref for ref in references):
                raise ValueError(f'Wrong engine family photo on {page}: {subject}')

HOME_CROPS = [(640, '(max-width:640px)'), (1024, '(640px < width <= 1024px)'), (1600, '(width > 1024px)')]

def home_preloads(assets):
    return ''.join(f'<link rel="preload" as="image" type="image/avif" media="{E(media)}" '
                   f'href="{assets[f"hero-{width}.avif"]}" fetchpriority="high">'
                   for width, media in HOME_CROPS)

class Images:
    def __init__(self, registry, assets, dimensions, asset_bytes):
        self.registry = registry
        self.assets = assets
        self.dimensions = dimensions
        self.asset_bytes = asset_bytes
        self.number = 0

    def image(self, subject, role, alt=None, eager=False, caption=None):
        record = self.registry[subject]
        src = record['asset']
        w,h = self.dimensions[src.removeprefix('assets/')]
        candidates = [(width, self.assets[src[:-5] + f'-responsive-{width}.webp'])
                      for width in RESPONSIVE_WIDTHS if width < w]
        candidates.append((w, self.assets[src]))
        def srcset(items):
            return ', '.join(f'{url} {width}w' for width, url in items)
        mobile = []
        if role == 'hero':
            candidates = [item for item in candidates if self.asset_bytes[item[1]] <= 150_000]
            mobile = [item for item in candidates if self.asset_bytes[item[1]] <= 75_000]
            if not mobile:
                raise ValueError('Missing mobile hero within 75 KB: ' + subject)
        sizes = {'thumbnail':'76px','tile':'(max-width:560px) 46vw, (max-width:1020px) 50vw, 620px','mosaic':'(max-width:760px) 65vw, 420px','hero':'(max-width:759px) calc(100vw - 2 * clamp(16px, 4vw, 48px)), (max-width:1240px) 44vw, 536px'}.get(role,'(max-width:760px) 94vw, 460px')
        if role == 'evidence':
            sizes = '(max-width:560px) 46vw, (max-width:760px) 94vw, 460px'
        if role not in {'hero', 'thumbnail'}:
            sizes = 'auto, ' + sizes
        priority = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
        alt = record['alt'] if alt is None else alt
        markup = (f'<img src="{candidates[-1][1]}" srcset="{srcset(candidates)}" sizes="{sizes}" width="{w}" height="{h}" '
                f'style="object-position:{E(record["focal"])}" alt="{E(alt)}" data-subject="{subject}" data-purpose="{role}" data-caption="{E(caption or record["caption"])}" {priority}>')
        if mobile and mobile != candidates:
            return f'<picture><source media="(max-width:759px)" srcset="{srcset(mobile)}" sizes="{sizes}">{markup}</picture>'
        return markup

    def figure(self, subject, role='evidence', caption=None, alt=None, stage_label=None):
        caption = caption or self.registry[subject]['caption']
        img = self.image(subject,role,alt,role=='hero',caption)
        label = ''
        if role in {'case', 'evidence'}:
            self.number += 1
            label = f'<span class="fig-label">FIG. {self.number:02d}</span> '
        if stage_label:
            label += E(stage_label) + ' · '
        natural = ' natural' if self.registry[subject].get('natural_hero') else ''
        if self.registry[subject].get('document') and role in {'evidence', 'case'}:
            natural += ' document'
            original = self.assets[self.registry[subject]['asset']]
            source_width = self.dimensions[self.registry[subject]['asset'].removeprefix('assets/')][0]
            img = f'<a class="document-link" style="max-width:{source_width}px" href="{original}" aria-label="Open full size: {E(caption)}">{img}<span>Open full size</span></a>'
        return f'<figure class="{role}-figure{natural}">{img}<figcaption>{label}{E(caption)}</figcaption></figure>'

    def home_picture(self, subject):
        sources = []
        for width, media in HOME_CROPS:
            for fmt in ['avif','webp']:
                sources.append(f'<source media="{E(media)}" type="image/{fmt}" srcset="{self.assets[f"hero-{width}.{fmt}"]}">')
        return '<picture class="backdrop">'+''.join(sources)+f'<img src="{self.assets["hero-1600.webp"]}" width="1600" height="900" data-subject="{subject}" data-purpose="backdrop" data-caption="ROTAX engine photograph behind the shop introduction." fetchpriority="high" alt=""></picture>'
