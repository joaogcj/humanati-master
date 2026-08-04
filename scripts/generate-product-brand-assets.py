from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "branding" / "products"
FONT_REGULAR = Path("C:/Windows/Fonts/arial.ttf")
FONT_BOLD = Path("C:/Windows/Fonts/arialbd.ttf")

BRANDS = {
    "monihook": {
        "name": "MoniHook",
        "tagline": "COCKPIT INTELIGENTE PARA GESTÃO OPERACIONAL.",
        "primary": "#0066FF",
        "secondary": "#00E5FF",
        "accent": "#00B4D8",
        "kind": "bars",
    },
    "vane": {
        "name": "VANE",
        "tagline": "INTELIGÊNCIA ARTIFICIAL PARA DECISÕES HUMANAS.",
        "primary": "#7C3AED",
        "secondary": "#A855F7",
        "accent": "#5821B6",
        "kind": "v",
    },
    "wic": {
        "name": "WIC",
        "tagline": "INTELIGÊNCIA PARA GESTÃO DE PESSOAS E ESCALAS.",
        "primary": "#00C896",
        "secondary": "#2DD4BF",
        "accent": "#14B8A6",
        "kind": "w",
    },
}


def hex_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i+2], 16) for i in (0, 2, 4))


def gradient_layer(size, first, second, horizontal=False):
    width, height = size
    image = Image.new("RGBA", size)
    pixels = image.load()
    a, b = hex_rgb(first), hex_rgb(second)
    for y in range(height):
        for x in range(width):
            ratio = x / max(width - 1, 1) if horizontal else y / max(height - 1, 1)
            pixels[x, y] = tuple(round(a[i] * (1-ratio) + b[i] * ratio) for i in range(3)) + (255,)
    return image


def symbol_mask(kind, size=400):
    base_size = 400
    mask = Image.new("L", (base_size, base_size), 0)
    draw = ImageDraw.Draw(mask)
    if kind == "bars":
        bars = [(45, 245, 95, 350), (125, 190, 175, 350), (205, 120, 255, 350), (285, 45, 335, 350)]
        for box in bars:
            draw.rounded_rectangle(box, radius=10, fill=255)
    elif kind == "v":
        draw.polygon([(35, 45), (135, 45), (225, 250), (180, 350)], fill=255)
        draw.polygon([(135, 45), (235, 45), (180, 170), (225, 250), (365, 45), (265, 45), (180, 245)], fill=255)
    else:
        for shift in (0, 105, 210):
            draw.polygon([(25+shift, 80), (95+shift, 80), (165+shift, 230), (115+shift, 330), (45+shift, 180)], fill=255)
            draw.polygon([(95+shift, 80), (145+shift, 80), (190+shift, 175), (165+shift, 230)], fill=255)
    return mask if size == base_size else mask.resize((size, size), Image.Resampling.LANCZOS)


def render_symbol(config, size=400, color_mode="brand", background=None):
    if background:
        image = Image.new("RGBA", (size, size), hex_rgb(background) + (255,))
    else:
        image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    mask = symbol_mask(config["kind"], size)
    if color_mode == "white":
        layer = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    elif color_mode == "black":
        layer = Image.new("RGBA", (size, size), (8, 13, 23, 255))
    else:
        layer = gradient_layer((size, size), config["secondary"], config["primary"], horizontal=True)
    image.alpha_composite(Image.composite(layer, Image.new("RGBA", (size, size)), mask))
    return image


def fit_font(path, size):
    return ImageFont.truetype(str(path), size)


