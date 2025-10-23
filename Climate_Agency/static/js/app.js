document.addEventListener('DOMContentLoaded', ()=> {
  // Leaflet map
  const map = L.map('map',{scrollWheelZoom:false}).setView([24.86,67.01], 4);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{ maxZoom:19, attribution:'© OpenStreetMap'}).addTo(map);

  let owmLayer = null;
  function setOverlay(name){
    if(owmLayer) map.removeLayer(owmLayer);
    const key = ''; // keep empty or inject server-side
    if(!key) return;
    const url = `https://tile.openweathermap.org/map/${name}/{z}/{x}/{y}.png?appid=${key}`;
    owmLayer = L.tileLayer(url,{opacity:0.6}).addTo(map);
  }

  const sel = document.getElementById('map-layer');
  if(sel) sel.addEventListener('change', e=> setOverlay(e.target.value));
  const btn = document.getElementById('center-my-location');
  if(btn) btn.addEventListener('click', ()=> map.locate({setView:true, maxZoom:7}));
});
