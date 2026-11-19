# Smart City MDM - demonstracao interativa para JupyterLab
# Dependencias: ipywidgets>=8, plotly>=5, numpy>=1.24
from IPython.display import display, clear_output
import ipywidgets as widgets
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import asyncio
import html

BG='#07111F'; PANEL='#101E31'; PANEL2='#14243A'; MUTED='#9DB1C8'; TEXT='#EFF7FF'; GREEN='#54E1C1'; AMBER='#FFC270'; RED='#FF7B86'; BLUE='#74B5FF'
EVENTS={
 'road':('Obra emergencial na Av. Central','Obras Públicas'),
 'water':('Rompimento de adutora na Av. Central','Saneamento'),
 'electric':('Falha elétrica na Av. Central','Energia'),
}
NODES={'event':(0.5,.90),'hub':(.5,.59),'transport':(.18,.20),'water':(.5,.20),'energy':(.82,.20)}
NAMES={'event':'Ocorrência','hub':'Integração','transport':'Transporte','water':'Saneamento','energy':'Energia'}
IDS={'transport':'TRN-4881','water':'SN-AVC-12','energy':'GRD-X20'}

STYLE='''<style>
.sc-title{background:linear-gradient(110deg,#132a43,#0d1929);padding:24px 27px;border:1px solid #294361;border-radius:18px;color:#f1f7ff;font-family:Arial,sans-serif}
.sc-kicker{font-size:11px;color:#54e1c1;font-weight:800;letter-spacing:2px}.sc-head{font-size:30px;line-height:1.18;font-weight:800;margin:9px 0}.sc-sub{font-size:14px;color:#a7bdd4;line-height:1.55}
.sc-metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:8px 0;font-family:Arial,sans-serif}
.sc-metric{background:#14243a;border:1px solid #2a405a;border-radius:13px;padding:15px;color:#fff}.sc-metric small{display:block;color:#9db1c8;font-size:11px;margin-top:8px}.sc-metric strong{font-size:26px}
.sc-tag{background:#183b42;color:#75ebd2;border-radius:20px;padding:4px 9px;font-size:11px}
.sc-mapping,.sc-logs{background:#101e31;border:1px solid #263b56;border-radius:13px;padding:18px;color:#dae8f7;font-family:Arial,sans-serif;font-size:13px;line-height:1.65}
.sc-logs{max-height:235px;overflow:auto}.sc-logs .entry{border-bottom:1px solid #29405b;padding:4px 0}.sc-mapping table{border-collapse:collapse;width:100%}.sc-mapping td,.sc-mapping th{text-align:left;border-bottom:1px solid #2a405a;padding:8px}.sc-mapping th{color:#9db1c8}
.sc-foot{color:#9db1c8;font:12px Arial,sans-serif;line-height:1.5;padding:12px 3px}
</style>'''

def card(label,value,colour=TEXT):
 return f'<div class="sc-metric"><strong style="color:{colour}">{value}</strong><small>{label}</small></div>'

