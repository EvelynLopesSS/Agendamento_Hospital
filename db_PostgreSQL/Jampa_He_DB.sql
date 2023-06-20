/* Lógico_Jampa_Health: */

CREATE TABLE agendamento (
    cod_agendamento VARCHAR PRIMARY KEY UNIQUE,
    cpf_paciente VARCHAR,
    cod_hospital VARCHAR,
    cod_tipo_fila VARCHAR,
    hora_inicio_agendamento TIME,
    hora_final_agendamento TIME,
    data_incio_agendamento DATE,
    data_final_agendamento DATE
);

CREATE TABLE tipo_fila (
    cod_tipo_fila VARCHAR PRIMARY KEY,
    fila VARCHAR
);

CREATE TABLE paciente (
    cpf_paciente VARCHAR PRIMARY KEY UNIQUE,
    nome_paciente VARCHAR,
    sexo_paciente VARCHAR(1),
    telefone_paciente VARCHAR(11),
    data_nascimento_paciente DATE
);

CREATE TABLE residencia_paciente (
    cpf_paciente VARCHAR,
    cod_residencia_paciente VARCHAR PRIMARY KEY,
    endereco_paciente VARCHAR,
    bairro_paciente VARCHAR,
    cep_paciente VARCHAR,
    cidade VARCHAR,
    estado VARCHAR(2),
    pais VARCHAR
);

CREATE TABLE profissional (
    cod_profissional VARCHAR PRIMARY KEY UNIQUE,
    cod_hospital VARCHAR,
    nome_profissional VARCHAR,
    id_profissional VARCHAR,
    sexo_profissional VARCHAR(1),
    profissao_profisional VARCHAR,
    especialidade_profissional VARCHAR
);

CREATE TABLE hospital (
    cod_hospital VARCHAR PRIMARY KEY,
    nome_hospital VARCHAR,
    dias_funcionamento VARCHAR,
    telefone_hospital VARCHAR(11)
);

CREATE TABLE localizacao_hospitais (
    cod_hospital VARCHAR,
    cod_localizacao_hospital VARCHAR PRIMARY KEY,
    endereco_hospital VARCHAR,
    bairro_hospital VARCHAR,
    cep_hospital VARCHAR,
    cidade_hospital VARCHAR,
    estado_hospital VARCHAR(2)
);

CREATE TABLE consulta (
    cod_consulta VARCHAR PRIMARY KEY,
    especialidade_consulta VARCHAR,
    cod_hospital VARCHAR
);

CREATE TABLE exame (
    cod_exame VARCHAR PRIMARY KEY,
    tipo_exame VARCHAR,
    cod_hospital VARCHAR
);

CREATE TABLE cirurgia (
    cod_cirurgia VARCHAR PRIMARY KEY,
    especialidade_cirurgia VARCHAR,
    cod_hospital VARCHAR
);
 
ALTER TABLE agendamento ADD CONSTRAINT FK_agendamento_CPF
    FOREIGN KEY (cpf_paciente)
    REFERENCES paciente(cpf_paciente);
	
ALTER TABLE agendamento ADD CONSTRAINT FK_agendamento_COD_HOSPITAL
    FOREIGN KEY (cod_hospital)
    REFERENCES hospital(cod_hospital); 

ALTER TABLE agendamento ADD CONSTRAINT FK_agendamento_COD_TIPO_FILA
    FOREIGN KEY (cod_tipo_fila)
    REFERENCES tipo_fila(cod_tipo_fila);
 
 
ALTER TABLE paciente ADD CONSTRAINT FK_CPF_PACI_COD_AGEDA
    FOREIGN KEY (cpf_paciente)
    REFERENCES agendamento (cod_agendamento);
 
ALTER TABLE residencia_paciente ADD CONSTRAINT FK_residencia_CPF_PACI
    FOREIGN KEY (cpf_paciente)
    REFERENCES paciente(cpf_paciente);
 
ALTER TABLE profissional ADD CONSTRAINT FK_profiss_COD_HOSP
    FOREIGN KEY (cod_hospital)
    REFERENCES hospital(cod_hospital);
 
ALTER TABLE localizacao_hospitais ADD CONSTRAINT FK_localizacao_COD_HOSP
    FOREIGN KEY (cod_hospital)
    REFERENCES hospital(cod_hospital);
 
ALTER TABLE consulta ADD CONSTRAINT FK_consulta_COD_HOSP
    FOREIGN KEY (cod_hospital)
    REFERENCES hospital(cod_hospital);
 
ALTER TABLE exame ADD CONSTRAINT FK_exame_COD_HOSP
    FOREIGN KEY (cod_hospital)
    REFERENCES hospital(cod_hospital);
 
 
ALTER TABLE cirurgia ADD CONSTRAINT FK_cirurgia_COD_HOSP
    FOREIGN KEY (cod_hospital)
    REFERENCES hospital(cod_hospital);