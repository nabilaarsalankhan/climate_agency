// Put this file at: static/js/dashboard.js
// Uses your API key:
const OPENWEATHER_KEY = "bedfaf1716027c9c280859ad56670795"; // provided by you

/* -----------------------
   Helpers
-------------------------*/
function q(id){ return document.getElementById(id); }
function el(tag, cls=''){ const e = document.createElement(tag); if(cls) e.className = cls; return e; }

/* -----------------------
   Live clock
-------------------------*/
function updateClock(){
  const now = new Date();
  const elClock = q('dateTime');
  if(elClock) elClock.innerText = now.toLocaleString();
}
setInterval(updateClock,1000);
updateClock();

/* -----------------------
   Initialize map (Leaflet)
-------------------------*/
let map, mapMarker;
function initMap(lat=24.86, lon=67.01){
  if(!map){
    map = L.map('map', { zoomControl:true }).setView([lat, lon], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
    }).addTo(map);
  } else {
    map.setView([lat,lon],10);
  }
  if(mapMarker) map.removeLayer(mapMarker);
  mapMarker = L.marker([lat,lon]).addTo(map);
}

/* -----------------------
   Fetch Weather (current + onecall)
   city default: Karachi
-------------------------*/
async function getWeather(city="Korangi,PK"){
  try{
    // 1) Get current to resolve coords
    const curRes = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&appid=${OPENWEATHER_KEY}&units=metric`);
    if(!curRes.ok) throw new Error("City not found");
    const cur = await curRes.json();

    // update UI
    q('cityName').innerText = `${cur.name}, ${cur.sys?.country||''}`;
    q('temperature').innerText = `${Math.round(cur.main.temp)}°C`;
    q('conditionText').innerText = cur.weather[0].description;
    q('humidityInfo').innerText = `${cur.main.humidity}%`;
    q('wind').innerText = `${cur.wind.speed} km/h`;
    q('weatherIcon').src = `https://openweathermap.org/img/wn/${cur.weather[0].icon}@2x.png`;
    q('sunriseSunset').innerText = `Sunrise: ${new Date(cur.sys.sunrise*1000).toLocaleTimeString()} - Sunset: ${new Date(cur.sys.sunset*1000).toLocaleTimeString()}`;

    // map
    initMap(cur.coord.lat, cur.coord.lon);

    // background change (image-free gradient + small tweaks)
    applyBg(cur.weather[0].main.toLowerCase(), cur.coord);

    // 2) Onecall for hourly & daily
    const onecallUrl = `https://api.openweathermap.org/data/2.5/onecall?lat=${cur.coord.lat}&lon=${cur.coord.lon}&exclude=minutely,alerts&appid=${OPENWEATHER_KEY}&units=metric`;
    const ocRes = await fetch(onecallUrl);
    if(ocRes.ok){
      const oc = await ocRes.json();
      fillHourly(oc.hourly || oc.hour || []);
      fillDaily(oc.daily || []);
      updateTrendChart(oc);
    } else {
      // fallback: build a simple hourly/daily from cur
      fillHourlyFallback(cur);
      fillDailyFallback(cur);
    }

    // news carousel (dummy for now)
    populateNews();

  } catch(err){
    console.error(err);
    alert("Weather error: " + err.message);
  }
}

/* -----------------------
   Background logic
-------------------------*/
function applyBg(cond, coord){
  const bg = document.getElementById('weatherBackground');
  cond = (cond||'').toLowerCase();
  if(cond.includes('rain')) bg.style.background = 'linear-gradient(135deg,#1e3a5f,#27496d)';
  else if(cond.includes('cloud')) bg.style.background = 'linear-gradient(135deg,#3b4a6b,#22314b)';
  else if(cond.includes('clear')) bg.style.background = 'linear-gradient(135deg,#2955bc,#0f1724)';
  else if(cond.includes('snow')) bg.style.background = 'linear-gradient(135deg,#bcdffb,#91b8e7)';
  else bg.style.background = 'linear-gradient(135deg,#2955bc,#0f1724)';
}

/* -----------------------
   Fill hourly (simple)
-------------------------*/
function fillHourly(hours){
  const wrap = q('hourlyForecast');
  wrap.innerHTML = '';
  const list = hours.slice(0,12);
  list.forEach(h => {
    const card = el('div','forecast-card');
    card.innerHTML = `<div>${new Date(h.dt*1000).getHours()}:00</div>
                      <img src="https://openweathermap.org/img/wn/${h.weather[0].icon}.png" width="40">
                      <div>${Math.round(h.temp)}°C</div>`;
    wrap.appendChild(card);
  });
  startAutoScroll(wrap,1600,2);
}