class SmartCityMDMDemo:
    """Experimento DIDATICO, deterministico e parametrizado (nao calibrado)."""
    def __init__(self):
        self.step_count=0; self.logs=[]; self.playing=False
        self.event=widgets.Dropdown(options=[(v[0],k) for k,v in EVENTS.items()],value='road',description='Ocorrência:',style={'description_width':'initial'},layout=widgets.Layout(width='390px'))
        self.speed=widgets.Dropdown(options=[('Lenta',1.15),('Normal',.60),('Rápida',.26)],value=.60,description='Ritmo:',style={'description_width':'initial'},layout=widgets.Layout(width='170px'))
        self.start=widgets.Button(description='▶ Executar comparação',button_style='success',layout=widgets.Layout(width='210px'))
        self.next=widgets.Button(description='→ Próximo passo',layout=widgets.Layout(width='155px'))
        self.reset_button=widgets.Button(description='↺ Reiniciar',layout=widgets.Layout(width='130px'))
        self.head=widgets.HTML(STYLE+'<div class="sc-title"><div class="sc-kicker">IA006 • CIÊNCIA DOS SISTEMAS COMPLEXOS</div><div class="sc-head">Uma cidade. Dois cenários.</div><div class="sc-sub">Modelagem ilustrativa: como referências semânticas compartilhadas podem afetar a coordenação de agentes urbanos?</div></div>')
        self.metrics=widgets.HTML()
        self.mapping=widgets.HTML('''<div class="sc-mapping"><strong>CATÁLOGO DE IDENTIDADES</strong><table><tr><th>Domínio</th><th>ID local</th><th>Entidade mestre</th></tr><tr><td>🚦 Transporte</td><td>TRN-4881</td><td>VIA-00042</td></tr><tr><td>💧 Saneamento</td><td>SN-AVC-12</td><td>VIA-00042</td></tr><tr><td>⚡ Energia</td><td>GRD-X20</td><td>VIA-00042</td></tr></table><p><b>Hipótese:</b> a reconciliação semântica pode reduzir ambiguidades e melhorar a coordenação.</p></div>''')
        self.logbox=widgets.HTML()
        self.chart=widgets.Output(layout=widgets.Layout(width='100%'))
        self.footer=widgets.HTML('<div class="sc-foot">⚠️ <b>Modelo conceitual.</b> Os passos e resultados são hipotéticos, definidos para fins didáticos. Não representam dados observados nem estimativas de ganhos de MDM em cidades reais. O MDM governa entidades; mensageria e operações permanecem sistemas independentes.</div>')
        self.start.on_click(self._start); self.next.on_click(self._next); self.reset_button.on_click(self._reset); self.event.observe(self._changed,names='value')
        self.ui=widgets.VBox([self.head,widgets.HBox([self.event,self.speed,self.start,self.next,self.reset_button],layout=widgets.Layout(flex_flow='row wrap',gap='9px',padding='12px 0')),self.metrics,self.chart,widgets.HBox([self.mapping,self.logbox],layout=widgets.Layout(gap='12px',align_items='stretch')),self.footer],layout=widgets.Layout(width='100%',max_width='1300px',gap='8px'))
        self.reset()

    def display(self): display(self.ui)
    def _changed(self,change): self.reset()
    def _reset(self,b): self.reset()
    def _next(self,b): self.playing=False; self.advance()
    def _start(self,b):
        if self.playing:return
        self.reset();self.playing=True
        asyncio.ensure_future(self._run())
    async def _run(self):
        while self.playing and self.step_count<7:
            self.advance()
            await asyncio.sleep(self.speed.value)
        self.playing=False
    def reset(self):
        self.playing=False;self.step_count=0
        self.logs=['Selecione uma ocorrência e execute a comparação, ou avance manualmente.']
        self.render()
    def advance(self):
        if self.step_count>=7: return
        self.step_count+=1
        s=self.step_count
        ev=EVENTS[self.event.value][0]
        if s==1:self.logs.append(f'T1 · Ambos — ocorrência registrada: {ev}.')
        if s==2:self.logs.extend(['T2 · Sem MDM — evento ainda sem correspondência universal.','T2 · Com MDM — AV-CENTRAL reconciliado com VIA-00042.'])
        if s==3:self.logs.extend(['T3 · Com MDM — 3 órgãos relacionaram a ocorrência à via.','T3 · Sem MDM — Transporte reconheceu a via; outras 2 correspondências pendentes.'])
        if s==4:self.logs.append('T4 · Sem MDM — iniciou reconciliação manual.')
        if s==5:self.logs.append('T5 · Sem MDM — Saneamento reconciliado.')
        if s==6:self.logs.append('T6 · Sem MDM — pendência no cadastro de Energia.')
        if s==7:self.logs.append('T7 · Sem MDM — último órgão informado. Comparação completa.')
        self.render()
    def _counts(self,with_mdm):
        s=self.step_count
        if with_mdm:return (3 if s>=3 else 0,0,3 if s>=3 else '—')
        return (3 if s>=7 else 2 if s>=5 else 1 if s>=3 else 0, 2 if 3<=s<5 else 1 if 5<=s<7 else 0, 7 if s>=7 else '—')
    def _diagram(self):
        fig=make_subplots(rows=1,cols=2,subplot_titles=['SEM MDM  •  referências fragmentadas','COM MDM FEDERADO  •  identidade compartilhada'],horizontal_spacing=.055)
        for col,mdm in [(1,False),(2,True)]:
            count,errors,_=self._counts(mdm)
            names=['event','hub','transport','water','energy']
            for dst in ['hub','transport','water','energy']:
                src='event' if dst=='hub' else 'hub'
                active=self.step_count>=2 if dst=='hub' else (self.step_count>=3 if mdm else self.step_count>= {'transport':3,'water':5,'energy':7}[dst])
                pending=not mdm and self.step_count>=3 and dst in ['water','energy'] and not active
                color=GREEN if active else AMBER if pending else '#38536e'
                dash='solid' if active else 'dash'
                fig.add_trace(go.Scatter(x=[NODES[src][0],NODES[dst][0]],y=[NODES[src][1],NODES[dst][1]],mode='lines',line=dict(color=color,width=3,dash=dash),hoverinfo='skip',showlegend=False),row=1,col=col)
            colors=[];sizes=[];labels=[];hover=[]
            for n in names:
                active= self.step_count>=1 if n=='event' else self.step_count>=2 if n=='hub' else (self.step_count>=3 if mdm else self.step_count>={'transport':3,'water':5,'energy':7}[n])
                pending=not mdm and self.step_count>=3 and n in ['water','energy'] and not active
                colors.append('#176b5e' if active else '#745029' if pending else '#19324b')
                sizes.append(78 if n=='hub' else 69 if n=='event' else 65)
                labels.append(NAMES[n]+('<br><span style="font-size:10px">'+('VIA-00042' if mdm and n not in ['event','hub'] else IDS[n] if n in IDS else 'MDM' if mdm and n=='hub' else 'eventos' if n=='hub' else 'perturbação')+'</span>'))
                hover.append(NAMES[n])
            fig.add_trace(go.Scatter(x=[NODES[n][0] for n in names],y=[NODES[n][1] for n in names],mode='markers+text',marker=dict(size=sizes,color=colors,line=dict(color='#6da4b3',width=2)),text=labels,textposition='middle center',textfont=dict(size=12,color=TEXT),hovertext=hover,hoverinfo='text',showlegend=False),row=1,col=col)
        fig.update_xaxes(visible=False,range=[0,1],fixedrange=True)
        fig.update_yaxes(visible=False,range=[0,1.08],fixedrange=True,scaleanchor=None)
        fig.update_layout(paper_bgcolor=PANEL,plot_bgcolor=PANEL,margin=dict(l=20,r=20,t=70,b=20),height=375,font=dict(color=TEXT,family='Arial'),showlegend=False)
        for a in fig.layout.annotations: a.font=dict(size=15,color=GREEN if 'COM MDM' in a.text else AMBER)
        return fig
    def render(self):
        left=self._counts(False);right=self._counts(True)
        self.metrics.value='<div class="sc-metrics">'+card('Órgãos informados • sem MDM',f'{left[0]}/3',AMBER)+card('Divergências pendentes',str(left[1]),AMBER)+card('Órgãos informados • com MDM',f'{right[0]}/3',GREEN)+card('Passos até completar • sem/com MDM',f'{left[2]} / {right[2]}',BLUE)+'</div>'
        self.logbox.value='<div class="sc-logs"><b>RASTREAMENTO DA SIMULAÇÃO</b><div style="margin-top:10px">'+''.join('<div class="entry">'+html.escape(x)+'</div>' for x in reversed(self.logs))+'</div></div>'
        with self.chart:
            clear_output(wait=True)
            display(self._diagram())

simulador=SmartCityMDMDemo()
simulador.display()
