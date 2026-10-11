"""Renderização aproximada da geometria PBIP revisada, com números ilustrativos.
Não executa DAX. Não usa consultas, imagens ou dados corporativos.
Instalação: python -m pip install Pillow
Execução: python scripts/gerar_previa_bi.py
"""
from pathlib import Path
import json,random,math
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]
BLUE='#2A6484'; LIGHT='#8CB6D9'; AQUA='#64ACAC'; GREY='#e5e7eb'; INK='#414b53'
rng=random.Random(77)
sample={'seed':77,'illustrative_only':True,'mapping':{'headcount':120,'corporate_machine':92,'own_machine':8,'no_machine':8,'unmapped':12,'collected':94,'never_collected':6,'recent':82,'attention':8,'critical':4},'daily_hours':[round(rng.uniform(510,660),1) for _ in range(22)],'daily_index':[round(rng.uniform(55,76),1) for _ in range(22)],'companies':['Empresa A','Empresa B','Empresa C','Empresa D'],'mapping_pct':[90,86.7,93.3,90]}
(R/'docs/visual-bi/amostra.json').write_text(json.dumps(sample,ensure_ascii=False,indent=2),encoding='utf8')
def font(n,b=False):
 for p in [('C:/Windows/Fonts/segoeuib.ttf' if b else 'C:/Windows/Fonts/segoeui.ttf'),('DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf')]:
  try:return ImageFont.truetype(p,max(10,int(n)))
  except OSError:pass
 return ImageFont.load_default(size=int(n))
