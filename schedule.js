/* Meeting times are civil times in Kazakhstan, never the device timezone. */
(function(root) {
    'use strict';
    const timeZone = 'Asia/Almaty';
    const formatter = new Intl.DateTimeFormat('en-CA', {timeZone, year:'numeric', month:'2-digit', day:'2-digit', hour:'2-digit', minute:'2-digit', second:'2-digit', hourCycle:'h23'});
    function clock(now = new Date()) {
        const p = Object.fromEntries(formatter.formatToParts(now).filter(x=>x.type!=='literal').map(x=>[x.type,Number(x.value)]));
        const civil = new Date(Date.UTC(p.year,p.month-1,p.day,p.hour,p.minute,p.second));
        return {year:p.year, month:p.month, day:p.day, weekday:civil.getUTCDay(), minutes:p.hour*60+p.minute, dateKey:civil.toISOString().slice(0,10)};
    }
    function instant(year,month,day,hhmm) {
        const target = Date.UTC(year,month-1,day,Math.floor(hhmm/100),hhmm%100);
        let value = target;
        for(let i=0;i<3;i++) {
            const p=clock(new Date(value));
            const represented=Date.UTC(p.year,p.month-1,p.day,Math.floor(p.minutes/60),p.minutes%60);
            value += target-represented;
        }
        return new Date(value);
    }
    function nextMeeting(g, includeCurrent=true, now=new Date()) {
        const p=clock(now);
        for(let offset=0;offset<8;offset++) {
            const day=new Date(Date.UTC(p.year,p.month-1,p.day+offset));
            const slots=(g.sc||[]).filter(s=>s.d===day.getUTCDay()).sort((a,b)=>a.s-b.s);
            for(const slot of slots) {
                const start=instant(day.getUTCFullYear(),day.getUTCMonth()+1,day.getUTCDate(),slot.s);
                const end=instant(day.getUTCFullYear(),day.getUTCMonth()+1,day.getUTCDate()+(slot.e<=slot.s?1:0),slot.e);
                if(start>now || (includeCurrent && end>now)) return {start,end,slot,offset,isLive:start<=now&&end>now};
            }
        }
        return null;
    }
    function hasZoom(g) { return !g.online && /https?:\/\/([^/]+\.)?zoom\.us\//i.test(g.z||''); }
    function remoteSlots(g) { return hasZoom(g) ? (g.sc||[]).filter(s=>s.format!=='onsite') : []; }
    const names=[['вс','воскресенье','sun','sunday','жс','жексенбі'],['пн','понедельник','mon','monday','дс','дүйсенбі'],['вт','вторник','tue','tuesday','сс','сейсенбі'],['ср','среда','wed','wednesday','сәрсенбі'],['чт','четверг','thu','thursday','бс','бейсенбі'],['пт','пятница','fri','friday','жм','жұма'],['сб','суббота','sat','saturday','сенбі']];
    function matchesSearch(g,query,now=new Date()) {
        const words=String(query||'').toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
        const haystack=[g.n,g.c,g.a,g.t,g.note,g.online?'online онлайн':'',hasZoom(g)?'zoom зум':'',g.k?'қазақша казахский kazakh':'русский russian',g.f?'женская әйелдер women':''].join(' ').toLocaleLowerCase();
        return words.every(word=>{
            const token=word.replace(/[.,;:]$/,'');
            const d=['сегодня','today','бүгін'].includes(token)?clock(now).weekday:names.findIndex(a=>a.includes(token));
            return d>=0 ? (g.sc||[]).some(s=>s.d===d) : haystack.includes(word);
        });
    }
    const api={timeZone,clock,instant,nextMeeting,hasZoom,remoteSlots,matchesSearch};
    if(typeof module!=='undefined'&&module.exports) module.exports=api;
    else root.AA_SCHEDULE=api;
})(typeof window!=='undefined'?window:globalThis);
