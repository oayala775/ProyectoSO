class Process:
    def __init__(self, operation, first_data, second_data, estimated_time, id):
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
        self.service_time = estimated_time
        
    
    # def __init__(self):
    #     print("Class created")
    def __str__(self):
        return f"""ID:{self.id}
Operación: {self.first_data}{self.operation}{self.second_data}
Tiempo estimado: {self.estimated_time}s 
Tiempo restante por ejecutar: {self.TRE}
Tiempo transcurrido: {self.TTE}"""
    
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
        self.return_time = self.finishing_time - self.start_time
        self.waiting_time = self.return_time - self.service_time
        
    def serializeOperation(self):
        string =  f"{self.first_data} {self.operation} {self.second_data}"
        return string
    