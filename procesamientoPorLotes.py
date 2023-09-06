import ttkbootstrap as ttk
import tkinter as tk
# from tkinter import ttk
from procesos import Process
from tkinter.scrolledtext import ScrolledText

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
    amount_of_processes_send = ttk.Button(master = window, command = lambda: firstScreen(window, amount_of_processes_label, amount_of_processes_text, amount_of_processes_send,title_label), text="OK")
    amount_of_processes_label.pack(pady=5)
    amount_of_processes_text.pack(pady=3)
    amount_of_processes_send.pack(pady=10)
    
    window.mainloop()
    

def firstScreen(window,amount_of_processes_label, amount_of_processes_text, amount_of_processes_send,title_label):
    global id_collection
    global batch_collection
    global aux_collection
    global process_count 
    global process_captured
    global amount_of_processes
    global is_captured
    
    amount_of_processes = amount_of_processes_text.get()
    amount_of_processes = int(amount_of_processes)
    
    amount_of_processes_label.pack_forget()
    amount_of_processes_text.pack_forget()
    amount_of_processes_send.pack_forget()
    
    window.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16),weight = 0)
    window.columnconfigure(0, weight= 0)
    window.columnconfigure(1, weight= 3)
    window.columnconfigure(2, weight= 1)
    
    title_label.grid(row = 0, column = 0, columnspan = 3, pady = 20)
    
    # Window setup
    process_captured_label = ttk.Label(window, text=f"Procesos capturados: {process_captured}", font="Arial 13")
    process_captured_label.grid(row = 1, column=0,pady=20,padx = 15)
    name_data = tk.StringVar()
    name_label = ttk.Label(master = window, text='Nombre del programador', font = "Arial 13")
    name_label.grid(row = 1, column = 1, pady = 5, sticky='s')
    name_text = ttk.Entry(master = window, textvariable = name_data)
    name_text.grid(row = 2, column = 1, pady = 5)

    operation_title = ttk.Label(master = window, text='Operación a realizar', font="Arial 13")
    operation_title.grid(row = 3, column = 1, pady = 5)

    first_data = tk.IntVar()
    first_data_label = ttk.Label(master = window, text = "Primer dato")
    first_data_label.grid(row = 4, column = 1, pady = 5, sticky='s')
    first_data_text = ttk.Entry(master = window, textvariable = first_data)
    first_data_text.grid(row = 5, column = 1, pady = 5)

    operation_data = tk.StringVar()
    operation_label = ttk.Label(master = window, text = "Operación")
    operation_label.grid(row = 6, column = 1, pady = 5, sticky='s')
    operation_text = ttk.Entry(master = window, textvariable = operation_data)
    operation_text.grid(row = 7, column = 1, pady = 5)
    
    second_data = tk.IntVar()
    second_data_label = ttk.Label(master = window, text = "Segundo dato")
    second_data_label.grid(row = 8, column = 1, pady = 5, sticky='s')
    second_data_text = ttk.Entry(master = window, textvariable = second_data)
    second_data_text.grid(row = 9, column = 1, pady = 5)

    estimated_time_variable = tk.IntVar()
    estimated_time_label = ttk.Label(master = window, text='Tiempo estimado', font = "Arial 13")
    estimated_time_label.grid(row = 10, column = 1, pady = 5, sticky='s')
    estimated_time_text = ttk.Entry(master = window,textvariable=estimated_time_variable)
    estimated_time_text.grid(row = 11, column = 1, pady = 5)

    ID_data = tk.IntVar()
    ID_label = ttk.Label(master = window, text='Número de programa', font = "Arial 13")
    ID_label.grid(row = 12, column = 1, pady = 5, sticky='s')
    ID_text = ttk.Entry(master = window, textvariable = ID_data)
    ID_text.grid(row = 13, column = 1, pady = 5)
    
    send_button = ttk.Button(master = window, text="Enviar proceso", command = lambda: verifications(estimated_time_text,first_data_text,second_data_text,ID_text,operation_text,name_text,window,process_captured_label,send_button), style="success")
    send_button.grid(row = 14, column = 1, pady = 5)
    
    # if is_captured == True:
    #     destroyFirstScreen(window)
    #     secondScreen()

def verifications(estimated_time_text,first_data_text,second_data_text,ID_text,operation_text,name_text,window,process_captured_label,send_button):
    global process_count
    global id_collection
    global batch_collection
    global aux_collection
    global batch_counter
    global process_captured
    
    estimated_time_variable = estimated_time_text.get()
    estimated_time_variable = int(estimated_time_variable)

    first_data = first_data_text.get()
    first_data = int(first_data)
    
    second_data = second_data_text.get()
    second_data = int(second_data)
    
    ID_data = ID_text.get()
    ID_data = int(ID_data)
    
    operation_data = str(operation_text.get())
    name_data = str(name_text.get())
    
    state_label = ttk.Label(master = window)
    
    is_correct = True
    if process_captured <= amount_of_processes -1:
        if estimated_time_variable <= 0:
            is_correct = False
            state_label['text'] = "El tiempo tiene que ser mayor a 0"   
        elif operation_data == "/" or operation_data == "%":
            if second_data == 0:
                is_correct = False
                state_label['text'] = "No se puede dividir entre 0"
        
        for i in range(len(id_collection)):
            if ID_data == id_collection[i]:
                is_correct = False
                state_label['text'] = "El ID está repetido"
        
        if is_correct == True:
            state_label.configure(background = "#19FF40", font = "Calibri 15", foreground="black")
            state_label['text'] = "Datos correctamente capturados"
            id_collection.append(ID_data)
            process_captured += 1
            process_captured_label.grid_forget()
            process_captured_label = ttk.Label(window, text=f"Procesos capturados: {process_captured}", font="Arial 13").grid(row = 1, column=0,pady=20,padx = 15)
            process = Process(name_data, operation_data, first_data, second_data, estimated_time_variable, ID_data,batch_counter)
            aux_collection.append(process)
            process_count += 1
        else:
            state_label.configure(background = "#FF5533", font = "Calibri 15", foreground="white") 
        
        if process_count%5 == 0 and is_correct == True:
            batch_counter += 1
            batch_collection.append(aux_collection.copy())
            for i in range(5):
                aux_collection.pop()
            state_label.configure(background = "#e6e600", font = "Calibri 15", foreground="black")
            state_label['text'] = "Lote completado"
            
        state_label.grid(row = 16, column = 1, pady = 50)
        state_label.after(2000,state_label.grid_forget)
        
        if process_captured == amount_of_processes:
            state_label['text'] = 'Último proceso capturado, presione terminar'
            state_label.configure(background = "#FF5533", font = "Calibri 15", foreground="white")
            state_label.grid(row = 16, column = 1, pady = 50)
            send_button.configure(text='Terminar',bootstyle="danger")
            state_label.after(2000,state_label.grid_forget)
    else: 
        destroyFirstScreen(window)
        secondScreen()
    