def render_signature(config, width=1600, height=500, layout="horizontal", mode="positive"):
    dark = mode == "negative"
    background = (7, 12, 22, 255) if dark else ((255, 255, 255, 255) if mode == "positive" else (0, 0, 0, 0))
    image = Image.new("RGBA", (width, height), background)
    text_color = (255, 255, 255, 255) if dark else (8, 13, 23, 255)
    symbol_mode = "white" if mode == "mono-white" else "black" if mode == "mono-black" else "brand"
    if layout == "horizontal":
        symbol_size = int(height * .72)
        symbol = render_symbol(config, symbol_size, symbol_mode)
        image.alpha_composite(symbol, (int(height*.12), int(height*.14)))
        draw = ImageDraw.Draw(image)
        name_size = int(height*.26 if config["name"] != "MoniHook" else height*.23)
        name_font = fit_font(FONT_BOLD, name_size)
        tagline_font = fit_font(FONT_BOLD, int(height*.055))
        x = int(height*.92)
        y = int(height*.27)
        draw.text((x, y), config["name"], font=name_font, fill=text_color)
        draw.text((x, y+name_size+20), config["tagline"], font=tagline_font, fill=hex_rgb(config["secondary"])+(255,))
    else:
        symbol_size = int(height*.50)
        symbol = render_symbol(config, symbol_size, symbol_mode)
        image.alpha_composite(symbol, ((width-symbol_size)//2, int(height*.05)))
        draw = ImageDraw.Draw(image)
        name_font = fit_font(FONT_BOLD, int(height*.13))
        tagline_font = fit_font(FONT_BOLD, int(height*.035))
        bbox = draw.textbbox((0,0), config["name"], font=name_font)
        draw.text(((width-(bbox[2]-bbox[0]))//2, int(height*.60)), config["name"], font=name_font, fill=text_color)
        bbox2 = draw.textbbox((0,0), config["tagline"], font=tagline_font)
        draw.text(((width-(bbox2[2]-bbox2[0]))//2, int(height*.77)), config["tagline"], font=tagline_font, fill=hex_rgb(config["secondary"])+(255,))
    return image


def symbol_svg(config, mode="brand"):
    if mode == "white":
        fill = "#FFFFFF"
    elif mode == "black":
        fill = "#080D17"
    else:
        fill = "url(#brandGradient)"
    defs = f'<defs><linearGradient id="brandGradient" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{config["secondary"]}"/><stop offset="1" stop-color="{config["primary"]}"/></linearGradient></defs>'
    if config["kind"] == "bars":
        shapes = ''.join(f'<rect x="{x}" y="{y}" width="50" height="{350-y}" rx="10"/>' for x,y in [(45,245),(125,190),(205,120),(285,45)])
    elif config["kind"] == "v":
        shapes = '<path d="M35 45H135L225 250L180 350Z"/><path d="M135 45H235L180 170L225 250L365 45H265L180 245Z"/>'
    else:
        shapes = ''.join(f'<path d="M{25+s} 80H{95+s}L{165+s} 230L{115+s} 330L{45+s} 180Z"/><path d="M{95+s} 80H{145+s}L{190+s} 175L{165+s} 230Z"/>' for s in (0,105,210))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">{defs}<g fill="{fill}">{shapes}</g></svg>\n'


def signature_svg(config, layout="horizontal", mode="positive"):
    dark = mode == "negative"
    background = '<rect width="100%" height="100%" fill="#070C16"/>' if dark else ''
    text_color = "#FFFFFF" if dark else "#080D17"
    symbol_mode = "white" if mode == "mono-white" else "black" if mode == "mono-black" else "brand"
    symbol_content = symbol_svg(config, symbol_mode).split('>',1)[1].rsplit('</svg>',1)[0]
    if layout == "horizontal":
        transform = 'translate(45 45) scale(.72)'
        text = f'<text x="430" y="215" fill="{text_color}" font-family="Inter,Arial,sans-serif" font-size="128" font-weight="700">{config["name"]}</text><text x="435" y="285" fill="{config["secondary"]}" font-family="Inter,Arial,sans-serif" font-size="30" font-weight="700" letter-spacing="3">{config["tagline"]}</text>'
        viewbox = '0 0 1600 400'
    else:
        transform = 'translate(300 25) scale(.75)'
        text = f'<text x="450" y="460" text-anchor="middle" fill="{text_color}" font-family="Inter,Arial,sans-serif" font-size="115" font-weight="700">{config["name"]}</text><text x="450" y="535" text-anchor="middle" fill="{config["secondary"]}" font-family="Inter,Arial,sans-serif" font-size="23" font-weight="700" letter-spacing="2">{config["tagline"]}</text>'
        viewbox = '0 0 900 600'
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" role="img" aria-label="{config["name"]}">{background}<g transform="{transform}">{symbol_content}</g>{text}</svg>\n'


def draw_pdf_symbol(pdf, config, x, y, scale, color):
    pdf.setFillColor(color)
    if config["kind"] == "bars":
        for bx, by, h in [(45,245,105),(125,190,160),(205,120,230),(285,45,305)]:
            pdf.roundRect(x+bx*scale, y+(400-by-h)*scale, 50*scale, h*scale, 7*scale, fill=1, stroke=0)
    elif config["kind"] == "v":
        for points in [[(35,45),(135,45),(225,250),(180,350)],[(135,45),(235,45),(180,170),(225,250),(365,45),(265,45),(180,245)]]:
            path=pdf.beginPath(); path.moveTo(x+points[0][0]*scale,y+(400-points[0][1])*scale)
            for px,py in points[1:]: path.lineTo(x+px*scale,y+(400-py)*scale)
            path.close(); pdf.drawPath(path,fill=1,stroke=0)
    else:
        for shift in (0,105,210):
            points=[(25+shift,80),(95+shift,80),(165+shift,230),(115+shift,330),(45+shift,180)]
            path=pdf.beginPath(); path.moveTo(x+points[0][0]*scale,y+(400-points[0][1])*scale)
            for px,py in points[1:]: path.lineTo(x+px*scale,y+(400-py)*scale)
            path.close(); pdf.drawPath(path,fill=1,stroke=0)


def make_pdf(path, config, mode):
    width, height = 1000, 320
    pdf = canvas.Canvas(str(path), pagesize=(width,height))
    dark = mode == "negative"
    if dark:
        pdf.setFillColor(HexColor("#070C16")); pdf.rect(0,0,width,height,fill=1,stroke=0)
    symbol_color = HexColor("#FFFFFF" if mode == "mono-white" else "#080D17" if mode == "mono-black" else config["primary"])
    draw_pdf_symbol(pdf,config,40,20,.65,symbol_color)
    pdf.setFillColor(HexColor("#FFFFFF" if dark else "#080D17")); pdf.setFont("Helvetica-Bold",78); pdf.drawString(350,175,config["name"])
    pdf.setFillColor(HexColor(config["secondary"])); pdf.setFont("Helvetica-Bold",17); pdf.drawString(354,130,config["tagline"])
    pdf.setTitle(f'{config["name"]} reconstructed signature'); pdf.save()


for slug, config in BRANDS.items():
    base = OUT / slug
    for folder in ["svg", "png/symbol", "png/horizontal", "png/vertical", "png/app-icon", "pdf", "favicons", "docs", "tokens"]:
        (base / folder).mkdir(parents=True, exist_ok=True)

    for mode in ["brand", "white", "black"]:
        (base / "svg" / f"{slug}_symbol_{mode}.svg").write_text(symbol_svg(config, mode), encoding="utf-8")
    for layout in ["horizontal", "vertical"]:
        for mode in ["positive", "negative", "mono-black", "mono-white"]:
            (base / "svg" / f"{slug}_{layout}_{mode}.svg").write_text(signature_svg(config, layout, mode), encoding="utf-8")

    for size in [16, 32, 48, 64, 128, 256, 512, 1024]:
        render_symbol(config, size).save(base / "png" / "symbol" / f"{slug}_symbol_{size}px.png")
        app = Image.new("RGBA", (size,size), (7,12,22,255))
        margin=max(1,int(size*.12)); icon=render_symbol(config,size-2*margin); app.alpha_composite(icon,(margin,margin))
        app.save(base / "png" / "app-icon" / f"{slug}_app_icon_{size}px.png")
    render_symbol(config,512).save(base / "favicons" / f"{slug}_favicon.ico",sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])

    for width in [1024, 2048]:
        height=round(width*500/1600)
        for mode in ["positive", "negative", "mono-black", "mono-white"]:
            render_signature(config,width,height,"horizontal",mode).save(base / "png" / "horizontal" / f"{slug}_horizontal_{mode}_{width}px.png")
    for mode in ["positive", "negative"]:
        render_signature(config,1024,1024,"vertical",mode).save(base / "png" / "vertical" / f"{slug}_vertical_{mode}_1024px.png")

    for mode in ["positive", "negative", "mono-black", "mono-white"]:
        make_pdf(base / "pdf" / f"{slug}_horizontal_{mode}.pdf",config,mode)

    tokens = {"brand": config["name"], "status": "reconstructed-from-reference-board", "colors": {"primary": config["primary"], "secondary": config["secondary"], "accent": config["accent"], "dark": "#070C16", "white": "#FFFFFF"}, "typography": {"specified": "Inter", "fallbackUsedForRasterGeneration": "Arial"}}
    (base / "tokens" / "brand-tokens.json").write_text(json.dumps(tokens,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    files=[str(p.relative_to(base)).replace('\\','/') for p in base.rglob('*') if p.is_file()]
    manifest={"brand":config["name"],"status":"reconstructed-from-reference-board","referenceBoard":f"branding/reference-boards/{slug}-master-package.png","originalEditableSourceRecovered":False,"files":sorted(files)}
    (base / "docs" / "manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    readme=f'''# {config["name"]} — pacote vetorial reconstruído

Status: **reconstrução baseada na prancha de referência**.

Os 32 pacotes recuperados não continham arquivos vetoriais editáveis desta marca. Este conjunto foi reconstruído a partir de `branding/reference-boards/{slug}-master-package.png` para viabilizar aplicações digitais e documentação. Ele não substitui um arquivo-fonte original aprovado pela direção de marca.

## Conteúdo

- SVG: símbolo e assinaturas horizontal/vertical, positiva, negativa e monocromática.
- PNG: símbolos, assinaturas, favicons e app icons em múltiplos tamanhos.
- PDF: assinaturas para revisão e impressão.
- Tokens: cores documentadas e metadados de tipografia.

## Tipografia

A prancha especifica Inter. Como os arquivos da fonte não estavam presentes, os SVGs mantêm `Inter, Arial, sans-serif` e os PNGs usam Arial como fallback local. Antes de aprovação externa, compare a geometria e converta a tipografia para curvas em uma ferramenta vetorial licenciada.
'''
    (base / "docs" / "README.md").write_text(readme,encoding="utf-8")

print(f"Pacotes de produto gerados em {OUT}")
