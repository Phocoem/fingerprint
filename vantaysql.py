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
from mysql.connector import Error

master = ModbusSerialClient(port= "COM1", Framer="RTU", baudrate= 9600, bytesize = 8, parity= "N",stopbits= 1,strict=True)
master.connect()
prev_data1 = [0]
prev_data2 = [0]
new_data1 = False
new_data2 = False 
messagevantay =False
# def kiemtra():
#     selected = danhsach.selection()[0]
    

def dongho():
# Lấy thời gian hiện tại
    thoigian = datetime.now().strftime("%H:%M:%S %p")
# Cập nhật nhãn thời gian với thời gian hiện tại
    time_label.config(text=thoigian)
# Gọi hàm này mỗi giây để cập nhật thời gian
    time_label.after(1000, dongho)

database=mysql.connector.connect(user='root', password='123456',host='localhost', database='qlnv')

#Lấy dữ liệu từ database vừa kết nối
dulieu='select * from quanlynhanvien'
show=database.cursor()
show.execute(dulieu)
rows=show.fetchall()# lấy từng hàng dữ liệu???

window = Tk()
#khai báo
MS= StringVar()
ten= StringVar()
ngaysinh =StringVar()
gioitinh= StringVar()
vitri =StringVar()
window.title("Cong ty 2/3")
window.geometry("1540x800+0+0")
title=Label(window,bd=20,relief=RIDGE, text="QUẢN LÝ NHÂN VIÊN", fg="red",bg="white",font=("arial",50,"bold") )
title.pack(side=TOP,fill=X)

