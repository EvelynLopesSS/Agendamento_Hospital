CREATE OR REPLACE FUNCTION gerar_cod_agendamento()
RETURNS TRIGGER AS $$
DECLARE
  novo_cod TEXT;
BEGIN
  novo_cod := 'AG' || LPAD(floor(random() * 10000)::TEXT, 4, '0');
  
  WHILE EXISTS(SELECT 1 FROM agendamento WHERE cod_agendamento = novo_cod) LOOP
    novo_cod := 'AG' || LPAD(floor(random() * 10000)::TEXT, 4, '0');
  END LOOP;
  
  NEW.cod_agendamento := novo_cod;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER gerar_cod_agendamento_trigger
BEFORE INSERT ON agendamento
FOR EACH ROW
EXECUTE FUNCTION gerar_cod_agendamento();
