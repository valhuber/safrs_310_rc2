This is to get the sample ALS app working with safrs 311, currently rc2.

> Suggestion: open this in GitHub using "Project View" (Shift + ".")

&nbsp;

---
&nbsp;

# Installation

&nbsp;

## Existing ALS (optional, for verification)

You can verify this works in existing safrs/ALS.  It should run OptLocking tests (see the readme), and `behave run` tests.  To install, setup the virtual env:

1. [shared venv](https://apilogicserver.github.io/Docs/Project-Env/#shared-venv), or

2. local venv - python3 -m venv venv; . venv/bin/activate; python3 -m pip install ApiLogicServer

&nbsp;

## safrs==3.1.0rc2 (WIP)

rc2 safrs requires the following (caution - still very brittle):

1. Create a local venv: `python3 -m venv venv; . venv/bin/activate`

2. Install ApiLogicServer: `pip install ApiLogicServer`

3. Update the local venv: `python3 -m pip install -r requirements.txt`

The requirements.txt file has been updated with safrs310 dependencies, noted in comments.

**Note:** one important dependency is `SQLAlchemy 2.0.15`.  This required manual update of the `models.py` to set `cascade_backrefs=False`.  That seemed to be sufficient.  This will require an ALS update (minor).

Besides the new versions, `pyyaml` and `flask_swagger_ui` were surprises.

4. Get the rc2 safrs

`python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple  safrs==3.1.0rc2`

&nbsp;

### Verify runs `No Security`

Use the existing Run Config, verify app / swagger run.

&nbsp;

### Fails with Security in DB Bind

But, fails when running with security:

`sqlalchemy.exc.UnboundExecutionError: Bind key 'authentication' is not in 'SQLALCHEMY_BINDS' config.`

Thomas concurs that binds need recoding.

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

To be continued.
