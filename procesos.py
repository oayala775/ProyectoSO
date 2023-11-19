class Process:
    def __init__(self, operation, first_data, second_data, estimated_time, id, quantum, size):
        self.operation = operation
        self.first_data = first_data
        self.second_data = second_data
        self.estimated_time = estimated_time
        self.id = id
        self.TRE = estimated_time
        self.TTE = 0
        self.result = 0
        self.error = False
        self.blocked_time = 0
        self.null_process = False
        self.start_time = 0
        self.finishing_time = 0
        self.return_time = 0
        self.response_time = 0
        self.response_flag = False
        self.waiting_time = 0
        self.service_time = self.TTE
        self.quantum = quantum
        self.transcurred_quantum = 0
        self.size = size
        self.page_number = self.size // 5
        self.page_decimal = self.size % 5
        if self.page_decimal != 0:
            self.page_number += 1

    def __str__(self):
        return f"""ID:{self.id}
Operación: {self.first_data}{self.operation}{self.second_data}
Tiempo estimado: {self.estimated_time}s 
Tiempo restante por ejecutar: {self.TRE}
Tiempo transcurrido: {self.TTE}
Quantum ejecutado: {self.transcurred_quantum}
Tamaño: {self.size}"""
    
    def operate(self,error):
        if self.operation == '+' and not error:
            self.result = self.first_data + self.second_data
            return self.result
        elif self.operation == '-' and not error:
            self.result = self.first_data - self.second_data
            return self.result
        elif self.operation == '*' and not error:
            self.result = self.first_data * self.second_data
            return self.result
        elif self.operation == '/' and not error:
            self.result = self.first_data/self.second_data
            self.result = float(self.result)
            return self.result
        elif self.operation == '%' and not error:
            self.result = self.first_data%self.second_data
            self.result = float(self.result)
            return self.result
        elif error == True:
            self.error = error
            self.result = "ERROR"
            return self.result
        
    def __eq__(self,other):
        return self.id == other.id
    
    def calculate_times(self):
        self.service_time = self.TTE
        self.return_time = self.finishing_time - self.start_time
        self.waiting_time = self.return_time - self.service_time
        
    def serializeOperation(self):
        string =  f"{self.first_data} {self.operation} {self.second_data}"
        return string
    