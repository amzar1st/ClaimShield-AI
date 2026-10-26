import {test} from 'node:test'; import assert from 'node:assert/strict';
import {classifyReceipt,trackTransaction} from '../frontend/lifecycle.mjs';
const receipt=(status,result='SUCCESS')=>({status,result_name:'MAJORITY_AGREE',consensus_data:{leader_receipt:[{execution_result:result}]}});
for(const s of ['PENDING','PROPOSING','ACCEPTED','COMMITTING','REVEALING','UNDETERMINED','VALIDATORS_TIMEOUT','LEADER_TIMEOUT']) test(s+' is pending',()=>assert.equal(classifyReceipt(receipt(s)).phase,'pending'));
for(const s of ['CANCELED']) test(s+' fails',()=>assert.equal(classifyReceipt(receipt(s)).phase,'failed'));
test('finalized successful execution',()=>assert.equal(classifyReceipt(receipt('FINALIZED')).phase,'success'));
test('finalized revert fails',()=>assert.equal(classifyReceipt(receipt('FINALIZED','ERROR')).phase,'failed'));
test('missing execution never success',()=>assert.equal(classifyReceipt({status:'FINALIZED'}).phase,'failed'));
test('tracks pending to final',async()=>{let n=0;const states=[];await trackTransaction({getTransaction:async()=>receipt(++n<3?'ACCEPTED':'FINALIZED')},'hash',s=>states.push(s.phase),{sleep:async()=>{}}); assert.deepEqual(states,['pending','pending','success']);});
test('RPC error retries without resubmitting',async()=>{let n=0;await trackTransaction({getTransaction:async()=>{if(n++===0)throw Error('offline');return receipt('FINALIZED');}},'hash',()=>{},{sleep:async()=>{}});assert.equal(n,2);});
test('timeout remains resumable',async()=>{await assert.rejects(trackTransaction({getTransaction:async()=>receipt('ACCEPTED')},'hash',()=>{},{attempts:1,sleep:async()=>{}}),e=>e.pending===true);});

test('finalized execution success with majority disagreement is failed',()=>assert.equal(classifyReceipt({...receipt('FINALIZED'),result_name:'MAJORITY_DISAGREE'}).phase,'failed'));
test('unknown consensus never success',()=>assert.equal(classifyReceipt({status:'FINALIZED',consensus_data:{leader_receipt:[{execution_result:'SUCCESS'}]}}).phase,'failed'));
