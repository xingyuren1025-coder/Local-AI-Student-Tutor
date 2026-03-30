import streamlit as st


def admin_login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    with st.sidebar:
        st.markdown("---")
        if not st.session_state.authenticated:
            st.subheader("🔑 Admin Access")
            pwd = st.text_input("Enter Password", type="password")
            if st.button("Login"):
                if pwd == "admin123":  # Default password 默认密码
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid Password")
        else:
            st.success("Logged in as Admin")
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.rerun()

    return st.session_state.authenticated
