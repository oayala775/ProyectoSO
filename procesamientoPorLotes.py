import ttkbootstrap as ttk
import tkinter as tk
# from tkinter import ttk
from procesos import Process
from ttkbootstrap.scrolled import ScrolledText
import random as rd

ready_list = []
new_list = []
blocked_list = []
finished_process_list = []

global_counter = 0
is_paused = False
process_to_show = 0
is_interrupted = False
is_executing_list_empty = False

def assignation():
    # Window config
    window = ttk.Window()
    window.title('Procesamiento por lotes')
    window.state('zoomed')

    # Title
    title_label = ttk.Label(master=window, text="Procesamiento por lotes",font="Calibri 24 bold")
    title_label.pack(pady=20)
    
    amount_of_processes_label = ttk.Label(master = window, text="Procesos a capturar", font='Arial 13')
    amount_of_processes_text = ttk.Entry(master = window)
    amount_of_processes_send = ttk.Button(master = window, command = lambda: verifications(window, amount_of_processes_text,amount_of_processes_label, amount_of_processes_send,title_label), text="OK")
    amount_of_processes_label.pack(pady=5)
    amount_of_processes_text.pack(pady=3)
    amount_of_processes_send.pack(pady=10)
    
    window.mainloop()

def verifications(window,amount_of_processes_text,amount_of_processes_label, amount_of_processes_send,title_label):
    global process_collection
    
    process_count = 0
    aux_collection = []
    
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
        
        process = Process(operation,first_data,second_data,estimated_time,ID)
        new_list.append(process)
        
        i += 1
    
    i = 0
    while i < 5:
        if i < amount_of_processes:
            ready_list.append(new_list.pop(0))
            ready_list[i].start_time = global_counter
            i += 1
        else:
            break
          
    for widget in window.winfo_children():
        widget.destroy()  
    
    secondScreen(window,amount_of_processes)
    
def secondScreen(window,amount_of_processes):
    # Window setup
    global new_list
    global global_counter
    global process_to_show
    global ready_list
    
    # Window config
    window.title('Procesamiento por lotes')
    window.state('zoomed')
    window.columnconfigure((0,1,2,3,4,5), weight = 1)
    window.rowconfigure((0,1,2,3,4,5,6,7), weight = 1)

    # Title
    title_label = ttk.Label(master=window, text="Procesamiento por lotes",font="Calibri 24 bold")
    title_label.grid(row = 0, column = 0, columnspan = 5, pady = 8, padx= 8)
    
    new_process_title = ttk.Label(master=window, text=f"Nuevos: {len(new_list)}", font="Arial 13")
    new_process_title.grid(row = 1, column = 0, pady = 5, padx = 5)
    
    global_counter_container = ttk.Label(master=window, text=f"Contador global: {global_counter}", font="Arial 13")
    global_counter_container.grid(row = 1, column = 2, pady = 5, padx = 5)
    
    # Recuadro de lote en ejecución
    ready_process_label = ttk.Label(window, text = "Procesos listos", font = "Arial 13")
    ready_process_label.grid(row = 2, column = 0, sticky='s')
    ready_process = tk.Text(master=window)
    ready_process.grid(row = 3, column = 0, rowspan = 2, padx = 5)
    
    #Recuadro de procesos bloqueados
    blocked_process_label = ttk.Label(window, text = "Procesos bloqueados", font = "Arial 13")
    blocked_process_label.grid(row = 5, column = 1, sticky='s')
    blocked_processes = tk.Text(master=window)
    blocked_processes.grid(row = 6, column = 1, rowspan = 2, padx = 5)
    
    # Recuadro de proceso en ejecución
    executing_process_label = ttk.Label(window, text = "Proceso en ejecución.", font = "Arial 13")
    executing_process_label.grid(row = 2, column = 1, sticky='s')
    executing_process = tk.Text(master = window)
    executing_process.grid(row = 3, column = 1, rowspan = 2, padx = 5)
    
    # Recuadro de procesos terminados
    finished_process_label = ttk.Label(window, text = "Procesos terminados", font = "Arial 13")
    finished_process_label.grid(row = 2, column = 2, sticky='s')
    # finished_process = ScrolledText(master = window,wrap=tk.WORD)
    finished_process = tk.Text(master = window)
    finished_process.grid(row = 3, column = 2, rowspan = 2, padx = 5)
    
    start_simulation = ttk.Button(master = window, text="Enviar proceso")
    
    # Obtiene el primer proceso y lo envía a proceso en ejecución
    process_to_show = ready_list.pop(0)
    process_to_show.response_time = global_counter - process_to_show.start_time
    process_to_show.response_flag = True
    # batches_counter = len(batch_collection)-1
    
    # Muestra el lote en ejecución
    if len(ready_list) != 0:
        for process in ready_list:
            ready_process.insert("end","ID: " + str(process.id) + " Tiempo máximo estimado: " + str(process.estimated_time) + "\n")
            
    executing_process.insert("end",process_to_show)
    
    counter(window, global_counter, global_counter_container,executing_process,ready_process,new_process_title,finished_process, finished_process_list,blocked_processes,amount_of_processes)
    
