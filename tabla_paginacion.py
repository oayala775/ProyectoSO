class PageTable:
    def __init__(self):
        self.size = 45
        self.page_array = []
        
        for i in range(0,41):
            self.page_array.append([i,'0/5','','Libre'])
        
        for i in range(41,45):
            self.page_array.append([i,'5/5','','SO'])      
            
    def count_free_pages(self):
        count = 0
        for page in self.page_array:
            if page[3] == 'Libre':
                count += 1
        return count
    
    def __str__(self):
        string = ''
        for i in range(0,45):
            string += str(self.page_array[i]) + '\n'
        return string
    
    def change_state(self, id,state):
        for i in range(0,45):
            if self.page_array[i][2] == id:
                self.page_array[i][3] = state
                
    def delete_process(self,id):
        for i in range(0,45):
            if self.page_array[i][2] == id:
                self.page_array[i][3] = 'Libre'
                self.page_array[i][1] = '0/5'
                self.page_array[i][2] = ''
                
    def search_free_page(self):
        for i in range(0,45):
            if self.page_array[i][3] == 'Libre':
                return i
            
    # def insert_item(self, position):
    #     self.page_array[position][2] 