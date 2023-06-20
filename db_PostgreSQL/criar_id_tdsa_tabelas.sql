DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename IN ('agendamento', 'exame', 'cirurgia', 'consulta', 'hospital', 'localizacao_hospital', 'paciente', 'profissional', 'residencia_paciente', 'tipo_fila')) LOOP
        EXECUTE 'ALTER TABLE ' || quote_ident(r.tablename) || ' ADD COLUMN id SERIAL';
    END LOOP;
END$$;
