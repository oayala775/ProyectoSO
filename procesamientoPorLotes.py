import ttkbootstrap as ttk
import tkinter as tk
# from tkinter import ttk
from procesos import Process
from tkinter.scrolledtext import ScrolledText
import random as rd
import msvcrt as ms
import keyboard as kb

id_collection = []
batch_collection = []
aux_collection = []
process_count = 0
global_counter = 0
batch_counter = 0
finished_process_list = []
process_captured = 0
amount_of_processes = 0
is_captured = False
is_paused = False
process_to_show = 0
error = False
is_interrupted = False

def assignation():
    global amount_of_processes
    
    window = ttk.Window()
    window.title('Procesamiento por lotes')
    window.state('zoomed')

    # Title
    title_label = ttk.Label(master=window, text="Procesamiento por lotes",font="Calibri 24 bold")
    title_label.pack(pady=20)
    
    amount_of_processes_label = ttk.Label(master = window, text="Procesos a capturar", font='Arial 13')
    amount_of_processes_text = ttk.Entry(master = window, textvariable=amount_of_processes)
    amount_of_processes_send = ttk.Button(master = window, command = lambda: verifications(window, amount_of_processes_text,amount_of_processes_label, amount_of_processes_send,title_label), text="OK")
    amount_of_processes_label.pack(pady=5)
    amount_of_processes_text.pack(pady=3)
    amount_of_processes_send.pack(pady=10)
    
    
    window.mainloop()

def verifications(window,amount_of_processes_text,amount_of_processes_label, amount_of_processes_send,title_label):
    global aux_collection
    global batch_collection
    global batch_counter
    global process_count
    
    amount_of_processes = amount_of_processes_text.get()
    amount_of_processes = int(amount_of_processes)
    i = 0
    
    while i < amount_of_processes:
        ID = i
        first_data = rd.randint(0,10000)
        second_data = rd.randint(0,10000)
        estimated_time = rd.randint(6,18)
        if second_data == 0:
            operation_list = ['+','-','*']
        else:
            operation_list = ['+','-','*','/','%']
        operation = rd.choices(operation_list)
        operation = operation[0]
        
        process = Process(operation,first_data,second_data,estimated_time,ID,batch_counter)
        aux_collection.append(process)
        
        process_count += 1
        
        if process_count%5 == 0:
            batch_counter += 1
            batch_collection.append(aux_collection.copy())
            for j in range(5):
                aux_collection.pop()
        
        i += 1
        
    if process_count % 5 != 0:
        batch_counter += 1
        batch_collection.append(aux_collection.copy())
            
    amount_of_processes_label.pack_forget()
    amount_of_processes_send.pack_forget()
    amount_of_processes_text.pack_forget()
    title_label.pack_forget()
    
    
    secondScreen(window)
    
        
def secondScreen(window):
    # Window setup
    global batch_collection
    global id_collection
    global process_count
    global aux_collection
    global global_counter
    global process_to_show
    
    window.title('Procesamiento por lotes')
    window.state('zoomed')
    window.columnconfigure((0,1,2,3,4,5), weight = 1)
    window.rowconfigure((0,1,2,3,4,5,6), weight = 1)

    # Title
    title_label = ttk.Label(master=window, text="Procesamiento por lotes",font="Calibri 24 bold")
    title_label.grid(row = 0, column = 0, columnspan = 5, pady = 8, padx= 8)
    
    batch_pendient_title = ttk.Label(master=window, text=f"Lotes pendientes: {len(batch_collection)-1}", font="Arial 13")
    batch_pendient_title.grid(row = 1, column = 0, pady = 5, padx = 5)
    
    global_counter_container = ttk.Label(master=window, text=f"Contador global: {global_counter}", font="Arial 13")
    global_counter_container.grid(row = 1, column = 2, pady = 5, padx = 5)
    
    batches_label = ttk.Label(window, text = "Lote en ejecución.", font = "Arial 13")
    batches_label.grid(row = 2, column = 0, sticky='s')
    batches = tk.Text(master=window)
    batches.grid(row = 3, column = 0, rowspan = 2, padx = 5)
    
    executing_process_label = ttk.Label(window, text = "Proceso en ejecución.", font = "Arial 13")
    executing_process_label.grid(row = 2, column = 1, sticky='s')
    executing_process = tk.Text(master = window)
    executing_process.grid(row = 3, column = 1, rowspan = 2, padx = 5)
    
    finished_process_label = ttk.Label(window, text = "Procesos terminados", font = "Arial 13")
    finished_process_label.grid(row = 2, column = 2, sticky='s')
    finished_process = tk.scrolledtext.ScrolledText(master = window,wrap=tk.WORD)
    finished_process.grid(row = 3, column = 2, rowspan = 2, padx = 5)
    
    start_simulation = ttk.Button(master = window, text="Enviar proceso")
    
    process_to_show = batch_collection[0].pop(0)
    batches_counter = len(batch_collection)-1
    if len(batch_collection[0]) != 0:
        for process in batch_collection[0]:
            batches.insert("end","ID: " + str(process.id) + "\nTiempo máximo estimado: " + str(process.estimated_time) + "\n")
            
    executing_process.insert("end",process_to_show)
    
    TTE = 0
    TRE = process_to_show.estimated_time
    
    counter(window, TTE, TRE, global_counter, global_counter_container,executing_process,batches,batch_pendient_title,batches_counter,finished_process, finished_process_list)
    
    
