from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import csv, html, json, textwrap

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGNS = ROOT / "marketing" / "campaigns"
BACKGROUND = CAMPAIGNS / "shared" / "assets" / "humanati-data-flow-hero-v1.png"
FONT_REGULAR = Path("C:/Windows/Fonts/arial.ttf")
FONT_BOLD = Path("C:/Windows/Fonts/arialbd.ttf")

FORMATS = {
    "feed-1080x1080": (1080,1080),
    "story-1080x1920": (1080,1920),
    "linkedin-1200x627": (1200,627),
    "display-1200x628": (1200,628),
}

BRANDS = {
    "humanati": {
        "name":"HUMANATI", "eyebrow":"INTELIGÊNCIA PARA GESTÃO", "color":"#0066FF", "secondary":"#00D4FF",
        "title":"Decisões melhores começam com dados conectados.",
        "body":"Unifique pessoas, operações e estratégia em uma visão confiável.", "cta":"SOLICITE UM DIAGNÓSTICO",
        "logo_png":ROOT/"branding/png/Horizontal/humanati_horizontal_negative_white_2048px.png",
        "logo_svg":"../../../../branding/svg/Horizontal/humanati_horizontal_negative_white.svg",
    },
    "monihook": {
        "name":"MoniHook", "eyebrow":"COCKPIT INTELIGENTE", "color":"#0066FF", "secondary":"#00E5FF",
        "title":"Do sinal à ação em tempo real.",
        "body":"Centralize indicadores, antecipe alertas e entregue insights para uma gestão mais ágil.", "cta":"CONHEÇA O MONIHOOK",
        "logo_png":ROOT/"branding/products/monihook/png/horizontal/monihook_horizontal_negative_2048px.png",
        "logo_svg":"../../../../branding/products/monihook/svg/monihook_horizontal_negative.svg",
    },
    "vane": {
        "name":"VANE", "eyebrow":"PLANEJAMENTO COM IA", "color":"#7C3AED", "secondary":"#A855F7",
        "title":"Planeje cenários. Decida com confiança.",
        "body":"Transforme sinais em cenários claros e recomendações acionáveis para a liderança.", "cta":"CONHEÇA A VANE",
        "logo_png":ROOT/"branding/products/vane/png/horizontal/vane_horizontal_negative_2048px.png",
        "logo_svg":"../../../../branding/products/vane/svg/vane_horizontal_negative.svg",
    },
    "wic": {
        "name":"WIC", "eyebrow":"WORKFORCE INTELLIGENCE", "color":"#00C896", "secondary":"#2DD4BF",
        "title":"Pessoas certas. Escalas inteligentes. Resultados reais.",
        "body":"Conecte capacidade, jornadas e produtividade para decisões melhores sobre sua força de trabalho.", "cta":"CONHEÇA O WIC",
        "logo_png":ROOT/"branding/products/wic/png/horizontal/wic_horizontal_negative_2048px.png",
        "logo_svg":"../../../../branding/products/wic/svg/wic_horizontal_negative.svg",
    },
}

def rgb(value):
    value=value.lstrip('#'); return tuple(int(value[i:i+2],16) for i in (0,2,4))

def font(path,size): return ImageFont.truetype(str(path),size)

def cover(image,size):
    w,h=size; ratio=max(w/image.width,h/image.height); resized=image.resize((round(image.width*ratio),round(image.height*ratio)),Image.Resampling.LANCZOS)
    left=(resized.width-w)//2; top=(resized.height-h)//2
    return resized.crop((left,top,left+w,top+h))

def tinted_background(size, color):
    base=cover(Image.open(BACKGROUND).convert('RGB'),size)
    overlay=Image.new('RGB',size,rgb(color)); base=Image.blend(base,overlay,.11)
    shade=Image.new('L',size); sd=ImageDraw.Draw(shade)
    w,h=size
    for x in range(w): sd.line((x,0,x,h),fill=max(0,min(255,230-round(175*x/max(w-1,1)))))
    dark=Image.new('RGB',size,(3,7,15)); base=Image.composite(dark,base,shade)
    return base

