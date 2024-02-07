from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Scrollbar

import src.semantic.analizador_semantico as asm

class Compilador():
    def __init__(self):
        self.isAnalyzed = False
        
        # Variables
        self.analysis = []
        self.program = []
        self.tokens = []
        self.result = []
        
        self.sub_tokens = None
        self.sub_symbols = None
        self.sub_errors = None
        
        #ventana
        self.root = Tk()
        self.root.geometry("900x720+400+50")
        self.root.title("TAS")
        self.root.config(bg="#34495E")
        self.root.resizable(False, False)

        # Componentes interfaz
        self.frame = Frame(self.root, background="#99A3A4", relief=SUNKEN, padx=2, pady=2)
        self.frame.pack(padx=10, pady=10)


        open_button = Button(self.frame, text="Abrir Gramática", background="#C0EFD2", command=lambda:self.open_file(self.grammar_entry))
        open_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.grammar_entry = Entry(self.frame, width=30)
        self.grammar_entry.grid(row=0, column=1, padx=10, pady=10)
        self.grammar_entry.insert(0, "")
        self.grammar_entry.config(state="readonly")

        open_button_tokens = Button(self.frame, text="Abrir Programa", background="#C0EFD2", command=lambda:self.open_file(self.tokens_entry))
        open_button_tokens.grid(row=1, column=0, padx=10, pady=10)
        
        self.tokens_entry = Entry(self.frame, width=30)
        self.tokens_entry.grid(row=1, column=1, padx=10, pady=10)
        self.tokens_entry.insert(0, "")
        self.tokens_entry.config(state="readonly")
        
        
        open_button_action = Button(self.frame, text="Abrir Acción", background="#C0EFD2", command=lambda:self.open_file(self.action_entry))
        open_button_action.grid(row=2, column=0, padx=10, pady=10)
        
        self.action_entry = Entry(self.frame, width=30)
        self.action_entry.grid(row=2, column=1, padx=10, pady=10)
        self.action_entry.insert(0, "")
        self.action_entry.config(state="readonly")
        
        self.analyze_button = Button(self.frame, text="Analizar", background="#C0EFD2", command=self.analyze)
        self.analyze_button.grid(row=3, column=0, padx=20, pady=20)
        
        clear_button = Button(self.frame, text="LimpiarTodo", background="#C0EFD2", command=self.clear)
        clear_button.grid(row=3, column=1, padx=20, pady=20)


        self.frame_show = Frame(self.root, background="#99A3A4", relief=FLAT, padx=20, pady=20)
        self.frame_show.pack(padx=20, pady=self.frame.winfo_reqheight()+1)

        
        self.canvas = Canvas(self.frame_show,width=600, height=350)
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)

        self.table_frame = Frame(self.canvas, bg="#CACFD2")
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        self.scrollbar_vertical = Scrollbar(self.frame_show, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar_vertical.pack(side=RIGHT, fill=Y)
        
        self.scrollbar_horizontal = Scrollbar(self.frame_show, orient=HORIZONTAL, command=self.canvas.xview)
        self.scrollbar_horizontal.pack(side=BOTTOM, fill="x")
    
    def open_file(self, entry_widget):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])

        if len(file_path) > 0:
            entry_widget.config(state="normal")
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file_path)
            entry_widget.config(state="readonly")
            messagebox.showinfo("Analizador Sintactico", "Archivo seleccionado correctamente")
        else:
            messagebox.showerror("Analizador Sintactico", "No se ha seleccionado un archivo!")

    def clear_gram(self):
    # Destruir y reconstruir el marco para la tabla
        if hasattr(self, 'table_frame'):
            self.table_frame.destroy()  # Destruir el marco existente

        self.table_frame = Frame(self.canvas, bg="#CACFD2")  # Crear un nuevo marco
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

    
    def clear(self):
        self.file_path = ""
        self.grammar_entry.config(state="normal")
        self.grammar_entry.delete(0, END)
        self.grammar_entry.config(state="readonly")
        
        self.tokens_entry.config(state="normal")
        self.tokens_entry.delete(0, END)
        self.tokens_entry.config(state="readonly")
        
        self.action_entry.config(state="normal")
        self.action_entry.delete(0, END)
        self.action_entry.config(state="readonly")
        
        # Variables
        self.analysis = []
        self.program = []
        self.tokens = []
        self.result = []
        
        
        # Reiniciar variables de estado
        self.isAnalyzed = False

        # Limpiar la tabla y la interfaz
        self.clear_gram()

    def analyze(self):
        if not self.isAnalyzed:
            resultado = asm.to_analyze(self.grammar_entry.get(), self.tokens_entry.get())
            print(resultado)
            
    def show_tokens(self):
        sub = Toplevel(self.root)
        sub.title("Tira De Tokens")
        sub.geometry("+100+50")
        table = ttk.Treeview(sub, columns=("# Linea", "Lexema", "Token"), show="headings")
        
        # Configuracion de las cabeceras
        table.heading("# Linea", text="# Linea")
        table.heading("Lexema", text="Lexema")
        table.heading("Token", text="Token")
        # Configuracion de las columnas
        table.column("# Linea", width=100, anchor="center")
        table.column("Lexema", width=100, anchor="center")
        table.column("Token", width=100, anchor="center")
        
        for elemento in al.Application.total:
            partes= elemento.split(',')
            if len(partes) >= 3:
                linea = partes[0].strip()
                lexema = partes[1].strip()
                token = partes[2].strip()
                # Insertar los valores en la tabla
                table.insert("", END, values=(linea, lexema, token))
        table.pack()
        
    def show_symbols(self):

        if self.sub_symbols is None or not self.sub_symbols.winfo_exists():
            sub = Toplevel(self.root)
            sub.title("Tira De Simbolos")
            sub.geometry("+100+400")
            table = ttk.Treeview(sub, columns=("ID", "Valor", "Funcion"), show="headings")
            # Configuracion de las cabeceras
            table.heading("ID", text="ID")
            table.heading("Valor", text="Valor")
            table.heading("Funcion", text="Funcion")
            # Configuracion de las columnas
            table.column("ID", width=100, anchor="center")
            table.column("Valor", width=100, anchor="center")
            table.column("Funcion", width=100, anchor="center")
            for elemento in al.Application.conjunto_sin_duplicados:
                table.insert("", END, values=elemento)
            table.pack()

    def show_errors(self):
        if self.sub_errors is None or not self.sub_errors.winfo_exists():
            sub = Toplevel(self.root)
            sub.title("Tira De Errores")
            sub.geometry("+1150+50")
            table = ttk.Treeview(sub, columns=("# Linea", "Valor", "Funcion"), show="headings")
            # Configuracion de las cabeceras
            table.heading("# Linea", text="# Linea")
            table.heading("Valor", text="Valor")
            table.heading("Funcion", text="Funcion")
            # Configuracion de las columnas
            table.column("# Linea", width=100, anchor="center")
            table.column("Valor", width=100, anchor="center")
            table.column("Funcion", width=100, anchor="center")
            
            for elemento in al.Application.errores:
                table.insert("", END, values=elemento)
            table.pack()
    
    def analizarLR(self):
        grammar_path = self.grammar_entry.get()
        tokens_path = self.tokens_entry.get()
        action_path = self.action_entry.get()
        font_style = ("Arial", 10, "bold")
        
        if grammar_path and tokens_path:
            analysis, program, tokens = lr.to_analyze(grammar_path, tokens_path, action_path)

            label = Label(self.table_frame,text=f"Programa : {program}",borderwidth=2,relief="solid",background="#16C4DF")
            label.grid(row=0, column=0, padx=2, pady=2)
            
            label = Label(self.table_frame,text=f"Tokens : {tokens}",borderwidth=2,relief="solid",background="#16C4DF")
            label.grid(row=1, column=0, padx=2, pady=2)

            label = Label(self.table_frame,text=" Pila ",borderwidth=1,width=35,relief="solid",background="#A43371", foreground="black", font=font_style)
            label.grid(row=2, column=0, padx=2, pady=2)
            label = Label(self.table_frame,text=" Entrada ",borderwidth=1,width=35,relief="solid",background="#A43371",  foreground="black", font=font_style)
            label.grid(row=2, column=1, padx=2, pady=2)
            label = Label(self.table_frame,text=" Accion ",borderwidth=1,width=35,relief="solid",background="#A43371", foreground="black", font=font_style)
            label.grid(row=2, column=2, padx=2, pady=2)
            
            self.result = ""
                
            for i in range(len(analysis)):
                for j in range(len(analysis[i])):
                    self.result+=f"{analysis[i][j]}|"
                self.result+=('\n\n|')
            
            header_columns = self.result.strip().split('|') 
            
            current_row = 4  # Comenzar desde la segunda fila
            current_col = 0 
        
            for j,header_text in enumerate(header_columns):
                if "\n\n" not in header_text:
                    rango = len(header_columns)
                    if j<rango-1:
                        label = Label(
                        self.table_frame,
                        text=header_text,
                        borderwidth=1,
                        width=35,
                        relief="solid",
                        background="#16DFAE",  # Color de fondo
                        foreground="black",       # Color de primer plano
                        font=font_style
                        )
                        label.grid(row=current_row, column=current_col, padx=2, pady=2)
                        current_col +=1
                else:
                    current_row +=1
                    current_col=0
                    
if __name__ == "__main__":
    app = Compilador()
    app.root.mainloop()

    #path = "gramatica2.txt"
    #program = "program.txt"
    #never = asm.to_analyze(path, program)

    #for elem in never:
    #    print(elem)