def counter(window, TTE, TRE, global_counter, global_counter_container,executing_process,batches,batch_pendient_title,batches_counter,finished_process,finished_process_list):
    
    global batch_counter
    global is_paused
    global process_to_show
    global error
    global batch_collection
    global is_interrupted
    
    executing_process.after(1000,lambda: counter(window, TTE, TRE, global_counter, global_counter_container,executing_process,batches,batch_pendient_title,batches_counter,finished_process,finished_process_list))
    
    executing_process.delete('1.0',"end")
    
    window.bind('<KeyRelease>',on_key_release)
        
    if not is_paused:
        if is_interrupted:
            batch_collection[0].insert(4,process_to_show)
            process_to_show = batch_collection[0].pop(0)
            is_interrupted = False
            batches.delete('1.0',"end")
            for process in batch_collection[0]:
                batches.insert("end","ID: " + str(process.id) + "\nTiempo máximo estimado: " + str(process.estimated_time) + "\n")
        elif process_to_show.TRE != 0 and not is_interrupted:                                # Llega cuando se termina la cuenta
            process_to_show.TRE -= 1
            process_to_show.TTE += 1
            global_counter += 1
            global_counter_container.config(text=f"Contador global: {global_counter}")
            executing_process.insert("end",process_to_show)
            
        elif len(batch_collection[0]) != 0:         # Sucede cada vez que la longitud de la lista interna es mayor a cero, es decir la lista no está vacía
            if process_to_show not in finished_process_list:
                finished_process_list.append(process_to_show)
            process_to_show = batch_collection[0].pop(0)
            batches.delete('1.0',"end")
            
            for process in batch_collection[0]:
                batches.insert("end","ID: " + str(process.id) + "\nTiempo máximo estimado: " + str(process.estimated_time) + "\n")
            executing_process.insert("end",process_to_show)
            TTE = 0
            TRE = process_to_show.estimated_time
            
            if batches_counter >= 0:
                batch_pendient_title.config(text=f"Lotes pendientes: {batches_counter}")
                finished_process.delete('1.0',"end")
                for finished in finished_process_list:
                    if not finished.error: 
                        finished_process.insert("end", f"LOTE: {str(finished.belonging_batch)}\n" + "ID: " + str(finished.id) + "\nOperación: " + str(finished.first_data) + finished.operation + str(finished.second_data) + "\nResultado: " + str(finished.operate(error=False)) + "\n\n")
                    else:
                        finished_process.insert("end", f"LOTE: {str(finished.belonging_batch)}\n" + "ID: " + str(finished.id) + "\nOperación: " + str(finished.first_data) + finished.operation + str(finished.second_data) + "\nResultado: " + str(finished.operate(error=True)) + "\n\n")

        else:                                   # Cambio de lote
            if batches_counter >= 0:
                if process_to_show not in finished_process_list:
                    finished_process_list.append(process_to_show)
                
                if(len(batch_collection) != 1):
                    batch_collection[0] = batch_collection[1]
                    batch_counter += 1
                    batches_counter -= 1
                    batch_collection.remove(batch_collection[1])   
                
                finished_process.delete('1.0',"end")
                for finished in finished_process_list:
                    if not finished.error: 
                        finished_process.insert("end", f"LOTE: {str(finished.belonging_batch)}\n" + "ID: " + str(finished.id) + "\nOperación: " + str(finished.first_data) + finished.operation + str(finished.second_data) + "\nResultado: " + str(finished.operate(error=False)) + "\n\n")
                    else:
                        finished_process.insert("end", f"LOTE: {str(finished.belonging_batch)}\n" + "ID: " + str(finished.id) + "\nOperación: " + str(finished.first_data) + finished.operation + str(finished.second_data) + "\nResultado: " + str(finished.operate(error=True)) + "\n\n")
            else:
                window.after_cancel(executing_process)
                finished_process.configure(state="disabled")
                executing_process.configure(state="disabled")
                batches.configure(state="disabled")
    else:
        executing_process.insert("end",process_to_show)

def on_key_release(event):
    global is_paused
    global process_to_show
    global error
    global batch_collection
    global is_interrupted
    
    if event.keysym == 'p' and not is_paused:
        is_paused = True
        print("paused")
    elif event.keysym == 'c':
        is_paused = False
        print("unpaused")
    elif event.keysym == 'e' and not is_paused:
        process_to_show.TRE = 0
        process_to_show.error = True
        print("error")
    elif event.keysym == 'i' and not is_paused:
        is_interrupted = True
        print("interruption")
    

assignation()