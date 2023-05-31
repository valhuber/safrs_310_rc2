[This project](https://github.com/valhuber/safrs_310_rc2) is to get the sample ALS app working with safrs 311, currently rc2.

Status:
* Basic no-security runs
* Known Issues (evidently due to SQLAlchemy 2.0.15) - details below...
    * Fails with Security in DB Bind
* Resolved Issues
    * Delete gets a stacktrace on flush

> Suggestion: open this in GitHub using "Project View" (Shift + ".")

&nbsp;

---
&nbsp;

# Installation safrs==3.1.0rc2 (WIP)

This project runs properly under the *old* safrs/flask/SQLAlchemy.  You can verify this as described in the Appendix: Project Executes with old safrs/flask/SQLAlchemy.

rc2 safrs, however, requires the following (caution - still very brittle):

**1. Create a local venv:** `python3 -m venv venv; . venv/bin/activate`

**2. Install ApiLogicServer:** `pip install ApiLogicServer`

**3. Update the local venv:** `python3 -m pip install -r requirements.txt`

The requirements.txt file has been updated with safrs310 dependencies, noted in comments.  Various issues were resolved:

* One important dependency is `SQLAlchemy 2.0.15`.  Two issues were encountered and resolved as described in Appendix.

* Besides the new versions, `pyyaml` and `flask_swagger_ui` were surprises (they were not formerly required - not a problem, just an observation).

**4. Get the rc2 safrs**

`python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple  safrs==3.1.0rc2`

&nbsp;

# Testing

&nbsp;

## Verify runs `No Security`

Use the existing Run Config, verify:

1. App / swagger run
2. Behave tests run
    * You must execute the Behave Tests using Run Config `Behave No Security'.

&nbsp;

## Fails with Security in DB Bind

But, fails when running with security (Run Config `ApiLogicServer`), when you attempt to **login as U1/p**:

`sqlalchemy.exc.UnboundExecutionError: Bind key 'authentication' is not in 'SQLALCHEMY_BINDS' config.`

Thomas concurs that binds need recoding... from an email:

previously:
```python
session = db.create_scoped_session(options={"bind": connection, "binds": {}}
```

currently:
```python
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
session_factory = sessionmaker(bind=connection)
session = scoped_session(session_factory)
```

See [this gist](https://github.com/thomaxxl/safrs-example/blob/414aae69719db4fa544a086ae694f82047ae772e/tests/conftest.py#L69).

This needs to be applied to [database.bind_databases.py](/database/bind_databases.py).

I blindly added code to `bind_databases#open_databases()`.  But it's **not even called...**

`api_logic_server_run.py` is supposed to call it as shown below.  But breakpoints in `open_databases()` are not hit, and step-into passes right by.  Not a clue why this should be so.

![open_databases not called](./images/open_database%20not%20invoked.png)

Stuck there.

&nbsp;

# Appendix

&nbsp;

## Resolution 1: `cascade_backref`

One important dependency is `SQLAlchemy 2.0.15`.  This required manual update of the `models.py` to set `cascade_backrefs=False`.

This enabled the server to start in non-security mode, and run Admin App and Swagger.

&nbsp;

### Behave tests failed in *SQLAlchemy 1.4* with `cascade_backref` fix

I wanted to run the Behave tests, but they were security dependent.  

So, I tried backporting the cascade_backref fix to the prior release (SQLAlchemy 1.4).  I then built a project, and tried the Behave tests.

It failed in Behave Tests (*Scenario: Good Order,  Step: Logic adjusts aggregates down on delete order* - the **delete gets a stacktrace on flush**).  I feared this to be serious - read on.

&nbsp;

## Resolution 2: Delete stacktrace works with *SQLAlchemy 2.0.15*

I then upgraded the Behave tests to run *without security*.  This enabled me to try to the tests in *this* project, using SQLAlchemy 2.0.15. 

This solved the problem - the Behave tests run properly (without security).

&nbsp;

## Project Executes with old safrs/flask/SQLAlchemy

**Optionally** (not really recommended), you can verify this project in existing safrs/ALS.  It should run the Admin app, and `behave run` tests.  To install, setup the virtual env:

1. [shared venv](https://apilogicserver.github.io/Docs/Project-Env/#shared-venv), or

2. local venv - `python3 -m venv venv; . venv/bin/activate; python3 -m pip install ApiLogicServer`

To run, use the Run Configs - these should both work:

* `No Security`
* `ApiLogicServer` - [activates security, overview here](https://apilogicserver.github.io/Docs/Security-Overview/).
