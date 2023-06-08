CREATE DATABASE source_db;

\c source_db;

CREATE TABLE customers (
    "id" int4 NOT NULL,
    "name" varchar,
    "country" varchar,
    "created_at" timestamp,
    PRIMARY KEY ("id")
);

CREATE TABLE "public"."products" (
    "id" int4 NOT NULL,
    "name" varchar,
    "group_name" varchar,
    "created_at" timestamp,
    PRIMARY KEY ("id")
);

CREATE TABLE "public"."sales" (
    "customer_id" int4,
    "product_id" int4,
    "qty" int4,
    "created_at" timestamp
);
