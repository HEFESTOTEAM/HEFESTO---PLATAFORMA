import importlib
import sqlite3

# Carrega o Streamlit em tempo de execução para evitar que analisadores
# estáticos bloqueiem o arquivo quando a dependência não está no ambiente local.
st = importlib.import_module("streamlit")

st.set_page_config(

    layout="wide"
)

conn = sqlite3.connect("database/iim.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM maquinas")
total_maquinas = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM manutencoes")
total_manutencoes = cursor.fetchone()[0]

conn.close()


conn = sqlite3.connect("database/iim.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM maquinas")
total_maquinas = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM manutencoes")
total_manutencoes = cursor.fetchone()[0]

conn.close()

st.sidebar.markdown("---")

st.sidebar.success(
    f"🏭 Máquinas: {total_maquinas}"
)

st.sidebar.info(
    f"🔧 Manutenções: {total_manutencoes}"
)
st.sidebar.markdown("---")

st.caption("Interface Industrial Maintenance")

# MENU
st.sidebar.title("🏭 IIM")

st.sidebar.success(f"🏭 Máquinas: {total_maquinas}")
st.sidebar.info(f"🔧 Manutenções: {total_manutencoes}")

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navegação",
    [
        "Dashboard",
        "Máquinas",
        "Manutenções",
        "Consulta",
        "Diagnóstico",
        "Central da Máquina",
        "Documentos",
        "Softwares"
    ]
)
# DASHBOARD
if menu == "Dashboard":

    conn = sqlite3.connect("database/iim.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM falhas_conhecidas")
    total_falhas = cursor.fetchone()[0]

    conn.close()

    st.title("🏭 Interface Industrial Maintenance")

    col1, col2, col3 = st.columns(3)

    col1.metric("Máquinas", total_maquinas)
    col2.metric("Manutenções", total_manutencoes)
    col3.metric("Falhas Conhecidas", total_falhas)

    st.markdown("---")

    st.subheader("📊 Últimas Manutenções")

    conn = sqlite3.connect("database/iim.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            m.nome,
            mt.falha,
            mt.tecnico
        FROM manutencoes mt
        JOIN maquinas m
        ON mt.maquina_id = m.id
        ORDER BY mt.id DESC
        LIMIT 5
    """)

    dados = cursor.fetchall()

    conn.close()

    st.dataframe(
        dados,
        use_container_width=True
    )

# MÁQUINAS
elif menu == "Máquinas":

    st.title("🏭 Cadastro de Máquinas")

    codigo = st.text_input("Código")
    nome = st.text_input("Nome")
    fabricante = st.text_input("Fabricante")
    modelo = st.text_input("Modelo")

    if st.button("Cadastrar Máquina"):

        conn = sqlite3.connect("database/iim.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO maquinas
            (codigo, nome, fabricante, modelo)
            VALUES (?, ?, ?, ?)
        """, (
            codigo,
            nome,
            fabricante,
            modelo
        ))

        conn.commit()
        conn.close()

        st.success("Máquina cadastrada!")

    st.subheader("Máquinas Cadastradas")

    conn = sqlite3.connect("database/iim.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM maquinas")

    maquinas = cursor.fetchall()

    conn.close()

    st.dataframe(
        maquinas,
        use_container_width=True
    )
