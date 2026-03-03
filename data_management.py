########### Admin/Import/Etc ###########
import sqlalchemy as sa
from sqlalchemy import ForeignKey, event
from sqlalchemy.exc import SQLAlchemyError
import os
import time
from utilities import print_error #DEBUG inconsistent - also why ut.fx V just ut all? 
DB_PATH = os.path.join(os.path.dirname(__file__), 'oauth2data.sqlite')

########### Deliverable ###########
db = sa.create_engine(f'sqlite:///{DB_PATH}')
metadata = sa.MetaData()

client = sa.Table(
    'Client', metadata,
    sa.Column('client_id', sa.String(255), nullable=False),
    sa.Column('client_secret', sa.String(255), nullable=False),
    sa.Column('scope', sa.String(255), nullable=False),
    sa.Column('RealmID', sa.String(255), nullable=False),
)
token = sa.Table(
    'Token', metadata,
    sa.Column('token_hash', sa.String(255), primary_key=True),
    sa.Column('type', sa.String(255), nullable=False),
    sa.Column('utc_created_at', sa.Integer, nullable=False),
    sa.Column('utc_expires_at', sa.Integer, nullable=False),
    sa.Column('client_id', sa.String(255), nullable=False)

)

def init_db() -> sa.engine:
    """
    Initializes database engine and metadata for use.
  
    Returns:
        sa.engine: Engine object for database to store and read from
    """
    metadata.create_all(db)
    Client = metadata.tables["Client"]
    Token = metadata.tables["Token"]
    return db

def write_to_db(db_table: str, attributes: dict) -> bool:
    """
    Helper function to write to either of our two tables any relevant client or token data

    Args:
        db_table (str): Which table to write in
        attributes (dict): dictionary of attributes to write to the table 

    Raises:
        ValueError: Raised if not valid token type is passed.

    Returns:
        bool: Return True on success or False on failure
    """
    if db_table.lower() not in ("client", "token"):
        raise ValueError(f"write_to_db: specified table is not valid: {db_table}.")
    try:
        with db.begin() as conn:
            if db_table == "Client": # If client table specified expect dict with client attributes
                client_id = attributes["client_id"]
                rows = conn.execute(sa.select(client).where(client.c.client_id == client_id))
                conn.execute(
                    sa.insert(client).values(
                        client_id = attributes["client_id"],
                        client_secret = attributes["client_secret"],
                        scope = attributes["scope"],
                        RealmID = attributes["RealmID"]
                    )
                )
            elif db_table == "Token": # If token table specified expect dict with token attributes and handle token existing
                token_hash = attributes["token_hash"]
                token_type = attributes["token_type"]
                rows = conn.execute(sa.select(token).where(token.c.token_hash == token_hash)).first()
                utc_now = int(time.time())
                if token_type == "refresh":
                    expires_at = utc_now + (86400*90) # refresh tokens last 90 days, so we add amount of seconds equivalent to 90 days.
                elif token_type == "access":
                    expires_at = utc_now + (58*60) # access tokens last 1 hour, so we put 58 minutes here to be safe
                else:
                    raise ValueError(f"Unsupported token type: {token_type}")
                if not rows:
                    statement = sa.insert(token).values(
                        token_hash = attributes["token_hash"],
                        type = attributes["token_type"],
                        utc_created_at=utc_now,
                        utc_expires_at=expires_at,
                        client_id = attributes["client_id"]
                    )
                else:
                    statement = (
                        sa.update(token)
                        .where(token.c.token_hash == token_hash)
                        .values(
                            type=token_type,
                            utc_created_at=utc_now,
                            utc_expires_at=expires_at,
                            client_id = attributes["client_id"]
                        )
                    )
                conn.execute(statement)
                return True
    except SQLAlchemyError as e:
        print_error(e, "write_to_db")
        return False
    
def lookup_db(table: str, type: str, value: str=None, column: str=None) -> dict:
    """
    Helper function to lookup data in the database with arguments to specify where to look and for what.

    Args:
        table (str): Which table to lookup data in
        type (str): Specify either to find a whole row or a certain attribute or value of a row
        value (str, optional): The specific value to find in a row. Defaults to None.

    Raises:
        ValueError: If passed type isn't row or value, raise value error.
        ValueError: If passed table isn't a valid table, raise value error.

    Returns:
        bool: Return true on success or false on failure.
    """
    if type.lower() not in ("row", "value"):
        raise ValueError(f"lookup_db: passed type not valid for db lookup: {type}")
    if table.lower() not in ("token", "client"):
        raise ValueError(f"lookup_db: passed table not valid for db lookup: {table}")
    
    table_object = client if table.lower() == "client" else token

    try:
        with db.connect() as conn:
            if value is None:
               statement = sa.select(table_object)
            else:
                statement = sa.select(table_object).where(table_object.c[column] == value)

            rows = conn.execute(statement).mappings().all()
            return [dict(r) for r in rows]
        #DEBUGU below is dead...
            if table.lower() == "token" and type.lower() == "row":
                created_col = None
                statement = sa.select(table_object).order_by(sa.desc("utc_created_at")).first()
            key_col = column if column is not None else (value if table.lower() == "client" and column is None and type.lower() == "row" and False else None)
            if key_col is None:
                key_col = "client_id" if table.lower() == "client" else "token_hash"
            statement = sa.select(table_object).where(table_object.c[key_col] == value)
        rows = conn.execute(statement).mappings().all()
        if not rows:
            return None
        return dict(rows[0]) if len(rows) == 1 else [dict(r) for r in rows]
            
    except SQLAlchemyError as e:
        print_error(e, "lookup_db")
        return None
    


if __name__ == "__main__":
    init_db()
    