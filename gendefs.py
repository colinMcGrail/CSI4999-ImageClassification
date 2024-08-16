import streamlit as st
import sqlite3

ROLES = [None, "Patient", "Doctor", "Specialist"]

def makeconnection():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    return con, cur