def paste_logo(canvas,path,max_width,max_height,x,y):
    logo=Image.open(path).convert('RGBA')
    scale=min(max_width/logo.width,max_height/logo.height)
    logo=logo.resize((round(logo.width*scale),round(logo.height*scale)),Image.Resampling.LANCZOS)
    canvas.alpha_composite(logo,(x,y)); return logo.size

def wrap_text(draw,text,typeface,max_width):
    words=text.split(); lines=[]; current=''
    for word in words:
        candidate=(current+' '+word).strip()
        if draw.textbbox((0,0),candidate,font=typeface)[2] <= max_width: current=candidate
        else:
            if current: lines.append(current)
            current=word
    if current: lines.append(current)
    return lines

def draw_campaign(slug,config,format_name,size):
    w,h=size; image=tinted_background(size,config['color']).convert('RGBA'); draw=ImageDraw.Draw(image)
    portrait=h/w>1.3; margin=round(w*.07)
    image.alpha_composite(Image.new('RGBA',size,(2,6,14,45)))
    logo_h=round(h*(.11 if portrait else .16)); paste_logo(image,config['logo_png'],round(w*.46),logo_h,margin,round(h*.055))
    eyebrow_y=round(h*(.25 if portrait else .31)); eyebrow_font=font(FONT_BOLD,round(w*(.025 if portrait else .018)))
    draw.text((margin,eyebrow_y),config['eyebrow'],font=eyebrow_font,fill=rgb(config['secondary'])+(255,))
    title_size=round(w*(.075 if portrait else .061)); title_font=font(FONT_BOLD,title_size); title_lines=wrap_text(draw,config['title'],title_font,round(w*(.82 if portrait else .62)))
    y=eyebrow_y+round(title_size*.8)
    for line in title_lines:
        draw.text((margin,y),line,font=title_font,fill=(255,255,255,255)); y+=round(title_size*1.02)
    body_font=font(FONT_REGULAR,round(w*(.030 if portrait else .020))); body_lines=wrap_text(draw,config['body'],body_font,round(w*(.78 if portrait else .55)))
    y+=round(h*.025)
    for line in body_lines:
        draw.text((margin,y),line,font=body_font,fill=(185,199,220,255)); y+=round(body_font.size*1.35)
    cta_y=min(round(h*.84),y+round(h*.05)); cta_font=font(FONT_BOLD,round(w*(.024 if portrait else .016)))
    cta_w=draw.textbbox((0,0),config['cta'],font=cta_font)[2]+round(w*.055); cta_h=round(cta_font.size*2.8)
    draw.rounded_rectangle((margin,cta_y,margin+cta_w,cta_y+cta_h),radius=cta_h//3,fill=rgb(config['color'])+(255,))
    draw.text((margin+round(w*.027),cta_y+(cta_h-cta_font.size)//2-2),config['cta'],font=cta_font,fill=(255,255,255,255))
    draw.text((margin,h-round(h*.055)),"humanati.com.br",font=font(FONT_BOLD,round(w*.016)),fill=(148,163,184,255))
    return image

def svg_source(slug,config,format_name,size):
    w,h=size; portrait=h/w>1.3; margin=round(w*.07); eyebrow_y=round(h*(.25 if portrait else .31)); title_size=round(w*(.075 if portrait else .061)); max_chars=20 if portrait else 28
    title_lines=textwrap.wrap(config['title'],width=max_chars); body_lines=textwrap.wrap(config['body'],width=38 if portrait else 54)
    title_y=eyebrow_y+round(title_size*.9); body_y=title_y+len(title_lines)*round(title_size*1.04)+round(h*.025); cta_y=min(round(h*.84),body_y+len(body_lines)*round(w*.04)+round(h*.045))
    tspans=''.join(f'<tspan x="{margin}" dy="{0 if i==0 else round(title_size*1.04)}">{html.escape(line)}</tspan>' for i,line in enumerate(title_lines))
    body_spans=''.join(f'<tspan x="{margin}" dy="{0 if i==0 else round(w*.04)}">{html.escape(line)}</tspan>' for i,line in enumerate(body_lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">
<defs><linearGradient id="shade" x1="0" x2="1"><stop offset="0" stop-color="#03070F" stop-opacity=".96"/><stop offset=".72" stop-color="#03070F" stop-opacity=".08"/></linearGradient></defs>
<image href="../../shared/assets/humanati-data-flow-hero-v1.png" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/>
<rect width="{w}" height="{h}" fill="url(#shade)"/>
<image href="{config['logo_svg']}" x="{margin}" y="{round(h*.055)}" width="{round(w*.46)}" height="{round(h*(.11 if portrait else .16))}" preserveAspectRatio="xMinYMid meet"/>
<text x="{margin}" y="{eyebrow_y}" fill="{config['secondary']}" font-family="Inter,Arial,sans-serif" font-size="{round(w*(.025 if portrait else .018))}" font-weight="700" letter-spacing="2">{html.escape(config['eyebrow'])}</text>
<text x="{margin}" y="{title_y}" fill="#FFFFFF" font-family="Sora,Arial,sans-serif" font-size="{title_size}" font-weight="700">{tspans}</text>
<text x="{margin}" y="{body_y}" fill="#B9C7DC" font-family="Inter,Arial,sans-serif" font-size="{round(w*(.030 if portrait else .020))}">{body_spans}</text>
<rect x="{margin}" y="{cta_y}" width="{round(w*.31)}" height="{round(h*.075)}" rx="{round(h*.02)}" fill="{config['color']}"/>
<text x="{margin+round(w*.025)}" y="{cta_y+round(h*.047)}" fill="#FFFFFF" font-family="Inter,Arial,sans-serif" font-size="{round(w*(.024 if portrait else .016))}" font-weight="700">{html.escape(config['cta'])}</text>
<text x="{margin}" y="{h-round(h*.04)}" fill="#94A3B8" font-family="Inter,Arial,sans-serif" font-size="{round(w*.016)}" font-weight="700">humanati.com.br</text>
</svg>\n'''

rows=[]
for slug,config in BRANDS.items():
    source_dir=CAMPAIGNS/slug/'source'; export_dir=CAMPAIGNS/slug/'exports'; docs_dir=CAMPAIGNS/slug/'docs'
    for folder in (source_dir,export_dir,docs_dir): folder.mkdir(parents=True,exist_ok=True)
    for format_name,size in FORMATS.items():
        draw_campaign(slug,config,format_name,size).save(export_dir/f'{slug}-{format_name}.png',optimize=True)
        (source_dir/f'{slug}-{format_name}.svg').write_text(svg_source(slug,config,format_name,size),encoding='utf-8')
        rows.append({'campaign':slug,'brand':config['name'],'format':format_name,'headline':config['title'],'supporting_copy':config['body'],'cta':config['cta'],'destination':'https://humanati.com.br/','utm_campaign':f'{slug}-always-on','source':f'marketing/campaigns/{slug}/source/{slug}-{format_name}.svg','export':f'marketing/campaigns/{slug}/exports/{slug}-{format_name}.png'})
    (docs_dir/'README.md').write_text(f'''# Campanha {config['name']}

Conceito: **{config['title']}**

O diretório `source/` contém os SVGs editáveis; `exports/` contém os PNGs finais. O fundo foi gerado especificamente para o ecossistema Humanati e as assinaturas de produto são reconstruções baseadas nas pranchas fornecidas, pendentes de validação final de marca.
''',encoding='utf-8')

with open(CAMPAIGNS/'campaign-assets.csv','w',newline='',encoding='utf-8-sig') as file:
    writer=csv.DictWriter(file,fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)

(CAMPAIGNS/'README.md').write_text('''# Kit de campanhas Humanati

Campanhas guarda-chuva e de produto para Humanati, MoniHook, VANE e WIC.

## Formatos

- Feed: 1080 × 1080.
- Story/Reels: 1080 × 1920.
- LinkedIn: 1200 × 627.
- Display/Meta landscape: 1200 × 628.

Cada peça possui fonte SVG editável e exportação PNG. Consulte `campaign-assets.csv` para mensagens, CTAs, destinos e nomes de campanha.
''',encoding='utf-8')
print(f'{len(rows)} peças geradas em {CAMPAIGNS}')
