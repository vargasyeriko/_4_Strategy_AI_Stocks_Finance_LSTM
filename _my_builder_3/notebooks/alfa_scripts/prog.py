# START

# 0 # ASK 
#exec(open(f"_i_ask.py",encoding="utf-8").read()) 
if __name__ == "__main__":
    try:
        # Execute _run_11.py in its own namespace
        exec(open("_ask.py").read(), {})
    except Exception as e:
        # Print error messages
        print("Error in _ask.py:", e)
        
# 1 # UPTD
if __name__ == "__main__":
    try:
        # Execute _run_11.py in its own namespace
        exec(open("_11_updt.py").read(), {})
    except Exception as e:
        # Print error messages
        print("Error in _11_updt.py:", e)

# 2 # TBLS

exec(open(f"_22_tbls.py",encoding="utf-8").read())

# if __name__ == "__main__":
#     try:
#         # Execute _run_11.py in its own namespace
#         exec(open("_22_tbls.py").read(), {})
#     except Exception as e:
#         # Print error messages
#         print("Error in _22_tbls.py:", e)


#  #1_2 # GRAPHS PDFS and TABLE FUNCTION FOR NEXT 
main_menu()