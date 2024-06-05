class AppSettings:
    db_ro: DatabaseSettings = DatabaseSettings(dsn='{"database": "db-whoosh-dev22", "host": "whoosh-db-test2.cluster-cnm8gsaqbmae.us-east-1.rds.amazonaws.com", "password": "db-whoosh", "port": "5432", "username": "db-whoosh", "scheme": "postgresql"}')
    db_write: DatabaseSettings = DatabaseSettings(dsn='{"database": "db-whoosh-dev22", "host": "whoosh-db-test2.cluster-cnm8gsaqbmae.us-east-1.rds.amazonaws.com", "password": "db-whoosh", "port": "5432", "username": "db-whoosh", "scheme": "postgresql"}')
