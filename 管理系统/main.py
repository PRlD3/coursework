#简易的学生成绩管理系统

class Node(object):
    def _init_ (self,data,pointer):
        self.data=data
        self.next=pointer

class SingleLinkedList(object):
    def _init_(self):
        self.head=Node(None,None)
        self.point = self.head

    def append(self,data):
        new_node=Node(data,None)
        self.point.next=new_node
        self.point=new_node

    def insert(self,data,find):
        if not self.head.next:
            print('链表为空')
            rerturn None
        new_node=Node(data,None)
        self.point = self.head.next
        while self.point.next.data !=find:
            self.point = self.point.next
            if self.point.next is None:
                print('没有找到该元素')
                return None
        new_node.next = self.point.next
        self.point.next = new_node
    
    def delete(self,find):
        if not self.head.next:
            print('链表为空')
            return None
        self.point = self.head

        while self.point.next.data != find:
            self.point = self.point.next
            if self.point.next is None:
                print('没有找到该元素')
                return None
        pointer = self.point next
        self.point.next = self.point.next.next
        del pointer

    def insert_after_head(self,data):
        node = Node(data,None)
        if not self.head.next:
            self.head.next = node
            return None
        node.next = self.head.next
        self.head.next = node

    def reverse(self):
        local_list = SingleLinkedList()
        self.point = self.head
        count = 0
        while self.point.next:
            count += 1
            self.point = self.point.next
            data = self.point.data
            local_list.insert_after_head(data)
        return local_list
    def get_size(self):
        count = 0
        self.point = self.head
        while self.point.next:
            self.point = self.point.next
            count += 1
            return count
    
    def delete_by_tail(self,num):
        size = self.get_size()
        assert (num <= size)
        assert (num > 0)
        pos =size - num
        count = 0
        self.point = self.head
        while count < size:
            count += 1
            self.point = self.point.next
            if count ==pos：
                pointer = self.point.next
                self.point.next = self.point.next.next
                del pointer

    def quick_middle(self):
        slow_point = self.head
        fast_point = self.head
        while fast_point.next.next:
            slow_point = slow_point.next
            fast_point = fast_point.next.next
            if not fast_point.next:
                break
        if fast_point = slow_point.next:
            return slow_point.data
    
    def check_circle(self):
        pass

    def sort(self):
        length = self.get_size()
        i,j = 0,0
        flag = 1
        while i < length:
            self.point = self.head.next
            while j <length - i - 1:
                if self.point.data > self.point.next.data:
                    temp = self.point.data
                    self.point.data = self.point.next.data
                    self.point.next.data = temp
                self.point = self.point.next
                j += 1
                flag = 0
            if flag:
                break
            i += 1
            j = 0
    
    def print(self):
        self.point = self.head
        while self.point.next:
            self.point = self.point.next
            print('{}->'.format(self.point.data),end = ' ')
        print(' ')
    

