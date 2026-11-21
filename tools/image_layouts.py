from build_common import E
from build_assets import RESPONSIVE_WIDTHS

class Images:
    def __init__(self, registry, assets, dimensions, page):
        self.registry = registry
        self.assets = assets
        self.dimensions = dimensions
        self.page = page
        self.number = 0

    def image(self, subject, role, alt=None, eager=False, caption=None):
        record = self.registry[subject]
        src = record['asset']
        w,h = self.dimensions[src.removeprefix('assets/')]
        widths = [(size, self.assets.get(src[:-5]+f'-responsive-{size}.webp')) for size in RESPONSIVE_WIDTHS if size<w]
        srcset = ', '.join(f'{url} {size}w' for size,url in widths+[(w,self.assets[src])] if url)
        sizes = {'thumbnail':'76px','tile':'(max-width:560px) 46vw, (max-width:1020px) 50vw, 620px','mosaic':'(max-width:760px) 65vw, 420px','hero':'(max-width:759px) calc(100vw - 2 * clamp(16px, 4vw, 48px)), (max-width:1240px) 44vw, 536px'}.get(role,'(max-width:760px) 94vw, 460px')
        if role == 'evidence':
            sizes = '(max-width:560px) 46vw, (max-width:760px) 94vw, 460px'
        if role not in {'hero', 'thumbnail'}:
            sizes = 'auto, ' + sizes
        priority = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
        alt = record['alt'] if alt is None else alt
        return (f'<img src="{self.assets[src]}" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" '
                f'style="object-position:{E(record["focal"])}" alt="{E(alt)}" data-subject="{subject}" data-purpose="{role}" data-caption="{E(caption or record["caption"])}" {priority}>')

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
            img = f'<a class="document-link" href="{original}" aria-label="Open full size: {E(caption)}">{img}</a>'
            caption += ' Open full size.'
        return f'<figure class="{role}-figure{natural}">{img}<figcaption>{label}{E(caption)}</figcaption></figure>'

    def home_picture(self, subject):
        sources = []
        for width, media in [(640,'(max-width:640px)'),(1024,'(max-width:1024px)'),(1600,'(min-width:1025px)')]:
            for fmt in ['avif','webp']:
                sources.append(f'<source media="{media}" type="image/{fmt}" srcset="{self.assets[f"hero-{width}.{fmt}"]}">')
        return '<picture class="backdrop">'+''.join(sources)+f'<img src="{self.assets["hero-1600.webp"]}" width="1600" height="900" data-subject="{subject}" data-purpose="backdrop" data-caption="ROTAX engine photograph behind the shop introduction." fetchpriority="high" alt=""></picture>'
