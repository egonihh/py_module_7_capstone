async function fetchSummary() { return await (await fetch('/api/summary')).json(); }
async function fetchRecommendations() { return await (await fetch('/api/recommendations')).json(); }
function secondsToHMS(s) { const h=Math.floor(s/3600); const m=Math.floor((s%3600)/60); return h?`${h}h ${m}m`:`${m}m`; }

async function renderDashboard() {
    const summary = await fetchSummary();
    const recs = await fetchRecommendations();
    const dashboard = document.getElementById('dashboard'); dashboard.innerHTML='';

    summary.forEach(device => {
        const deviceRecs = recs.find(r=>r.device===device.device)?.recommendations||[];
        const card = document.createElement('div'); card.className='device-card';
        const appLabels = Object.keys(device.by_app);
        const appValues = Object.values(device.by_app);

        card.innerHTML = `
            <h2>${device.device}</h2>
            <div class="total-time">Total: ${secondsToHMS(device.total_seconds)}</div>
            <canvas id="chart-${device.device}"></canvas>
            <div class="recommendations"><strong>Recommendations:</strong>
                <ul>${deviceRecs.map(r=>`<li>${r.msg}</li>`).join('')}</ul>
            </div>`;
        dashboard.appendChild(card);

        new Chart(document.getElementById(`chart-${device.device}`), {
            type:'bar',
            data:{ labels: appLabels, datasets:[{ label:'Seconds', data: appValues, backgroundColor:'#4a90e2' }] },
            options:{ responsive:true, plugins:{ legend:{display:false} } }
        });
    });
}

renderDashboard();