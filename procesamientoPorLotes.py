import ttkbootstrap as ttk
import tkinter as tk
from procesos import Process
import random as rd
from tabla_paginacion import PageTable

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
quantum_size = 0
page_table = PageTable()
page_table_object = 0

number_of_processes = 0


def insert_process_in_table(process):
    global new_list
    global ready_list

    size = process.size
    if page_table.count_free_pages() >= process.page_number:
        new_list[0].start_time = global_counter
        ready_list.append(new_list.pop(0))
        for i in range(0, 41):
            if size > 0:
                if page_table.page_array[i][3] == 'Libre':
                    if size >= 5:
                        page_table.page_array.pop(i)
                        page_table.page_array.insert(
                            i, [i, '5/5', process.id, 'Listo'])
                    else:
                        page_table.page_array.pop(i)
                        page_table.page_array.insert(
                            i, [i, f'{size}/5', process.id, 'Listo'])
                    size -= 5
            else:
                break


def assignation():
    # Window config
    window = ttk.Window()
    window.title('Procesamiento por lotes')
    window.state('zoomed')

    # Title
    title_label = ttk.Label(
        master=window, text="Procesamiento por lotes", font="Calibri 24 bold")
    title_label.pack(pady=20)

    amount_of_processes_label = ttk.Label(
        master=window, text="Procesos a capturar", font='Arial 13')
    amount_of_processes_text = ttk.Entry(master=window)
    amount_of_processes_send = ttk.Button(master=window, command=lambda: verifications(
        window, amount_of_processes_text, amount_of_processes_label, amount_of_processes_send, title_label, quantum_label, quantum_text), text="OK")

    quantum_label = ttk.Label(
        master=window, text="Tamaño del quantum", font='Arial 13')
    quantum_text = ttk.Entry(master=window)

    amount_of_processes_label.pack(pady=5)
    amount_of_processes_text.pack(pady=3)
    quantum_label.pack(pady=5)
    quantum_text.pack(pady=3)
    amount_of_processes_send.pack(pady=10)

    window.mainloop()


def verifications(window, amount_of_processes_text, amount_of_processes_label, amount_of_processes_send, title_label, quantum_label, quantum_text):
    global process_collection
    global number_of_processes
    global quantum_size
    global page_table
    global process_to_show
    global new_list
    global ready_list

    # Conversión del valor del quantum
    quantum_size = quantum_text.get()
    quantum_size = int(quantum_size)

    # Conversión de la cantidad de procesos
    amount_of_processes = amount_of_processes_text.get()
    amount_of_processes = int(amount_of_processes)
    i = 0

    # Genera los procesos de forma aleatoria
    while i < amount_of_processes:
        ID = i
        first_data = rd.randint(0, 10000)
        second_data = rd.randint(0, 10000)
        estimated_time = rd.randint(6, 18)
        size = rd.randint(6, 26)
        if second_data == 0:
            operation_list = ['+', '-', '*']
        else:
            operation_list = ['+', '-', '*', '/', '%']
        operation = rd.choices(operation_list)
        operation = operation[0]

        process = Process(operation, first_data, second_data,
                          estimated_time, ID, quantum_size, size)
        new_list.append(process)

        i += 1

    # Establece el numero de procesos totales
    number_of_processes = amount_of_processes
    # Obtiene el proceso a ejecutar de la lista de nuevos procesos
    process_to_show = new_list.pop(0)
    # Establece su tiempo de respuesta a 0 (valor del contador global en este instante)
    process_to_show.start_time = global_counter
    # Establece el valor del tiempo de respuesta (0 en este instante)
    process_to_show.response_time = global_counter - process_to_show.start_time
    # Al ya cambiar el valor del tiempo de respuesta se enciende la bandera que indica este hecho
    process_to_show.response_flag = True
    # Realiza una copia del tamaño del proceso a ejecutar
    size = process_to_show.size
    # Busca espacio libre en la tabla de paginación para almacenar el proceso a ejecutar
    for i in range(0, 41):
        # Checa si el tamaño es mayor a 0 y si es así se inserta el proceso en la tabla de paginación
        if size > 0:
            # Si se encuentra un espacio libre
            if page_table.page_array[i][3] == 'Libre':
                # Checa si el tamaño es mayor o igual que 5
                if size >= 5:
                    # Sustituye el valor actual de la tabla de paginación por el proceso a ejecutar
                    page_table.page_array.pop(i)
                    page_table.page_array.insert(
                        i, [i, '5/5', process_to_show.id, 'Ejecución'])
                # Si el tamaño es menor que 5
                else:
                    # Sustituye el valor actual de la tabla de paginación por el tamaño restante del proceso a ejecutar
                    page_table.page_array.pop(i)
                    page_table.page_array.insert(
                        i, [i, f'{size}/5', process_to_show.id, 'Ejecución'])
                # Disminuye en 5 (tamaño del marco de página) el tamaño del proceso
                size -= 5
        # Si el tamaño es menor a 5, el proceso se ha terminado de capturar
        else:
            break

    # Se crea una variable que servirá para el proceso de la primer captura de datos
    last_id = 0
    # Para cada proceso en la lista de nuevos
    for process in new_list:
        # Se establece el valor del tamaño del proceso
        size = process.size
        # Si encuentra espacio libre en la tabla de paginación para almacenar el proceso (hay más páginas libres que el número de páginas que requiere el proceso)
        if page_table.count_free_pages() >= process.page_number:
            # Se actualiza el valor del último id al del proceso actual
            last_id = process.id
            # Se itera por cada página del proceso
            for i in range(0, 41):
                # Si el tamaño del proceso es mayor a 0
                if size > 0:
                    # Si se encuentra un marco de página libre
                    if page_table.page_array[i][3] == 'Libre':
                        # Checa si el tamaño es mayor o igual a 5
                        if size >= 5:
                            # Sustituye el valor actual de la tabla de paginación por el proceso a ejecutar
                            page_table.page_array.pop(i)
                            page_table.page_array.insert(
                                i, [i, '5/5', process.id, 'Listo'])
                        # Si el tamaño es menor a 5
                        else:
                            # Sustituye el valor actual de la tabla de paginación por el tamaño restante del proceso
                            page_table.page_array.pop(i)
                            page_table.page_array.insert(
                                i, [i, f'{size}/5', process.id, 'Listo'])
                        # Disminuye en 5 (tamaño del marco de página) el tamaño del proceso
                        size -= 5
                # Si el tamaño del proceso es menor a 5, el proceso se ha terminado de capturar
                else:
                    break
        # Si no hay un espacio libre se ha terminado la captura de procesos
        else:
            break

    # Se checa que el id del primer elemento de la lista de nuevos sea distinto al del último elemento capturado
    while new_list[0].id <= last_id:
        # Se agrega el proceso a lista de nuevos
        ready_list.append(new_list.pop(0))
        # Se establece su tiempo de respuesta a 0 (valor del contador global en este instante)
        ready_list[0].start_time = global_counter
        # Si la lista de nuevos está vacía se ha terminado la captura
        if len(new_list) == 0:
            break
    # Destruye todos los elementos de la pantalla para redibujar
    for widget in window.winfo_children():
        widget.destroy()

    secondScreen(window, amount_of_processes, quantum_size)


