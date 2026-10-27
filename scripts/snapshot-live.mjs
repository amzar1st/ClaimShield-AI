import {createClient} from 'genlayer-js';import {studionet} from 'genlayer-js/chains';import {TransactionHashVariant} from 'genlayer-js/types';import fs from 'node:fs';
const d=JSON.parse(fs.readFileSync('dist/deployment.json','utf8'));const c=createClient({chain:studionet});
const txs=await c.request({method:'sim_getTransactionsForAddress',params:[d.address]});
fs.writeFileSync('/tmp/claimshield-all-txs.json',JSON.stringify(txs,(_,v)=>typeof v==='bigint'?v.toString():v,2));console.log({transactions:txs.length,statuses:txs.map(t=>({hash:t.hash,status:t.status}))});
const read=async(functionName,args=[])=>JSON.parse(await c.readContract({address:d.address,functionName,args,transactionHashVariant:TransactionHashVariant.LATEST_FINAL}));
const config=await read('get_config');let ids=[];for(let i=0;i<config.claim_count;i+=20)ids.push(...await read('list_claims',[i]));
const claims=await Promise.all(ids.map(async id=>{const claim=await read('get_claim',[id]);const history=[];for(let r=0;r<=claim.round;r++){try{history.push(await read('get_history',[id,r]));}catch{}}return {claim,history};}));
fs.writeFileSync('docs/live-state.json',JSON.stringify({capturedAt:new Date().toISOString(),deployment:d,config,claims},null,2));
