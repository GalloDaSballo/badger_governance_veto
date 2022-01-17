import pytest
import brownie

#fixture to flag an operation
@pytest.fixture()
def flag_operation(deploy, schedule_operation):
    id = schedule_operation
    contract = deploy.contract
    contract.flagOperation(id, {'from': deploy.proposer})
    return id 

# test - an operation can not be executed if it is paused
def test_execute(deploy, flag_operation, random_operation):
    id = flag_operation
    deployer = deploy.deployer 
    contract = deploy.contract
    # transaction should revert as it is paused
    with brownie.reverts("TimelockController: operation is paused can not be executed"):
        contract.execute(random_operation.target, random_operation.value, random_operation.data, random_operation.salt, random_operation.delay , {"from" : deploy.executer})

# test- if a supreme court decision is true, it should be paused after afterFlagOperation
def test_veto_passed(deploy, flag_operation):
    id = flag_operation
    deployer = deploy.deployer 
    contract = deploy.contract
    contract.afterFlagOperation(id , True)
    assert(contract.getFlagStatus(id)==1)

# test- if a supreme court decision is false, it should not be paused after afterFlagOperation
def test_veto_failed(deploy , flag_operation):
    id = flag_operation
    deployer = deploy.deployer 
    contract = deploy.contract
    contract.afterFlagOperation(id , False)
    assert(contract.getFlagStatus(id)==2)
