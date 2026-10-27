import json
import hashlib
from pathlib import Path
import pytest

REPO='amzar1st/ClaimShield-AI'
ROOT='https://raw.githubusercontent.com/'+REPO+'/'+'a'*40+'/fixtures/'
POLICY=Path('fixtures/policy.txt').read_text()
INCIDENT=Path('fixtures/incident-supported.txt').read_text()

def source(name, text):
    return {'url':ROOT+name,'sha256':hashlib.sha256(text.encode()).hexdigest()}
P=source('policy.txt',POLICY)
E=source('incident-supported.txt',INCIDENT)
I=json.dumps({'reference':'CS-DEMO-001','date':'2026-10-20','description':'A van accidentally hit the parked DEMO-CAR-01, matching claim CS-DEMO-001.'})

def answer(**changes):
    x={'coverage':'YES','exclusion':'NO','incident':'YES','reason':'The pinned policy and incident report support the fictional claim.','citations':[
        {'field':'coverage','source':'P','line':4},
        {'field':'exclusion','source':'P','line':6},
        {'field':'incident','source':'E0','line':3}]}
    x.update(changes)
    return json.dumps(x)

@pytest.fixture
def ctx(direct_vm,direct_deploy):
    c=direct_deploy('contracts/claimshield.py',REPO,sdk_version='v0.3.0-rc7')
    c.register_policy('motor',P['url'],P['sha256'])
    c.open_claim('CS-DEMO-001','motor',I,json.dumps([E]))
    return c,direct_vm

def mocks(vm, output=None, policy=POLICY, incident=INCIDENT):
    vm.mock_web('policy.txt',{'status':200,'body':policy})
    vm.mock_web('incident-supported.txt',{'status':200,'body':incident})
    vm.mock_llm('You independently',answer() if output is None else output)

def result(c):
    return json.loads(c.get_claim('CS-DEMO-001'))['result']['result']

def test_supported_and_validator(ctx):
    c,vm=ctx; mocks(vm); c.assess('CS-DEMO-001')
    assert result(c)['verdict']=='SUPPORTED'
    assert vm.run_validator()
    record=json.loads(c.get_history('CS-DEMO-001',0))
    h=record.pop('decision_sha256')
    assert h==hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()

@pytest.mark.parametrize('field,value,expected',[('coverage','NO','NOT_SUPPORTED'),('exclusion','YES','NOT_SUPPORTED'),('incident','NO','NOT_SUPPORTED'),('incident','UNCLEAR','NEEDS_REVIEW'),('coverage','UNCLEAR','NEEDS_REVIEW')])
def test_verdict_derivation(ctx,field,value,expected):
    c,vm=ctx; mocks(vm,answer(**{field:value})); c.assess('CS-DEMO-001'); assert result(c)['verdict']==expected

@pytest.mark.parametrize('output',['oops','{}','[]',answer(coverage='MAYBE'),answer(reason='x'*1201),answer(citations=[]),answer(citations=[{'field':'incident','source':'E0','quote':'fabricated supporting quotation'}]),answer(citations=[{'field':'coverage','source':'E0','quote':'A delivery van accidentally struck the stationary parked vehicle, damaging its rear panel.'}])])
def test_malformed_or_fabricated_model_output(ctx,output):
    c,vm=ctx; mocks(vm,output); c.assess('CS-DEMO-001'); assert result(c)['verdict']=='NEEDS_REVIEW'

@pytest.mark.parametrize('which',['policy','incident'])
def test_hash_mismatch(ctx,which):
    c,vm=ctx; mocks(vm,**{which:'tampered content'}); c.assess('CS-DEMO-001'); assert result(c)['verdict']=='INSUFFICIENT_EVIDENCE'; assert vm.run_validator()

def test_validator_disagrees(ctx):
    c,vm=ctx; mocks(vm); c.assess('CS-DEMO-001'); vm.clear_mocks(); mocks(vm,answer(incident='UNCLEAR')); assert not vm.run_validator()

def test_validator_rejects_forged_leader(ctx):
    c,vm=ctx; mocks(vm); c.assess('CS-DEMO-001'); leader=result(c); leader['reason']='forged'; leader['citations'][0]['quote']='THIS IS A FORGED QUOTE'; assert not vm.run_validator(leader_result=leader)

def test_validator_rejects_error(ctx):
    c,vm=ctx; mocks(vm); c.assess('CS-DEMO-001'); assert not vm.run_validator(leader_error=Exception('failed'))

@pytest.mark.parametrize('op',['policy','assess','challenge'])
def test_unauthorized(ctx,direct_bob,op):
    c,vm=ctx; vm.sender=direct_bob
    with pytest.raises(Exception):
        if op=='policy': c.register_policy('another',P['url'],P['sha256'])
        elif op=='assess': c.assess('CS-DEMO-001')
        else: c.challenge('CS-DEMO-001','A long enough challenge reason',json.dumps(E))

