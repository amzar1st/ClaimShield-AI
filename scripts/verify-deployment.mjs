import {createClient} from 'genlayer-js';import {studionet} from 'genlayer-js/chains';import fs from 'node:fs';import {createHash} from 'node:crypto';
const d=JSON.parse(fs.readFileSync('dist/deployment.json','utf8'));const client=createClient({chain:studionet});
const [chainId,code]=await Promise.all([client.getChainId(),client.getContractCode(d.address)]);
const hash=s=>createHash('sha256').update(s).digest('hex');const local=fs.readFileSync('contracts/claimshield.py');
if(chainId!==61999||hash(code)!==hash(local)||hash(local)!==d.sourceSha256)throw Error('Network or deployed-source mismatch');
const proof={capturedAt:new Date().toISOString(),chainId,address:d.address,deployedSourceSha256:hash(code),localSourceSha256:hash(local),exactMatch:true};
fs.writeFileSync('docs/source-verification.json',JSON.stringify(proof,null,2));console.log(proof);
