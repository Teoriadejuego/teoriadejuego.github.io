document.documentElement.classList.add('js');
const menu=document.querySelector('.menu-toggle'),nav=document.querySelector('.nav');
menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open)});
document.querySelector('.print-button')?.addEventListener('click',()=>window.print());
const search=document.querySelector('#pub-search'),topic=document.querySelector('#pub-topic'),year=document.querySelector('#pub-year');
if(search){
 const rows=[...document.querySelectorAll('.publication')],count=document.querySelector('#pub-count'),empty=document.querySelector('#pub-empty'),reset=document.querySelector('#pub-reset'),en=document.documentElement.lang==='en';
 const normal=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 const read=()=>{const q=new URLSearchParams(location.search);search.value=q.get('q')||'';for(const [control,key] of [[topic,'topic'],[year,'year']]){const value=q.get(key)||'';control.value=[...control.options].some(o=>o.value===value)?value:''}};
 const filter=(sync=true)=>{let n=0;for(const row of rows){const show=normal(row.textContent+' '+(row.dataset.search||'')).includes(normal(search.value.trim()))&&(!topic.value||row.dataset.topic===topic.value)&&(!year.value||row.dataset.year===year.value);row.hidden=!show;if(show)n++}count.textContent=en?`${n} of ${rows.length} articles`:`${n} de ${rows.length} artículos`;empty.hidden=n!==0;reset.hidden=!search.value&&!topic.value&&!year.value;
  if(sync){const url=new URL(location.href);for(const [key,value] of [['q',search.value.trim()],['topic',topic.value],['year',year.value]]){if(value)url.searchParams.set(key,value);else url.searchParams.delete(key)}history.replaceState(null,'',url)}
 };
 [search,topic,year].forEach(el=>el.addEventListener(el===search?'input':'change',()=>filter()));
 reset.addEventListener('click',()=>{search.value='';topic.value='';year.value='';filter();search.focus()});
 window.addEventListener('popstate',()=>{read();filter(false)});read();filter(false);
}
const lab=document.querySelector('#experiment-lab');
if(lab){
 const en=document.documentElement.lang==='en',n=document.querySelector('#sample'),delta=document.querySelector('#effect'),noise=document.querySelector('#noise');
 const format=(x,d=1)=>Number(x).toLocaleString(en?'en-GB':'es-ES',{minimumFractionDigits:d,maximumFractionDigits:d});
 const update=()=>{
  const size=Number(n.value),effect=Number(delta.value),sd=Number(noise.value),half=1.96*Math.sqrt(2*sd*sd/size),lo=effect-half,hi=effect+half;
  document.querySelector('#sample-value').textContent=format(size,0);document.querySelector('#effect-value').textContent=format(effect);document.querySelector('#noise-value').textContent=format(sd,0);
  document.querySelector('#estimate').textContent=`${format(effect)} ${en?'points':'puntos'}`;
  document.querySelector('#interval').textContent=`[${format(lo)}; ${format(hi)}]`;
  document.querySelector('#interpretation').textContent=lo>0?(en?'Under these assumptions, the interval lies above zero. Statistical separation alone does not establish business value.':'Bajo estos supuestos, el intervalo queda por encima de cero. La separación estadística no demuestra por sí sola valor para el negocio.'):(en?'The interval includes zero: these inputs leave substantial uncertainty about the direction of the effect.':'El intervalo incluye el cero: con estos valores persiste incertidumbre sobre la dirección del efecto.');
  const scale=Math.max(20,Math.ceil(Math.max(Math.abs(lo),Math.abs(hi))/10)*10),x=v=>250+200*v/scale;
  document.querySelector('#ci-negative').textContent='−'+format(scale,0);document.querySelector('#ci-positive').textContent='+'+format(scale,0);
  document.querySelector('#ci-line').setAttribute('x1',x(lo));document.querySelector('#ci-line').setAttribute('x2',x(hi));
  document.querySelector('#point').setAttribute('cx',x(effect));
  document.querySelector('#chart-title').textContent=en?`Illustrative effect ${format(effect)}, approximate 95% interval ${format(lo)} to ${format(hi)}`:`Efecto ilustrativo ${format(effect)}, intervalo aproximado del 95% entre ${format(lo)} y ${format(hi)}`;
 };
 [n,delta,noise].forEach(el=>el.addEventListener('input',update));update();
}
