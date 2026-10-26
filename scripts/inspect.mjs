import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import {TransactionHashVariant} from 'genlayer-js/types';
import fs from 'node:fs';
const c=createClient({chain:studionet});
const hash=process.argv[2];
const r=hash ? await c.getTransaction({hash}) : await c.readContract({address:'0xBFd0736a262DE3aA14D2e42f4E6b79772cC00dDa',functionName:'get_config',args:[],transactionHashVariant:TransactionHashVariant.LATEST_FINAL});
console.log(JSON.stringify(r,(_,v)=>typeof v==='bigint'?v.toString():v,2));
