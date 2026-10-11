"use strict";
(() => {
  const data = window.PRODUTIVIDADE_DATA;
  if (!data || data.synthetic !== true) {
    document.getElementById("scope").textContent = "Não foi possível carregar a demonstração sintética.";
    return;
  }
  const months = [...new Set(data.monthly.map(r => r.month))];
  const departments = [...new Map(data.monthly.map(r => [r.department_id,r.department])).entries()];
  const month = document.getElementById("month"), department = document.getElementById("department");
  const labels = ["Jan","Fev","Mar","Abr","Mai","Jun"];
  const pct = v => v === null ? "Sem base" : (v*100).toLocaleString("pt-BR",{maximumFractionDigits:1})+"%";
  const brl = v => v.toLocaleString("pt-BR",{style:"currency",currency:"BRL",maximumFractionDigits:0});
  months.forEach((m,i) => month.add(new Option(labels[i]+" / 2025",m)));
  departments.forEach(([id,name]) => department.add(new Option(name,id)));
  month.value=months.at(-1);
  function render() {
    const history = data.monthly.filter(r => r.department_id===Number(department.value));
    const r = history.find(r => r.month===month.value);
    document.getElementById("scope").textContent = `${r.department} · ${month.selectedOptions[0].text} · dados 100% sintéticos`;
    const kpis = [
      ["Headcount final",r.headcount,"Pessoas ativas no último dia"],
      ["Folha demonstrativa",brl(r.payroll_brl),"Salário-base proporcional, sem encargos"],
      ["Turnover de saída",pct(r.turnover),`${r.exits} saídas / HC médio ${((r.opening_headcount+r.headcount)/2).toLocaleString('pt-BR')}`],
      ["Cobertura de mapeamento",pct(r.mapping_coverage),`${r.mapped_employees} / ${r.eligible_employees} elegíveis`]
    ];
    document.getElementById("kpis").replaceChildren(...kpis.map(([label,value,note]) => {
      const div=document.createElement("div"); div.className="kpi";
      for (const [tag,text] of [["span",label],["strong",String(value)],["small",note]]) {
        const element=document.createElement(tag); element.textContent=text; div.append(element);
      }
      return div;
    }));
    const trend=document.getElementById("trend");
    trend.setAttribute("aria-label",`Cobertura de mapeamento em ${r.department}: `+history.map((h,i)=>labels[i]+" "+pct(h.mapping_coverage)).join(", "));
    trend.replaceChildren(...history.map((h,i) => {
      const column=document.createElement("div");column.className="bar-col";column.setAttribute("aria-hidden","true");
      const value=document.createElement("span");value.className="bar-value";value.textContent=pct(h.mapping_coverage);
      const bar=document.createElement("div");bar.className="bar"+(h.month===month.value?" current":"");bar.style.height=(h.mapping_coverage*165)+"px";
      const label=document.createElement("span");label.className="bar-label";label.textContent=labels[i];
      column.append(value,bar,label);return column;
    }));
    const baseline=history[0];
    const change=(r.mapping_coverage-baseline.mapping_coverage)*100;
    document.getElementById("insight-title").textContent=month.value===months[0]?"O ponto de partida da cobertura":`${change>=0?"+":""}${change.toLocaleString('pt-BR',{maximumFractionDigits:1})} p.p. de cobertura versus janeiro`;
    document.getElementById("insight").textContent=`No mês selecionado, a coleta representa ${pct(r.collection_coverage)} do tempo previsto. A atividade classificada como produtiva equivale a ${pct(r.observed_activity_ratio)} do tempo capturado. Os denominadores são diferentes e precisam acompanhar a interpretação.`;
    document.getElementById("table-caption").textContent=`Histórico mensal · ${r.department} · dados sintéticos`;
    document.getElementById("rows").replaceChildren(...history.map((h,i)=>{
      const tr=document.createElement("tr");
      [labels[i],h.headcount,h.hires,h.exits,brl(h.payroll_brl),`${h.mapped_employees} / ${h.eligible_employees}`,pct(h.collection_coverage),pct(h.observed_activity_ratio)].forEach(v=>{const td=document.createElement("td");td.textContent=v;tr.append(td);});return tr;
    }));
  }
  month.addEventListener("change",render);department.addEventListener("change",render);
  document.getElementById("reset").addEventListener("click",()=>{month.value=months.at(-1);department.value="0";render();});
  render();
})();
