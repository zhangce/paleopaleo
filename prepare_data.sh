#! /bin/bash

# Configuration
DB_NAME=deepdive_titles
DB_USER=czhang
DB_PASSWORD="Password is set via the PGPASSWORD environment variable"

cd `dirname $0`
BASE_DIR=`pwd`



#dropdb -U $DB_USER deepdive_titles

#createdb -U $DB_USER deepdive_titles

#psql -U $DB_USER -c "drop schema if exists public cascade; create schema public;" $DB_NAME
#
psql -U $DB_USER -c "delete from documents;"             $DB_NAME
psql -U $DB_USER -c "delete from entities;"             $DB_NAME
psql -U $DB_USER -c "delete from relations_taxonomy;"             $DB_NAME
psql -U $DB_USER -c "delete from relations_formation;"             $DB_NAME
psql -U $DB_USER -c "delete from relations_formationtemporal;"             $DB_NAME
psql -U $DB_USER -c "delete from relations_formationlocation;"             $DB_NAME
psql -U $DB_USER -c "delete from relations_features_taxonomy;"             $DB_NAME
psql -U $DB_USER -c "delete from relations_features_formation;"             $DB_NAME
psql -U $DB_USER -c "delete from relations_features_formationtemporal;"             $DB_NAME
psql -U $DB_USER -c "delete from relations_features_formationlocation;"             $DB_NAME

psql -U $DB_USER -c "CREATE TABLE documents (id bigserial primary key, \
											 docid  text,               \
											 document text);"             $DB_NAME

psql -U $DB_USER -c "CREATE TABLE entities (id   bigserial primary key, \
											 docid  text,                  \
											 type   text,                   \
											 eid    text,  \
											 entity text,\
											 features text);"                $DB_NAME

psql -U $DB_USER -c "CREATE TABLE relations_features_taxonomy (id   bigserial primary key, \
											 docid  text,                  \
											 type   text,                   \
											 eid1    text,  \
											 eid2    text,  \
											 entity1 text,  \
											 entity2 text,\
											 features text,\
											 is_correct boolean);"                $DB_NAME


psql -U $DB_USER -c "CREATE TABLE relations_features_formation (id   bigserial primary key, \
											 docid  text,                  \
											 type   text,                   \
											 eid1    text,  \
											 eid2    text,  \
											 entity1 text,  \
											 entity2 text,\
											 features text,\
											 is_correct boolean);"                $DB_NAME


psql -U $DB_USER -c "CREATE TABLE relations_features_formationtemporal (id   bigserial primary key, \
											 docid  text,                  \
											 type   text,                   \
											 eid1    text,  \
											 eid2    text,  \
											 entity1 text,  \
											 entity2 text,\
											 features text,\
											 is_correct boolean);"                $DB_NAME


psql -U $DB_USER -c "CREATE TABLE relations_features_formationlocation (id   bigserial primary key, \
											 docid  text,                  \
											 type   text,                   \
											 eid1    text,  \
											 eid2    text,  \
											 entity1 text,  \
											 entity2 text,\
											 features text,\
											 is_correct boolean);"                $DB_NAME


psql -U $DB_USER -c "CREATE TABLE relations_taxonomy (id   bigserial primary key, \
											 docid  text,                  \
											 type   text,                   \
											 eid1    text,  \
											 eid2    text,  \
											 entity1 text,  \
											 entity2 text,\
											 is_correct boolean);"                $DB_NAME


psql -U $DB_USER -c "CREATE TABLE relations_formation (id   bigserial primary key, \
											 docid  text,                  \
											 type   text,                   \
											 eid1    text,  \
											 eid2    text,  \
											 entity1 text,  \
											 entity2 text,\
											 is_correct boolean);"                $DB_NAME


psql -U $DB_USER -c "CREATE TABLE relations_formationtemporal (id   bigserial primary key, \
											 docid  text,                  \
											 type   text,                   \
											 eid1    text,  \
											 eid2    text,  \
											 entity1 text,  \
											 entity2 text,\
											 is_correct boolean);"                $DB_NAME


psql -U $DB_USER -c "CREATE TABLE relations_formationlocation (id   bigserial primary key, \
											 docid  text,                  \
											 type   text,                   \
											 eid1    text,  \
											 eid2    text,  \
											 entity1 text,  \
											 entity2 text,\
											 is_correct boolean);"                $DB_NAME









