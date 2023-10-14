import ttkbootstrap as ttk
import tkinter as tk
from procesos import Process
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
is_generated_new_process = False
is_bcp_called = False

number_of_processes = 0

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
    global number_of_processes
    
    process_count = 0
    aux_collection = []
    
    amount_of_processes = amount_of_processes_text.get()
    amount_of_processes = int(amount_of_processes)
    i = 0
    
    # Genera los procesos de forma aleatoria
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
    number_of_processes = amount_of_processes
    # Mientras que los procesos sean menores a 5 o al total ingresado se añaden a la cola de listos
    while i < 5 and i < amount_of_processes:
        ready_list.append(new_list.pop(0))
        ready_list[i].start_time = global_counter
        i += 1
          
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
    
    # Muestra la cola de listos
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
    global is_generated_new_process
    global is_bcp_called
    global number_of_processes
    
    # Llamada recursiva cada segundo
    executing_process.after(1000,lambda: counter(window, global_counter, global_counter_container,executing_process,ready_process,new_process_title,finished_process, finished_process_list,blocked_processes,amount_of_processes))
    
    executing_process.delete('1.0',"end")
    
    window.bind('<KeyRelease>',on_key_release)
         
    if not is_paused:
        # Menos de 5 procesos bloqueados al mismo tiempo
        # Si la cola de listos no está vacía
        if is_interrupted and len(ready_list) > 0:
            # Checa si no existe un proceso en ejecución
            if is_generated_new_process:
                new_process_title.config(text=f"Nuevos: {len(new_list)}")  
                ready_process.delete('1.0',"end")
                for process in ready_list:
                    ready_process.insert("end","ID: " + str(process.id) + " Tiempo máximo estimado: " + str(process.estimated_time) + "\n")
                is_generated_new_process = False
            
            if is_executing_list_empty == True:
                # En caso de que sea cierto toma un proceso de la cola de listos para ejecutarse
                process_to_show = ready_list.pop(0)
                # Checa si ya se midió el tiempo de respuesta
                if process_to_show.response_flag == False:
                    process_to_show.response_time = global_counter - process_to_show.start_time
                    process_to_show.response_flag = True
                # Regresa la bandera a falso pues ya existe un proceso en ejecución
                is_executing_list_empty = False
            else:
                # Si hay un proceso en ejecución lo manda a bloqueo
                blocked_list.append(process_to_show)
                # Obtiene un nuevo proceso a ejecutar
                process_to_show = ready_list.pop(0)
                # Si el proceso no se ha medido su tiempo de respuesta lo mide
                if process_to_show.response_flag == False:
                    process_to_show.response_time = global_counter - process_to_show.start_time
                    process_to_show.response_flag = True
            
            # Regresa el estado de interrupción a falso
            is_interrupted = False    
            
            executing_process.insert('1.0',process_to_show)
            
            ready_process.delete('1.0',"end")
            for process in ready_list:
                ready_process.insert("end","ID: " + str(process.id) + " Tiempo máximo estimado: " + str(process.estimated_time) + "\n")
            
            blocked_processes.delete('1.0',"end")
            for process in blocked_list:
                blocked_processes.insert("end","ID: " + str(process.id) + " Tiempo bloqueado: " + str(process.blocked_time) + "\n")
                
        # 5 procesos bloqueados al mismo tiempo, por tanto la cola de listos está vacía
        elif is_interrupted and len(ready_list) == 0:
            if is_generated_new_process:
                new_process_title.config(text=f"Nuevos: {len(new_list)}")  
                ready_process.delete('1.0',"end")
                for process in ready_list:
                    ready_process.insert("end","ID: " + str(process.id) + " Tiempo máximo estimado: " + str(process.estimated_time) + "\n")
                is_generated_new_process = False
            # Aumenta el contador global
            global_counter += 1
            global_counter_container.config(text=f"Contador global: {global_counter}")
            # Si existe un proceso en ejecución lo bloquea
            if not is_executing_list_empty:
                blocked_list.append(process_to_show)
            # Como todos los procesos están en bloqueados, entonces no hay procesos en ejecución
            is_executing_list_empty = True
            # Si hay más de un proceso bloqueado continúa la cuenta hasta que uno sale de bloqueo
            if len(blocked_list) != 0:
                blocked_processes.delete('1.0',"end")
                for process in blocked_list:
                    if process.blocked_time < 8:
                        process.blocked_time += 1
                        blocked_processes.insert("end","ID: " + str(process.id) + " Tiempo bloqueado: " + str(process.blocked_time) + "\n")
                    else:
                        # Reinicia el tiempo de bloqueo para que pueda volver a bloquearse
                        process.blocked_time = 0
                        # Añade el proceso a la cola de listos
                        ready_list.append(process)
                        # Quita el proceso de la lista de bloqueados
                        blocked_list.remove(process)
                        break
        # Cuando el proceso está en ejecución y no se produce una interrupción
        elif process_to_show.TRE != 0 and not is_interrupted:  
            if is_generated_new_process:
                new_process_title.config(text=f"Nuevos: {len(new_list)}")  
                ready_process.delete('1.0',"end")
                for process in ready_list:
                    ready_process.insert("end","ID: " + str(process.id) + " Tiempo máximo estimado: " + str(process.estimated_time) + "\n")
                is_generated_new_process = False               
            # Actualiza los contadores de tiempo restante y tiempo transcurrido del proceso               
            process_to_show.TRE -= 1
            process_to_show.TTE += 1
            # Actualiza el contador global
            global_counter += 1
            global_counter_container.config(text=f"Contador global: {global_counter}")
            executing_process.insert("end",process_to_show)
            # Si existen uno o más procesos bloqueados
            if len(blocked_list) != 0:
                blocked_processes.delete('1.0',"end")
                i = 0
                # Ciclo while que actualiza constantemente el tiempo de bloqueo de los procesos bloqueados
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
                            # Actualiza el contador, de forma que nunca se pase del tamaño del arreglo
                            i = -1
                        i += 1             
            
        # Se termina un proceso porque su tiempo restante es 0
        elif process_to_show.TRE == 0:
            if is_generated_new_process:
                new_process_title.config(text=f"Nuevos: {len(new_list)}")  
                ready_process.delete('1.0',"end")
                for process in ready_list:
                    ready_process.insert("end","ID: " + str(process.id) + " Tiempo máximo estimado: " + str(process.estimated_time) + "\n")
                is_generated_new_process = False
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
                
                # Si hay uno o más procesos en la cola de procesos nuevos, añade el primero a la cola de listos
                if len(new_list) > 0:
                    # Establece el tiempo de inicio del proceso nuevo
                    new_list[0].start_time = global_counter
                    ready_list.append(new_list.pop(0))
                # Actualiza el contador de la cola de procesos nuevos
                new_process_title.config(text=f"Nuevos: {len(new_list)}")
                
                # Reimprime la lista de procesos nuevos
                ready_process.delete('1.0', "end")
                for process in ready_list:
                    ready_process.insert("end","ID: "+str(process.id)+" Tiempo máximo estimado: "+str(process.estimated_time)+"\n")
                
                # Actualiza la lista de procesos terminados
                finished_process_show(finished_process_list,finished_process)
            else: 
                # Si todos los procesos han terminado
                if(len(finished_process_list) == number_of_processes):
                    # Actualiza la lista de procesos terminados, para añadir el último proceso a dicha lista
                    finished_process_show(finished_process_list,finished_process)
                    # Muestra el BCP
                    for widget in window.winfo_children():
                        widget.destroy()
                    process_to_show.null_process = True
                    bcp(window,global_counter)
                # Si la cola de listos no tiene procesos, y la cola de nuevos tampoco, todos los procesos se encuentran bloqueados
                elif(len(blocked_list) != 0) and len(new_list) == 0:
                    if is_generated_new_process:
                        new_process_title.config(text=f"Nuevos: {len(new_list)}")  
                        ready_process.delete('1.0',"end")
                        for process in ready_list:
                            ready_process.insert("end","ID: " + str(process.id) + " Tiempo máximo estimado: " + str(process.estimated_time) + "\n")
                        process_to_show.null_process = True
                        is_generated_new_process = False
                    # Llama recursivamente cada segundo a la funcion finishes_remaining_blocked_process que se encarga de terminar la ejecución de un proceso
                    # bloqueado para salir de este estado
                    blocked_processes.after(1000,lambda:finishes_remaining_blocked_process(blocked_processes))
                    # Actualiza el contador global
                    global_counter += 1
                    global_counter_container.config(text=f"Contador global: {global_counter}")
                    # Checa si el primer proceso de la lista de bloqueado haya terminado su tiempo de bloqueo
                    if blocked_list[0].blocked_time == 8:
                        blocked_processes.delete('1.0',"end")
                        # Reestablece su valor de tiempo de bloqueado a 0 para que se pueda volver a bloquear
                        blocked_list[0].blocked_time = 0
                        # Agrega el proceso a la cola de listos
                        ready_list.append(blocked_list.pop(0))
                        #Restaura el proceso a un proceso no nulo
                        process_to_show.null_process = False
                        # Agrega el proceso a ejecución
                        process_to_show = ready_list.pop()
                        # Actualiza el recuadro de GUI
                        executing_process.insert("end",process_to_show)
                        # Evita que se siga llamando recursivamente a la función finishes_remaining_blocked_process
                        blocked_processes.after_cancel(blocked_processes)  
                    else:
                        blocked_processes.delete('1.0', "end")
                        for process in blocked_list:
                            blocked_processes.insert("end","ID: "+str(process.id)+" Tiempo bloqueado: "+str(process.blocked_time)+"\n")
                # Si la cola de listos está vacía pero la cola de nuevos no está vacía se obtiene el primer dato de la cola de nuevos como proceso en ejecución
                elif len(blocked_list) != 0 and len(new_list) != 0:
                    if is_generated_new_process:
                        new_process_title.config(text=f"Nuevos: {len(new_list)}")  
                        ready_process.delete('1.0',"end")
                        for process in ready_list:
                            ready_process.insert("end","ID: " + str(process.id) + " Tiempo máximo estimado: " + str(process.estimated_time) + "\n")
                        is_generated_new_process = False
                    # Añade el proceso a cola de listos
                    ready_list.append(new_list.pop(0)) 
                    # Convierte el proceso en el proceso a ejecutar    
                    process_to_show = ready_list.pop()
                    # Establece el tiempo de incio y el tiempo de respuesta
                    process_to_show.start_time = global_counter
                    process_to_show.response_time = global_counter - process_to_show.start_time            
    else:
        if is_bcp_called:
            window2 = ttk.Window(title='Bloque de control de procesos')
            window2.state('zoomed')
            bcp(window2,global_counter)
            is_bcp_called = False
        # Si está pausado entonces se mantiene el proceso en pantalla
        executing_process.insert("end",process_to_show)

