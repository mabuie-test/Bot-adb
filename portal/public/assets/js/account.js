async function postJSON(url, payload){
  const r = await fetch(url, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
  return r.json();
}

const reg = document.getElementById('register-form');
reg?.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const payload = Object.fromEntries(new FormData(reg));
  const d = await postJSON('/api/account/register', payload);
  document.getElementById('register-result').textContent = JSON.stringify(d, null, 2);
});

const login = document.getElementById('login-form');
login?.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const payload = Object.fromEntries(new FormData(login));
  const d = await postJSON('/api/account/login', payload);
  document.getElementById('login-result').textContent = JSON.stringify(d, null, 2);
});

const req = document.getElementById('reset-request-form');
req?.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const payload = Object.fromEntries(new FormData(req));
  const d = await postJSON('/api/account/password/request-reset', payload);
  document.getElementById('reset-result').textContent = JSON.stringify(d, null, 2);
});

const reset = document.getElementById('reset-form');
reset?.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const payload = Object.fromEntries(new FormData(reset));
  const d = await postJSON('/api/account/password/reset', payload);
  document.getElementById('reset-result').textContent = JSON.stringify(d, null, 2);
});