def destroyFirstScreen(window):
    global aux_collection
    
    if process_count % 5 != 0:
        batch_collection.append(aux_collection.copy())
    
    window.destroy()
        
def secondScreen():
    # Window setup
    global batch_collection
    global id_collection
    global process_count
    global aux_collection
    global global_counter
    global window2
    
    # window2 = tk.Tk()
    window2 = ttk.Window()
    
    window2.title('Procesamiento por lotes')
    window2.state('zoomed')
    window2.columnconfigure((0,1,2,3,4,5), weight = 1)
    window2.rowconfigure((0,1,2,3,4,5,6), weight = 1)

    # Title
    title_label = ttk.Label(master=window2, text="Procesamiento por lotes",font="Calibri 24 bold")
    title_label.grid(row = 0, column = 0, columnspan = 5, pady = 8, padx= 8)
    
    batch_pendient_title = ttk.Label(master=window2, text=f"Lotes pendientes: {len(batch_collection)-1}", font="Arial 13")
    batch_pendient_title.grid(row = 1, column = 0, pady = 5, padx = 5)
    
    global_counter_container = ttk.Label(master=window2, text=f"Contador global: {global_counter}", font="Arial 13")
    global_counter_container.grid(row = 1, column = 2, pady = 5, padx = 5)
    
    batches_label = ttk.Label(window2, text = "Lote en ejecución.", font = "Arial 13")
    batches_label.grid(row = 2, column = 0, sticky='s')
    batches = tk.Text(master=window2)
    batches.grid(row = 3, column = 0, rowspan = 2, padx = 5)
    
    executing_process_label = ttk.Label(window2, text = "Proceso en ejecución.", font = "Arial 13")
    executing_process_label.grid(row = 2, column = 1, sticky='s')
    executing_process = tk.Text(master = window2)
    executing_process.grid(row = 3, column = 1, rowspan = 2, padx = 5)
    
    finished_process_label = ttk.Label(window2, text = "Procesos terminados", font = "Arial 13")
    finished_process_label.grid(row = 2, column = 2, sticky='s')
    finished_process = tk.scrolledtext.ScrolledText(master = window2,wrap=tk.WORD)
    finished_process.grid(row = 3, column = 2, rowspan = 2, padx = 5)
    
    start_simulation = ttk.Button(master = window2, text="Enviar proceso")
    
    process_to_show = batch_collection[0].pop(0)
    batches_counter = len(batch_collection)-1
    if len(batch_collection[0]) != 0:
        for process in batch_collection[0]:
            batches.insert("end","ID: " + str(process.id) + "\nTiempo máximo estimado: " + str(process.estimated_time) + "\n")
            
    executing_process.insert("end",process_to_show)
    
    TTE = 0
    TRE = process_to_show.estimated_time
    
    counter(process_to_show, TTE, TRE, global_counter, global_counter_container,executing_process,batches,batch_pendient_title,batch_collection,batches_counter,finished_process, finished_process_list)
    
    window2.mainloop()
    
def counter(process_to_show, TTE, TRE, global_counter, global_counter_container,executing_process,batches,batch_pendient_title,batch_collection,batches_counter,finished_process,finished_process_list):
    
    global batch_counter
    
    executing_process.after(1000,lambda: counter(process_to_show, TTE, TRE, global_counter, global_counter_container,executing_process,batches,batch_pendient_title,batch_collection,batches_counter,finished_process,finished_process_list))
    
    executing_process.delete('1.0',"end")
    
    if process_to_show.TRE != 0:                                # Llega cuando se termina la cuenta
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
                finished_process.insert("end", f"LOTE: {str(finished.belonging_batch)}\n" + "ID: " + str(finished.id) + "\nOperación: " + str(finished.first_data) + finished.operation + str(finished.second_data) + "\nResultado: " + str(finished.operate()) + "\n")

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
                finished_process.insert("end", f"LOTE: {str(finished.belonging_batch)}\n" + "ID: " + str(finished.id) + "\nOperación: " + str(finished.first_data) + finished.operation + str(finished.second_data) + "\nResultado: " + str(finished.operate()) + "\n\n")
        else:
            window2.after_cancel(executing_process)
            finished_process.configure(state="disabled")
            executing_process.configure(state="disabled")
            batches.configure(state="disabled")
assignation()
# firstScreen()
# secondScreen()
######################################################################### First screen #########################################################


########################################################################## Second screen #################################################################