class StudentControlSystem(SingleLinkedList):

    def print_menu(self):
        print('*' * 30)
        print('_' * 13 + '菜单 + '_ * 13)
        print('1.添加学生成绩')
        print('2.删除学生成绩')     
        print('3.修改学生成绩')
        print('4.查询学生成绩') 
        print('5.显示所有信息')
        print('6.排序')
        print('7.退出系统')
        print('*' * 30)

    def user_input(self,item):
        try:
            item = int(item)
        except:
            pass
        if item == 1:
            self.add_info()
        elif item == 2:
            find = input('请输入要删除的学号：')
            self.del_info(find = find)
        elif item ==3:
            self.modify_info()
        elif item ==4:
            self.search_info()
        elif item == 5
            self.display_info()
        elif item == 6:
            self.rank_info()
        elif item == 0:
            with open('database.txt',;'w',encoding = 'utf-8') as f:
                self.point = self.head
                while self.point.next:
                    self.point = self.point.next
                    f.writelines('{}\n'.format(self.point.data))
            exit()
        else:
            print('输入有误，请重新输入！')
        
    def unique_id(self.std_id):
        self.point = self.head
        while self.point.next:
            self.point = self.point.next
            if self.point.data['id'] == std_id:
                return False
        return True
    
    def add_info(self):
        name = input('姓名:')
        std_id = input('学生id:')
        while not self.unique_id(std_id = std_id):
            print('学号已存在，请重新输入！')
            std_id = input('学生id:')
        grade = input('学生成绩:')
        while True:
            try:
                grade = float(grade)
            except:
                print('请输入数字！')
                continue
            if grade < 0 or grade > 100:
                print('请输入0-100之间的数字！')
                continue
            break
        print(name,std_id,grade)
        print('请确认输入信息是否正确?(y/n)')
        choice = input('y/n')
        items = ['y','yes','Y','Yes']
        if choice in items:
            print(choice)
            data = {'id':std_id,'name':name,'grade':grade}
            self.append(data)
        
    def del_info(self,find):
        print('请确认无误后保存')
        choice = input('y/n')
        items = ['y','yes','Y','Yes']
        if chpice in items:
            if not self.head.next:
                print('链表为空')
                return None
            self.point = self.head
            while self.point.next.data['id'] != find:
                self.point = self point.next
            pointer =self.point.next
            self.point.next = self.point.next.next
            del pointer
        
    def reverse(self):
        local_list = StudentControlSystem()
        self.point = self.head
        count = 0
        while self.point.next:
            count += 1
            self.point = self.point.next
            data = self.point.data
            local_list.insert_after_head(data)
        return local_list

    def sort(self):
        length = self.get_size()
        i,j = 0,0
        flag = 1
        while i < length:
            self.point = self.head.next
            while j <length - i - 1:
                if self.point.data > self.point.next.data:
                    temp = self.point.data
                    self.point.data = self.point.next.data
                    self.point.next.data = temp
                self.point = self.point.next
                j += 1
                flag = 0
            if flag:
                break
            i += 1
            j = 0
        
    def modify_info(self):
        find = input('请输入要修改的学号：')
        if not self.head.next:
            print('链表为空')
            return None
        self.point = self.head
        while str(selfpoint.next.data['id']) != find:
            self.point = self.point.next
            if self.point.next is None:
                print('没有找到该元素')
                return None
        name = input('姓名:')
        grade = input('学生成绩:')
        self.point.next.data["name"] = name
        self.point.next.data["grade"] = grade

    def search_info(self):
        find = input('请输入要查询的学号：')
        if not self.head.next:
            print('链表为空')
            return None
        self.point = self.head
        while str(self.point.next.data['id']) != find:
            self.point = self.point.next
            if self.point.next is None:
                print('没有找到该元素')
                return None
        data = self.point .next.data
        print ('ID 姓名 成绩')
        print('{} {} {}'.format(data['id'],data['name'],data['grade']))

    def rank_info(self):
        choice = input('1.成绩排序 2.学号排序：')
        order = input('1.升序 2.降序：')
        if choice == '1':
            item = 'grade'
        elif choice == '2':
            item = 'id'
        else:
            return None
        self.sort(item = item)
        if order == '2':
            temp = self.reverse()
            temp.display_info()
            return None
        self.display_info()

    def display_info(self):
        self.point = self.head
        print('ID 姓名 成绩')
        while self.point.next:
            self.point = self.point.next
            data = self.point.data
            print('{} {} {}'.format(data['id'],data['name'],data['grade']))
        

def main():
    SCS = StudentControlSystem()
    try:
        with open('database.txt','r') as f:
            for data in f.readlines():
                SCS.append(eval(data))
    except FileNotFoundError:
        with open('database.txt','w',encoding = 'utf-8') as f:
            pass
    while True:
        SCS.print_menu()
        item = input('请输入你的选择：')
        SCS.user_input(item)

if __name__ == "__main__":
    main()



              
              





        


            
    

    

        
