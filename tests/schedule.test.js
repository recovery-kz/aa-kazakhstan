const assert=require('node:assert/strict');
const s=require('../schedule');
const groups=require('../groups.json');
const group=name=>groups.find(g=>g.n.includes(name));
const now=new Date('2026-09-30T13:00:00Z'); // Wednesday 18:00 Kazakhstan
assert.equal(s.clock(now).weekday,3);
assert.equal(s.clock(new Date('2026-09-30T20:00:00Z')).dateKey,'2026-10-01');
assert.equal(s.nextMeeting(group('Бірлік'),false,now).start.toISOString(),'2026-10-01T16:00:00.000Z');
assert.equal(s.nextMeeting(group('Виктория'),false,now).start.toISOString(),'2026-10-01T14:30:00.000Z');
assert.equal(s.nextMeeting(group('Бірлік'),true,new Date('2026-10-01T16:30:00Z')).isLive,true);
assert.equal(s.nextMeeting(group('Бірлік'),true,new Date('2026-10-01T17:15:00Z')).start.toISOString(),'2026-10-08T16:00:00.000Z');
for(const query of ['среда','ср','wednesday','wed','сәрсенбі','today','бүгін','сегодня'])assert(s.matchesSearch(group('8 Марта'),query,now),query);
assert(s.matchesSearch(groups.find(g=>g.c==='Караганда'),'суббота',now));
assert(!s.matchesSearch(group('Бірлік'),'среда',now));
assert(s.matchesSearch(group('Бірлік'),'четверг',now));
assert(s.matchesSearch(group('Виктория'),'алматы четверг',now));
assert(!group('Виктория').online);
assert(s.hasZoom(group('Виктория')));
assert(!s.hasZoom(group('Наурыз'))); // Telegram information channel is not Zoom
assert.deepEqual(s.remoteSlots(group('Пана')).map(x=>x.d),[3]);
assert.deepEqual(s.remoteSlots(group('Сырдария')).map(x=>x.d),[2,4]);
assert.equal(s.nextMeeting({sc:[]},false,now),null);
assert.equal(s.nextMeeting({sc:[{d:3,s:2330,e:30}]},false,now).end.toISOString(),'2026-09-30T19:30:00.000Z');
console.log('OK: schedule, midnight, boundaries, search in 3 languages, Zoom formats; TZ='+process.env.TZ);
