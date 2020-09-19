# Generated by Django 3.1 on 2020-08-31 00:34

from django.db import migrations, models

"""
To use this migration file you need to create a new database on Heroku or locally. Once the project has been pushed
to your Heroku instance or has been configured to run locally, you can automatically populate the database with all
of the required tables and data by executing the following command: 

For local migration: python manage.py migrate
For Heroku migration: heroku run python manage.py migrate


See the following URL for examples
https://docs.djangoproject.com/en/3.1/topics/migrations/
"""
class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(
            """ 
                CREATE EXTENSION pgcrypto; --Allows PostgreSQL to understand UUIDs. Only have to create the extension once for a database.
                --DROP TABLE register_product;
                CREATE TABLE register_product (
                    id uuid NOT NULL DEFAULT gen_random_uuid(),
                    lookupcode character varying(32) NOT NULL DEFAULT(''),
                    count int NOT NULL DEFAULT(0),
                    createdon timestamp without time zone NOT NULL DEFAULT now(),
                    CONSTRAINT product_pkey PRIMARY KEY (id)
                ) WITH (
                    OIDS=FALSE
                );

                --DROP INDEX ix_product_lookupcode;

                CREATE INDEX ix_product_lookupcode --An index on the product table lookupcode column
                    ON register_product
                    USING btree
                    (lower(lookupcode::text) COLLATE pg_catalog."default"); --Index on the lower case of the lookup code. Queries for product by lookupcode should search using the lower case of the lookup code.

                INSERT INTO register_product (lookupcode, count) VALUES ( --id and createdon are generated by default.
                    'lookupcode1'
                    , 100)
                RETURNING id, createdon;

                INSERT INTO register_product (lookupcode, count) VALUES (
                    'lookupcode2'
                    , 125)
                RETURNING id, createdon;

                INSERT INTO register_product (lookupcode, count) VALUES (
                    'lookupcode3'
                    , 150)
                RETURNING id, createdon;

                --SELECT * FROM register_product;

                --DELETE FROM register_product;

                """
        ),
    ]
