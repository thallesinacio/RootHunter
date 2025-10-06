# Salve este código como: interface_grafica.py

import customtkinter as ctk
import subprocess
import sys


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Analisador de Métodos Numéricos (Dois Arquivos)")
        self.geometry("950x750")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        frame_entradas = ctk.CTkFrame(self)
        frame_entradas.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        frame_entradas.grid_columnconfigure(1, weight=1)

        # --- WIDGETS ---
        ctk.CTkLabel(frame_entradas, text="Função f(x):").grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0),
                                                               sticky="w")
        self.entry_funcao = ctk.CTkEntry(frame_entradas, placeholder_text="Ex: 80*exp(-2*x) + 20*exp(-0.1*x) - 10")
        self.entry_funcao.grid(row=1, column=0, columnspan=5, padx=10, pady=(0, 10), sticky="ew")

        ctk.CTkLabel(frame_entradas, text="Busca [A, B] e Passo:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_a_macro = ctk.CTkEntry(frame_entradas, placeholder_text="A (macro)")
        self.entry_a_macro.grid(row=2, column=1, padx=(10, 5), pady=5, sticky="ew")
        self.entry_b_macro = ctk.CTkEntry(frame_entradas, placeholder_text="B (macro)")
        self.entry_b_macro.grid(row=2, column=2, padx=(0, 5), pady=5, sticky="ew")
        self.entry_passo = ctk.CTkEntry(frame_entradas, placeholder_text="Passo (ex: 0.1)")
        self.entry_passo.grid(row=2, column=3, padx=(0, 10), pady=5, sticky="ew")
        self.botao_buscar = ctk.CTkButton(frame_entradas, text="1. Buscar Intervalos",
                                          command=self.buscar_intervalos_command)
        self.botao_buscar.grid(row=2, column=4, padx=10, pady=5)

        ctk.CTkLabel(frame_entradas, text="Análise (Intervalo, ε, Max Iter):").grid(row=3, column=0, padx=10, pady=5,
                                                                                    sticky="w")
        self.combo_intervalos = ctk.CTkComboBox(frame_entradas, values=[], state="disabled")
        self.combo_intervalos.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.entry_tol = ctk.CTkEntry(frame_entradas)
        self.entry_tol.insert(0, "0.000001")
        self.entry_tol.grid(row=3, column=2, padx=5, pady=5, sticky="ew")
        self.entry_iter = ctk.CTkEntry(frame_entradas)
        self.entry_iter.insert(0, "100")
        self.entry_iter.grid(row=3, column=3, padx=(0, 10), pady=5, sticky="ew")

        self.botao_analisar = ctk.CTkButton(frame_entradas, text="2. Executar Análise",
                                            command=self.executar_analise_command, font=("", 14, "bold"),
                                            state="disabled")
        self.botao_analisar.grid(row=3, column=4, padx=10, pady=5)

        self.text_resultado = ctk.CTkTextbox(self, font=("Courier New", 13))
        self.text_resultado.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def mostrar_erro(self, mensagem):
        self.text_resultado.delete("1.0", "end")
        self.text_resultado.insert("1.0", f"ERRO:\n\n{mensagem}")

    def buscar_intervalos_command(self):
        self.text_resultado.delete("1.0", "end")
        try:
            comando = [
                sys.executable, "versao_gui/Trabalho_CN_Adaptado.py", "--buscar",
                self.entry_funcao.get(),
                self.entry_a_macro.get(),
                self.entry_b_macro.get(),
                self.entry_passo.get()
            ]
            resultado = subprocess.run(comando, capture_output=True, text=True, check=True, encoding='utf-8')

            intervalos_str = resultado.stdout.strip().split('\n')
            if not intervalos_str or not intervalos_str[0]:
                self.text_resultado.insert("1.0", "Nenhum intervalo com troca de sinal foi encontrado.")
                self.combo_intervalos.configure(values=[], state="disabled")
                self.botao_analisar.configure(state="disabled")
            else:
                self.combo_intervalos.configure(values=intervalos_str, state="normal")
                self.combo_intervalos.set(intervalos_str[0])
                self.botao_analisar.configure(state="normal")
                self.text_resultado.insert("1.0",
                                           "Intervalo(s) encontrado(s).\n\nSelecione um no menu e clique em 'Executar Análise'.")
        except subprocess.CalledProcessError as e:
            self.mostrar_erro(f"Erro ao buscar intervalos:\n{e.stderr}")
        except Exception as e:
            self.mostrar_erro(f"Dados de entrada para busca inválidos. Detalhes: {e}")

    def executar_analise_command(self):
        self.text_resultado.delete("1.0", "end")
        self.text_resultado.insert("1.0", "Executando análise, aguarde...")
        self.update_idletasks()
        try:
            intervalo_selecionado = self.combo_intervalos.get().strip('[] ').replace(' ', '')
            a, b = intervalo_selecionado.split(',')

            comando = [
                sys.executable, "Trabalho_CN_Adaptado.py", "--analisar",
                self.entry_funcao.get(), a, b,
                self.entry_tol.get(), self.entry_iter.get()
            ]
            resultado = subprocess.run(comando, capture_output=True, text=True, check=True, encoding='utf-8')

            # Separa a tabela do log usando o delimitador
            output_completo = resultado.stdout
            separador = "---LOG_DETALHADO---"
            if separador in output_completo:
                tabela, log = output_completo.split(separador)
                texto_final = tabela.strip() + "\n\n" + log.strip()
            else:
                texto_final = output_completo  # Caso algo dê errado, mostra tudo

            self.text_resultado.delete("1.0", "end")
            self.text_resultado.insert("1.0", texto_final)

        except subprocess.CalledProcessError as e:
            self.mostrar_erro(f"Erro na análise:\n{e.stderr}")
        except Exception as e:
            self.mostrar_erro(f"Erro ao preparar análise. Detalhes: {e}")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    app = App()
    app.mainloop()