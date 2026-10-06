'use strict';
// Progressive enhancement; never store form contents or send them to analytics.
const emit=(name,topic)=>document.dispatchEvent(new CustomEvent('lca:measurement',{detail:{event:name,topic:topic||'unsure'}}));
document.querySelectorAll('a[href^="tel:"],a[href^="sms:"]').forEach(a=>a.addEventListener('click',()=>emit(a.href.startsWith('tel:')?'contact_call_click':'contact_text_click')));
const form=document.querySelector('#aircraft-intake-form');
if(form){
 form.noValidate=true;
 const method=form.elements.preferred_contact,email=form.elements.email,phone=form.elements.best_contact,topic=form.elements.need_type,status=document.querySelector('#form-status'),send=form.querySelector('button[type=submit]');
 let busy=false,started=false;
 const topics=new Set([...topic.options].map(o=>o.value));
 const legacy={'Prebuy':'prebuy','Records review':'records','E-PROPS propeller support':'eprops','ROTAX Alert Service Bulletin / applicability review':'notice','ROTAX engine systems / troubleshooting':'symptom','Avionics / Electrical / Panel Support':'avionics','Five-Year Rubber Hose Package':'service'};
 const query=new URLSearchParams(location.search),requested=query.get('topic')||query.get('need')||query.get('need_type');
 if(requested){const value=topics.has(requested)?requested:legacy[requested];if(value){topic.value=value;const info=document.querySelector('#topic-prefill');info.hidden=false;info.textContent='Selected topic: '+topic.selectedOptions[0].textContent+'. You can change it below.'}}
 // Remove tracking query values from the address without copying them into the payload.
 if(location.search)history.replaceState(null,'',location.pathname+location.hash);
 const sync=()=>{email.required=method.value==='email';phone.required=['phone','text'].includes(method.value);document.querySelector('#email-required').textContent=email.required?' (required)':'';document.querySelector('#phone-required').textContent=phone.required?' (required)':''};
 method.addEventListener('change',sync);sync();
 const clear=()=>{form.querySelectorAll('[aria-invalid]').forEach(el=>el.removeAttribute('aria-invalid'));form.querySelectorAll('.error').forEach(el=>el.textContent='')};
 const problem=(field,message)=>{field.setAttribute('aria-invalid','true');const node=document.querySelector('#'+field.id+'-error');if(node)node.textContent=message;};
 const announce=(message,success)=>{status.hidden=false;status.className='form-status '+(success?'success':'failure');status.textContent=message;status.focus()};
 form.addEventListener('input',e=>{if(!started){started=true;emit('form_start',topic.value)}if(e.target.hasAttribute('aria-invalid')){e.target.removeAttribute('aria-invalid');const n=document.querySelector('#'+e.target.id+'-error');if(n)n.textContent=''}});
 form.addEventListener('submit',async e=>{
  e.preventDefault();if(busy)return;clear();sync();
  let first=null;for(const field of form.querySelectorAll('input,select,textarea')){if(!field.checkValidity()||field.required&&!field.value.trim()){problem(field,field.validity.typeMismatch?'Enter a valid email address.':'Please complete this field.');first=first||field;}}
  if(phone.required&&(phone.value.replace(/\D/g,'').length<7||phone.value.replace(/\D/g,'').length>15)){problem(phone,'Enter a phone number Lima Charlie Aero can use.');first=first||phone}
  if(first){announce('Please check the indicated fields. Your request has not been sent.',false);first.focus();return}
  busy=true;send.disabled=true;send.textContent='Sending…';form.setAttribute('aria-busy','true');status.hidden=true;
  const payload=new FormData(form);for(const [key,value] of [...payload.entries()])if(typeof value==='string'&&!value.trim())payload.delete(key);
  payload.set('source','support-request');payload.set('need_type',topic.value);
  const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),15000);
  try{const response=await fetch(form.action,{method:'POST',body:payload,headers:{Accept:'application/json'},signal:controller.signal});let data;try{data=await response.json()}catch{throw new Error('unconfirmed')}
   if(response.ok&&(data.ok===true||data.success===true)){emit('form_accepted',topic.value);form.reset();sync();announce('Request submitted. Lima Charlie Aero will review your inquiry and contact you to discuss the next step. This does not confirm an appointment. For a time-sensitive concern, call or text 980.382.1344.',true)}
   else{if(response.ok)throw new Error('unconfirmed');const errors=Array.isArray(data.errors)?data.errors:[];for(const error of errors){const field=form.elements.namedItem(error.field);if(field&&field.id)problem(field,String(error.message||'Check this field.'))}
    announce(response.status===429?'The form service is receiving too many requests. Wait before trying again, or call/text the shop.':response.status>=500?'We could not confirm submission. Call or text the shop before resending, so a duplicate request can be avoided.':'The request was not accepted. Check the indicated fields or call/text the shop. Your details remain in the form.',false)}
  }catch{announce('We could not confirm submission. Your details remain in the form. Call or text the shop before resending to avoid a possible duplicate.',false)}
  finally{clearTimeout(timer);busy=false;send.disabled=false;send.textContent='Send inquiry';form.removeAttribute('aria-busy')}
 });
}
