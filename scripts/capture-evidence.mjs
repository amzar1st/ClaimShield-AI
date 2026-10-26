import {createClient} from 'genlayer-js'; import {studionet} from 'genlayer-js/chains';import {TransactionHashVariant} from 'genlayer-js/types';import fs from 'node:fs';
const client=createClient({chain:studionet});
const cfg=JSON.parse(fs.readFileSync('dist/deployment.json','utf8'));
const file=process.argv[2];const hashes=process.argv.slice(3);
const receipts=await Promise.all(hashes.map(async hash=>{const tx=await client.getTransaction({hash});const lr=tx.consensus_data?.leader_receipt;const leader=Array.isArray(lr)?lr[0]:lr;return {hash,status:tx.statusName||tx.status,consensusResult:tx.result_name||tx.resultName,sender:tx.from_address||tx.sender,recipient:tx.to_address||tx.recipient,execution:leader?.execution_result,executionDetail:leader?.genvm_result,leaderOutput:leader?.eq_outputs?Object.fromEntries(Object.entries(leader.eq_outputs).map(([k,v])=>[k,v.payload?.readable||v])):undefined,votes:tx.consensus_data?.votes,validators:tx.consensus_data?.validators?.map(v=>({vote:v.vote,execution:v.execution_result,address:v.node_config?.address})),leaderOnly:tx.data?.leader_only};}));
fs.writeFileSync(file,JSON.stringify({capturedAt:new Date().toISOString(),network:'studionet',chainId:61999,contract:cfg.address,receipts},null,2));
console.log(receipts.map(x=>({hash:x.hash,status:x.status,execution:x.execution,stdout:x.executionDetail?.stdout}))); 
