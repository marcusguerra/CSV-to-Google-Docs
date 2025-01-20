import functions as ft

sheets_link = "https://docs.google.com/spreadsheets/d/1b5v4makJSmBwjxz7qk1uwJyDwQ04mN7tm3-dbumcpYQ/edit?gid=328103558#gid=328103558"
credentials_path = 'credentials.json'

ft.sheets_to_docs(sheets_link, credentials_path)