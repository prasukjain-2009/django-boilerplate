find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
find . -name "__pycache__" -type d -exec rm -r "{}" \;
rm "db.sqlite3"