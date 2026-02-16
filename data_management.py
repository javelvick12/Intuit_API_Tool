########### Admin/Import/Etc ###########
import pandas as pd
import sqlalchemy as sa
import os
from passlib.hash import pbkdf2_sha256
DB_PATH = os.path.join(os.path.dirname(__file__), 'oauth2data.db')
#NOTE: This is insecure and will need to be moved to a database after being encyrpted (These tokens are also likely expired).
auth_token = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwieC5vcmciOiJIMCJ9..9W_pWKhnsRsFlPxoLlcM8g.k90g5RitQL1jt9ytj0DhxYKw6AxH31qP4TE4sfssBBD2jmfJg6gm3TNsalpf9pnMm7_lBM_hzhiloLTJTF9v8bTtgGtj_j57n7dVUqqhl7kBZlek7uTToOlvY0-vNJm6YtpmBoiYno-0Qi14QkPzKSbeRbSctJtK6HAJm8obcIaH3Q8uLFiMtnFbyaFBOTObPTLjIVsS51x8am4h2OxqfuqulBIatOx31F6ZFo9gzzk6aowiqA5Mhpi5MyJmDOioZ4NL0IqqCmG6kUorYxms1mpNlsB2Hi8r4AePqZz9LWgI5EY1nwCDwm366xtA6S5Pn_bEyCjxlEptJFrwDQK2gahtMOlYoqmR7h7YtXGQ7OizWn4HcdUa-TzAOMQy1ABZUympL4aF1GuMFfSyTubh1NkFTKVSbDUIWasiMz5HkgNwac4z7Lyeg9zggViKG0-O0vamQPRcHoBfPiA66LV3iM4uv4Ihor64GPZ5CVG4Mxg.R3-AwiCHXfqcn-BObKW5zg"
auth_code = 'XAB11771045729evRoojHWkpMu87KgVav2ZrnekQqXTvlfxi2f'
refresh_token = 'RT1-118-H0-1779773174411jr6gmro0h9qwici4o'
realm_id = '9341456224866626'
########### Deliverable ###########
db = sa.create_engine(f'sqlite:///{DB_PATH}')

client = sa.Table(
    'Client', sa.MetaData(),
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('client_id', sa.String(255), nullable=False),
    sa.Column('client_secret', sa.String(255), nullable=False),
    sa.Column('access_token', sa.String(255), nullable=False),
    sa.Column('refresh_token', sa.String(255), nullable=False),
    sa.Column('realm_id', sa.String(255), nullable=False)
)