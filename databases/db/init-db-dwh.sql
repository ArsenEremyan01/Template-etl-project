CREATE DATABASE dwh_db;

\c dwh_db;

CREATE TABLE "public"."dim_product_group" (
    "id" int4 NOT NULL,
    "group_name" varchar,
    PRIMARY KEY ("id")
);


CREATE TABLE "public"."dim_product_name" (
    "id" int4 NOT NULL,
    "name" varchar,
    PRIMARY KEY ("id")
);


CREATE SEQUENCE IF NOT EXISTS fact_sales_id_seq;
CREATE TABLE "public"."fact_sales" (
    "id" int4 NOT NULL DEFAULT nextval('fact_sales_id_seq'::regclass),
    "product_group_id" int4,
    "product_name_id" int4,
    "total_qty" int4,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("product_group_id") REFERENCES "public"."dim_product_group"(id),
    FOREIGN KEY ("product_name_id") REFERENCES "public"."dim_product_name"(id)
);


CREATE TABLE "public"."fact_sales_validation_logs" (
    "error_type" varchar NOT NULL,
    "created_at" timestamp NOT NULL
);

-- Simple method to convert text to Upper case
CREATE OR REPLACE FUNCTION convert_to_uppercase(input_string text)
  RETURNS text
AS $$
BEGIN
  RETURN UPPER(input_string);
END;
$$ LANGUAGE plpgsql;

-- Checks for negative quantity number and insert to log table
CREATE OR REPLACE PROCEDURE check_negative_values()
LANGUAGE plpgsql
AS $$
DECLARE
  rec RECORD;
  value_check integer;
  cur CURSOR FOR SELECT total_qty FROM fact_sales;
BEGIN
  BEGIN
    OPEN cur;
    LOOP
      FETCH cur INTO rec;
      EXIT WHEN NOT FOUND;
      value_check := rec.total_qty;
      IF value_check < 0 THEN
        RAISE EXCEPTION 'Negative value found: %', value_check;
      END IF;
    END LOOP;
  CLOSE cur;
  EXCEPTION
    WHEN others THEN
      BEGIN
		INSERT INTO fact_sales_validation_logs (error_type, created_at) VALUES ('negative_number', CURRENT_TIMESTAMP);
      EXCEPTION
        WHEN others THEN
          NULL;
      END;
      RAISE NOTICE 'An error occurred: %', SQLERRM;
  END;
END;
$$;