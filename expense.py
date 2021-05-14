from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime

GUI = Tk()
GUI.title(' โปรแกรมบันทึกค่าใช้จ่าย by qwerty ')
GUI.geometry('600x650+5+50')
###################################
menubar = Menu(GUI)
GUI.config(menu=menubar)

#finemenu
filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import csv')
filemenu.add_command(label='Export to Googlesheet')

#help
def About():
	messagebox.showinfo('Abount','โปรแกรมนี้เป็นโปรแกรมบันทึกค่าใช้จ่าย')
helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)


#Donate
def Donate():
	messagebox.showinfo('Donate','โอนเงินมาเลย')
donatemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemenu)
donatemenu.add_command(label='Donate',command=Donate)


###################################
Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1) 

icon_t1 = PhotoImage(file='wallet.png')
icon_t2 = PhotoImage(file='list.png')


Tab.add(T1, text=f'{"ค่าใช้จ่าย":^{30}}',image=icon_t1, compound='top')
Tab.add(T2, text=f'{"ค่าใช้จ่ายทั้งหมด":^{30}}',image=icon_t2, compound='top')

F1=Frame(T1)
#F1.place(x=100,y=50)
F1.pack()

days={'Mon':'จันทร์','Tue':'อังคาร','Wed':'พุธ','Thu':'พฤหัสบดี','Fri':'ศุกร์','Sat':'เสาร์','Sun':'อาทิตย์'}

def Save(event=None):
	expense=v_expense .get() #.get() คือ ดึงค่ามาจาก v_expense =StrintVar()
	price = v_price.get()
	piece = v_piece.get()
	if expense == '' :
		print('NO DATA')
		messagebox.showwarning('ERROR','กรุณากรอกข้อมูลค่าใช้จ่าย')
		return
	elif price == '':
		messagebox.showwarning('ERROR','กรุณากรอกราคา')
		return
	elif piece == '':
		price=1
		return

	try:
		total=int(price)*int(piece)  
		print('รายการ: {} ราคา: {} ชิ้น: {} รวม: {} ' .format(expense,price,piece,total))
		text ='รายการ: {} ราคา: {} \nชิ้น: {} รวม: {} ' .format(expense,price,piece,total)
		v_result.set(text)
		v_expense.set('')#clear=ช่องบน
		v_price.set('')#clear=ช่องล่าง
		v_piece.set('')

		#บันทึกข้อมูลลง csv
		today = datetime.now().strftime('%a')
		dt = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
		dt= days[today] + '-' + dt
		with open('savedata.csv','a',encoding='utf-8' ,newline='') as f:
			fw = csv.writer(f) 
			data = [expense,price,piece,total,dt]
			fw.writerow(data)
	#ทำให้เคอเซอร์กลับไปช่องกรอกบน
		update_table()
		E1.focus()
		
	except:
		print('ERROR')
		#messagebox.showwarning('ERROR','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		messagebox.showerror('ERROR','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		#messagebox.showinfo('ERROR','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		v_expense.set(' ')#clear=ช่องบน
		v_price.set(' ')#clear=ช่องล่าง
		v_piece.set(' ')


#ทำให้กด Enter
GUI.bind('<Return>',Save)#ต้องเพิ่มใน Def Save(event=None) ด้วย


FONT1 = (None,20)
#------------image--------
main_icon=PhotoImage(file='iconmoney.png')
Mainicon = Label(F1,image=main_icon)
Mainicon.pack()


L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1) .pack()

v_expense = StringVar()
E1=ttk.Entry(F1,textvariable=v_expense,font=FONT1) #Entry = ช่องรับข้อมูล
E1.pack()

L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1) .pack()

v_price = StringVar()
E2=ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()

L = ttk.Label(F1,text='จำนวน (ชิ้น)',font=FONT1) .pack()

v_piece = StringVar()
E3=ttk.Entry(F1,textvariable=v_piece,font=FONT1)
E3.pack()

icon_b1=PhotoImage(file='save_b.png')

B2=ttk.Button(F1,text=f'{"Save": >{10}}',image=icon_b1,compound='left',command=Save)
B2.pack(ipadx=50,ipady=20,pady=20)

v_result=StringVar()
v_result.set('last added')
result = ttk.Label(F1, textvariable=v_result,font=FONT1,foreground='green')
result.pack(pady=20)

##############tab2###############
def read_csv():
	with open('savedata.csv',newline='',encoding='utf-8')as f :
		fr=csv.reader(f)
		data= list(fr)
	return data
## table

L=ttk.Label(T2,text='ตารางแสดงผลลัพธ์ทั้งหมด',font=FONT1).pack(pady=20)

header = ['รายการ','ค่าใช้จ่าย','จำนวน','รวม','วัน-เวลา']
resulttable=ttk.Treeview(T2,columns=header,show='headings',height=10)
resulttable.pack()		

#or i in range(len(header)):
#resulttable.heading(header[i],text=header[i])

for h in header:
	resulttable.heading(h,text=h)

headerwidth = [170,80,80,80,150]
for h,w in zip(header,headerwidth):
	resulttable.column(h,width=w)



def update_table():
	resulttable.delete(*resulttable.get_children())
	data=read_csv()
	for d in data:
		resulttable.insert('',0,value=d)

update_table()


GUI.mainloop()
