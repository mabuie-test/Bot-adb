async function getJSON(url, options = {}) {
  const response = await fetch(url, options);
  return response.json();
}

async function csrf(){
  const d = await getJSON('/api/csrf');
  return d.csrf_token;
}

async function loadGames() {
  const data = await getJSON('/api/games');
  const select = document.getElementById('game');
  (data.data || []).forEach(g => {
    const opt = document.createElement('option');
    opt.value = g.shortcode;
    opt.textContent = `${g.name} (${g.shortcode})`;
    select.appendChild(opt);
  });
}

let latestBetId = null;

document.getElementById('create-round')?.addEventListener('click', async ()=>{
  const game = document.getElementById('game').value || 'aviator';
  const d = await getJSON('/api/rounds', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({game})});
  document.getElementById('round_id').value = d.data.round_id;
  document.getElementById('game-result').textContent = JSON.stringify(d, null, 2);
});

const form = document.getElementById('deposit-form');
form?.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const token = await csrf();
  const payload = Object.fromEntries(new FormData(form));
  payload.csrf_token = token;
  const d = await getJSON('/api/deposits/manual',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  document.getElementById('deposit-result').textContent = JSON.stringify(d, null, 2);
});

const betForm = document.getElementById('bet-form');
betForm?.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const payload = Object.fromEntries(new FormData(betForm));
  const d = await getJSON('/api/bets', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
  latestBetId = d.bet_id;
  document.getElementById('game-result').textContent = JSON.stringify(d, null, 2);
});

document.getElementById('cashout')?.addEventListener('click', async ()=>{
  if (!latestBetId) return;
  const d = await getJSON('/api/bets/cashout', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({bet_id: latestBetId, multiplier: 2.0})});
  document.getElementById('game-result').textContent = JSON.stringify(d, null, 2);
});

const status = document.getElementById('status');
const mult = document.getElementById('multiplier');
function connectSSE(){
  const sse = new EventSource('/sse.php');
  sse.onmessage = (e)=>{const d=JSON.parse(e.data); mult.textContent=`${d.multiplier.toFixed(2)}x`; status.textContent='SSE ativo';};
  sse.onerror = ()=>{status.textContent='Reconectando...'; sse.close(); setTimeout(connectSSE,1500);};
}

loadGames().catch(()=>{});
connectSSE();