/* -----------------------
   Fill daily
-------------------------*/
function fillDaily(days){
  const container = q('dailyForecast');
  container.innerHTML = '';
  days.slice(0,7).forEach(d => {
    const row = el('div','d-flex align-items-center gap-2');
    row.innerHTML = `<div style="width:48px">${new Date(d.dt*1000).toLocaleDateString(undefined,{weekday:'short'})}</div>
                     <img src="https://openweathermap.org/img/wn/${d.weather[0].icon}.png" width="36">
                     <div><strong>${Math.round(d.temp.day)}°C</strong><div class="small text-muted">Min ${Math.round(d.temp.min)} / Max ${Math.round(d.temp.max)}</div></div>`;
    container.appendChild(row);
  });
}

/* Fallback simple hourly/daily */
function fillHourlyFallback(cur){
  const wrap = q('hourlyForecast');
  wrap.innerHTML = '';
  for(let i=1;i<=8;i++){
    const temp = Math.round(cur.main.temp + i - 2);
    const card = el('div','forecast-card');
    card.innerHTML = `<div>${(new Date(Date.now()+i*3600*1000)).getHours()}:00</div>
                      <img src="https://openweathermap.org/img/wn/${cur.weather[0].icon}.png" width="40">
                      <div>${temp}°C</div>`;
    wrap.appendChild(card);
  }
}
function fillDailyFallback(cur){
  const container = q('dailyForecast'); container.innerHTML='';
  for(let d=1; d<=7; d++){
    const col = el('div'); col.className='d-flex gap-2';
    col.innerHTML = `<div style="width:48px">Day ${d}</div>
                     <img src="https://openweathermap.org/img/wn/${cur.weather[0].icon}.png" width="36">
                     <div><strong>${Math.round(cur.main.temp + d -3)}°C</strong></div>`;
    container.appendChild(col);
  }
}

/* -----------------------
   Auto horizontal scroll
-------------------------*/
let autoScrollIntervals = new Map();
function startAutoScroll(el, intervalMs=2000, step=2){
  if(autoScrollIntervals.has(el)){ clearInterval(autoScrollIntervals.get(el)); }
  const id = setInterval(()=> {
    if(el.scrollLeft + el.clientWidth >= el.scrollWidth - 5) el.scrollTo({left:0, behavior:'smooth'});
    else el.scrollBy({left:step, behavior:'smooth'});
  }, intervalMs);
  autoScrollIntervals.set(el, id);
}

/* -----------------------
   News carousel (dummy)
-------------------------*/
function populateNews(){
  const inner = q('newsInner');
  inner.innerHTML = '';
  const headlines = [
    "🌍 Climate change report released",
    "☔ Heavy rains expected this week",
    "🔥 Heatwave alert issued",
    "🌱 New renewable energy policy"
  ];
  headlines.forEach((h,i)=>{
    const item = el('div','carousel-item' + (i===0? ' active':''));
    item.innerText = h;
    inner.appendChild(item);
  });
  // bootstrap carousel init (auto)
  try{ if(typeof bootstrap !== 'undefined' && bootstrap.Carousel) new bootstrap.Carousel(document.getElementById('newsCarousel'),{interval:3500}); }catch(e){}
}