def finished_process_show(finished_process_list,finished_process):
    finished_process.delete('1.0',"end")
    for finished in finished_process_list:              #Imprime la lista de finalizados
        if not finished.error: 
            # Si no terminó por error se calculan los tiempos
            finished.calculate_times()
            finished_process.insert("end", f"ID: " + str(finished.id) + " Operación: " + str(finished.first_data) + finished.operation + str(finished.second_data) + " Resultado: " + str(finished.operate(error=False)) + "\n\n")
        else:
            # Si terminó por error el tiempo de servicio será igual al tiempo que estuvo en ejecución
            finished.service_time = finished.TTE
            # Calcula los tiempos
            finished.calculate_times()
            finished_process.insert("end", f"ID: " + str(finished.id) + " Operación: " + str(finished.first_data) + finished.operation + str(finished.second_data) + " Resultado: " + str(finished.operate(error=True)) + "\n\n")
    
def on_key_release(event):
    global is_paused
    global process_to_show
    global is_interrupted
    global is_generated_new_process
    global is_bcp_called
    
    if event.keysym == 'p' and not is_paused:
        is_paused = True
    elif event.keysym == 'c':
        is_paused = False
    elif event.keysym == 'e' and not is_paused:
        process_to_show.TRE = 0
        process_to_show.error = True
    elif event.keysym == 'i' and not is_paused:
        is_interrupted = True
    elif event.keysym == 'n' and not is_paused:
        generate_new_process()
        is_generated_new_process = True
    elif event.keysym == 'b' and not is_paused:
        is_paused = True
        is_bcp_called = True