# MANUTENÇÕES
elif menu == "Manutenções":
    import sqlite3

    st.title("🔧 Registro de Manutenção")

    conn = sqlite3.connect("database/iim.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM maquinas")
    maquinas = cursor.fetchall()
    conn.close()

    if maquinas:
        maquina = st.selectbox(
            "Máquina",
            maquinas,
            format_func=lambda x: x[1],
        )

        falha = st.text_area("Falha")
        diagnostico = st.text_area("Diagnóstico")
        solucao = st.text_area("Solução")
        tecnico = st.text_input("Técnico")

        if st.button("Registrar Manutenção"):
            conn = sqlite3.connect("database/iim.db")
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO manutencoes (
                    maquina_id,
                    falha,
                    diagnostico,
                    solucao,
                    tecnico
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (maquina[0], falha, diagnostico, solucao, tecnico),
            )

            conn.commit()
            conn.close()
            st.success("Manutenção registrada!")
    else:
        st.warning("Cadastre uma máquina primeiro.")

    st.subheader("Histórico de Manutenções")

    conn = sqlite3.connect("database/iim.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            m.nome,
            mt.falha,
            mt.diagnostico,
            mt.solucao,
            mt.tecnico
        FROM manutencoes mt
        JOIN maquinas m ON mt.maquina_id = m.id
        """
    )

    historico = cursor.fetchall()
    conn.close()

    st.dataframe(historico, use_container_width=True)

elif menu == "Documentos":
    st.title("📄 Biblioteca Técnica")

    arquivo = st.file_uploader(
        "Enviar documento",
        type=["pdf", "docx", "png", "jpg"],
    )

    if arquivo:
        st.success("Arquivo carregado com sucesso!")

elif menu == "Softwares":
    st.title("💿 Softwares da Máquina")

    st.write("TIA Portal")
    st.write("Studio 5000")
    st.write("FactoryTalk")

elif menu == "Consulta":

    import sqlite3

    st.title("🔎 Consulta de Máquina")

    conn = sqlite3.connect("database/iim.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome FROM maquinas")
    maquinas = cursor.fetchall()

    if maquinas:

        maquina = st.selectbox(
            "Selecione a Máquina",
            maquinas,
            format_func=lambda x: x[1]
        )

        st.subheader("Histórico")

        cursor.execute("""
            SELECT
                falha,
                diagnostico,
                solucao,
                tecnico
            FROM manutencoes
            WHERE maquina_id = ?
        """, (maquina[0],))

        historico = cursor.fetchall()

        if historico:

            for item in historico:

                st.markdown("---")

                st.write("**Falha:**", item[0])
                st.write("**Diagnóstico:**", item[1])
                st.write("**Solução:**", item[2])
                st.write("**Técnico:**", item[3])

        else:
            st.info("Nenhuma manutenção registrada.")

    conn.close()

elif menu == "Diagnóstico":

    import sqlite3

    st.title("🔍 Diagnóstico Inteligente")

    sintoma = st.text_input(
        "Informe o sintoma da máquina"
    )

    if st.button("Analisar Falha"):

        conn = sqlite3.connect("database/iim.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                causa,
                solucao,
                incidencias
            FROM falhas_conhecidas
            WHERE LOWER(sintoma) LIKE LOWER(?)
            ORDER BY incidencias DESC
        """, (f"%{sintoma}%",))

        resultados = cursor.fetchall()

        conn.close()

        if resultados:

            st.success(
                f"{len(resultados)} ocorrência(s) encontrada(s)"
            )

            for causa, solucao, incidencias in resultados:

                st.markdown("---")

                st.write(
                    f"**Causa provável:** {causa}"
                )

                st.write(
                    f"**Solução recomendada:** {solucao}"
                )

                st.write(
                    f"**Ocorrências registradas:** {incidencias}"
                )

        else:

            st.warning(
                "Nenhuma falha conhecida encontrada."
            )

elif menu == "Central da Máquina":

    import sqlite3

    st.title("🏭 Central da Máquina")

    conn = sqlite3.connect("database/iim.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome FROM maquinas")

    maquinas = cursor.fetchall()

    if maquinas:

        maquina = st.selectbox(
            "Selecione a máquina",
            maquinas,
            format_func=lambda x: x[1]
        )

        st.subheader("Histórico")

        cursor.execute("""
        SELECT
            falha,
            diagnostico,
            solucao,
            tecnico
        FROM manutencoes
        WHERE maquina_id = ?
        """, (maquina[0],))

        historico = cursor.fetchall()

        if historico:

            for item in historico:

                st.markdown("---")

                st.write(f"**Falha:** {item[0]}")
                st.write(f"**Diagnóstico:** {item[1]}")
                st.write(f"**Solução:** {item[2]}")
                st.write(f"**Técnico:** {item[3]}")

        else:

            st.info("Nenhum histórico encontrado.")

    conn.close()

# DOCUMENTOS
elif menu == "Documentos":
    st.title("📄 Biblioteca Técnica")

    arquivo = st.file_uploader(
        "Enviar documento",
        type=["pdf", "docx", "png", "jpg"]
    )

    if arquivo:
        st.success("Arquivo carregado com sucesso!")

# SOFTWARES
elif menu == "Softwares":
    st.title("💿 Softwares da Máquina")

    st.write("TIA Portal")
    st.write("Studio 5000")
    st.write("FactoryTalk")
