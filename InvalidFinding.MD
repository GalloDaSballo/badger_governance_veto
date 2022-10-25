## Reentrancy for re-execution. NOTE: Disputed, see test
https://github.com/Fatimanaz/badger_governance_veto/blob/9f4db872e618e21d70c1bc87b1491d2b3c36320f/contracts/governance/TimeController.sol#L448-L449

```solidity
            _call(id, i, targets[i], values[i], datas[i]);

```

Hunch: If timestamp is how we know a tx is done, we can reEnter and execute the tx multiple times

https://github.com/Fatimanaz/badger_governance_veto/blob/9f4db872e618e21d70c1bc87b1491d2b3c36320f/contracts/governance/TimeController.sol#L479-L480

```solidity
        _timestamps[id] = _DONE_TIMESTAMP;

```

As shown here
https://github.com/Fatimanaz/badger_governance_veto/blob/9f4db872e618e21d70c1bc87b1491d2b3c36320f/contracts/governance/TimeController.sol#L205-L214

```solidity
    function isOperationReady(bytes32 id)
        public
        view
        virtual
        returns (bool ready)
    {
        uint256 timestamp = getTimestamp(id);
        return timestamp > _DONE_TIMESTAMP && timestamp <= block.timestamp;
    }

```

We can reEnter and execute a proposal multiple times.

E.g.

A transfer of 1/10 of value from treasury + a transfer of ETH is going to happen

-> Via the ETH transfer we can Reenter and use that to cause the treasury to pay 10 times more in USD.
(Can send ETH back and forth to keep it working)


See: `test_reenter_exploit`