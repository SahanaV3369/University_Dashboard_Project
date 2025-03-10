import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns

st.title("University Student Dashboard")

# Load the dataset
data = pd.read_csv('data/university_student_dashboard_data.csv')

# Preprocessing data
data['Year-Term'] = data['Year'].astype(str) + ' ' + data['Term']
data['Admission Rate (%)'] = (data['Admitted'] / data['Applications']) * 100
data['Enrollment Rate (%)'] = (data['Enrolled'] / data['Admitted']) * 100

# Sidebar Filters
st.sidebar.header("Filter Options")

# Filter by Term
term = st.sidebar.multiselect("Select Term", data["Term"].unique(), default=data["Term"].unique())

# Filter by Year
year = st.sidebar.multiselect("Select Year", data["Year"].unique(), default=data["Year"].unique())

filtered_data = data[(data["Term"].isin(term)) & (data["Year"].isin(year))]

# Total Applications, Admissions, and Enrollments
st.subheader("Applications, Admissions, and Enrollments")
fig1 = px.line(filtered_data, x="Year-Term", y=["Applications", "Admitted", "Enrolled"], markers=True)
st.plotly_chart(fig1, use_container_width=True)

# Retention Rate Trends
st.subheader("Retention Rate Trends")
fig2 = px.bar(filtered_data, x="Year-Term", y="Retention Rate (%)", color="Retention Rate (%)", text_auto=True, template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)

# Student Satisfaction Scores
st.subheader("Student Satisfaction Scores")
fig3 = px.area(filtered_data, x="Year-Term", y="Student Satisfaction (%)", markers=True, template="plotly_white")
st.plotly_chart(fig3, use_container_width=True)

# Enrollment Breakdown by Department
st.subheader("Enrollment Breakdown by Department")
department_data = filtered_data.melt(id_vars='Year-Term', value_vars=['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled'], 
                                     var_name='Department', value_name='Enrollment')
fig4 = px.bar(department_data, x="Year-Term", y="Enrollment", color="Department", barmode='group')
st.plotly_chart(fig4, use_container_width=True)

# Spring vs Fall term comparison
st.subheader("Spring vs Fall Enrollment Comparison")
sf_fig = px.line(filtered_data, x="Year", y="Enrolled", color="Term", markers=True, template="seaborn")
st.plotly_chart(sf_fig, use_container_width=True)

# Retention vs Satisfaction
st.subheader("Retention Rate vs Student Satisfaction")
fig5 = px.scatter(filtered_data, x='Retention Rate (%)', y='Student Satisfaction (%)', color='Term', size='Enrolled', template='ggplot2')
st.plotly_chart(fig5, use_container_width=True)

# Downloadable Data
with st.expander("Download Filtered Data"):
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data as CSV", data=csv, file_name="filtered_university_data.csv", mime='text/csv')
