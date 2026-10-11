"""Gera prévias ilustrativas do portfólio a partir dos agregados sintéticos.
Requer Pillow (python -m pip install Pillow). Não lê arquivos empresariais.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'reports/metrics.json').read_text(encoding='utf8'))['monthly']
MONTHS=['Jan','Fev','Mar','Abr','Mai','Jun']
BG='#f1f5f9'; INK='#162638'; MUTED='#53687b'; TEAL='#087f8c'; LINE='#dbe5ed'
def font(n,bold=False):
    candidates=['C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf','DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf']
    for c in candidates:
        try:return ImageFont.truetype(c,n)
        except OSError:pass
    return ImageFont.load_default(size=n)
def pct(v):return f'{v*100:.1f}%'.replace('.',',')
def num(v):return f'{v:,.0f}'.replace(',','.')
def render(mapping):
    im=Image.new('RGB',(1600,1000),BG);d=ImageDraw.Draw(im)
    def txt(x,y,t,size=20,color=INK,bold=False): d.text((x,y),t,font=font(size,bold),fill=color)
    def box(x,y,w,h,color='white'):d.rounded_rectangle((x,y,x+w,y+h),radius=15,fill=color)
    d.rectangle((0,0,235,1000),fill='#112638')
    txt(26,38,'PRODUTIVIDADE',23,'white',True);txt(26,76,'PORTFÓLIO / BI',15,'#8fbbca')
    for i,n in enumerate(['Visão geral','Analytics','Mapeamento','Backend']):
        y=174+i*65
        if i==(2 if mapping else 1):box(15,y-12,204,49,'#224b60')
        txt(29,y,n,20,'white')
    txt(27,805,'VERSÃO PÚBLICA',14,'#8fbbca',True)
    txt(27,838,'Dados sintéticos',17,'white')
    txt(27,870,'Jan — Jun / 2025',17,'#8fbbca')
    title='Controle de mapeamento' if mapping else 'Analytics operacional'
    txt(275,30,title,36,bold=True)
    txt(275,84,'Prévia reconstruída para o portfólio • não é uma captura do Power BI original',18,MUTED)
    box(275,125,1275,53)
    txt(298,139,'PERÍODO  Junho / 2025',18,bold=True);txt(675,139,'ÁREA  Todas as áreas',18,bold=True)
    txt(1190,140,'Cenário demonstrativo',16,TEAL,True)
    total=[r for r in DATA if r['department_id']==0];cur=total[-1]
    cards=([('Elegíveis no mês',num(cur['eligible_employees']),'Vínculo em parte do mês'),('Mapeados',num(cur['mapped_employees']),'Sinal de mapeamento = 1'),('Não mapeados',num(cur['eligible_employees']-cur['mapped_employees']),'Lacuna de cobertura'),('Cobertura',pct(cur['mapping_coverage']),'Mapeados / elegíveis')] if mapping else [('Headcount final',num(cur['headcount']),'Ativos no último dia'),('Folha demonstrativa','R$ 1,35 mi','Salário-base proporcional'),('Cobertura de coleta',pct(cur['collection_coverage']),'Tempo capturado / previsto'),('Atividade observada',pct(cur['observed_activity_ratio']),'Tempo produtivo / capturado')])
    for i,(a,b,c) in enumerate(cards):
        x=275+i*322;box(x,202,307,144);txt(x+19,222,a,18,MUTED);txt(x+19,257,b,37,TEAL,True);txt(x+19,312,c,15,MUTED)
    box(275,369,762,339);box(1060,369,490,339)
    metric='mapping_coverage' if mapping else 'collection_coverage'
    txt(300,389,'Cobertura de mapeamento' if mapping else 'Cobertura de coleta',24,bold=True)
    txt(300,425,'Evolução mensal • escala de 0% a 100%',17,MUTED)
    for p in [0,.5,1]:
        y=652-p*160;d.line((355,y,1005,y),fill=LINE,width=1);txt(302,y-10,f'{int(p*100)}%',14,MUTED)
    for i,row in enumerate(total):
        x=390+i*105;h=row[metric]*160;d.rounded_rectangle((x,652-h,x+56,652),radius=5,fill=TEAL)
        txt(x-4,652-h-27,pct(row[metric]),15,INK,True);txt(x+5,665,MONTHS[i],15,MUTED)
    txt(1084,389,'Cobertura por área',24,bold=True)
    txt(1084,425,'Junho • mesma escala de 0% a 100%',16,MUTED)
    for i,row in enumerate([r for r in DATA if r['month']==cur['month'] and r['department_id']]):
        y=463+i*53;txt(1084,y,row['department'],17);txt(1460,y,pct(row[metric]),16,TEAL,True)
        d.rounded_rectangle((1084,y+27,1517,y+37),radius=5,fill=LINE)
        d.rounded_rectangle((1084,y+27,1084+433*row[metric],y+37),radius=5,fill=TEAL)
    box(275,730,1275,187)
    txt(300,748,'O que este recorte permite investigar',23,bold=True)
    lines=(['13 vínculos elegíveis ainda não estão mapeados no mês.','209 elegíveis no período e 204 ativos no último dia: denominadores diferentes.','Antes de comparar áreas, investigue as lacunas de mapeamento e coleta.'] if mapping else ['Coleta e atividade observada medem coisas diferentes: 82,2% versus 68,3%.','A ausência de observação não comprova ausência de trabalho.','A simulação não mede valor entregue nem sustenta ranking individual.'])
    for i,t in enumerate(lines):txt(300,789+i*32,t,19,MUTED)
    txt(275,945,'Fonte: reports/metrics.json • seed 42 • layout ilustrativo • nenhum dado empresarial',17,MUTED)
    out=ROOT/'docs/imagens'/('mapeamento.png' if mapping else 'analytics.png');out.parent.mkdir(parents=True,exist_ok=True);im.save(out)
    print(out.name)
if __name__=='__main__':
    render(False);render(True)