def counter(window, global_counter, global_counter_container,executing_process,ready_process,new_process_title,finished_process, finished_process_list, blocked_processes,amount_of_processes):
    
    global is_paused
    global process_to_show
    global is_interrupted
    global ready_list
    global new_list
    global blocked_list
    global is_executing_list_empty
    
    # Llamada recursiva cada segundo
    executing_process.after(1000,lambda: counter(window, global_counter, global_counter_container,executing_process,ready_process,new_process_title,finished_process, finished_process_list,blocked_processes,amount_of_processes))
    
    executing_process.delete('1.0',"end")
    
    window.bind('<KeyRelease>',on_key_release)
        
    if not is_paused:
        # Menos de 5 procesos bloqueados al mismo tiempo
        if is_interrupted and len(ready_list) > 0:
            # Si la lista de listos no está vacía
            if is_executing_list_empty == True:
                process_to_show = ready_list.pop(0)
                # Checa si ya se midió el tiempo de respuesta
                if process_to_show.response_flag == False:
                    process_to_show.response_time = global_counter - process_to_show.start_time
                    process_to_show.response_flag = True
                is_executing_list_empty = False
            else:
                blocked_list.append(process_to_show)
                process_to_show = ready_list.pop(0)
                if process_to_show.response_flag == False:
                    process_to_show.response_time = global_counter - process_to_show.start_time
                    process_to_show.response_flag = True
            
            is_interrupted = False    
            
            executing_process.insert('1.0',process_to_show)
            
            ready_process.delete('1.0',"end")
            for process in ready_list:
                ready_process.insert("end","ID: " + str(process.id) + " Tiempo máximo estimado: " + str(process.estimated_time) + "\n")
            
            blocked_processes.delete('1.0',"end")
            for process in blocked_list:
                blocked_processes.insert("end","ID: " + str(process.id) + " Tiempo bloqueado: " + str(process.blocked_time) + "\n")
                
        # 5 procesos bloqueados al mismo tiempo
        elif is_interrupted and len(ready_list) == 0:
            global_counter += 1
            global_counter_container.config(text=f"Contador global: {global_counter}")
            if not is_executing_list_empty:
                blocked_list.append(process_to_show)
            is_executing_list_empty = True
            if len(blocked_list) != 0:
                blocked_processes.delete('1.0',"end")
                for process in blocked_list:
                    if process.blocked_time < 8:
                        process.blocked_time += 1
                        blocked_processes.insert("end","ID: " + str(process.id) + " Tiempo bloqueado: " + str(process.blocked_time) + "\n")
                    else:
                        process.blocked_time = 0
                        ready_list.append(process)
                        blocked_list.remove(process)
                        break
            
        elif process_to_show.TRE != 0 and not is_interrupted:                                # Actualiza el tiempo restante y el contador global
            process_to_show.TRE -= 1
            process_to_show.TTE += 1
            global_counter += 1
            global_counter_container.config(text=f"Contador global: {global_counter}")
            executing_process.insert("end",process_to_show)
            if len(blocked_list) != 0:
                blocked_processes.delete('1.0',"end")
                i = 0
                while i < len(blocked_list): 
                    if len(blocked_list) != 0:
                        if blocked_list[i].blocked_time < 8:
                            blocked_list[i].blocked_time += 1
                            blocked_processes.insert("end","ID: " + str(blocked_list[i].id) + " Tiempo bloqueado: " + str(blocked_list[i].blocked_time) + "\n")
                        else:
                            blocked_list[i].blocked_time = 0
                            ready_list.append(blocked_list[i])
                            ready_process.insert("end","ID: " + str(blocked_list[i].id) + " Tiempo máximo estimado: " + str(blocked_list[i].estimated_time) + "\n")
                            blocked_list.remove(blocked_list[i])
                            i = -1
                        i += 1             
            
        # Se termina un proceso porque su tiempo restante es 0
        elif process_to_show.TRE == 0:
            # Se actualiza la lista de procesos terminados
            if not process_to_show in finished_process_list:
                process_to_show.finishing_time = global_counter
                finished_process_list.append(process_to_show)
                finished_process_show(finished_process_list,finished_process)
            
            # Si la cola de listos no está vacía, se saca el siguiente proceso
            if len(ready_list) != 0:
                process_to_show = ready_list.pop(0)
                if process_to_show.response_flag == False:
                    process_to_show.response_time = global_counter - process_to_show.start_time
                    process_to_show.response_flag = True
                
                 # Imprime el nuevo proceso a ejecutar
                executing_process.insert("end",process_to_show)
                
                # Actualiza el contador de nuevos procesos
                if len(new_list) > 0:
                    new_list[0].start_time = global_counter
                    ready_list.append(new_list.pop(0))
                new_process_title.config(text=f"Nuevos: {len(new_list)}")
                
                # Reimprime la lista de procesos nuevos
                ready_process.delete('1.0', "end")
                for process in ready_list:
                    ready_process.insert("end","ID: "+str(process.id)+" Tiempo máximo estimado: "+str(process.estimated_time)+"\n")
                
                # Actualiza la lista de procesos terminados
                finished_process_show(finished_process_list,finished_process)
            else: 
                if(len(finished_process_list) == amount_of_processes):
                    finished_process_show(finished_process_list,finished_process)
                    bcp(window)
                elif(len(blocked_list) != 0) and len(new_list) == 0:
                    blocked_processes.after(1000,lambda:finishes_remaining_blocked_process(blocked_processes))
                    global_counter += 1
                    global_counter_container.config(text=f"Contador global: {global_counter}")
                    if blocked_list[0].blocked_time == 8:
                        blocked_processes.delete('1.0',"end")
                        blocked_list[0].blocked_time = 0
                        ready_list.append(blocked_list.pop())
                        process_to_show = ready_list.pop()
                        executing_process.insert("end",process_to_show) 
                        blocked_processes.after_cancel(blocked_processes)  
                elif len(blocked_list) != 0 and len(new_list) != 0 and len(ready_list) == 0:
                    ready_list.append(new_list.pop(0))     
                    process_to_show = ready_list.pop()
                    process_to_show.start_time = global_counter
                    process_to_show.response_time = global_counter - process_to_show.start_time            
    else:
        executing_process.insert("end",process_to_show)

