'''!
@package config

this file fixes a correct working of the program, it is comparable with the settings page of a app.

'''

# databank credentials

dbname = "'hmsmeetnet_v3LP'"
user = "'postgres'"
host = "'localhost'"
password="'dataviz'"
gssencmode = 'disable'

# databank queries
lspi_query = "select series_id, lspi from lookup;"
eenheid_query = "select eenheid, type from eenheden where code = %s"
beschikbaarheden_query = "select percent, month, year from beschikbaarheden(%s)"
