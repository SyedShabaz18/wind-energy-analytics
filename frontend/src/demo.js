// Synthetic values are ONLY for interface preview and never represented as Elexon observations.
export function syntheticPreview(decisionDate, cutoffHour) {
  const rows = Array.from({length: 48}, (_, i) => {
    const h = i / 2;
    const actual = Math.round(6700 + 1400*Math.sin(i/7) + 500*Math.cos(i/3.6));
    const forecast = Math.round(actual + 440*Math.sin(i/5 + 0.8) - 130);
    const delivery = new Date(`${decisionDate}T00:00:00Z`);
    delivery.setUTCDate(delivery.getUTCDate() + 1);
    delivery.setUTCMinutes(delivery.getUTCMinutes() + i*30);
    return {startTime:delivery.toISOString(), localTime:`${String(Math.floor(h)).padStart(2,'0')}:${i%2?'30':'00'}`, actualMW:actual, forecastMW:forecast, errorMW:forecast-actual, publishedAt:null};
  });
  const e=rows.map(r=>r.errorMW), a=rows.map(r=>r.actualMW);
  return {mode:'synthetic',source:'Synthetic preview — NOT Elexon data',decisionDate,deliveryDate:new Date(Date.parse(`${decisionDate}T00:00:00Z`)+86400000).toISOString().slice(0,10),decisionCutoff:null,assumption:`Illustrative cutoff ${String(cutoffHour).padStart(2,'0')}:00 UK local time`,metrics:{maeMW:Math.round(e.reduce((s,x)=>s+Math.abs(x),0)/e.length),rmseMW:Math.round(Math.sqrt(e.reduce((s,x)=>s+x*x,0)/e.length)),biasMW:Math.round(e.reduce((s,x)=>s+x,0)/e.length),wapePercent:Math.round(e.reduce((s,x)=>s+Math.abs(x),0)/a.reduce((s,x)=>s+x,0)*1000)/10,matchedIntervals:48,totalIntervals:48,coveragePercent:100},intervals:rows};
}