def secondScreen(window, amount_of_processes, quantum_size):
    # Window setup
    global new_list
    global global_counter
    global process_to_show
    global ready_list
    global page_table
    global page_table_object

    # Window config
    window.title('Procesamiento por lotes')
    window.state('zoomed')
    window.columnconfigure((0, 1, 2, 3), weight=1)
    window.rowconfigure((0, 1, 2, 3), weight=1)

    # Title
    title_label = ttk.Label(
        master=window, text="Procesamiento por lotes", font="Calibri 24 bold")
    title_label.grid(row=0, column=0, columnspan=5, pady=8, padx=8)

    new_process_title = ttk.Label(
        master=window, text=f"Nuevos: {len(new_list)}", font="Arial 13")
    new_process_title.grid(row=1, column=0, padx=5)
    if len(new_list) > 0:
        next_process = ttk.Label(
            window, text=f"Siguiente proceso: ID({new_list[0].id}) Tamaño({new_list[0].size})", font="Arial 13")
    else:
        next_process = ttk.Label(
            window, text=f"Siguiente proceso: ID() Tamaño()", font="Arial 13")
    next_process.grid(row=1, column=1, columnspan=2, padx=5)

    global_counter_container = ttk.Label(
        master=window, text=f"Contador global: {global_counter}", font="Arial 13")
    global_counter_container.grid(row=1, column=3, padx=5)

    # Frame de estados
    states_frame = ttk.Frame(window)
    states_frame.grid(row=2, column=0, columnspan=2, sticky='nsew')
    # Configuración de filas y columnas del frame de estados
    states_frame.columnconfigure((0, 1), weight=1)
    states_frame.rowconfigure((0, 1, 2, 3), weight=1)

    # Recuadro de lote en ejecución
    ready_process_label = ttk.Label(
        states_frame, text="Procesos listos", font="Arial 13")
    ready_process_label.grid(row=0, column=0, sticky='s')
    ready_process = tk.Text(master=states_frame)
    ready_process.grid(row=1, column=0, padx=5)

    # Recuadro de procesos bloqueados
    blocked_process_label = ttk.Label(
        states_frame, text="Procesos bloqueados", font="Arial 13")
    blocked_process_label.grid(row=0, column=1, sticky='s')
    blocked_processes = tk.Text(master=states_frame)
    blocked_processes.grid(row=1, column=1, padx=5)

    # Recuadro de proceso en ejecución
    executing_process_label = ttk.Label(
        states_frame, text="Proceso en ejecución.", font="Arial 13")
    executing_process_label.grid(row=2, column=0, sticky='s')
    executing_process = tk.Text(master=states_frame)
    executing_process.grid(row=3, column=0, padx=5)

    # Recuadro de procesos terminados
    finished_process_label = ttk.Label(
        states_frame, text="Procesos terminados", font="Arial 13")
    finished_process_label.grid(row=2, column=1, sticky='s')
    finished_process = tk.Text(master=states_frame)
    finished_process.grid(row=3, column=1, padx=5)

    # Tabla de paginación
    page_frame = ttk.Frame(window)
    page_frame.grid(row=2, column=2, columnspan=2, sticky='nsew')
    # Configuración de columnas y filas de la tabla de paginación
    page_frame.rowconfigure(0, weight=0)
    page_frame.rowconfigure(1, weight=5)
    # Título de la tabla de paginación
    page_label = ttk.Label(master=page_frame, text="Páginas", font="Arial 13")
    page_label.grid(row=0, pady=5, padx=5, sticky='s')
    # Creación de la tabla de paginación
    page_table_object = ttk.Treeview(page_frame, columns=(
        "Marco", "Espacio", "ID", "Estado"), show="headings")
    page_table_object.grid(row=1, sticky='nsew')
    # Se establece el formato de la tabla de paginación
    page_table_object.column('Marco', width=100, anchor=tk.CENTER)
    page_table_object.column('Espacio', width=100, anchor=tk.CENTER)
    page_table_object.column('ID', width=50, anchor=tk.CENTER)
    page_table_object.column('Estado', width=100, anchor=tk.CENTER)
    # Se escriben los títulos de la tabla de paginación
    page_table_object.heading('Marco', text='Marco')
    page_table_object.heading('Espacio', text='Espacio')
    page_table_object.heading('ID', text='ID')
    page_table_object.heading('Estado', text='Estado')
    # Se rellena por primera vez la tabla de paginación
    for i in range(0, 45):
        page_table_object.insert(
            parent='', index=tk.END, values=page_table.page_array[i])

    # # Muestra la cola de listos
    if len(ready_list) != 0:
        for process in ready_list:
            ready_process.insert("end", "ID: " + str(process.id) + " Tiempo máximo estimado: " + str(
                process.estimated_time) + " Tiempo Transcurrido: " + str(process.TTE) + "\n")

    # Actualiza el recuadro del proceso en ejecución
    executing_process.insert("end", process_to_show)

    counter(window, global_counter_container, executing_process, ready_process, new_process_title,
            finished_process, finished_process_list, blocked_processes, amount_of_processes, next_process)


