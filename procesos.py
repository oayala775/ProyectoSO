class Process:
    def __init__(self, operation, first_data, second_data, estimated_time, id, belonging_batch):
        self.operation = operation
        self.first_data = first_data
        self.second_data = second_data
        self.estimated_time = estimated_time
        self.id = id
        self.TRE = estimated_time
        self.TTE = 0
        self.belonging_batch = belonging_batch
        self.result = 0
    
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
            result = self.first_data + self.second_data
            return result
        elif self.operation == '-' and not error:
            result = self.first_data - self.second_data
            return result
        elif self.operation == '*' and not error:
            result = self.first_data * self.second_data
            return result
        elif self.operation == '/' and not error:
            result = self.first_data/self.second_data
            result = float(result)
            return result
        elif self.operation == '%' and not error:
            result = self.first_data%self.second_data
            result = float(result)
            return result
        elif error == True:
            result = "ERROR"
            return result
        
    def __eq__(self,other):
        return self.id == other.id
        
    