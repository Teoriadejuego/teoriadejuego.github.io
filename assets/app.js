document.documentElement.classList.add('js');
const menu=document.querySelector('.menu-toggle'),nav=document.querySelector('.nav');
const setMenu=(open,restore=false)=>{menu?.setAttribute('aria-expanded',String(open));nav?.classList.toggle('open',open);if(restore)menu?.focus()};
menu?.addEventListener('click',()=>setMenu(menu.getAttribute('aria-expanded')!=='true'));
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu?.getAttribute('aria-expanded')==='true'){setMenu(false,true)}});
nav?.addEventListener('click',e=>{if(e.target.closest('a'))setMenu(false)});
window.matchMedia('(max-width:760px)').addEventListener('change',()=>setMenu(false));
document.querySelector('.print-button')?.addEventListener('click',()=>window.print());
const search=document.querySelector('#pub-search'),topic=document.querySelector('#pub-topic'),year=document.querySelector('#pub-year');
if(search){
 const rows=[...document.querySelectorAll('.publication')],count=document.querySelector('#pub-count'),empty=document.querySelector('#pub-empty'),reset=document.querySelector('#pub-reset'),en=document.documentElement.lang==='en';
 const normal=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 const read=()=>{const q=new URLSearchParams(location.search);search.value=q.get('q')||'';for(const [control,key] of [[topic,'topic'],[year,'year']]){const value=q.get(key)||'';control.value=[...control.options].some(o=>o.value===value)?value:''}};
 const languageLink=document.querySelector('a.lang');
 const syncLanguage=()=>{if(!languageLink)return;const url=new URL(languageLink.href);url.search='';for(const [key,value] of [['q',search.value.trim()],['topic',topic.value],['year',year.value]])if(value)url.searchParams.set(key,value);url.hash=location.hash;languageLink.href=url.href};
 const filter=(sync=true)=>{let n=0;for(const row of rows){const show=normal(row.textContent+' '+(row.dataset.search||'')).includes(normal(search.value.trim()))&&(!topic.value||row.dataset.topic===topic.value)&&(!year.value||row.dataset.year===year.value);row.hidden=!show;if(show)n++}count.textContent=en?`${n} of ${rows.length} articles`:`${n} de ${rows.length} artículos`;empty.hidden=n!==0;reset.hidden=!search.value&&!topic.value&&!year.value;
  if(sync){const url=new URL(location.href);for(const [key,value] of [['q',search.value.trim()],['topic',topic.value],['year',year.value]]){if(value)url.searchParams.set(key,value);else url.searchParams.delete(key)}history.replaceState(null,'',url)}
  syncLanguage();
 };
 [search,topic,year].forEach(el=>el.addEventListener(el===search?'input':'change',()=>filter()));
 reset.addEventListener('click',()=>{search.value='';topic.value='';year.value='';filter();search.focus()});
 window.addEventListener('popstate',()=>{read();filter(false)});read();filter(false);
 window.addEventListener('hashchange',syncLanguage);
}
const lab=document.querySelector('#experiment-lab');
if(lab){
 const en=document.documentElement.lang==='en',n=document.querySelector('#sample'),delta=document.querySelector('#effect'),noise=document.querySelector('#noise');
 const format=(x,d=1)=>Number(x).toLocaleString(en?'en-GB':'es-ES',{minimumFractionDigits:d,maximumFractionDigits:d});
 const bound=x=>format(x,x!==0&&Math.abs(x)<0.05?Math.min(8,Math.ceil(-Math.log10(Math.abs(x)))):1);
 const controls=[[n,'n',200],[delta,'delta',3],[noise,'sd',15]],languageLink=document.querySelector('a.lang');
 const readLab=()=>{const params=new URLSearchParams(location.search);for(const [el,key,fallback] of controls){const raw=params.get(key),value=raw===null||raw.trim()===''?fallback:Number(raw),min=Number(el.min),max=Number(el.max),step=Number(el.step);el.value=String(Number.isFinite(value)?Math.min(max,Math.max(min,min+Math.round((value-min)/step)*step)):fallback)}};
 const syncLab=()=>{const url=new URL(location.href);for(const [el,key,fallback] of controls){if(Number(el.value)===fallback)url.searchParams.delete(key);else url.searchParams.set(key,el.value)}history.replaceState(null,'',url);if(languageLink){const target=new URL(languageLink.href);target.search='';for(const [,key] of controls)if(url.searchParams.has(key))target.searchParams.set(key,url.searchParams.get(key));target.hash=url.hash;languageLink.href=target.href}};
 const update=()=>{
  const size=Number(n.value),effect=Number(delta.value),sd=Number(noise.value),half=1.96*Math.sqrt(2*sd*sd/size),lo=effect-half,hi=effect+half;
  document.querySelector('#sample-value').textContent=format(size,0);document.querySelector('#effect-value').textContent=format(effect);document.querySelector('#noise-value').textContent=format(sd,0);
  document.querySelector('#estimate').textContent=`${format(effect)} ${en?'points':'puntos'}`;
  document.querySelector('#interval').textContent=`[${bound(lo)}; ${bound(hi)}]`;
  document.querySelector('#interpretation').textContent=hi<0?(en?'Under these assumptions, the interval lies below zero. Whether a negative difference is useful depends on the outcome being measured.':'Bajo estos supuestos, el intervalo queda por debajo de cero. Que una diferencia negativa sea útil depende del indicador medido.'):lo>0?(en?'Under these assumptions, the interval lies above zero. Statistical separation alone does not establish business value.':'Bajo estos supuestos, el intervalo queda por encima de cero. La separación estadística no demuestra por sí sola valor para el negocio.'):(en?'The interval includes zero: these inputs leave substantial uncertainty about the direction of the effect.':'El intervalo incluye el cero: con estos valores persiste incertidumbre sobre la dirección del efecto.');
  const scale=Math.max(20,Math.ceil(Math.max(Math.abs(lo),Math.abs(hi))/10)*10),x=v=>250+200*v/scale;
  document.querySelector('#ci-negative').textContent='−'+format(scale,0);document.querySelector('#ci-positive').textContent='+'+format(scale,0);
  document.querySelector('#ci-line').setAttribute('x1',x(lo));document.querySelector('#ci-line').setAttribute('x2',x(hi));
  document.querySelector('#point').setAttribute('cx',x(effect));
  document.querySelector('#chart-title').textContent=en?`Illustrative effect ${format(effect)}, approximate 95% interval ${bound(lo)} to ${bound(hi)}`:`Efecto ilustrativo ${format(effect)}, intervalo aproximado del 95% entre ${bound(lo)} y ${bound(hi)}`;
 };
 [n,delta,noise].forEach(el=>el.addEventListener('input',()=>{update();syncLab()}));document.querySelector('#lab-reset')?.addEventListener('click',()=>{for(const [el,,fallback] of controls)el.value=String(fallback);update();syncLab();n.focus()});window.addEventListener('popstate',()=>{readLab();update();syncLab()});window.addEventListener('hashchange',syncLab);readLab();update();syncLab();
}

document.querySelectorAll('[data-copy-email]').forEach(button=>button.addEventListener('click',async()=>{
 const en=document.documentElement.lang==='en',status=button.nextElementSibling;
 try{await navigator.clipboard.writeText(button.dataset.copyEmail);status.textContent=en?'Email address copied.':'Correo copiado.'}
 catch{status.textContent=en?'Select the email address above and copy it with your browser.':'Selecciona la dirección de arriba y cópiala con tu navegador.'}
}));