/* -----------------------
   Datasets CRUD (frontend placeholders)
   Expects REST endpoints: /api/datasets/
-------------------------*/
async function loadDatasets(){
  const tbody = q('datasetsBody');
  tbody.innerHTML = '<tr><td colspan="5">Loading...</td></tr>';
  try{
    // Replace this with your real API:
    const res = await fetch('/api/datasets/');
    if(!res.ok) throw new Error('No backend (placeholder)'); 
    const data = await res.json();
    renderDatasets(data);
  }catch(err){
    // placeholder demo rows so UI looks filled
    tbody.innerHTML = '';
    for(let i=1;i<=5;i++){
      const tr = el('tr');
      tr.innerHTML = `<td>Dataset ${i}</td><td>Source ${i}</td><td>${100*i}</td><td>${new Date().toLocaleString()}</td>
                      <td>
                        <button class="btn btn-sm btn-outline-light me-1" onclick="editDataset('demo${i}')">Edit</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteDataset('demo${i}')">Delete</button>
                      </td>`;
      tbody.appendChild(tr);
    }
  }
}
function renderDatasets(data){
  const tbody = q('datasetsBody'); tbody.innerHTML='';
  data.forEach(d=>{
    const tr = el('tr');
    tr.innerHTML = `<td>${d.name}</td><td>${d.source}</td><td>${d.records||0}</td><td>${d.updated||''}</td>
                    <td>
                      <button class="btn btn-sm btn-outline-light me-1" onclick="editDataset('${d.id}')">Edit</button>
                      <button class="btn btn-sm btn-danger" onclick="deleteDataset('${d.id}')">Delete</button>
                    </td>`;
    tbody.appendChild(tr);
  });
}
function editDataset(id){
  // placeholder - open modal with dummy content
  q('datasetModalTitle').innerText = 'Edit Dataset';
  q('datasetId').value = id;
  q('datasetName').value = 'Demo Name';
  q('datasetSource').value = 'https://source.example';
  q('datasetRecords').value = 100;
  new bootstrap.Modal(q('datasetModal')).show();
}
function deleteDataset(id){
  if(!confirm('Delete dataset?')) return;
  // call DELETE /api/datasets/:id (placeholder)
  alert('Deleted (placeholder) ' + id);
  loadDatasets();
}

/* -----------------------
   Dataset form submit
-------------------------*/
document.addEventListener('DOMContentLoaded', ()=>{
  // modal handlers
  q('addDatasetBtn').addEventListener('click', ()=> {
    q('datasetModalTitle').innerText = 'Add Dataset';
    q('datasetForm').reset();
    q('datasetId').value = '';
    new bootstrap.Modal(q('datasetModal')).show();
  });

  q('datasetForm').addEventListener('submit', async (e)=>{
    e.preventDefault();
    const id = q('datasetId').value;
    const payload = {
      name: q('datasetName').value,
      source: q('datasetSource').value,
      records: q('datasetRecords').value
    };
    // Placeholder: send to backend endpoints
    console.log('Save dataset', id, payload);
    // close modal
    bootstrap.Modal.getInstance(q('datasetModal')).hide();
    loadDatasets();
  });

  // refresh and search
  q('refreshDatasets').addEventListener('click', loadDatasets);
  // top search form
  window.doSearch = function(){
    const v = q('cityInputTop').value.trim();
    if(!v) return;
    getWeather(v);
    q('cityInputTop').value = '';
  };

  // theme toggle
  q('themeToggle').addEventListener('click', ()=>{
    const body = document.getElementById('weatherBackground');
    if(body.classList.contains('dark')){ body.classList.remove('dark'); body.style.filter='none'; }
    else{ body.classList.add('dark'); body.style.filter='contrast(.9)'; }
  });

  // load initial dataset + weather
  loadDatasets();
  getWeather('Korangi,PK');
  initTrendChart(); // chart with demo data
});

/* -----------------------
   Chart (demo) - Chart.js
-------------------------*/
let trendChart;
function initTrendChart(){
  const ctx = document.getElementById('trendChart').getContext('2d');
  trendChart = new Chart(ctx, {
    type:'line',
    data:{
      labels:['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
      datasets:[{
        label:'Karachi',
        data:[30,31,29,32,33,34,31],
        tension:0.35,
        borderColor:'#ffd369',
        backgroundColor:'rgba(255,211,105,0.12)',
        fill:true
      },{
        label:'London',
        data:[18,17,16,15,19,20,18],
        tension:0.35,
        borderColor:'#6bc1ff',
        backgroundColor:'rgba(107,193,255,0.08)',
        fill:true
      }]
    },
    options:{
      responsive:true,
      plugins:{ legend:{labels:{color:'#e8f0ff'}}},
      scales:{ x:{ ticks:{color:'#cfe0ff'}}, y:{ ticks:{color:'#cfe0ff'}}}
    }
  });
}
function updateTrendChart(onecall){
  if(!trendChart) return;
  // if onecall provided build simple next-7 from daily
  if(onecall && onecall.daily){
    const labels = onecall.daily.slice(0,7).map(d=> new Date(d.dt*1000).toLocaleDateString(undefined,{weekday:'short'}));
    const temps = onecall.daily.slice(0,7).map(d=> Math.round(d.temp.day));
    trendChart.data.labels = labels;
    trendChart.data.datasets[0].data = temps;
    trendChart.update();
  }
}
