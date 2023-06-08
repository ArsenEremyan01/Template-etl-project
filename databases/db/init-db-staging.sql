CREATE DATABASE staging_db;

\c staging_db;

CREATE TABLE "public"."stg_dim_product_group" (
    "id" int4 NOT NULL,
    "group_name" varchar,
    PRIMARY KEY ("id")
);


CREATE TABLE "public"."stg_dim_product_name" (
    "id" int4 NOT NULL,
    "name" varchar,
    PRIMARY KEY ("id")
);

CREATE TABLE "public"."stg_products" (
    "id" int4 NOT NULL,
    "name" varchar,
    "group_name" varchar,
    "created_at" timestamp,
    PRIMARY KEY ("id")
);

CREATE TABLE "public"."stg_fact_sales" (
    "product_group_id" int4,
    "product_name_id" int4,
    "total_qty" int4,
    FOREIGN KEY ("product_group_id") REFERENCES "public"."stg_dim_product_group"(id),
    FOREIGN KEY ("product_name_id") REFERENCES "public"."stg_dim_product_name"(id)
);


CREATE TABLE "public"."stg_sales" (
    "customer_id" int4,
    "product_id" int4,
    "qty" int4,
    "created_at" timestamp
);
