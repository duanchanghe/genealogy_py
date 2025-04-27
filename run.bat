python manage.py createsuperuser
python manage.py migrate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
# Generate GraphQL schema
# This command generates a GraphQL schema file named `schema.graphql` in the current directory.
python manage.py graphql_schema --out schema.graphql