def counter(window, global_counter_container, executing_process, ready_process, new_process_title, finished_process, finished_process_list, blocked_processes, amount_of_processes, next_process):

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
    global global_counter
    global page_table
    global page_table_object

    # Llamada recursiva cada segundo
    executing_process.after(1000, lambda: counter(window, global_counter_container, executing_process, ready_process,
                            new_process_title, finished_process, finished_process_list, blocked_processes, amount_of_processes, next_process))

    executing_process.delete('1.0', "end")

    window.bind('<KeyRelease>', on_key_release)

    # Checa si la lista de nuevos no está vacía
    if len(new_list) > 0:
        # Trata de insertar el primer elemento de la lista de nuevos en la tabla de paginación
        insert_process_in_table(new_list[0])
        # Actualiza el banner del siguiente proceso en la lista de nuevos
        if len(new_list) > 0:
            next_process.config(
                text=f"Siguiente proceso: ID({new_list[0].id}) Tamaño({new_list[0].size})")
        else:
            next_process.config(text=f"Siguiente proceso: ID() Tamaño()")

        # Actualiza gráficamente la tabla de paginación
        delete_and_update_table(page_table.page_array)
        # Actualiza el banner de la cantidad de procesos nuevos
        new_process_title.config(text=f"Nuevos: {len(new_list)}")
        # Actualiza el recuadro de la cola de listos
        ready_process.delete('1.0', 'end')
        for process in ready_list:
            ready_process.insert("end", "ID: " + str(process.id) + " Tiempo máximo estimado: " + str(
                process.estimated_time) + " Tiempo Transcurrido: " + str(process.TTE) + "\n")

    if not is_paused:
        # Si la cola de listos no está vacía
        if is_interrupted and len(ready_list) > 0:
            # Cuando se genera un proceso nuevo, se actualiza la lista de procesos listos y el contador de procesos nuevos
            if is_generated_new_process:
                # Actualiza el banner de la cantidad de procesos nuevos
                new_process_title.config(text=f"Nuevos: {len(new_list)}")
                # Actualiza el recuadro de la cola de listos
                ready_process.delete('1.0', "end")
                for process in ready_list:
                    ready_process.insert("end", "ID: " + str(process.id) + " Tiempo máximo estimado: " + str(
                        process.estimated_time) + " Tiempo Transcurrido: " + str(process.TTE) + "\n")
                # Se regresa la bandera a falso
                is_generated_new_process = False

            # Checa si no existe un proceso en ejecución
            if is_executing_list_empty == True:
                # En caso de que sea cierto toma un proceso de la cola de listos para ejecutarse
                process_to_show = ready_list.pop(0)
                # Actualiza su estado en la tabla de paginación
                page_table.change_state(process_to_show.id, 'En ejecución')
                # Actualiza la tabla de paginación
                delete_and_update_table(page_table.page_array)
                # Checa si ya se midió el tiempo de respuesta
                if process_to_show.response_flag == False:
                    process_to_show.response_time = global_counter - process_to_show.start_time
                    process_to_show.response_flag = True
                # Regresa la bandera a falso pues ya existe un proceso en ejecución
                is_executing_list_empty = False
            else:
                # Cambia el estado del proceso en ejecución a bloqueado en la tabla de paginación
                page_table.change_state(process_to_show.id, "Bloqueado")
                # Si hay un proceso en ejecución lo manda a bloqueo
                blocked_list.append(process_to_show)
                # Obtiene un nuevo proceso a ejecutar
                process_to_show = ready_list.pop(0)
                # Cambia el estado del nuevo proceso en ejecución a ejecución
                page_table.change_state(process_to_show.id, "Ejecución")
                # Actualiza la tabla de paginación
                delete_and_update_table(page_table.page_array)
                # Si el proceso no se ha medido su tiempo de respuesta lo mide
                if process_to_show.response_flag == False:
                    process_to_show.response_time = global_counter - process_to_show.start_time
                    process_to_show.response_flag = True

            # Regresa el estado de interrupción a falso
            is_interrupted = False

            executing_process.insert('1.0', process_to_show)

            ready_process.delete('1.0', "end")
            for process in ready_list:
                ready_process.insert("end", "ID: " + str(process.id) + " Tiempo máximo estimado: " + str(
                    process.estimated_time) + " Tiempo Transcurrido: " + str(process.TTE) + "\n")

            blocked_processes.delete('1.0', "end")
            for process in blocked_list:
                blocked_processes.insert(
                    "end", "ID: " + str(process.id) + " Tiempo bloqueado: " + str(process.blocked_time) + "\n")

        # 5 procesos bloqueados al mismo tiempo, por tanto la cola de listos está vacía
        elif is_interrupted and len(ready_list) == 0:
            # Cuando se genera un proceso nuevo, se actualiza la lista de procesos listos y el contador de procesos nuevos
            if is_generated_new_process:
                # Se actualiza el banner de la cantidad de procesos nuevos
                new_process_title.config(text=f"Nuevos: {len(new_list)}")
                # Se actualiza el recuadro de la cola de listos
                ready_process.delete('1.0', "end")
                for process in ready_list:
                    ready_process.insert("end", "ID: " + str(process.id) + " Tiempo máximo estimado: " + str(
                        process.estimated_time) + " Tiempo Transcurrido: " + str(process.TTE) + "\n")
                # Se regresa la bandera a falso
                is_generated_new_process = False
            # Aumenta el contador global
            global_counter += 1
            global_counter_container.config(
                text=f"Contador global: {global_counter}")
            # Si existe un proceso en ejecución lo bloquea
            if not is_executing_list_empty:
                blocked_list.append(process_to_show)
            # Como todos los procesos están en bloqueados, entonces no hay procesos en ejecución
            is_executing_list_empty = True
            # Si hay más de un proceso bloqueado continúa la cuenta hasta que uno sale de bloqueo
            if len(blocked_list) != 0:
                blocked_processes.delete('1.0', "end")
                for process in blocked_list:
                    if process.blocked_time < 8:
                        process.blocked_time += 1
                        blocked_processes.insert(
                            "end", "ID: " + str(process.id) + " Tiempo bloqueado: " + str(process.blocked_time) + "\n")
                    else:
                        # Reinicia el tiempo de bloqueo para que pueda volver a bloquearse
                        process.blocked_time = 0
                        # Cambia el estado del proceso a listo en la tabla de paginación
                        page_table.change_state(process.id, 'Listo')
                        # Añade el proceso a la cola de listos
                        ready_list.append(process)
                        # Actualiza la tabla de paginación
                        delete_and_update_table(page_table.page_array)
                        # Quita el proceso de la lista de bloqueados
                        blocked_list.remove(process)
                        break
        # Cuando el proceso está en ejecución y no se produce una interrupción
        elif process_to_show.TRE != 0 and not is_interrupted:
            # Cuando se genera un proceso nuevo, se actualiza la lista de procesos listos y el contador de procesos nuevos
            if is_generated_new_process:
                # Actualiza el banner de la cantidad de procesos nuevos
                new_process_title.config(text=f"Nuevos: {len(new_list)}")
                # Actualiza el recuadro de la cola de listos
                ready_process.delete('1.0', "end")
                for process in ready_list:
                    ready_process.insert("end", "ID: " + str(process.id) + " Tiempo máximo estimado: " + str(
                        process.estimated_time) + " Tiempo Transcurrido: " + str(process.TTE) + "\n")
                # Se regresa la bandera a falso
                is_generated_new_process = False
            # Actualiza los contadores de tiempo restante y tiempo transcurrido del proceso
            process_to_show.TRE -= 1
            process_to_show.TTE += 1
            # Incrementa la cantidad de tiempo transcurrido hasta el valor máximo del quantum
            process_to_show.transcurred_quantum += 1
            # Actualiza el contador global
            global_counter += 1
            global_counter_container.config(
                text=f"Contador global: {global_counter}")
            executing_process.insert("end", process_to_show)
            # Si existen uno o más procesos bloqueados
            if len(blocked_list) != 0:
                blocked_processes.delete('1.0', "end")
                i = 0
                # Ciclo while que actualiza constantemente el tiempo de bloqueo de los procesos bloqueados
                while i < len(blocked_list):
                    if len(blocked_list) != 0:
                        if blocked_list[i].blocked_time < 8:
                            blocked_list[i].blocked_time += 1
                            blocked_processes.insert(
                                "end", "ID: " + str(blocked_list[i].id) + " Tiempo bloqueado: " + str(blocked_list[i].blocked_time) + "\n")
                        else:
                            blocked_list[i].blocked_time = 0
                            # Actualiza su estado en la tabla de paginación
                            page_table.change_state(
                                blocked_list[i].id, 'Listo')
                            # Actualiza la tabla de paginación
                            delete_and_update_table(page_table.page_array)
                            ready_list.append(blocked_list[i])
                            ready_process.insert("end", "ID: " + str(blocked_list[i].id) + " Tiempo máximo estimado: " + str(
                                blocked_list[i].estimated_time) + "Tiempo Transcurrido: " + str(blocked_list[i].TTE) + "\n")
                            blocked_list.remove(blocked_list[i])
                            # Actualiza el contador, de forma que nunca se pase del tamaño del arreglo
                            i = -1
                        i += 1
            # Si el valor del quantum transcurrido es igual al valor ingresado del quantum
            if process_to_show.transcurred_quantum == process_to_show.quantum:
                # Cambia el estado en la tabla de procesos
                page_table.change_state(process_to_show.id, 'Listo')
                # Agrega el proceso a la cola de listos
                ready_list.append(process_to_show)
                # Regresa el valor del quantum transcurrido a 0
                process_to_show.transcurred_quantum = 0
                # Obtiene un nuevo proceso a ejecutar
                process_to_show = ready_list.pop(0)
                # Cambia el estado en la tabla de procesos
                page_table.change_state(process_to_show.id, 'En ejecución')
                if not process_to_show.response_flag:
                    process_to_show.response_time = global_counter - process_to_show.start_time
                    process_to_show.response_flag = True
                # Actualiza la cola de listos
                ready_process.delete('1.0', "end")
                for process in ready_list:
                    ready_process.insert("end", "ID: " + str(process.id) + " Tiempo máximo estimado: " + str(
                        process.estimated_time) + " Tiempo Transcurrido: " + str(process.TTE) + "\n")
                delete_and_update_table(page_table.page_array)
                # Actualiza el cuadro de proceso en ejecución
                executing_process.delete('1.0', "end")
                executing_process.insert("end", process_to_show)

        # Se termina un proceso porque su tiempo restante es 0
        elif process_to_show.TRE == 0:
            # Cuando se genera un proceso nuevo, se actualiza la lista de procesos listos y el contador de procesos nuevos
            if is_generated_new_process:
                new_process_title.config(text=f"Nuevos: {len(new_list)}")
                ready_process.delete('1.0', "end")
                for process in ready_list:
                    ready_process.insert("end", "ID: " + str(process.id) + " Tiempo máximo estimado: " + str(
                        process.estimated_time) + " Tiempo Transcurrido: " + str(process.TTE) + "\n")
                # Se regresa la bandera a falso
                is_generated_new_process = False
            # Se actualiza la lista de procesos terminados
            if not process_to_show in finished_process_list:
                process_to_show.finishing_time = global_counter
                finished_process_list.append(process_to_show)
                page_table.delete_process(process_to_show.id)
                finished_process_show(finished_process_list, finished_process)

            # Si la cola de listos no está vacía, se saca el siguiente proceso
            if len(ready_list) != 0:
                process_to_show = ready_list.pop(0)
                if process_to_show.response_flag == False:
                    process_to_show.response_time = global_counter - process_to_show.start_time
                    process_to_show.response_flag = True

                # Actualiza el estado en la tabla de paginación
                page_table.change_state(process_to_show.id, 'En ejecución')
                # Actualiza la tabla de paginación
                delete_and_update_table(page_table.page_array)
                if len(new_list) > 0:
                    # insert_process_in_table(new_list[0])
                    # Trata de insertar el primer elemento de la lista de nuevos en la tabla de paginación
                    insert_process_in_table(new_list[0])
                    # Actualiza el banner del siguiente proceso en la lista de nuevos
                    if len(new_list) > 0:
                        next_process.config(
                            text=f"Siguiente proceso: ID({new_list[0].id}) Tamaño({new_list[0].size})")
                    else:
                        next_process.config(
                            text=f"Siguiente proceso: ID() Tamaño()")

                    # Actualiza gráficamente la tabla de paginación
                    delete_and_update_table(page_table.page_array)
                    # Actualiza el banner de la cantidad de procesos nuevos
                    new_process_title.config(text=f"Nuevos: {len(new_list)}")
                 # Imprime el nuevo proceso a ejecutar
                executing_process.insert("end", process_to_show)

                # Si hay uno o más procesos en la cola de procesos nuevos, añade el primero a la cola de listos
                if len(new_list) > 0:
                    # Establece el tiempo de inicio del proceso nuevo
                    insert_process_in_table(new_list[0])

                # Actualiza el contador de la cola de procesos nuevos
                new_process_title.config(text=f"Nuevos: {len(new_list)}")
                # Actualiza el banner de siguiente proceso
                if len(new_list) > 0:
                    next_process.config(
                        text=f"Siguiente proceso: ID({new_list[0].id}) Tamaño({new_list[0].size})")
                else:
                    next_process.config(
                        text=f"Siguiente proceso: ID() Tamaño()")

                # Reimprime la lista de procesos nuevos
                ready_process.delete('1.0', "end")
                for process in ready_list:
                    ready_process.insert("end", "ID: "+str(process.id)+" Tiempo máximo estimado: "+str(
                        process.estimated_time)+"Tiempo Transcurrido: " + str(process.TTE) + "\n")

                # Actualiza la lista de procesos terminados
                finished_process_show(finished_process_list, finished_process)
            else:
                # Si todos los procesos han terminado
                if (len(finished_process_list) == number_of_processes):
                    # Actualiza la lista de procesos terminados, para añadir el último proceso a dicha lista
                    finished_process_show(
                        finished_process_list, finished_process)
                    # Muestra el BCP
                    for widget in window.winfo_children():
                        widget.destroy()
                    bcp(window, global_counter)
                # Si la cola de listos no tiene procesos, y la cola de nuevos tampoco, todos los procesos se encuentran bloqueados
                elif (len(blocked_list) != 0) and len(new_list) == 0:
                    # Cuando se genera un proceso nuevo, se actualiza la lista de procesos listos y el contador de procesos nuevos
                    if is_generated_new_process:
                        new_process_title.config(
                            text=f"Nuevos: {len(new_list)}")
                        ready_process.delete('1.0', "end")
                        for process in ready_list:
                            ready_process.insert("end", "ID: " + str(process.id) + " Tiempo máximo estimado: " + str(
                                process.estimated_time) + " Tiempo Transcurrido: " + str(process.TTE) + "\n")
                        # Se regresa la bandera a falso
                        is_generated_new_process = False
                    # Llama recursivamente cada segundo a la funcion finishes_remaining_blocked_process que se encarga de terminar la ejecución de un proceso
                    # bloqueado para salir de este estado
                    blocked_processes.after(
                        1000, lambda: finishes_remaining_blocked_process(blocked_processes))
                    # Actualiza el contador global
                    global_counter += 1
                    global_counter_container.config(
                        text=f"Contador global: {global_counter}")
                    # Checa si el primer proceso de la lista de bloqueado haya terminado su tiempo de bloqueo
                    if blocked_list[0].blocked_time == 8:
                        blocked_processes.delete('1.0', "end")
                        # Reestablece su valor de tiempo de bloqueado a 0 para que se pueda volver a bloquear
                        blocked_list[0].blocked_time = 0
                        # Actualiza su estado en la tabla de paginación
                        page_table.change_state(blocked_list[0].id, 'Listo')
                        # Agrega el proceso a la cola de listos
                        ready_list.append(blocked_list.pop(0))
                        # Restaura el proceso a un proceso no nulo
                        process_to_show.null_process = False
                        # Agrega el proceso a ejecución
                        process_to_show = ready_list.pop()
                        # Actualiza el recuadro de GUI
                        executing_process.insert("end", process_to_show)
                        # Actualiza la tabla de paginación
                        delete_and_update_table(page_table.page_array)
                        # Evita que se siga llamando recursivamente a la función finishes_remaining_blocked_process
                        blocked_processes.after_cancel(blocked_processes)
                    else:
                        blocked_processes.delete('1.0', "end")
                        for process in blocked_list:
                            blocked_processes.insert(
                                "end", "ID: "+str(process.id)+" Tiempo bloqueado: "+str(process.blocked_time)+"\n")
                # Si la cola de listos está vacía pero la cola de nuevos no está vacía se obtiene el primer dato de la cola de nuevos como proceso en ejecución
                elif len(blocked_list) != 0 and len(new_list) != 0:
                    page_table.change_state(blocked_list[0].id, 'Bloqueado')
                    delete_and_update_table(page_table.page_array)
                    # Cuando se genera un proceso nuevo, se actualiza la lista de procesos listos y el contador de procesos nuevos
                    if is_generated_new_process:
                        new_process_title.config(
                            text=f"Nuevos: {len(new_list)}")
                        ready_process.delete('1.0', "end")
                        for process in ready_list:
                            ready_process.insert("end", "ID: " + str(process.id) + " Tiempo máximo estimado: " + str(
                                process.estimated_time) + " Tiempo Transcurrido: " + str(process.TTE) + "\n")
                        # Se regresa la bandera a falso
                        is_generated_new_process = False
                    # Añade el proceso a cola de listos
                    ready_list.append(new_list.pop(0))
                    # Convierte el proceso en el proceso a ejecutar
                    process_to_show = ready_list.pop()
                    # Establece el tiempo de incio y el tiempo de respuesta
                    process_to_show.start_time = global_counter
                    process_to_show.response_time = global_counter - process_to_show.start_time
                    process_to_show.response_flag = True

        elif process_to_show.transcurred_quantum == process_to_show.quantum:
            process_to_show.transcurred_quantum = 0
            ready_list.append(process_to_show)
            process_to_show = ready_list.pop(0)
            if not process_to_show.response_flag:
                process_to_show.response_flag = True
                process_to_show.response_time = global_counter - process_to_show.start_time
    else:
        if is_bcp_called:
            window2 = ttk.Window(title='Bloque de control de procesos')
            window2.state('zoomed')
            bcp(window2, global_counter)
            is_bcp_called = False
        # Si está pausado entonces se mantiene el proceso en pantalla
        executing_process.insert("end", process_to_show)