def render(page):
 w,h=page['width'],page['height'];im=Image.new('RGB',(w,h+86),'white');d=ImageDraw.Draw(im)
 def txt(x,y,t,n=24,c=INK,b=False,center=False):
  f=font(n,b)
  if center:x-=d.textlength(t,font=f)/2
  d.text((x,y),t,font=f,fill=c)
 def wrap(x,y,t,width,n=23,c=INK,center=False):
  line='';lines=[]
  for word in t.split():
   if d.textlength((line+' '+word).strip(),font=font(n))>width and line:lines.append(line);line=word
   else:line=(line+' '+word).strip()
  if line:lines.append(line)
  for j,line in enumerate(lines):txt(x,y+j*(n+5),line,n,c,center=center)
 def cardbox(x,y,vw,vh):
  d.rounded_rectangle((x+3,y+4,x+vw,y+vh),radius=8,fill='#e0e0e0')
  d.rounded_rectangle((x,y,x+vw-3,y+vh-4),radius=8,fill='white',outline='#cccccc',width=1)
 def title(x,y,vw,label):txt(x+vw/2,y+10,label,25,BLUE,True,True)
 mapping=page['name']=='Mapeamento'
 for v in sorted(page['visuals'],key=lambda a:a['position']['z']):
  p=v['position'];x,y,vw,vh=[int(p[k]) for k in ['x','y','width','height']];t=v['type'];label=v['label']
  if t=='shape':
   if vw>100 and (vh>1000 or vh<50):d.rectangle((x,y,x+vw,y+vh),fill=BLUE)
  elif t=='textbox':
   if label.startswith('_'):d.line((x+10,y+15,x+vw-10,y+15),fill='white',width=1)
   else:wrap(x+vw/2,y+5,label,vw-8,27 if vw>250 else 20,'white' if x<190 else BLUE,True)
  elif t=='slicer':
   wrap(x+8,y+4,label,vw-12,18,'white')
   if label=='Empresa' and vh>120:
    for i,name in enumerate(sample['companies']):txt(x+9,y+32+i*25,'□ '+name,17,'white')
   elif 'Status' in label or label=='Classificação':
    for i,name in enumerate(['Todos','Categoria A','Categoria B','Categoria C']):txt(x+9,y+90+i*26,'□ '+name,17,'white')
   else:
    d.rectangle((x+7,y+38,x+vw-9,y+65),outline='#b9d0df');txt(x+12,y+40,'Todos  v' if label!='Data' else 'Jun / 2025',17,'white')
  elif t=='cardVisual':
   if vh<80:
    if y<240:txt(x+vw/2,y+9,'Exemplo sintético',17,BLUE,center=True)
    else:txt(x+vw/2,y+28,'Série ilustrativa',19,BLUE,center=True)
    continue
   cardbox(x,y,vw,vh);wrap(x+vw/2,y+12,label,vw-12,22,BLUE,True)
   values={'Headcount':'120','Com Máquina':'92','Máquina Própria':'8','Sem Máquina':'8','Não Mapeados':'12','Sucesso na Implantação':'94','Erro na Implantação':'6','Cobertura de Implantação':'94,0%','Recente':'82','Atenção':'8','Crítica':'4','Saúde':'87,2%','Índice de Performance':'65,4%','Aderência à Jornada':'82,0%','Eficiência Operacional':'79,8%','Total Mapeado':'108'}
   value=values.get(label,'—')
   if label=='Horas Monitoradas':value=(f'{sum(sample["daily_hours"]):,.0f}'.replace(',','.')+' h') if x<1100 else ('08:00' if x<1400 else '18:00')
   txt(x+vw/2,y+69,value,42,'#666666',False,True)
   if mapping:txt(x+vw/2,y+127,'Cenário fictício',17,'#888888',center=True)
  elif t in ['tableEx','pivotTable']:
   cardbox(x,y,vw,vh);title(x,y,vw,label)
   cols=['Empresa','Identificação','Área','Situação','Coleta'] if mapping else ['Empresa','Identificação','Área','Horas','Índice ilustrativo']
   if t=='pivotTable':cols=['Atividade','Categoria','Horas','Participação']
   cy=y+62;colw=(vw-30)/len(cols)
   d.rectangle((x+12,cy,x+vw-12,cy+35),fill=BLUE)
   for i,c in enumerate(cols):txt(x+20+i*colw,cy+3,c,19,'white')
   for j in range(min(9,int((vh-115)/35))):
    yy=cy+38+j*35
    if j%2==0:d.rectangle((x+12,yy,x+vw-12,yy+33),fill='#edf3f7')
    row=['Empresa '+chr(65+j%4),f'Pessoa fictícia {j+1:03}',f'Área {j%4+1}','Mapeado' if mapping else str(100+j*3)+' h','Recente' if mapping else f'{60+j},0%']
    if t=='pivotTable':row=[f'Atividade {j+1}',f'Categoria {j%3+1}',str(240-j*17),f'{100*(240-j*17)/sum(240-k*17 for k in range(9)):.1f}%']
    for i,c in enumerate(row):txt(x+20+i*colw,yy+3,c,18)
   txt(x+20,y+vh-36,'Exibição de amostra fictícia; não contém registros do relatório original.',17,'#888888')
  else:
   cardbox(x,y,vw,vh);title(x,y,vw,label)
   px=x+105;py=y+70;pw=vw-150;ph=vh-140
   if t=='hundredPercentStackedAreaChart':
    # Two stacked bands, preserving the original visual type.
    points=[(px+i*pw/3,py+ph*(1-a/100)) for i,a in enumerate(sample['mapping_pct'])]
    d.polygon([(px,py)]+[(px+pw,py)]+list(reversed(points)),fill='#EB1E2D')
    d.polygon(points+[(px+pw,py+ph),(px,py+ph)],fill='#29AE3F')
    for i,(cx,cy) in enumerate(points):txt(max(px+50,min(px+pw-50,cx)),cy+ph/3,str(sample['mapping_pct'][i]).replace('.',',')+'%',22,'white',True,True);txt(max(px+70,min(px+pw-70,cx)),py+ph+15,sample['companies'][i],19,center=True)
    txt(px,py-25,'Mapeados',18,'#29AE3F');txt(px+190,py-25,'Não mapeados',18,'#EB1E2D')
    for val in [0,50,100]:txt(px-73,py+ph*(1-val/100)-10,f'{val}%',17)
   elif t=='lineStackedColumnComboChart':
    for k in [0,200,400,600,800]:
     yy=py+ph*(1-k/800);d.line((px,yy,px+pw,yy),fill=GREY);txt(px-80,yy-13,f'{k} h',18)
    pts=[]
    for i,a in enumerate(sample['daily_hours']):
     cx=px+(i+.5)*pw/22;top=py+ph*(1-a/800);d.rectangle((cx-18,top,cx+18,py+ph),fill='#33639B')
     pts.append((cx,py+ph*(1-sample['daily_index'][i]/100)))
     if i%2==0:txt(cx,py+ph+13,str(i+1).zfill(2),18,center=True)
    d.line(pts,fill='#FBA324',width=4)
    for k in [0,50,100]:txt(px+pw+7,py+ph*(1-k/100)-10,f'{k}%',16,BLUE)
    txt(px+pw/2,py+ph+40,'Dias úteis fictícios • barras: horas / linha: índice ilustrativo',19,center=True)
   elif t=='areaChart':
    vals=[.08,.15,.38,.68,.83,.88,.65,.56,.76,.86,.8,.64,.32,.12]
    pts=[(px+i*pw/13,py+ph*(1-a)) for i,a in enumerate(vals)]
    for factor,col in [(1.0,'#29AE3F'),(.25,'#FBA324'),(.08,'#EB1E2D')]:
     series=[(px+i*pw/13,py+ph*(1-a*factor)) for i,a in enumerate(vals)]
     d.polygon([(px,py+ph)]+series+[(px+pw,py+ph)],fill=col)
     d.line(series,fill=col,width=3)
    for i in range(14):txt(px+i*pw/13,py+ph+18,f'{i+6:02}:00',18,center=True)
    for i,(name,col) in enumerate([('Produtivo','#29AE3F'),('Neutro','#FBA324'),('Improdutivo','#EB1E2D')]):
     txt(px+i*245,py-20,name,18,col)
   else:
    labels=(['Área 1','Área 2','Área 3','Área 4'] if 'Centro' in label or label in ['Diretoria','Departamentos'] else ['Categoria A','Categoria B','Categoria C','Categoria D'])
    if label=='Ferramentas':labels=['Ferramenta A','Ferramenta B','Ferramenta C','Ferramenta D']
    if t=='barChart':
     legend=[('Mapeado','#94BCC4'),('Não mapeado','#FBA324'),('Máq. pessoal',BLUE),('Sem máquina','#757E8B')] if mapping else [('Produtivo','#29AE3F'),('Neutro','#FBA324'),('Improdutivo','#EB1E2D')]
     for k,(name,col) in enumerate(legend):txt(x+25+k*(vw-50)/len(legend),y+48,name,17,col)
     py+=35;ph-=35
    for i,lab in enumerate(labels):
     yy=py+i*ph/4;txt(x+20,yy+10,lab,20);start=x+vw*.24;value=sample['mapping_pct'][i] if mapping else 87-i*12;length=(vw*.67)*value/100
     if t=='barChart':
      pieces=[(.78,'#94BCC4'),(.10,'#FBA324'),(.06,BLUE),(.06,'#757E8B')] if mapping else [(.72,'#29AE3F'),(.20,'#FBA324'),(.08,'#EB1E2D')]
      at=start
      for share,col in pieces:
       d.rectangle((at,yy,at+length*share,yy+32),fill=col);at+=length*share
     else:
      col='#29AE3F' if value>=75 else ('#3C9394' if value>=60 else '#E77517')
      d.rectangle((start,yy,start+length,yy+32),fill=col)
     txt(start+length+9,yy+4,f'{value:g}%',18,BLUE)
    txt(x+vw/2,y+vh-38,'Valores ilustrativos • escala de 0% a 100%',18,'#888888',center=True)
 # White label outside the original canvas distinguishes reference layout from actual rendering.
 d.rectangle((0,h,w,h+86),fill='#eef4f8')
 txt(w/2,h+10,'LAYOUT DO PBIP • DADOS FICTÍCIOS • RENDERIZAÇÃO APROXIMADA',24,BLUE,True,True)
 txt(w/2,h+47,'Posições e títulos preservados; sem executar DAX, sem logos e sem dados empresariais.',21,INK,center=True)
 path=R/'docs/imagens'/('mapeamento' if mapping else 'analytics')
 im.save(str(path)+'-completo.png')
 # A readable first section for the README, with disclosure always visible.
 cropheight=1258 if mapping else 1478
 crop=im.crop((0,0,w,cropheight));preview=Image.new('RGB',(w,cropheight+86),'white');preview.paste(crop);preview.paste(im.crop((0,h,w,h+86)),(0,cropheight));preview.save(str(path)+'.png')
 print(page['name'])
if __name__=='__main__':
 for page in json.loads((R/'docs/visual-bi/layout.json').read_text(encoding='utf8'))['pages']:render(page)
