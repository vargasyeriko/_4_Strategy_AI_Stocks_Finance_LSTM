# Finance Program
exec(open(f"_0_fn_graphs/_Pie_Chart_Percentage_Breakdown_.py",encoding="utf-8").read())
from _fns_pdf import pdf_pie_all

# Display the program introduction and instructions with ASCII art for "Finance PRO"
dinero = r"""
⠀⠀⠀⠀⠀⠀⠀ ⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡤⡄⠒⠊⠉⢀⣀⢨⠷⡄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⡇⠈⢹⣩⢟⣜⣐⡵⡿⢇⠀⠀⠀⠀⠀⠀
⠀⠀⡠⠖⠊⠉⠀⠀⠈⠻⢅⠀⠀⠀⠀⠀⠈⠒⠠⢀⠀⠀
⠀⡜⠁⠀⠀⠀⠀⠀⠀⠀⠀⠙⠢⣄⠀⠀⠀⠀⣀⣀⣼⠂
⢰⠃⠀⠀⠀⡀⡀⠀⠀⠀⠀⠀⠀⠈⢷⡲⡺⣩⡤⢊⠌⡇
⠸⡆⠀⠀⡞⠀⡇⠀⢰⣓⢢⣄⠀⠀⢸⣞⡞⢉⠔⡡⢊⣷
⠀⢣⠀⠀⠹⡄⡇⠀⢸⣂⡡⢖⠳⣄⢸⢋⠔⡡⢊⣰⠠⠋
⠀⠀⢣⡀⠀⠈⠁⠀⠸⣗⠾⣙⣭⡾⢿⡶⢏⠁⠀⠀⠀⠀
⠀⠀⠀⠳⡀⠀⠀⠀⠀⠻⣽⠊⣡⠞⢉⢔⠝⣑⢄⠀⠀⠀
⠀⠀⠀⢀⣹⣆⠀⠀⠀⠀⠈⠳⣤⢊⠔⡡⠊⢁⡤⠓⠄⠀
⠀⡶⡿⣋⣵⢟⣧⠀⠀⠀⠀⠀⠈⢧⡊⣀⠔⡩⠐⣀⠙⡄
⠸⡇⢹⣋⠕⡫⠘⡇⠀⣄⠀⠀⠀⠀⢻⡕⢁⠤⠊⢁⡀⡇
⠀⡇⠀⠳⣵⢊⢽⡇⠀⡏⢳⡀⠀⠀⠀⣟⣡⠴⠚⡉⠠⡇
⠀⠘⢆⡀⠈⠉⠉⠀⠀⣧⣼⡗⠀⠀⠀⣹⠐⣈⠠⠤⣰⠀
⠀⠀⠀⠙⠦⡀⠀⠀⠀⠉⠉⠀⠀⠀⢀⡯⠥⣒⣂⡱⠃⠀
⠀⠀⠀⠀⠀⠈⢧⠀⠀⠀⠀⠀⠀⢀⣞⣉⠭⠴⠋⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⡆⠀⡶⣶⠶⠒⠉⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀ ⠈⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""

print('\t\t\t\t\t\t',dinero)
print("Welcome to the Enhanced Finance PRO Program!\n")
print("Dive into a world of financial data ")
print("✓ Dynamic Data Management")
print("✓ Time Travel Retrieval:.")
print("✓ Sleek User Interface: ")
print("✓ Adaptive Operations: ")

def main_menu():
    while True:
        print("\n*\n*\nPlease select what you would like to see:\n")
        #print("(1) REPORT")
        #print("(2) EXPORT REPORT")
        #print("(2) EXPORT REPORT")
        #print("(3) EXPORT GRAPH")
        print("(5) Pie Chart Percentage Breakdown ")

        print("(4) EXIT")
        try:
            choice = int(input("\nEnter your choice (1/2/3/4): "))
            if choice == 1:
                print(report_p1)
            elif choice == 2:
                c.save()
                print("PDF generated:", pdf_filename)
            elif choice == 3:
                plt.savefig(f'_returns_graph.png', dpi=300)
                print('_returns_graph.png EXPORTED\n')
            elif choice == 4:
                print("Exiting the main menu...")
                break  # Breaks the loop, effectively exiting the main menu
            elif choice == 5:
                _g1_perc_pie_both(df_final)
                pdf_pie_all()
                break  # Breaks the loop, effectively exiting the main menu
            else:
                print("Invalid choice, please select 1, 2, 3, or 4.")
        except ValueError:
            print("Please enter a valid number.")


exec(open(f"prog.py",encoding="utf-8").read()) 
