UPDATE agendamento SET especialidade_tipo = (SELECT especialidade_consulta FROM consulta WHERE consulta.cod_consulta = agendamento.cod_especialidade AND agendamento.tipo_agendamento = 'Consulta');

UPDATE agendamento SET especialidade_tipo = (SELECT tipo_exame FROM exame WHERE exame.cod_exame = agendamento.cod_especialidade AND agendamento.tipo_agendamento = 'Exame');

UPDATE agendamento SET especialidade_tipo = (SELECT especialidade_cirurgia FROM cirurgia WHERE cirurgia.cod_cirurgia = agendamento.cod_especialidade AND agendamento.tipo_agendamento = 'Cirurgia');

