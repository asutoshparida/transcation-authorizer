# authorizer

## Summary
**Class Hierarchy**
The authorizer is comprised of a set of self-contained plugable components.
Components are comprised as part of the authorizer component class hierarchy:
```
Component
    -> Action
```

At a minimum each component has the following:
- Each component must accept input transaction(String), memory store, rate limiter required to do its job.
- Each component returns the generated output json
- Each component must provide a run() method for invocation.

## Prerequisites
- Python 3.7
- Linux, MacOS

## Quick Start Setup

### Run the tests
```
sudo python setup.py test
```

### Run Setup. 
This will install all required packages and will allow you to run the app from anywhere on your machine.
`develop` will allow you to develop against a symlink of the current codebase
```
$> cd transcation-authorizer
$> sudo python setup.py install
$> sudo python setup.py develop
```

### Running Locally
authorizer can be executed as folows:

```
PROJECT_ROOT=$(pwd)
authorizer < $PROJECT_ROOT/authorizer/data/operations
```
## Walk-Through
There are 2 different type of operation `account` and  `transaction`. 
So I have decided to create a abstract class `component`, and 2 implementation class
`Account` and  `Transaction` respectively.

If incoming operation is of type `account` then code will instantiate `Account` class and then invoke `run()` which contains the business rules.

Same if incoming operation is of type `transaction` then code will instantiate `Transaction` class and then invoke `run()` which contains the business rules.

Let's say in future we are planning to add a new operation `recharge`. Then we need to create a new class `Recharge` and implement the business rules in `run()`,
this way we can make application more extensible.

For rate-limit check I am using a `list<tuple>` i.e `list[(transaction_merchant, transaction_amount, transaction_date_time)]`

For storage check I am using a `list<object> ` i.e `list[ActionBean/TrasactionBean]`