def finished_process_show(finished_process_list,finished_process):
    finished_process.delete('1.0',"end")
    for finished in finished_process_list:              #Imprime la lista de finalizados
        if not finished.error: 
            finished.calculate_times()
            finished_process.insert("end", f"ID: " + str(finished.id) + " Operación: " + str(finished.first_data) + finished.operation + str(finished.second_data) + " Resultado: " + str(finished.operate(error=False)) + "\n\n")
            print(finished)
        else:
            finished.service_time = finished.TTE
            finished.calculate_times()
            finished_process.insert("end", f"ID: " + str(finished.id) + " Operación: " + str(finished.first_data) + finished.operation + str(finished.second_data) + " Resultado: " + str(finished.operate(error=True)) + "\n\n")
            print(finished)
    
def on_key_release(event):
    global is_paused
    global process_to_show
    global is_interrupted
    
    if event.keysym == 'p' and not is_paused:
        is_paused = True
    elif event.keysym == 'c':
        is_paused = False
    elif event.keysym == 'e' and not is_paused:
        process_to_show.TRE = 0
        process_to_show.error = True
    elif event.keysym == 'i' and not is_paused:
        is_interrupted = True
        
def bcp(window):
    for widget in window.winfo_children():
        widget.destroy()
        
    table = ttk.Treeview(window, columns=('ID','Operación','Resultado','Tiempo Inicio','Tiempo Finalización','Tiempo Servicio','Tiempo Espera','Tiempo Retorno', 'Tiempo Respuesta'),show='headings')
    
    table.column('ID',anchor=tk.CENTER)
    table.column('Operación',anchor=tk.CENTER)
    table.column('Resultado',anchor=tk.CENTER)
    table.column('Tiempo Inicio',anchor=tk.CENTER)
    table.column('Tiempo Finalización',anchor=tk.CENTER)
    table.column('Tiempo Servicio',anchor=tk.CENTER)
    table.column('Tiempo Espera',anchor=tk.CENTER)
    table.column('Tiempo Retorno',anchor=tk.CENTER)
    table.column('Tiempo Respuesta',anchor=tk.CENTER)
    
    table.heading('ID', text='ID')
    table.heading('Operación', text='Operación')
    table.heading('Resultado', text='Resultado')
    table.heading('Tiempo Inicio', text='Tiempo Inicio')
    table.heading('Tiempo Finalización', text='Tiempo Finalización')
    table.heading('Tiempo Servicio', text='Tiempo Servicio')
    table.heading('Tiempo Espera', text='Tiempo Espera')
    table.heading('Tiempo Retorno', text='Tiempo Retorno')
    table.heading('Tiempo Respuesta', text='Tiempo Respuesta')
    table.pack(fill='both',expand=True)
    
    for process in finished_process_list:
        values = (process.id,process.serializeOperation(),process.result,process.start_time,process.finishing_time,process.service_time,process.waiting_time,process.return_time,process.response_time)
        table.insert(parent='',index=tk.END,values=values)
        print(values)

def finishes_remaining_blocked_process(blocked_processes):
    global blocked_list
    if len(blocked_list) != 0:
        blocked_processes.delete('1.0',"end")
        blocked_list[0].blocked_time += 1
        blocked_processes.insert("end","ID: " + str(blocked_list[0].id) + " Tiempo bloqueado: " + str(blocked_list[0].blocked_time) + "\n")

assignation()