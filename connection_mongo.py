import streamlit as st
import time
from pymongo import MongoClient

# ---------------------------
# CONEXÃO COM O MONGODB ATLAS
# ---------------------------

MONGO_URI = "mongodb+srv://gustavomarco_db_user:labbd123@lab-bd.50wjwhy.mongodb.net/?appName=lab-bd"

client = MongoClient(MONGO_URI)
# Banco para currículos
db_curriculos = client["curriculos"]
curriculos = db_curriculos["curriculos"]

# Banco para vagas
db_vagas = client["vagas"]
vagas = db_vagas["vagas"]