def finished_process_show(finished_process_list, finished_process):
    finished_process.delete('1.0', "end")
    for finished in finished_process_list:  # Imprime la lista de finalizados
        if not finished.error:
            # Si no terminó por error se calculan los tiempos
            finished.calculate_times()
            finished_process.insert("end", f"ID: " + str(finished.id) + " Operación: " + str(finished.first_data) +
                                    finished.operation + str(finished.second_data) + " Resultado: " + str(finished.operate(error=False)) + "\n\n")
        else:
            # Si terminó por error el tiempo de servicio será igual al tiempo que estuvo en ejecución
            finished.service_time = finished.TTE
            # Calcula los tiempos
            finished.calculate_times()
            finished_process.insert("end", f"ID: " + str(finished.id) + " Operación: " + str(finished.first_data) +
                                    finished.operation + str(finished.second_data) + " Resultado: " + str(finished.operate(error=True)) + "\n\n")


def on_key_release(event):
    global is_paused
    global process_to_show
    global is_interrupted
    global is_generated_new_process
    global is_bcp_called
    global global_counter

    if event.keysym == 'p' and not is_paused:
        is_paused = True
    elif event.keysym == 'c':
        is_paused = False
    elif event.keysym == 'e' and not is_paused:
        process_to_show.TRE = 0
        process_to_show.error = True
    elif event.keysym == 'i' and not is_paused:
        is_interrupted = True
        process_to_show.transcurred_quantum = 0
    elif event.keysym == 'n' and not is_paused:
        generate_new_process(global_counter)
        is_generated_new_process = True
    elif event.keysym == 'b' and not is_paused:
        is_paused = True
        is_bcp_called = True
    elif event.keysym == 't' and not is_paused:
        is_paused = True


