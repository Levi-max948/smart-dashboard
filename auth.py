import streamlit as st
from database import connect_db

def login_signup():
    st.sidebar.title('Login/Signup')
    choice = st.sidebar.selectbox('Select', ['Login', 'Signup'])

    conn = connect_db()
    cursor = conn.cursor()
    
    if choice == 'Signup':
        name = st.sidebar.text_input('Name')
        email = st.sidebar.text_input('Email')
        password = st.sidebar.text_input('Password', type='password')

        if st.sidebar.button('Create Account'):
            cursor.execute('INSERT INTO user (name, email, password) VALUES (%s, %s, %s)',(name, email, password))
            conn.commit()
            st.success('Account Created!')

    if choice == 'Login':
        email = st.sidebar.text_input('Email')
        password = st.sidebar.text_input('Password', type='password')
        
        if st.sidebar.button('Login'):
            cursor.execute('SELECT * FROM user WHERE email=%s AND password=%s',(email,password))
            user = cursor.fetchone()
            if user:
                st.session_state.logged_in = True
                st.success('Login Successful')
            else:
                st.error('Invalid Credentils')
                           