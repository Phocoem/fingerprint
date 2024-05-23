from tkinter import *
from tkinter import ttk
import tkinter as tk
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from datetime import datetime
from pymodbus.client.serial import ModbusSerialClient
from time import sleep
from datetime import datetime
import mysql.connector
from tkcalendar import DateEntry

master = ModbusSerialClient(port= "COM5", Framer="RTU", baudrate= 9600, bytesize = 8, parity= "N",stopbits= 1,strict=True)
master.connect()

messagevantay =False
modbus_data=[]
 

def dongho():
# Lấy thời gian hiện tại
    thoigian = datetime.now().strftime("%H:%M:%S %p")
# Cập nhật nhãn thời gian với thời gian hiện tại
    time_label.config(text=thoigian)
# Gọi hàm này mỗi giây để cập nhật thời gian
    time_label.after(1000, dongho)

database=mysql.connector.connect(user='root', password='123456',host='localhost', database='qlnv')

# #Lấy dữ liệu từ database vừa kết nối
# dulieu='select * from quanlynhanvien'
# show=database.cursor()
# show.execute(dulieu)
# rows=show.fetchall()
# def save():  #ok

# 	dulieu='select * from quanlynhanvien'
# 	show.execute(dulieu)
# 	result = show.fetchall()  	#chọn và nạp dữ liệu từ con trỏ       
# 	return result
# def update():
#     item=danhsach.get_children()
#     for eachItem in item :
#         danhsach.delete(eachItem)
#     data=save()
#     for i in data:
#         danhsach.insert("","end",iid=i[0],values=i)
window = Tk()
#khai báo
MS= StringVar()
ten= StringVar()
gioitinh= StringVar()
vitri =StringVar()
vantay=StringVar()
window.title("Nhóm 2/3")
window.geometry("1540x800")
title=Label(window,bd=20,relief=RIDGE, text="QUẢN LÝ BẰNG VÂN TAY", fg="red",bg="white",font=("arial",50,"bold") )
title.pack(side=TOP,fill=X)

Frame3=LabelFrame(window,bd=20,relief=RIDGE,padx=20,font=("arial",12,"bold"), text="Xử lý dữ liệu")
Frame3.place(x=1000,y=120,width=530,height=270)

Dataframe3=LabelFrame(window,bd=20,relief=RIDGE,padx=20,font=("arial",12,"bold"), text="Chi tiết")
Dataframe3.place(x=1000,y=390,width=530,height=330)

Framethongbao=Frame(window,bd=20,relief=RIDGE)
Framethongbao.place(x=0,y=720,width=1530,height=65)

Dataframe2=Frame(window,bd=20,relief=RIDGE)
Dataframe2.place(x=0,y=120,width=1000,height=600)

