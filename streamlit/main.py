import  streamlit as st
import pandas as pd

import folium
from streamlit_folium import st_folium

from folium.plugins import MeasureControl
from geopy.distance import distance

import locale


df_hospitais = pd.read_csv("C:/Users/Evelyn/Documents/Jampa_Health/endereco_hospitais.csv", encoding = 'utf-8', sep = ';')
residencias_df= pd.read_csv("C:/Users/Evelyn/Documents/Jampa_Health/endereco_PACIENTE.csv", encoding = 'utf-8', sep = ';')

# Definir a localização inicial do mapa
mapa = folium.Map(location=[-7.1195, -34.8450], zoom_start=13)


# Adicionar um marcador para a residência do paciente
residencia = [-7.177045, -34.8516827]
folium.Marker(location=residencia, popup="Residência do paciente").add_to(mapa)

# Adicionar um marcador para o hospital selecionado
hospital = [-7.121803, -34.864032]

folium.Marker(location=hospital, popup="Hospital selecionado").add_to(mapa)

# Calcular a distância entre a residência e o hospital
distancia = round(distance(residencia, hospital).km, 2)
dfloc = df_hospitais[['LATIDUDE', 'LONGITUDE', 'NOME']]
dfloc_lista = dfloc.values.tolist()

# Adicionar um marcador para cada hospital

for hospital in dfloc_lista:
    folium.Marker(location=[hospital[0], hospital[1]],
                  tooltip=hospital[2]).add_to(mapa)

#_____________________________________________________________
import psycopg2

# Configuração da conexão
conn = psycopg2.connect(
    host="localhost",
    port=" ",
    database=" ",
    user="postgres",
    password=" ")

# Cria um cursor object
cur = conn.cursor()
#_____________________________________________________________

def login():
    st.title('Login')

    # Obter username e password
    username = st.text_input('Nome de usuário')
    password = st.text_input('Senha', type='password')

    # Conferir se o username e password estão corretas
    if username == 'usuario' and password == 'senha':
        st.success('Login realizado com sucesso!')
        return True
    else:
        st.error('Nome de usuário ou senha incorretos.')
        return False




#_____________________________________________________________

def main():
    if not login():
        return

    # set page background color
    bgcolor = '#00BFB2'
    st.markdown(f'<style>body{{background-color: {bgcolor};}}</style>', unsafe_allow_html=True)
    st.sidebar.title('CRUD App com Streamlit')
    st.sidebar.image('JampaHealth_Logo.png',use_column_width=True)
    menu = ['Agendar', 'Visualizar', 'Atualizar', 'Cancelar']
    escolha = st.sidebar.selectbox('Menu', menu)