def generate_new_process(global_counter):
    global new_list
    global ready_list
    global blocked_list
    global number_of_processes
    global quantum_size
    global page_table
    global page_table_object

    # Genera todos los datos necesarios para un nuevo proceso
    ID = number_of_processes
    number_of_processes += 1
    first_data = rd.randint(0, 10000)
    second_data = rd.randint(0, 10000)
    estimated_time = rd.randint(6, 18)
    size = rd.randint(6, 26)
    if second_data == 0:
        operation_list = ['+', '-', '*']
    else:
        operation_list = ['+', '-', '*', '/', '%']
    operation = rd.choices(operation_list)
    operation = operation[0]
    # Crea el nuevo proceso
    process = Process(operation, first_data, second_data,
                      estimated_time, ID, quantum_size, size)

    # Checa que haya espacio suficiente para almacenar el proceso en la tabla de paginación
    if len(new_list) == 0:
        if page_table.count_free_pages() >= process.page_number:
            # Se crea una copia del tamaño del proceso
            size = process.size
            # Se guarda el valor del contador global en el tiempo de inicio del proceso
            process.start_time = global_counter
            # Se añade el proceso a la lista de procesos listos
            ready_list.append(process)
            # Busca en todos los procesos aquellos espacios libres
            for i in range(0, 41):
                # Si el tamaño aún no es cero
                if size > 0:
                    # Busca si esa posición en la tabla de paginación está sin ocupar
                    if page_table.page_array[i][3] == 'Libre':
                        # En caso de que esté desocupada y el tamaño es mayor o igual a 5
                        if size >= 5:
                            # Sustituye el valor con los datos del proceso
                            page_table.page_array.pop(i)
                            page_table.page_array.insert(
                                i, [i, '5/5', process.id, 'Listo'])
                        # En caso de que esté desocupado el espacio y el tamaño sea menor a 5, se añade el tamaño final
                        else:
                            page_table.page_array.pop(i)
                            page_table.page_array.insert(
                                i, [i, f'{size}/5', process.id, 'Listo'])
                        size -= 5
                # Cuando el tamaño es menor a 0, el proceso ha sido totalmente capturado
                else:
                    break
            # Se actualiza la tabla de paginación
            delete_and_update_table(page_table.page_array)
        # En dado caso que no exista suficiente espacio, el proceso se añade a la lista de nuevos
        else:
            new_list.append(process)
    else:
        new_list.append(process)


