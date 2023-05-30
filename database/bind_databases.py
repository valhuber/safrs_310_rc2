from safrs import SAFRSAPI
import logging as logging

app_logger = logging.getLogger("api_logic_server_app")

# use absolute path import for easier multi-{app,model,db} support
database = __import__('database')

def open_databases(flask_app, session, safrs_api, method_decorators):
    """ called by api_logic_server_run to open each additional database, and expose APIs """

    # Begin Bind URLs


    from api import authentication_expose_api_models
    from database import authentication_models

    # flask_app.config.update(SQLALCHEMY_BINDS = \
    #     {'authentication': flask_app.config['SQLALCHEMY_DATABASE_URI_AUTHENTICATION']})
    
    app_logger.debug(f"\nauthentication Config complete - database/authentication_models.py"
        + f'\n -- with bind: authentication'
        + f'\n -- len(database.authentication_models.authentication.metadata.tables) tables loaded')
    
    authentication_expose_api_models.expose_models(safrs_api, method_decorators= method_decorators)

        # End Bind URLs

    safrs_version = "3.1.0"  # or, 3.0.4

    if safrs_version == "3.0.4":
        flask_app.config.update(SQLALCHEMY_BINDS = {
            'authentication': flask_app.config['SQLALCHEMY_DATABASE_URI_AUTHENTICATION']
        })  # make multiple databases available to SQLAlchemy
    else:
        app_logger.debug("trying binds for safrs 3.1.0")  # good place for breakpoint, prayers...

        # Start a scoped session (i.e it'll be closed after current application context)
        from sqlalchemy.orm import scoped_session
        from sqlalchemy.orm import sessionmaker

        session_factory = sessionmaker(bind=session)  # ??
        session = scoped_session(session_factory)
        #session = db.create_scoped_session(options={"bind": connection, "binds": {}})

        # Put our session on the db object for the codebase to use
        db = safrs_api.DB  # ??
        db.session = session

        yield session


    return