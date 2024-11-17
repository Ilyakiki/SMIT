DO $$ BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database WHERE datname = '${POSTGRES_DB}'
   ) THEN
      CREATE DATABASE "${POSTGRES_DB}";
   END IF;
END $$;

