import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# ================= CONFIG =================
st.set_page_config(layout="wide", page_title="Smart AI Dashboard")

# ================= DATABASE =================
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="king1manish",
        database="smart_dashboard"
    )

# ================= AUTH =================
def auth_system():
    st.sidebar.title("🔐 Authentication")
    choice = st.sidebar.radio("Select", ["Login", "Signup"])

    conn = connect_db()
    cursor = conn.cursor()

    if choice == "Signup":
        name = st.sidebar.text_input("Name")
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Create Account"):
            cursor.execute(
                "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",
                (name, email, password),
            )
            conn.commit()
            st.sidebar.success("Account Created!")

    if choice == "Login":
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):
            cursor.execute(
                "SELECT * FROM users WHERE email=%s AND password=%s",
                (email, password),
            )
            user = cursor.fetchone()
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user[1]
                st.sidebar.success("Login Successful")
            else:
                st.sidebar.error("Invalid Credentials")

# ================= CACHE =================
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

# ================= SESSION INIT =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

auth_system()

# ================= MAIN DASHBOARD =================
if st.session_state.logged_in:

    st.title("🚀 Executive AI Analytics Dashboard")
    st.caption(f"Welcome, {st.session_state.user}")

    file = st.file_uploader("📂 Upload CSV File", type=["csv"])

    if file:
        df = load_data(file)

        numeric_cols = df.select_dtypes(include=['int64','float64']).columns
        cat_cols = df.select_dtypes(include=['object']).columns

        # ================= SAMPLING FOR HEAVY VISUALS =================
        if len(df) > 5000:
            df_sample = df.sample(5000)
        else:
            df_sample = df

        # ================= SIDEBAR FILTER =================
        st.sidebar.header("🔎 Filters")

        if len(cat_cols) > 0:
            filter_col = st.sidebar.selectbox("Filter By", cat_cols)
            selected_values = st.sidebar.multiselect(
                "Select Values",
                df[filter_col].unique(),
                default=df[filter_col].unique()
            )
            df = df[df[filter_col].isin(selected_values)]

        # ================= KPI CARDS =================
        st.subheader("📊 Key Metrics")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Records", len(df))

        if len(numeric_cols) > 0:
            col2.metric("Total Sum", round(df[numeric_cols[0]].sum(),2))
            col3.metric("Average", round(df[numeric_cols[0]].mean(),2))
            col4.metric("Max Value", round(df[numeric_cols[0]].max(),2))

        st.divider()

        # ================= AGGREGATED BAR CHART =================
        if len(cat_cols) > 0:
            grouped = df.groupby(cat_cols[0])[numeric_cols[0]].sum().reset_index()

            fig1 = px.bar(
                grouped,
                x=cat_cols[0],
                y=numeric_cols[0],
                color=cat_cols[0],
                title="Category Performance"
            )
            st.plotly_chart(fig1, use_container_width=True)

        st.divider()

        # ================= DISTRIBUTION (SAMPLED) =================
        fig2 = px.histogram(
            df_sample,
            x=numeric_cols[0],
            title="Value Distribution (Sampled for Speed)"
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.divider()

        # ================= MACHINE LEARNING (OPTIMIZED) =================
        st.subheader("🤖 AI Prediction")

        target = st.selectbox("Select Target Column", numeric_cols)

        if st.button("Train AI Model"):

            # limit training size
            if len(df) > 10000:
                df_train = df.sample(10000)
            else:
                df_train = df

            X = df_train[numeric_cols].drop(target, axis=1)
            y = df_train[target]

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2
            )

            model = LinearRegression()
            model.fit(X_train, y_train)

            preds = model.predict(X_test)
            score = r2_score(y_test, preds)

            st.success("Model Trained Successfully!")
            st.metric("R² Score", round(score, 2))

        st.divider()

        st.subheader("📄 Data Preview (First 100 Rows)")
        st.dataframe(df.head(100), use_container_width=True)