def bcp(window, global_counter):
    global blocked_list
    global ready_list
    global process_to_show
    global finished_process_list
    global new_list

    window.bind("<KeyRelease>", second_key_release)

    if len(blocked_list) > 0:
        table = ttk.Treeview(window, columns=('ID', 'Operación', 'Resultado', 'Tiempo Inicio', 'Tiempo Finalización', 'Tiempo Servicio',
                             'Tiempo Espera', 'Tiempo Retorno', 'Tiempo Respuesta', 'Tiempo Restante CPU', 'Tiempo Restante'), show='headings')
    else:
        table = ttk.Treeview(window, columns=('ID', 'Operación', 'Resultado', 'Tiempo Inicio', 'Tiempo Finalización',
                             'Tiempo Servicio', 'Tiempo Espera', 'Tiempo Retorno', 'Tiempo Respuesta', 'Tiempo Restante CPU'), show='headings')

    # Formato de columnas
    table.column('ID', anchor=tk.CENTER)
    table.column('Operación', anchor=tk.CENTER)
    table.column('Resultado', anchor=tk.CENTER)
    table.column('Tiempo Inicio', anchor=tk.CENTER)
    table.column('Tiempo Finalización', anchor=tk.CENTER)
    table.column('Tiempo Servicio', anchor=tk.CENTER)
    table.column('Tiempo Espera', anchor=tk.CENTER)
    table.column('Tiempo Retorno', anchor=tk.CENTER)
    table.column('Tiempo Respuesta', anchor=tk.CENTER)
    table.column('Tiempo Restante CPU', anchor=tk.CENTER)
    if len(blocked_list) > 0:
        table.column('Tiempo Restante', anchor=tk.CENTER)

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
    table.heading('Tiempo Restante CPU', text='TR CPU')
    if len(blocked_list) > 0:
        table.heading('Tiempo Restante', text='TR Bloqueo')
    table.pack(fill='both', expand=True)

    # Checa que el proceso en ejecución no esté en la lista de bloqueados ni en la lista de procesos finalizados
    if process_to_show not in blocked_list and process_to_show not in finished_process_list:
        # El tiempo en servicio se actualiza al valor actual del tiempo transcurrido
        process_to_show.service_time = process_to_show.TTE
        # Se calcula el tiempo en espera
        process_to_show.waiting_time = global_counter - \
            process_to_show.start_time - process_to_show.TTE
        # Establece el formato de valores
        if len(blocked_list) > 0:
            table.insert(parent='', index=tk.END, values=(
                '-', '-', '-', '-', '-', 'PROCESO EN EJECUCION', '-', '-', '-', '-', '-'))
            values = (process_to_show.id, process_to_show.serializeOperation(), ' ', process_to_show.start_time, ' ', process_to_show.service_time,
                      process_to_show.waiting_time, process_to_show.return_time, process_to_show.response_time, process_to_show.TRE, ' ')
        else:
            table.insert(parent='', index=tk.END, values=(
                '-', '-', '-', '-', 'PROCESO EN EJECUCION', '-', '-', '-', '-', '-'))
            values = (process_to_show.id, process_to_show.serializeOperation(), ' ', process_to_show.start_time, ' ', process_to_show.service_time,
                      process_to_show.waiting_time, process_to_show.return_time, process_to_show.response_time, process_to_show.TRE)
        table.insert(parent='', index=tk.END, values=values)

    # Si hay procesos finalizados los inserta en la tabla
    if len(finished_process_list) != 0:
        if len(blocked_list) > 0:
            table.insert(parent='', index=tk.END, values=(
                '-', '-', '-', '-', '-', 'PROCESOS FINALIZADOS', '-', '-', '-', '-', '-'))
        else:
            table.insert(parent='', index=tk.END, values=(
                '-', '-', '-', '-', 'PROCESOS FINALIZADOS', '-', '-', '-', '-', '-'))
        for process in finished_process_list:
            # El tiempo en servicio se actualiza al valor actual del tiempo transcurrido
            process_to_show.service_time = process_to_show.TTE
            # Establece el formato de valores
            if len(blocked_list) > 0:
                values = (process.id, process.serializeOperation(), process.result, process.start_time, process.finishing_time,
                          process.service_time, process.waiting_time, process.return_time, process.response_time, ' ', ' ')
            else:
                values = (process.id, process.serializeOperation(), process.result, process.start_time, process.finishing_time,
                          process.service_time, process.waiting_time, process.return_time, process.response_time, ' ')
            table.insert(parent='', index=tk.END, values=values)

    # Si hay procesos listos los inserta en la tabla
    if len(ready_list) != 0:
        if len(blocked_list) > 0:
            table.insert(parent='', index=tk.END, values=(
                '-', '-', '-', '-', '-', 'PROCESOS LISTOS', '-', '-', '-', '-', '-'))
        else:
            table.insert(parent='', index=tk.END, values=(
                '-', '-', '-', '-', 'PROCESOS LISTOS', '-', '-', '-', '-'))
        for process in ready_list:
            # El tiempo en servicio se actualiza al valor actual del tiempo transcurrido
            process.service_time = process.TTE
            # El valor de tiempo de espera se actualiza al valor del contador global - tiempo de inicio - tiempo de servicio
            process.waiting_time = global_counter - process.start_time - process.TTE
            if len(blocked_list) > 0:
                values = (process.id, process.serializeOperation(), ' ', process.start_time, ' ', process.service_time,
                          process.waiting_time, process.return_time, process.response_time, process.TRE, 0)
            else:
                values = (process.id, process.serializeOperation(), ' ', process.start_time, ' ', process.service_time,
                          process.waiting_time, process.return_time, process.response_time, process.TRE)
            table.insert(parent='', index=tk.END, values=values)

    # Si hay procesos bloqueados los inserta en la tabla
    if len(blocked_list) != 0:
        table.insert(parent='', index=tk.END, values=(
            '-', '-', '-', '-', '-', 'PROCESOS BLOQUEADOS', '-', '-', '-', '-', '-'))
        for process in blocked_list:
            # El tiempo en servicio se actualiza al valor actual del tiempo transcurrido
            process.service_time = process.TTE
            # El valor de tiempo de espera se actualiza al valor del contador global - tiempo de inicio - tiempo de servicio
            process.waiting_time = global_counter - process.start_time - process.TTE
            values = (process.id, process.serializeOperation(), ' ', process.start_time, ' ', process.service_time,
                      process.waiting_time, process.return_time, process.response_time, process.TRE, 8 - process.blocked_time)
            table.insert(parent='', index=tk.END, values=values)

    if len(new_list) != 0:
        if len(blocked_list) > 0:
            table.insert(parent='', index=tk.END, values=(
                '-', '-', '-', '-', '-', 'PROCESOS NUEVOS', '-', '-', '-', '-', '-'))
        else:
            table.insert(parent='', index=tk.END, values=(
                '-', '-', '-', '-', 'PROCESOS NUEVOS', '-', '-', '-', '-'))
        for process in new_list:
            values = (process.id, process.serializeOperation(), ' ',
                      ' ', ' ', ' ', ' ', ' ', ' ', process.TRE, ' ')
            table.insert(parent='', index=tk.END, values=values)


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
        blocked_processes.delete('1.0', "end")
        for process in blocked_list:
            # Incrementa el tiempo de bloqueo
            process.blocked_time += 1
            blocked_processes.insert(
                "end", "ID: "+str(process.id)+" Tiempo bloqueado: "+str(process.blocked_time)+"\n")


def delete_and_update_table(new_values):
    global page_table_object
    # Elimina todos los datos en la tabla de paginación
    for i in page_table_object.get_children():
        page_table_object.delete(i)
    # Los sustituye con los nuevos valores de la tabla de paginación
    for i in range(0, 45):
        page_table_object.insert(parent='', index=tk.END, values=new_values[i])


assignation()
