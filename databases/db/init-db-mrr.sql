CREATE DATABASE mrr_db;

\c mrr_db;

CREATE TABLE "public"."mrr_customers" (
    "id" int4 NOT NULL,
    "name" varchar,
    "country" varchar,
    "created_at" timestamp,
    PRIMARY KEY ("id")
);


CREATE TABLE "public"."mrr_high_water_mark" (
    "source_table" varchar,
    "target_table" varchar,
    "last_modified" timestamp
);

CREATE TABLE "public"."mrr_products" (
    "id" int4 NOT NULL,
    "name" varchar,
    "group_name" varchar,
    "created_at" timestamp,
    PRIMARY KEY ("id")
);


CREATE TABLE "public"."mrr_sales" (
    "customer_id" int4,
    "product_id" int4,
    "qty" int4,
    "created_at" timestamp
);

CREATE UNIQUE INDEX unique_pair_index_mrr_hwm ON mrr_high_water_mark (source_table, target_table);
