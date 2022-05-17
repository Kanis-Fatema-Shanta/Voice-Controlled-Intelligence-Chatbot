import sys
from cx_Freeze import setup, Executable

setup(
    name = "Intelligent Chatbot",
    version = "0.1",
    description = "",
    executables = [Executable("chatbot2.py", base = "Win32GUI")])
