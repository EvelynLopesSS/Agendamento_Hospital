ALTER TABLE cirurgia
ADD CONSTRAINT unique_cirurgia_hospital
UNIQUE (cod_cirurgia, cod_hospital);

ALTER TABLE consulta
ADD CONSTRAINT unique_consulta_hospital
UNIQUE (cod_consulta, cod_hospital);

ALTER TABLE exame
ADD CONSTRAINT unique_exame_hospital
UNIQUE (cod_exame, cod_hospital);