def generate_new_process():
    global new_list
    global ready_list
    global blocked_list
    global number_of_processes
             
    ID = number_of_processes
    number_of_processes += 1
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
    len_ready_list = len(ready_list)
    len_blocked_list = len(blocked_list)
    
    if len_blocked_list == 5: 
        new_list.append(process)
    elif len_ready_list + len_blocked_list >= 4:
        new_list.append(process)
    else:
        ready_list.append(process)
        
        
def bcp(window, global_counter):
    # for widget in window.winfo_children():
    #     widget.destroy()
    # window2 = ttk.Window(title='Bloque de control de procesos')
    # window2.state('zoomed')
    global blocked_list
    global ready_list
    global process_to_show
    global finished_process_list
    
    window.bind("<KeyRelease>", second_key_release)
        
    table = ttk.Treeview(window, columns=('ID','Operación','Resultado','Tiempo Inicio','Tiempo Finalización','Tiempo Servicio','Tiempo Espera','Tiempo Retorno', 'Tiempo Respuesta'),show='headings')
    
    # Formato de columnas
    table.column('ID',anchor=tk.CENTER)
    table.column('Operación',anchor=tk.CENTER)
    table.column('Resultado',anchor=tk.CENTER)
    table.column('Tiempo Inicio',anchor=tk.CENTER)
    table.column('Tiempo Finalización',anchor=tk.CENTER)
    table.column('Tiempo Servicio',anchor=tk.CENTER)
    table.column('Tiempo Espera',anchor=tk.CENTER)
    table.column('Tiempo Retorno',anchor=tk.CENTER)
    table.column('Tiempo Respuesta',anchor=tk.CENTER)
    
    # Cabeceros de columnas
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
    
    # Itera sobre los procesos y los va insertando en el BCP
    if process_to_show not in blocked_list and process_to_show not in finished_process_list:
        table.insert(parent='',index=tk.END,values=('-','-','-','-','PROCESO EN EJECUCION','-','-','-','-'))
        # Establece el formato de valores
        process_to_show.service_time = process_to_show.TTE
        values = (process_to_show.id,process_to_show.serializeOperation(),process_to_show.result,process_to_show.start_time,process_to_show.finishing_time,process_to_show.service_time,process_to_show.waiting_time,process_to_show.return_time,process_to_show.response_time)
        table.insert(parent='',index=tk.END,values=values)
    
    if len(finished_process_list) != 0: 
        table.insert(parent='',index=tk.END,values=('-','-','-','-','PROCESOS FINALIZADOS','-','-','-','-'))
        for process in finished_process_list:
            # Establece el formato de valores
            process_to_show.service_time = process_to_show.TTE
            values = (process.id,process.serializeOperation(),process.result,process.start_time,process.finishing_time,process.service_time,process.waiting_time,process.return_time,process.response_time)
            table.insert(parent='',index=tk.END,values=values)
            
    if len(ready_list) != 0:    
        table.insert(parent='',index=tk.END,values=('-','-','-','-','PROCESOS LISTOS','-','-','-','-'))
        for process in ready_list:
            process.service_time = process.TTE
            process.waiting_time = global_counter - process.start_time - process.TTE
            values = (process.id,process.serializeOperation(),process.result,process.start_time,process.finishing_time,process.service_time,process.waiting_time,process.return_time,process.response_time)
            table.insert(parent='',index=tk.END,values=values)
    
    if len(blocked_list) != 0:        
        table.insert(parent='',index=tk.END,values=('-','-','-','-','PROCESOS BLOQUEADOS','-','-','-','-'))
        for process in blocked_list:
            process.service_time = process.TTE
            process.waiting_time = global_counter - process.start_time - process.TTE
            values = (process.id,process.serializeOperation(),process.result,process.start_time,process.finishing_time,process.service_time,process.waiting_time,process.return_time,process.response_time)
            table.insert(parent='',index=tk.END,values=values)
    

def second_key_release(event):
    global is_paused
    global is_bcp_called
    if event.keysym == 'c':
        event.widget.destroy()
        is_paused = False
        is_bcp_called = False
    
def finishes_remaining_blocked_process(blocked_processes):
    global blocked_list
    # Si hay más de un proceso bloqueado actualiza su tiempo de bloqueo
    if len(blocked_list) != 0:
        blocked_processes.delete('1.0',"end")
        for process in blocked_list:
            # Incrementa el tiempo de bloqueo
            process.blocked_time += 1
            blocked_processes.insert("end","ID: "+str(process.id)+" Tiempo bloqueado: "+str(process.blocked_time)+"\n")

assignation()