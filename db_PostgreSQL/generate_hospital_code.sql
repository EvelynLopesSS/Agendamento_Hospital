
CREATE OR REPLACE FUNCTION generate_hospital_code()
RETURNS trigger AS $$
DECLARE
  code text;
BEGIN
  WHILE TRUE LOOP
    code := 'H' || LPAD(FLOOR(RANDOM() * 10000)::text, 4, '0');
    IF NOT EXISTS (SELECT 1 FROM hospital WHERE cod_hospital = code) THEN
      NEW.cod_hospital := code;
      RETURN NEW;
    END IF;
  END LOOP;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER set_hospital_code
BEFORE INSERT ON hospital
FOR EACH ROW
WHEN (NEW.cod_hospital IS NULL)
EXECUTE FUNCTION generate_hospital_code();


