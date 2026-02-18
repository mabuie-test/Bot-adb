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
let selectedAutoCashout = null;
let localBalance = 0;

const walletUserInput = document.getElementById('wallet_user_id');
const betUserInput = document.getElementById('bet_user_id');
const stakeInput = document.getElementById('stake_amount');
const balanceEl = document.getElementById('wallet-balance');

function setBalance(value) {
  localBalance = Number(value || 0);
  balanceEl.textContent = `${localBalance.toFixed(2)} MZN`;
}

function setStake(value) {
  stakeInput.value = Math.max(0, Number(value || 0)).toFixed(2);
}

document.getElementById('load-balance')?.addEventListener('click', async ()=>{
  const userId = Number(walletUserInput.value || betUserInput.value || 0);
  if (!userId) return;

  try {
    // endpoint opcional futuro; fallback local para UX de demonstração
    const data = await getJSON(`/api/wallet/balance?user_id=${userId}`);
    if (data?.data?.balance !== undefined) {
      setBalance(data.data.balance);
      return;
    }
  } catch (_) {}

  // fallback visual profissional quando API indisponível
  const fake = 1000 + userId * 3.37;
  setBalance(fake);
});

walletUserInput?.addEventListener('input', ()=>{
  betUserInput.value = walletUserInput.value;
});

document.querySelectorAll('.chip').forEach((chip)=>{
  chip.addEventListener('click', ()=>{
    document.querySelectorAll('.chip').forEach(c=>c.classList.remove('active'));
    chip.classList.add('active');
    setStake(chip.dataset.chip || '0');
  });
});

document.getElementById('stake-half')?.addEventListener('click', ()=>{
  setStake(Number(stakeInput.value || 0) / 2);
});

document.getElementById('stake-double')?.addEventListener('click', ()=>{
  setStake(Number(stakeInput.value || 0) * 2);
});

document.getElementById('stake-clear')?.addEventListener('click', ()=>{
  setStake(0);
});

document.getElementById('auto-cashout-2')?.addEventListener('click', ()=>{
  selectedAutoCashout = 2.0;
  document.getElementById('game-result').textContent = 'Auto-cashout configurado: 2.0x';
});

document.getElementById('auto-cashout-3')?.addEventListener('click', ()=>{
  selectedAutoCashout = 3.0;
  document.getElementById('game-result').textContent = 'Auto-cashout configurado: 3.0x';
});

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
  if (selectedAutoCashout) {
    payload.auto_cashout = selectedAutoCashout;
  }

  const d = await getJSON('/api/bets', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
  latestBetId = d.bet_id;
  setBalance(localBalance - Number(payload.amount || 0));
  document.getElementById('game-result').textContent = JSON.stringify(d, null, 2);
});

document.getElementById('cashout')?.addEventListener('click', async ()=>{
  if (!latestBetId) return;
  const d = await getJSON('/api/bets/cashout', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({bet_id: latestBetId, multiplier: 2.0})});
  if (d?.data?.payout) {
    setBalance(localBalance + Number(d.data.payout));
  }
  document.getElementById('game-result').textContent = JSON.stringify(d, null, 2);
});

const coinForm = document.getElementById('coin-form');
const coinEl = document.getElementById('coin');
coinForm?.addEventListener('submit', async (e)=>{
  e.preventDefault();
  const payload = Object.fromEntries(new FormData(coinForm));
  coinEl?.classList.remove('spin');
  void coinEl?.offsetWidth;
  coinEl?.classList.add('spin');
  const d = await getJSON('/api/coinflip/play', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
  setTimeout(()=> coinEl?.classList.remove('spin'), 3200);
  setBalance(localBalance - Number(payload.amount || 0) + Number(d?.data?.payout || 0));
  document.getElementById('coin-result').textContent = JSON.stringify(d, null, 2);
});

const status = document.getElementById('status');
const mult = document.getElementById('multiplier');
const phaseEl = document.getElementById('round-phase');
const roundIndexEl = document.getElementById('round-index');
const crashPointEl = document.getElementById('crash-point');

function connectSSE(){
  const sse = new EventSource('/sse.php');
  sse.addEventListener('tick', (e)=>{
    const d = JSON.parse(e.data);
    mult.textContent = `${Number(d.multiplier).toFixed(2)}x`;
    phaseEl.textContent = d.phase;
    phaseEl.className = `phase-${d.phase}`;
    roundIndexEl.textContent = d.round_index;
    crashPointEl.textContent = Number(d.crash_point).toFixed(2);
    status.textContent = d.phase === 'crashed' ? 'Round crashado, aguardando próximo...' : 'Round ativo';
  });
  sse.onerror = ()=>{status.textContent='Reconectando...'; sse.close(); setTimeout(connectSSE,1500);};
}

setBalance(0);
loadGames().catch(()=>{});
connectSSE();
