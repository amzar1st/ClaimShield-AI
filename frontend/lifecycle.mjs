export function classifyReceipt(tx) {
  const status = tx.statusName || tx.status;
  const receipts = tx.consensus_data?.leader_receipt;
  const leader = Array.isArray(receipts) ? receipts[0] : receipts;
  const execution = tx.txExecutionResultName || leader?.execution_result;
  if (['CANCELED'].includes(status)) return {phase:'failed',status,detail:'The network did not complete this transaction successfully.'};
  if (status !== 'FINALIZED') return {phase:'pending',status:String(status || 'PENDING'),detail:'Waiting for finality. Accepted results may still change.'};
  const consensus = tx.result_name || tx.resultName;
  if (!['MAJORITY_AGREE','SUCCESS'].includes(consensus)) return {phase:'failed',status:'FINALIZED',detail:'Finalized without accepted consensus ('+String(consensus || 'unknown')+'). Contract state was not confirmed.'};
  if (execution === 'SUCCESS') return {phase:'success',status:'FINALIZED',detail:'Finalized with successful contract execution.'};
  return {phase:'failed',status:'FINALIZED',detail:leader?.error || 'Finalized without verified successful execution.'};
}
export async function trackTransaction(client,hash,onUpdate,{attempts=180,delay=3000,sleep=ms=>new Promise(r=>setTimeout(r,ms))}={}) {
  for(let i=0;i<attempts;i++) {
    let tx;
    try { tx=await client.getTransaction({hash}); }
    catch(e) { onUpdate({phase:'pending',status:'RPC_RETRY',detail:'Receipt unavailable; tracking will retry. Do not resubmit.'}); await sleep(delay); continue; }
    const state=classifyReceipt(tx); onUpdate({...state,receipt:tx});
    if(state.phase==='success') return tx;
    if(state.phase==='failed') throw new Error(state.detail);
    await sleep(delay);
  }
  const e=new Error('Tracking timed out. Transaction may still finalize. Resume tracking with the same hash.'); e.pending=true; throw e;
}
