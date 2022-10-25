## TODO: Check old advisory - Safe
https://github.com/OpenZeppelin/openzeppelin-contracts/security/advisories/GHSA-fg47-3c2x-m2wr


## Gotcha - Lack of return value check
https://github.com/Fatimanaz/badger_governance_veto/blob/9f4db872e618e21d70c1bc87b1491d2b3c36320f/contracts/governance/TimeController.sol#L494-L495

```solidity
        (bool success, ) = target.call{value: value}(data);

```

We may want to verify what the return value is, e.g. a ERC20 can return success and still fail

TODO: Check OZ / Other Governors

## Admin Privilege  - Caller becomes ADMIN_ROLE
https://github.com/Fatimanaz/badger_governance_veto/blob/9f4db872e618e21d70c1bc87b1491d2b3c36320f/contracts/governance/TimeController.sol#L119-L120

```solidity
        _setupRole(TIMELOCK_ADMIN_ROLE, _msgSender());

```

Allowing caller to become admin role is a risk as that's an EOA that can basically manage everything.
It should not be allowed / it should be then renounced


## Philosophy

Do we want roles vs just address?

Roles makes each line exponentially more complex and broadens the attack area

Roles could be achieved by making each role a separate Smart Contract (module) meaning there's no loss of generalizability, however this code can create gotchas



## R - Use Enum instead of 0, 1 and 2 for clarity
https://github.com/Fatimanaz/badger_governance_veto/blob/9f4db872e618e21d70c1bc87b1491d2b3c36320f/contracts/governance/TimeController.sol#L462-L463

```solidity
            getDisputeStatus(id) != 1,

```

## R - Use Enum for clarity for Ruling
https://github.com/Fatimanaz/badger_governance_veto/blob/9f4db872e618e21d70c1bc87b1491d2b3c36320f/contracts/governance/TimeController.sol#L559-L560

```solidity
        bool ruling,

```

## Gotcha - You need new salt for same operation else id clash will cause revert
https://github.com/Fatimanaz/badger_governance_veto/blob/9f4db872e618e21d70c1bc87b1491d2b3c36320f/contracts/governance/TimeController.sol#L325-L326

```solidity
        bytes32 salt,

```

Just a note

## NC - Emit an event for Ruling in the positive
https://github.com/Fatimanaz/badger_governance_veto/blob/9f4db872e618e21d70c1bc87b1491d2b3c36320f/contracts/governance/TimeController.sol#L570-L571

```solidity
            _disputed[id] = 2;

```

## Coverage is not there - Need higher coverage 
```python
Launching 'ganache-cli --accounts 10 --hardfork istanbul --gasLimit 12000000 --mnemonic brownie --port 8545'...

tests/test_after_call_disputed.py ...                                                                                           [ 37%]
tests/test_call_dispute.py ...                                                                                                  [ 75%]
tests/test_integration.py ..                                                                                                    [100%]
============================================================== Coverage ===============================================================


  contract: TimelockController - 41.7%
    AccessControl._checkRole - 100.0%
    TimelockController.callDispute - 87.5%
    TimelockController.callDisputeResolve - 87.5%
    TimelockController._beforeCall - 81.2%
    TimelockController._afterCall - 75.0%
    TimelockController._call - 75.0%
    TimelockController._schedule - 75.0%
    AccessControl._grantRole - 0.0%
    AccessControl._revokeRole - 0.0%
    AccessControl.renounceRole - 0.0%
    TimelockController.cancel - 0.0%
    TimelockController.executeBatch - 0.0%
    TimelockController.scheduleBatch - 0.0%
    TimelockController.updateDelay - 0.0%
```

Should improve coverage.

Also `AccessControl` needs coverage as well



## Gas

## Can pack _timestamps and _disputed by using a struct

    mapping(bytes32 => uint256) private _timestamps;

    /**
     * @dev disputed is mapping which tells if the operation is disputed or can be disputed.
     * 0 => is not disputed and can be disputed
     * 1 => disputed
     * 2 => not disputed and can not be disputed, needed as if an operation is disputed once and
     *      supreme court rejects it, it can not be disputed again.
     */
    mapping(bytes32 => uint16) public _disputed;

Should net some gas savings (about 5k per operation)