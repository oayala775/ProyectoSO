class Process:
    def __init__(self, programmer_name, operation, first_data, second_data, estimated_time, id, belonging_batch):
        self.programmer_name = programmer_name
        self.operation = operation
        self.first_data = first_data
        self.second_data = second_data
        self.estimated_time = estimated_time
        self.id = id
        self.TRE = estimated_time
        self.TTE = 0
        self.belonging_batch = belonging_batch
    
    # def __init__(self):
    #     print("Class created")
    def __str__(self):
        return f"""Nombre del programador: {self.programmer_name}
ID:{self.id}
Operación: {self.first_data}{self.operation}{self.second_data}
Tiempo estimado: {self.estimated_time}s 
Tiempo restante por ejecutar: {self.TRE}
Tiempo transcurrido: {self.TTE}"""
    
    def operate(self):
        if self.operation == '+':
            return self.first_data + self.second_data
        elif self.operation == '-':
            return self.first_data - self.second_data
        elif self.operation == '*':
            return self.first_data * self.second_data
        elif self.operation == '/':
            return self.first_data/self.second_data
        elif self.operation == '%':
            return self.first_data%self.second_data
        
    def __eq__(self,other):
        return self.id == other.id
        
    