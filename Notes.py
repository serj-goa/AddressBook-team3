from collections import UserDict


class Notes(UserDict):
    def tag() -> str:
        while True:
            add_tag = input('Some tag(y/n): ')
            
            if add_tag.lower() == 'y':
                tag = input('Please enter tag: ')
                break
            
            elif add_tag.lower() == 'n':
                tag = 'unknown'
                break
           
            else:
                print('Unexpected enter. Please try again\n')
        return tag        
    
    def create_notice(self, notice: list) -> None:
        tag = Notes.tag()
        if tag not in self.data:
            self.data[tag] = [notice[1]]
            print(f'"{notice[1]}" was added successfully!\n')
        else:
            self.data[tag].append(notice[1])
            print(f'"{notice[1]}" was added successfully!\n')

    
    def upd_notice(self, notice: list) -> None:
        tag = Notes.tag()
        if tag in self.data and self.data.get(tag):
           
            for note in self.data[tag]:
                print (f'Notice {self.data[tag].index(note)}: {note}')
            
            while True:
                number = input('Enter number of notice should be updated: ')
                
                if type(int(number)) == int and 0 <= int(number) < len(self.data[tag]):
                    self.data[tag][int(number)] = notice[1]
                    print (f'Notice: "{self.data[tag][int(number)]}" is updeted successfully!\n')
                    break
                
                else:
                    print('Wrong input!\n')
        
        elif tag in self.data and len(self.data.get(tag)) == 0:
            print('There are no notices\n')
        
        else:
            print(f'Relevant data wasn\'t found\n')

    def del_notice(self, number: str) -> None:
        tag = Notes.tag()
        if tag in self.data and self.data.get(tag):
            for i in range(len(self.data[tag])):
                print (f'Notice {i}: {self.data[tag][i]}')
            
            while True:
                number = input('Enter number of notice should be removed: ')
                
                if type(int(number)) == int and 0 <= int(number) < len(self.data[tag]):
                    print(f'Notice: "{self.data[tag].pop(int(number))}" was removed successfully!\n')
                    break
                
                else:
                    print('Wrong input!\n')
        
        elif tag in self.data and len(self.data.get(tag)) == 0:
            print('There are no notices\n')
       
        else:
            print(f'Relevant data wasn\'t found\n')
        
    def search_notice(self, notice: str) -> None:
        flag = True
        for note in self.data.values():
            
            for i in note:
                
                if notice[1] in i:
                    flag = False
                    print(i)
        if flag:
            print('Relevant data wasn\'t found\n')

    def search_tag(self, tag: str) -> None:
        tag=Notes.tag()
        if tag in self.data and self.data[tag]:
            counter = 0
            
            for notice in self.data[tag]:
                counter += 1
                print(f'Notice {counter}: "{notice}"')
        
        elif tag in self.data and bool(self.data[tag])==False:
            print('There are no notices\n')
        
        else:
            print(f'Relevant data wasn\'t found\n')
    
    def sorted(self, order: list) -> None:
        if order[1].lower() != 'asc' and order[1].lower() != 'desc':
            print('Only "asc" and "desc" order is available\n')
            return None

        tag = Notes.tag()
        if tag in self.data and self.data[tag]:
            counter = 0
            
            if order[1].lower() == 'asc':
                for notice in sorted(self.data[tag]):
                    counter += 1
                    print(f'Notice {counter}: "{notice}"')
            else:
                for notice in sorted(self.data[tag], reverse=True):
                    counter += 1
                    print(f'Notice {counter}: "{notice}"')    

            
        elif tag in self.data and bool(self.data[tag]) == False:
            print('There are no notices\n')
       
        else:
            print(f'Relevant data wasn\'t found\n')


if __name__ == '__main__':
    p = Notes()
    p.create_notice('1zert anoterdfg', 'a')
    # print(p)
    p.create_notice('gert anoterdfg', 'a')
    print(p)
    p.create_notice('notice')
    # print(p)
    p.create_notice('hnotice')
    # print(p)
    p.add_notice('r', 'a')
    print(p)

    print(p.add_notice('p', 'a'))
    p.add_notice('as')
    print(p)
    p.search_tag('a')
    print()
    p.sorted('a')
    #p.upd_notice('a', 0, '123')
    # print(p)
    # p.del_notice(0)
    # print(p)
    p.search_notice('noter')