@pytest.mark.parametrize('url',[ROOT.replace('a'*40,'main')+'p.txt','https://evil.example/p.txt',ROOT+'../policy.txt',ROOT+'policy.txt?token=1',ROOT.replace('raw.githubusercontent.com','raw.githubusercontent.com.evil.test')+'p.txt'])
def test_source_restrictions(ctx,url):
    c,vm=ctx
    with pytest.raises(Exception): c.register_policy('bad',url,P['sha256'])

def test_duplicate_and_immutable(ctx):
    c,vm=ctx
    with pytest.raises(Exception): c.register_policy('motor',P['url'],P['sha256'])
    with pytest.raises(Exception): c.open_claim('CS-DEMO-001','motor',I,json.dumps([E]))
    with pytest.raises(Exception): c.open_claim('new','motor',I,json.dumps([E,E]))

def test_challenge_history_and_bound(ctx):
    c,vm=ctx; mocks(vm); c.assess('CS-DEMO-001'); old=c.get_history('CS-DEMO-001',0)
    text=Path('fixtures/counter-evidence.txt').read_text(); extra=source('counter-evidence.txt',text)
    c.challenge('CS-DEMO-001','A contradicting report requires review.',json.dumps(extra))
    assert json.loads(c.get_claim('CS-DEMO-001'))['state']=='CHALLENGED'
    vm.clear_mocks(); mocks(vm,answer(incident='UNCLEAR')); vm.mock_web('counter-evidence.txt',{'status':200,'body':text}); c.assess('CS-DEMO-001')
    assert result(c)['verdict']=='NEEDS_REVIEW'; assert c.get_history('CS-DEMO-001',0)==old
    with pytest.raises(Exception): c.challenge('CS-DEMO-001','A second challenge should not pass.',json.dumps(extra))
    with pytest.raises(Exception): c.assess('CS-DEMO-001')

def test_bad_attachment_does_not_veto_good(ctx):
    c,vm=ctx; bad=source('missing.txt','missing'); c.open_claim('extra','motor',I,json.dumps([E,bad])); mocks(vm); vm.mock_web('missing.txt',{'status':404,'body':''}); c.assess('extra'); r=json.loads(c.get_claim('extra'))['result']['result']; assert r['verdict']=='SUPPORTED'; assert r['sources'][2]['status']=='UNAVAILABLE'

@pytest.mark.parametrize('incident,evidence',[('x'*2001,json.dumps([E])),('{}',json.dumps([E])),(I,'[]'),(I,json.dumps([E]*4)),(I,json.dumps([{'url':E['url'],'sha256':'0'}]))])
def test_input_bounds(ctx,incident,evidence):
    c,vm=ctx
    with pytest.raises(Exception): c.open_claim('bad','motor',incident,evidence)

def test_empty_oversized_and_failed_source(ctx):
    c,vm=ctx; vm.mock_web('policy.txt',{'status':500,'body':'err'}); c.assess('CS-DEMO-001'); assert result(c)['verdict']=='INSUFFICIENT_EVIDENCE'

def test_pagination_config(ctx):
    c,vm=ctx; assert json.loads(c.list_claims(0))==['CS-DEMO-001']; assert json.loads(c.list_policies())==['motor']; assert json.loads(c.get_config())['claim_count']==1
    with pytest.raises(Exception): c.list_claims(-1)

@pytest.mark.parametrize('date',['2026-99-10','2026-02-30','abcd-ef-gh'])
def test_invalid_calendar_date(ctx,date):
    c,vm=ctx; incident=json.loads(I); incident['date']=date
    with pytest.raises(Exception): c.open_claim('bad-date','motor',json.dumps(incident),json.dumps([E]))

@pytest.mark.parametrize('body',['','x'*24001])
def test_source_size_limits(ctx,body):
    c,vm=ctx; mocks(vm,policy=body); c.assess('CS-DEMO-001'); assert result(c)['verdict']=='INSUFFICIENT_EVIDENCE'

@pytest.mark.parametrize('line',[True,-1,9999,'4'])
def test_invalid_line_reference(ctx,line):
    c,vm=ctx; data=json.loads(answer()); data['citations'][0]['line']=line; mocks(vm,json.dumps(data)); c.assess('CS-DEMO-001'); assert result(c)['verdict']=='NEEDS_REVIEW'

def test_selected_lines_become_exact_quotes(ctx):
    c,vm=ctx; mocks(vm); c.assess('CS-DEMO-001'); assert result(c)['citations'][0]['quote']==POLICY.splitlines()[4]; assert vm.run_validator()

def test_long_document_lines_preserve_all_characters(ctx):
    import sys
    module=next(m for m in list(sys.modules.values()) if hasattr(m,'document_lines') and hasattr(m,'ClaimShield'))
    text='x'*1100+'EXCLUDED'
    assert ''.join(module.document_lines(text))==text
    assert max(map(len,module.document_lines(text)))<=350