Framebutton=Frame(Frame3)
Framebutton.place(x=0,y=203)
scroll_x=ttk.Scrollbar(Dataframe2,orient=HORIZONTAL)
scroll_y=ttk.Scrollbar(Dataframe2,orient=VERTICAL)
danhsach= ttk.Treeview(Dataframe2,columns=(1,2,3,4,5),show='headings',xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
scroll_x.pack(side=BOTTOM,fill=X)
scroll_y.pack(side=RIGHT,fill=Y)
scroll_x=ttk.Scrollbar(command=danhsach.xview)
scroll_y=ttk.Scrollbar(command=danhsach.yview)
danhsach.column(1,width=30)
danhsach.column(2,width=150)
danhsach.column(3,width=60)
danhsach.column(4,width=40)
danhsach.column(5,width=60)

danhsach.heading(1, text='ID')
danhsach.heading(2, text='Họ và tên')
danhsach.heading(3, text='Ngày sinh')
danhsach.heading(4, text='Giới tính')
danhsach.heading(5, text='Chức vụ')
danhsach.pack(fill=BOTH,expand=1)
#Lấy dữ liệu từ database vừa kết nối
dulieu='select * from quanlynhanvien'
show=database.cursor()
show.execute(dulieu)
rows=show.fetchall()
for i in rows:
    danhsach.insert('','end',iid=i[0],values=i)


def xoa():

    a=MS.get()
    #vantay_selected=danhsach.item(selected_item)['values'][5]
    if a:
        dulieu='delete from quanlynhanvien where ID=%s'#tuple
        data=(a,)
        trumot=database.cursor()
        trumot.execute(dulieu,data)
        database.commit()
        messagebox.showinfo("Thông báo", "Xóa dữ liệu thành công!")
        xoa = int(a)
        master.write_registers(2,[3, xoa],1)
        response1 = master.read_holding_registers(0, 6, 1)
        if(response1.registers[2]==1):
            master.write_registers(0,[0,0,1,0],1)
        # du='select * from quanlynhanvien'
        # show.execute(du)
        # result = show.fetchall()  	#chọn và nạp dữ liệu từ con trỏ 
        # item=danhsach.get_children()
        # for eachItem in item :
        #     danhsach.delete(eachItem)
        #     for i in result:
        #         danhsach.insert("","end",iid=i[0],values=i)
        selected_items = danhsach.get_children()
        for item in selected_items:
            values = danhsach.item(item, 'values')
            if (values[1] == a):
                danhsach.delete(item)

        
    else:
        messagebox.showinfo("Thông báo", "Muốn xóa cần nhập ID vân tay để có thể xóa toàn bộ!")
        
        
def them(): 
    a= MS.get()# nếu thiếu dữ liệu nhập vào sẽ hiện lable thông báo lỗi hiển thị trong vài giây
    b=ten.get()
    c = ngaysinh.get_date().strftime("%Y-%m-%d")
    d=gioitinh.get()
    e=vitri.get()
    g=MS.get()
    response1 = master.read_holding_registers(0, 6, 1)
    f= response1.registers[1]
    s= response1.registers
    send = int(g)
    master.write_registers(2,[2, send],1)
    if not a or not b or not c or not d or not e or not g:
        messagebox.showinfo("Lỗi", "Vui lòng nhập đủ thông tin.")
        master.write_registers(0,[0,0,1,0],1)
        return
    if a:
        show.execute('select * from quanlynhanvien WHERE ID = %s', (a,))
        result=show.fetchone()

        if result: 
            messagebox.showinfo("Cảnh báo", "ID đã tồn tại!")
            master.write_registers(0,[0,0,1,0],1)
            return

        if f==send and response1.registers[0]==2:
            themmot=database.cursor()
            dulieu='insert into `qlnv`.`quanlynhanvien` (`ID`, `Name`, `Birthday`, `Sex`, `Post`,`Vantay`) values (%s,%s,%s,%s,%s,%s)'
            val=(a,b,c,d,e,f)
            themmot.execute(dulieu,val)
            database.commit()
            
            danhsach.insert('', 'end', values=(a,b,c,d,e))
            messagebox.showinfo("Thông báo", "Thêm dữ liệu thành công!")
            master.write_registers(0,[0,0,1,0],1)
            return
        print(s)
    if(not response1.registers==2):
        window.after(100,them)

def sua():

    f=MS.get()
    new_a= MS.get()
    new_b=ten.get()
    new_c = ngaysinh.get_date().strftime("%d-%m-%Y")
    new_d=gioitinh.get()
    new_e=vitri.get()
    if(f):
        messagebox.showinfo("Cảnh báo", "Ko đổi được ID. Đi chỗ khác")
        return
    else:  
        selected = danhsach.selection()[0]
        olddata = danhsach.item(selected)['values']
        
        if new_a:
            show.execute('select * from quanlynhanvien WHERE ID = %s', (new_a,))
            result=show.fetchone()
            if result: 
                messagebox.showinfo("Cảnh báo", "ID đã tồn tại!")
                return
        a= new_a if new_a else olddata[0]
        b= new_b if new_b else olddata[1]
        c= new_c if new_c else olddata[2]
        d= new_d if new_d else olddata[3]
        e= new_e if new_e else olddata[4]
        print(d)

        suamot=database.cursor()
        dulieu='UPDATE quanlynhanvien SET ID = %s, Name = %s, Birthday = %s, Sex = %s, Post = %s WHERE ID = %s'
        val=(a,b,c,d,e, selected)
        suamot.execute(dulieu,val)
        database.commit()
        danhsach.item(selected, values=(a,b,c,d,e))
        messagebox.showinfo("Thông báo", "Sửa dữ liệu thành công!")

prev_data1 = [0]

new_data1 = False
thongbao=Listbox(Dataframe3,width=75, height=18)
thongbao.grid()
path = 'D:\\QLNV.txt'


def update_data():
    global prev_data1, new_data1, employee_fingerprint, thongbao
    # master.write_registers(6,[1,0],1)
    response1 = master.read_holding_registers(0, 6, 1)
    employee_fingerprint=  response1.registers[5]
    if(response1.registers[4]==1):
        if employee_fingerprint != prev_data1[-1]:
            new_data1 = True
            prev_data1.append(employee_fingerprint)
            show.execute('SELECT * FROM quanlynhanvien')
            employees = show.fetchall()
            # Tạo một danh sách chứa tất cả các ID nhân viên
            employee_ids = [employee[0] for employee in employees]
            placeholders = ','.join(['%s'] * len(employee_ids))
            query = f"SELECT * FROM quanlynhanvien WHERE ID IN ({placeholders}) AND Vantay = %s"
            bindings = tuple(employee_ids + [employee_fingerprint])
            current_time = datetime.now().strftime("%H:%M:%S %d-%m-%Y ")
            show.execute(query, bindings)
            results = show.fetchall()
            path = 'D:\\QLNV.txt'

            with open(path, "a") as file:
                for result in results:
                    # Kiểm tra xem dữ liệu hiện tại có khớp với ID vân tay hay không
                    if result[5] :
                        # Nếu khớp, in ra là đã điểm danh
                        file.write(f"Phong so 1: {result[1]} da diem danh thanh cong luc {current_time}.\n")
                        thongbao.insert(tk.END, f"Phong so 1: {result[1]} da diem danh thanh cong luc {current_time}.")
            with open(path, "r") as file:
                thongbao.delete(0,tk.END)
                for line in file:
                    thongbao.insert(tk.END, line.strip())
            if results: 
                master.write_registers(0,[100,0,1,0],1)
                messagebox.showinfo("Cảnh báo", f"{results [0][1]} đã điểm danh thành công!")
    # Gọi lại hàm sau một khoảng thời gian
    window.after(50, update_data)
    print(response1.registers)
# Khởi tạo biến cờ để kiểm tra dữ liệu mới
new_data1 = False
 

# Gọi hàm update_data() lần đầu tiên
update_data()

###########################################################################
# def thongke():
#     global prev_data1
#     print(prev_data1)
#     show.execute('SELECT * FROM quanlynhanvien')
#     employees = show.fetchall()

#     # Tạo một danh sách chứa tất cả các ID nhân viên
#     employee_ids = [employee[0] for employee in employees]

#     # Truy vấn tất cả các ID nhân viên trong một lần
#     if prev_data1:
#         for fingerprint_value in prev_data1:
#             placeholders = ','.join(['%s'] * len(employee_ids))
#             query = f"SELECT * FROM quanlynhanvien WHERE ID IN ({placeholders}) AND Vantay = %s"
#             bindings = tuple(employee_ids + [fingerprint_value])

#             show.execute(query, bindings)
#             results = show.fetchall()

#             # Duyệt qua kết quả truy vấn và in ra kết quả
#             with open('D:\\QLNV.txt', "a") as file:
#                 for result in results:
#                     # Kiểm tra xem dữ liệu hiện tại có khớp với ID vân tay hay không
#                     if result[5] :
#                         # Nếu khớp, in ra là đã điểm danh
#                         file.write(f"Phong so 1: {result[1]} da diem danh thanh cong luc.\n")
                        
#                     # else:
#                     #     # Nếu không khớp, in ra là chưa điểm danh
#                     #     file.write(f"Phong so 1: {result[1]} chua diem danh.\n")
#             if results: 
#                 messagebox.showinfo("Cảnh báo", f"{results [0][1]} đã điểm danh thành công!")
                


#Nhập dữ liệu
IDne=Label(Frame3,font=("arial",13), text='ID:',width=10)
IDne.grid(row=0,column=0)
NhapID=Entry(Frame3,width=40, textvariable=MS)
NhapID.grid(row=0,column=1)
Tenne=Label(Frame3,font=("arial",13), text='Họ và tên:',width=15)
Tenne.grid(row=1,column=0)
Nhapten=Entry(Frame3,width=40, textvariable=ten)
Nhapten.grid(row=1,column=1)
Ngayne=Label(Frame3,font=("arial",13), text='Ngày sinh:',width=10)
Ngayne.grid(row=2,column=0)
# Nhapngay=Entry(Frame3,width=40,textvariable=ngaysinh)
ngaysinh = DateEntry(Frame3, width=37, year=2000, month=1, day=1, date_pattern='dd-mm-yyyy')

ngaysinh.grid(row=2,column=1)
Tinhne=Label(Frame3,font=("arial",13), text='Giới tính:', width=10)
Tinhne.grid(row=3,column=0)
Nhaptinh = ttk.Combobox(Frame3, textvariable=gioitinh, values=["Nam", "Nu", "Khac"], width=37)
Nhaptinh.set("")  # Thiết lập giá trị mặc định
Nhaptinh.grid(row=3,column=1)
Trine=Label(Frame3,font=("arial",13), text='Vị trí:',width=10)
Trine.grid(row=4,column=0)
Nhaptri = ttk.Combobox(Frame3, textvariable=vitri, values=["Truong nhom", "Culi","Thu quy", "Khac"], width=37)
Nhaptri.set("")  # Thiết lập giá trị mặc định
Nhaptri.grid(row=4,column=1)
################################################################
# # Tạo nhãn để hiển thị thời gian
time_label = ttk.Label(Framethongbao, font=("Arial", 15))
time_label.place(x=1370,y=0)
# Gọi hàm để cập nhật thời gian
dongho()
nutthem=Frame(Framebutton)
nutthem.grid(row=0,column=0)
nutthemvantay=Frame(Framebutton)
nutthemvantay.grid(row=0,column=1)
nutsua=Frame(Framebutton)
nutsua.grid(row=0,column=2)
nutxoa=Frame(Framebutton)
nutxoa.grid(row=0,column=3)
nutkiemtra=Frame(Framebutton)
nutkiemtra.grid(row=0,column=4)
nutthoat=Frame(Framebutton)
nutthoat.grid(row=0,column=5)

Button(nutthem,text='Thêm',width=10,command=them).pack()
# Button(nutthemvantay,text='Thêmvântay',width=10,command=themvantay).pack()
Button(nutsua,text='Sửa',width=10,command=sua).pack()
Button(nutxoa,text='Xóa',width=10,command=xoa).pack()
# Button(nutkiemtra,text='Kiểm tra',width=10,command=thongke).pack()
Button(nutthoat,text='Thoát',width=10,command=window.quit).pack()

path = 'D:\\QLNV.txt'
# def read_file_into_listbox(path, listbox):
#     with open(path, "r") as file:
#         for line in file:
#             listbox.insert(tk.END, line.strip())

# def refresh_listbox(listbox):
#     listbox.delete(0, tk.END)  # Xóa nội dung hiện tại của Listbox
#     read_file_into_listbox(path, listbox)  # Đọc lại nội dung từ tệp và thêm vào Listbox
# # Tạo một nút "Refresh"
# thongbao=Listbox(Dataframe3,width=75, height=18)
# thongbao.grid() 
# read_file_into_listbox(path, thongbao) 
def clear_file(path):
    # Mở tệp ở chế độ ghi để xóa hết dữ liệu
    with open(path, "w") as file:
        file.truncate(0)  # Xóa hết nội dung của tệp
    with open(path, "r") as file:
        thongbao.delete(0,tk.END)
        for line in file:
            thongbao.insert(tk.END, line.strip())
# with open(path, "r") as file:
#     thongbao.delete(0,tk.END)
#     for line in file:
#         thongbao.insert(tk.END, line.strip())
# refresh_button = tk.Button(Dataframe3, text="Refresh", command=lambda: refresh_listbox(thongbao))
# refresh_button.place(x=400,y=200)
clear_button = tk.Button(Dataframe3, text="Clear", command=lambda: clear_file(path))
clear_button.place(x=400,y=250)
window.mainloop()
