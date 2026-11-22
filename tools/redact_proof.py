"""Derive publication pixels directly from Git blobs. Coordinates use native pixels."""
import io
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
LIGHT = '#e4e9ed'
DARK = '#192d3b'
# Rectangles are inclusive. Polygon vertices follow the skew on the photographed pages.
PROOF = {
    'eprops-engineering-packet-fanout-1200-clean': (
        'eprops/proof/eprops-engineering-packet-fanout-1200-clean', (1200,780), LIGHT, [
            [(861,556),(902,550),(904,560),(863,566)],  # issuer name
            [(865,600),(919,591),(921,601),(866,610)],  # contact address
            (996,549,1026,580), (1031,537,1098,571),  # signature and stamp
            [(993,582),(1065,572),(1067,582),(995,595)],  # signature caption
        ]),
    'eprops-install-checklist-preview-1200': (
        'eprops/proof/eprops-install-checklist-preview-1200', (1200,760), LIGHT, [
            (203,198,251,210),(287,198,319,210),  # airframe serial and registration
            (195,242,299,254),(188,256,258,267),  # blade and hub serials
        ]),
    'ndt-magnetic-particle-report': (
        'lca-proof/v28/ndt-magnetic-particle-report-1200', (916,1200), LIGHT, [
            (422,482,488,500),(723,888,818,906),  # equipment and airframe serial values
            (162,999,383,1051),(203,1052,343,1074),  # inspector signature and name
        ]),
    'tl-ultralight-designer-correspondence': (
        'lca-proof/v28/tl-ultralight-designer-correspondence-1200',(951,1200),DARK,[
            (32,19,124,111),(152,25,374,56),  # avatar and display name
            (30,615,382,653),(30,1014,457,1057),(30,1059,314,1098),  # signatory, email and phone
        ]),
    'lca-logbook-work-sticker-proof-800': (
        'lca-proof/webp_1200/lca-logbook-work-sticker-proof-1200',(1200,847),DARK,[
            (1011,447,1052,465),(981,540,1091,575),  # sticker identification and handwriting
            (245,436,432,466),(245,590,606,620),(244,693,438,722),  # endorsement tails
        ]),
    'garmin-g5-box-unit': (
        'lca-proof/webp_1200/garmin-g5-box-unit-1200',(1200,900),LIGHT,[
            [(460,335),(610,352),(610,395),(460,375)],  # purchasing barcode and number
            [(482,402),(683,431),(681,548),(481,522)],  # fields below DESC, including lower barcode
        ]),
}

def coverage(size, shapes):
    mask = Image.new('1', size)
    draw = ImageDraw.Draw(mask)
    for shape in shapes:
        if isinstance(shape, list):
            draw.polygon(shape, fill=1)
        else:
            draw.rectangle(shape, fill=1)
    return mask

def redact():
    for subject, (source, size, color, shapes) in PROOF.items():
        src = subprocess.check_output(['git','show','3d48ea6:assets/images/'+source+'.webp'], cwd=ROOT)
        with Image.open(io.BytesIO(src)) as original:
            if original.size != size:
                raise ValueError('Unexpected dimensions: '+subject)
            image = original.convert('RGB')
        image.paste(color, mask=coverage(size, shapes))
        image.info.clear()
        image.save(ROOT/'assets-src/images/proof'/(subject+'.webp'),lossless=True,method=6)

if __name__ == '__main__':
    redact()