#___________________________________________________________________________
    # Executar query SQL para obter códigos de consulta
    cur.execute("SELECT especialidade_consulta FROM consulta")
    espci_consultas = [str(c[0]) for c in cur.fetchall()]
    cur.execute("SELECT tipo_exame FROM exame")
    espci_exame = [str(c[0]) for c in cur.fetchall()]
    cur.execute("SELECT especialidade_cirurgia FROM cirurgia")
    espci_cirurgia = [str(c[0]) for c in cur.fetchall()]
    cur.execute("SELECT fila FROM tipo_fila")
    tipo_fila = [str(c[0]) for c in cur.fetchall()]
    cur.execute("SELECT nome_hospital FROM hospital")
    hospital = [str(c[0]) for c in cur.fetchall()]
    cur.execute("SELECT * FROM agendamento")
    agendamento_cancelar = [str(c[0]) for c in cur.fetchall()]

    if escolha == 'Agendar':
        st.subheader('Agendar Consulta, Exame ou Cirurgia')
        # Layout
        col1, col2 = st.columns(2)
        with col1:
            tipo_agendamento = st.selectbox('Selecione o tipo de agendamento:', ['Consulta', 'Exame', 'Cirurgia'])

            if tipo_agendamento == "Consulta":
                especialidade_medica = st.selectbox("Selecione a especialidade médica:", espci_consultas)
            elif tipo_agendamento == "Exame":
                especialidade_medica = st.selectbox("Selecione o tipo de exame:", espci_exame)
            elif tipo_agendamento == "Cirurgia":
                especialidade_medica = st.selectbox("Selecione a especialidade cirúrgica:", espci_cirurgia)
            selected_tipo_fila = st.selectbox('Selecione o tipo de fila:', tipo_fila)
        with col2:
            locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
            data = st.date_input('Selecione a data:')
            hora = st.time_input('Selecione a hora:')
            selected_hospital = st.selectbox('Selecione o Hospital:', hospital)
        st_mapa = st_folium(mapa, width=700, height=300)
        if st.button('Agendar'):
            data_formatada = data.strftime('%A, %d de %B de %Y')
            st.success(
                f'Agendamento para {tipo_agendamento} em {data_formatada} às {hora} no {selected_hospital} realizado!')

            # Obter o código da especialidade com base no tipo de agendamento
            if tipo_agendamento == 'Consulta':
                cur.execute("SELECT cod_consulta FROM consulta WHERE especialidade_consulta = %s",
                            (especialidade_medica,))
                cod_especialidade = cur.fetchone()[0]
            elif tipo_agendamento == 'Exame':
                cur.execute("SELECT cod_exame FROM exame WHERE tipo_exame = %s", (especialidade_medica,))
                cod_especialidade = cur.fetchone()[0]
            elif tipo_agendamento == 'Cirurgia':
                cur.execute("SELECT cod_cirurgia FROM cirurgia WHERE especialidade_cirurgia = %s",
                            (especialidade_medica,))
                cod_especialidade = cur.fetchone()[0]
            else:
                cod_especialidade = None

            # Obter o código do hospital
            cur.execute("SELECT cod_hospital FROM hospital WHERE nome_hospital = %s", (selected_hospital,))
            cod_hospital = cur.fetchone()[0]
            cur.execute("SELECT cod_tipo_fila FROM tipo_fila WHERE fila = %s", (selected_tipo_fila,))
            cod_tipo_fila = cur.fetchone()[0]

            # Inserir os dados na tabela agendamento
            cur.execute(
                "INSERT INTO agendamento (cod_hospital, cod_tipo_fila, data_agendamento, hora_agendamento, cod_especialidade, tipo_agendamento, especialidade_tipo) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (cod_hospital, cod_tipo_fila, data, hora, cod_especialidade, tipo_agendamento, especialidade_medica))
            conn.commit()

    elif escolha == 'Visualizar':
        st.subheader('Visualizar Agendamento')
        with st.spinner('Carregando agendamentos...'):
            cur.execute(
                "SELECT cod_agendamento, tipo_agendamento, especialidade_tipo, tipo_fila.fila, data_agendamento, hora_agendamento, nome_hospital FROM agendamento INNER JOIN hospital ON agendamento.cod_hospital = hospital.cod_hospital INNER JOIN tipo_fila ON agendamento.cod_tipo_fila = tipo_fila.cod_tipo_fila")
            agendamentos = cur.fetchall()
            if len(agendamentos) > 0:
                agendamentos_df = pd.DataFrame(agendamentos, columns=['Código', 'Tipo Agendamento', 'Especialidade', 'Tipo Fila', 'Data', 'Hora', 'Hospital'])
                agendamentos_df['Data'] = pd.to_datetime(agendamentos_df['Data']).dt.date
                st.dataframe(agendamentos_df)
            else:
                st.warning('Não há agendamentos para visualizar.')


    elif escolha == 'Atualizar':
        st.subheader('Atualizar Agendamento')
        cod_agendamento = st.text_input('Digite o código do agendamento que deseja atualizar:')
        mostrar_botao_atualizar = False  # Variável de controle
        if st.button('Buscar Agendamento'):
            # Verificar se o agendamento existe
            cur.execute("SELECT * FROM agendamento WHERE cod_agendamento = %s", (cod_agendamento,))
            agendamento = cur.fetchone()
            if agendamento is None:
                st.warning('O agendamento não foi encontrado.')
            else:
                # Obter o nome do hospital e do tipo da fila
                cur.execute("SELECT nome_hospital FROM hospital WHERE cod_hospital = %s", (agendamento[1],))
                nome_hospital = cur.fetchone()[0]
                cur.execute("SELECT fila FROM tipo_fila WHERE cod_tipo_fila = %s", (agendamento[6],))
                tipo_fila_2 = cur.fetchone()[0]

                # Exibir os detalhes do agendamento em um layout de card personalizado
                st.write('Detalhes do Agendamento:')
                st.markdown(
                    """
                    <div style='border: 1px solid #e6e6e6; border-radius: 10px; padding: 10px;'>
                        <p><strong>Código:</strong> {codigo}</p>
                        <p><strong>Tipo Agendamento:</strong> {tipo_agendamento}</p>
                        <p><strong>Especialidade:</strong> {especialidade}</p>
                        <p><strong>Tipo Fila:</strong> {tipo_fila}</p>
                        <p><strong>Data:</strong> {data}</p>
                        <p><strong>Hora Agendamento:</strong> {hora_agendamento}</p>
                        <p><strong>Hospital:</strong> {hospital}</p>
                    </div>
                    """.format(
                        codigo=agendamento[5],
                        tipo_agendamento=agendamento[7],
                        especialidade=agendamento[8],
                        tipo_fila=tipo_fila_2,
                        data=agendamento[3],
                        hora_agendamento=agendamento[2],
                        hospital=nome_hospital
                    ),
                    unsafe_allow_html=True
                )
                mostrar_botao_atualizar = True  # Ativar variável de controle para exibir o botão
        if mostrar_botao_atualizar:
            # Obter os dados atualizados do agendamento
            data = st.date_input('Selecione a nova data:', value=agendamento[3])
            hora_agendamento = st.time_input('Selecione a nova hora do agendamento:', value=agendamento[2])
            if st.button('Atualizar Data e Hora'):
                # Atualizar os dados de data e hora do agendamento no banco de dados
                cur.execute(
                    "UPDATE agendamento SET data_agendamento = %s, hora_agendamento = %s WHERE cod_agendamento = %s",(data, hora_agendamento, cod_agendamento))
                conn.commit()
                st.success('A data e hora do agendamento foram atualizadas com sucesso.')

    elif escolha == 'Cancelar':
        st.subheader('Cancelar Agendamento')
        cod_cancelar = st.text_input('Digite o código do agendamento que deseja cancelar:')

        if st.button('Buscar Agendamento'):
            # Verificar se o agendamento existe
            cur.execute("SELECT * FROM agendamento WHERE cod_agendamento = %s", (cod_cancelar,))
            agendamento = cur.fetchone()

            if agendamento is None:
                st.warning('O agendamento não foi encontrado.')
            else:
                # Obter o nome do hospital e do tipo da fila
                cur.execute("SELECT nome_hospital FROM hospital WHERE cod_hospital = %s", (agendamento[1],))
                nome_hospital = cur.fetchone()[0]
                cur.execute("SELECT fila FROM tipo_fila WHERE cod_tipo_fila = %s", (agendamento[6],))
                tipo_fila_2 = cur.fetchone()[0]

                # Exibir os detalhes do agendamento
                st.markdown(
                    """
                    <div style='border: 1px solid #e6e6e6; border-radius: 10px; padding: 10px;'>
                        <p><strong>Código:</strong> {codigo}</p>
                        <p><strong>Tipo Agendamento:</strong> {tipo_agendamento}</p>
                        <p><strong>Especialidade:</strong> {especialidade}</p>
                        <p><strong>Tipo Fila:</strong> {tipo_fila}</p>
                        <p><strong>Data:</strong> {data}</p>
                        <p><strong>Hora Agendamento:</strong> {hora_agendamento}</p>
                        <p><strong>Hospital:</strong> {hospital}</p>
                    </div>
                    """.format(
                        codigo=agendamento[5],
                        tipo_agendamento=agendamento[7],
                        especialidade=agendamento[8],
                        tipo_fila=tipo_fila_2,
                        data=agendamento[3],
                        hora_agendamento=agendamento[2],
                        hospital=nome_hospital
                    ),
                    unsafe_allow_html=True
                )

        cancelar_agendamento = st.button('Cancelar Agendamento')
        if cancelar_agendamento:
            cur.execute("DELETE FROM agendamento WHERE cod_agendamento = %s", (cod_cancelar,))
            conn.commit()
            st.success(f'O agendamento {cod_cancelar} foi cancelado com sucesso!')
    else:
        st.subheader ('About')

        # Fechar conexão com o banco de dados
        cur.close()
        conn.close()

if __name__ == '__main__':
    main()