Frame3=LabelFrame(window,bd=20,relief=RIDGE,padx=20,font=("arial",12,"bold"), text="Dữ liệu nhân viên")
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
danhsach= ttk.Treeview(Dataframe2,columns=(1,2,3,4,5,6),show='headings',xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
scroll_x.pack(side=BOTTOM,fill=X)
scroll_y.pack(side=RIGHT,fill=Y)
scroll_x=ttk.Scrollbar(command=danhsach.xview)
scroll_y=ttk.Scrollbar(command=danhsach.yview)
danhsach.column(1,width=30)
danhsach.column(2,width=150)
danhsach.column(3,width=60)
danhsach.column(4,width=40)
danhsach.column(5,width=60)
danhsach.column(6,width=60)
danhsach.heading(1, text='ID')
danhsach.heading(2, text='Tên nhân viên')
danhsach.heading(3, text='Ngày sinh')
danhsach.heading(4, text='Giới tính')
danhsach.heading(5, text='Chức vụ')
danhsach.heading(6, text='ID vân tay')
for i in rows:
    danhsach.insert('','end',iid=i[0],values=i)
    danhsach.pack(fill=BOTH,expand=1)

#Nhập dữ liệu
IDne=Label(Frame3,font=("arial",13), text='ID:',width=10)
IDne.grid(row=0,column=0)
NhapID=Entry(Frame3,width=40, textvariable=MS)
NhapID.grid(row=0,column=1)
Tenne=Label(Frame3,font=("arial",13), text='Tên nhân viên:',width=15)
Tenne.grid(row=1,column=0)
Nhapten=Entry(Frame3,width=40, textvariable=ten)
Nhapten.grid(row=1,column=1)
Ngayne=Label(Frame3,font=("arial",13), text='Ngày sinh:',width=10)
Ngayne.grid(row=2,column=0)
Nhapngay=Entry(Frame3,width=40,textvariable=ngaysinh)
Nhapngay.grid(row=2,column=1)
Tinhne=Label(Frame3,font=("arial",13), text='Giới tính:', width=10)
Tinhne.grid(row=3,column=0)
Nhaptinh=Entry(Frame3,width=40,textvariable=gioitinh)
Nhaptinh.grid(row=3,column=1)
Trine=Label(Frame3,font=("arial",13), text='Vị trí:',width=10)
Trine.grid(row=4,column=0)
Nhaptri=Entry(Frame3,width=40,textvariable=vitri)
Nhaptri.grid(row=4,column=1)
def xoa():
    selected = danhsach.selection()[0]
    dulieu='delete from quanlynhanvien where id=%s'#tuple
    data=(selected,)
    trumot=database.cursor()
    trumot.execute(dulieu,data)
    database.commit()
    danhsach.delete(selected)
    messagebox.showinfo("Thông báo", "Xóa dữ liệu thành công!")
def them():
    a= MS.get()# nếu thiếu dữ liệu nhập vào sẽ hiện lable thông báo lỗi hiển thị trong vài giây
    b=ten.get()
    c=ngaysinh.get()
    d=gioitinh.get()
    e=vitri.get()
    if not a or not b or not c or not d or not e:
        messagebox.showinfo("Lỗi", "Vui lòng nhập đủ thông tin.")
        return
    if a:
        show.execute('select * from quanlynhanvien WHERE ID = %s', (a,))
        result=show.fetchone()
        if result: 
            messagebox.showinfo("Cảnh báo", "ID đã tồn tại!")
            return
    
    themmot=database.cursor()
    dulieu='insert into `qlnv`.`quanlynhanvien` (`ID`, `Name`, `Birthday`, `Sex`, `Post`) values (%s,%s,%s,%s,%s)'
    val=(a,b,c,d,e)
    themmot.execute(dulieu,val)
    database.commit()
    danhsach.insert('', 'end', values=(a,b,c,d,e))
    messagebox.showinfo("Thông báo", "Thêm dữ liệu thành công!")
          
def themvantay():
    selected_item = danhsach.selection()
    if not selected_item:
        messagebox.showinfo("Lỗi", "Vui lòng chọn một dòng dữ liệu.")
        return
    
    selected_id = danhsach.item(selected_item)['values'][0]  # Lấy ID của dòng dữ liệu được chọn
    if not selected_id:
        messagebox.showinfo("Lỗi", "Vui lòng chọn một dòng dữ liệu hợp lệ.")
        return
 
    # Đọc dữ liệu vân tay từ thiết bị Modbus
    response1 = master.read_holding_registers(0, 1, 1)
    data1 = response1.registers
    if data1:
        show.execute('select * from quanlynhanvien WHERE Vantay = %s', (data1[0],))
        result=show.fetchone()
        if result: 
            messagebox.showinfo("Cảnh báo", "Vân tay đã tồn tại!")
            return   
    # Thêm ID vân tay vào cột tương ứng của dòng dữ liệu được chọn trong cơ sở dữ liệu MySQL
    cursor = database.cursor()
    sql_query = "UPDATE quanlynhanvien SET Vantay = %s WHERE ID = %s"
    cursor.execute(sql_query, (data1[0],selected_id))
    database.commit()
    danhsach.item(selected_id, values=(i[0], i[1], i[2], i[3],i[4],data1[0]))
    messagebox.showinfo("Thông báo", "Thêm ID vân tay thành công!")

    # Hiển thị thông báo thành công
    messagebox.showinfo("Thông báo", "Thêm ID vân tay thành công cho nhân viên có ID: {}".format(selected_id))
#     # Gọi lại hàm sau một khoảng thời gian
#######################################################################

########################################################################

    

def sua():
    selected = danhsach.selection()[0]
    olddata = danhsach.item(selected)['values']
    new_a= MS.get()
    new_b=ten.get()
    new_c=ngaysinh.get()
    new_d=gioitinh.get()
    new_e=vitri.get()
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

    suamot=database.cursor()
    dulieu='update quanlynhanvien set ID = %s, Name = %s, Birthday = %s, Sex =%s, Post=%s WHERE id = %s'
    val=(a,b,c,d,e, selected)
    suamot.execute(dulieu,val)
    database.commit()
    danhsach.item(selected, values=(a,b,c,d,e))
    messagebox.showinfo("Thông báo", "Sửa dữ liệu thành công!")
prev_data1 = [0]
prev_data2 = [0]
new_data1 = False
new_data2 = False   
#def kiemtra():
def thongke():
    selected_item = danhsach.selection()
    if not selected_item:
        messagebox.showinfo("Lỗi", "Vui lòng chọn một dòng dữ liệu.")
        return
    
    selected_id = danhsach.item(selected_item)['values'][0]  # Lấy ID của dòng dữ liệu được chọn
    selected_name = danhsach.item(selected_item)['values'][1]
    if not selected_id:
        messagebox.showinfo("Lỗi", "Vui lòng chọn một dòng dữ liệu hợp lệ.")
        return
    response1 = master.read_holding_registers(0, 1, 1)
    data1 = response1.registers
    if data1[0]:
        show.execute('SELECT * FROM quanlynhanvien WHERE ID = %s AND Vantay = %s', (selected_id, data1[0]))
        result=show.fetchone() 
        path = 'D:\\QLNV.txt'
        with open(path, "a") as file:

            if result is not None:
                file.write(f"Phong so 1: {selected_name} da diem danh thanh cong.\n")
            else:
                file.write(f"Phong so 1: {selected_name} chua diem danh.\n")
    # Gọi lại hàm sau một khoảng thời gian




# Gọi hàm update_data() để bắt đầu cập nhật dữ liệu
   

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
Button(nutthemvantay,text='Thêmvântay',width=10,command=themvantay).pack()
Button(nutsua,text='Sửa',width=10,command=sua).pack()
Button(nutxoa,text='Xóa',width=10,command=xoa).pack()
Button(nutkiemtra,text='Kiểm tra',width=10,command=thongke).pack()
Button(nutthoat,text='Thoát',width=10,command=window.quit).pack()

path = 'D:\\QLNV.txt'
def read_file_into_listbox(path, listbox):
    with open(path, "r") as file:
        for line in file:
            listbox.insert(tk.END, line.strip())
def refresh_listbox(listbox):
    listbox.delete(0, tk.END)  # Xóa nội dung hiện tại của Listbox
    read_file_into_listbox(path, listbox)  # Đọc lại nội dung từ tệp và thêm vào Listbox
# Tạo một nút "Refresh"
thongbao=Listbox(Dataframe3,width=75, height=18)
thongbao.grid() 
read_file_into_listbox(path, thongbao) 
refresh_button = tk.Button(Dataframe3, text="Refresh", command=lambda: refresh_listbox(thongbao))
refresh_button.place(x=400,y=200)
window.mainloop()
