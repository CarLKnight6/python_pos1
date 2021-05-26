from tkinter import *
import time;
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import datetime
import csv
import json
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import timeit
from tkinter.simpledialog import askfloat, askinteger
import io
import os
from contextlib import redirect_stdout
''' coded by : Jesus Carl B. Sanchej BSIT-1R2'''



output = None
class login_window:
    def __init__(self,master):
        self.master =master
        self.frame = Frame(self.master,bg='light blue',width=500,height=300,relief=RIDGE,bd=10)
        self.master.title("verify")
        self.master.geometry("500x300+430+200")
        self.frame.pack()
        self.logcount =5
        self.admin_lbl = Label(self.frame,text='ADMIN',font=('tahoma',15),bg='light blue')
        self.admin_lbl.place(x=30,y=50)
        self.password_lbl = Label(self.frame,text='PASSWORD',font=('tahoma',15),bg='light blue')
        self.password_lbl.place(x=30,y=100)                  
        self.admin_entry = Entry(self.frame,font=('tahoma',15,'italic'),width = 20)
        self.admin_entry.place(x=200,y=50)
        self.password_entry = Entry(self.frame,font=('tahoma',15,'italic'),width = 20,show="*")
        self.password_entry.place(x=200,y=100)
        #self.keepmelogin_checkbtn = Checkbutton(self.frame,text="Keep me logged in!" ,font=('times new roman',10,'italic'),bg='light blue')
        #self.keepmelogin_checkbtn.place(x=200,y=150)
        self.login_btn  = Button(self.frame,text="LOGIN",padx=15,pady=5,bd=10,relief=RAISED,font=('tahoma',12,'bold'),fg='white',bg='black',command=self.to_verify)
        self.login_btn.place(x=200,y=200)
        self.exit_btn  = Button(self.frame,text="EXIT",padx=15,pady=5,bd=10,relief=RAISED,font=('tahoma',12,'bold'),fg='white',bg='red',command=self.to_exit)
        self.exit_btn.place(x=330,y=200)
        
    def to_verify(self):
        self.logcount -= 1
        self.user = self.admin_entry.get()
        self.password = self.password_entry.get()
        if self.user =="jesus" and self.password== "carl":
            messagebox.showinfo("system message", "welcome, admin!")
            self.frame.pack_forget()
            self.frame = Mainmenu(root)
        elif self.logcount == 2:
            messagebox.showinfo("system message","PLEASE CONTACT ADMINISTRATOR!"+ '\n' +"Log count remaining: " + str(self.logcount))
        elif self.logcount==1:
            messagebox.showinfo("system message","WARNING,PROGRAM IS CLOSING!!!"+ '\n' +"Log count remaining: " + str(self.logcount))
        elif self.logcount==0:


            self.to_exit()
        else:
            
            messagebox.showinfo("system message","INVALID ID OR PASSWORD" + '\n' +"Log count remaining: " + str(self.logcount))

    def to_exit(self):      

        root.destroy()
        sys.exit()


class POS_window():
    def __init__(self,master):
        self.master = master
        self.master.title("POS")
        self.master.geometry("1340x680+0+0")
        #TOP LEVEL FRAME--------
        self.topframe = Frame(self.master,bg='light blue',width=1340,height=100)
        self.topframe.pack(side='top',fill='both',expand =True)
        self.f0 = Frame(self.topframe,bg='light blue',width=1340,height=100, relief=SUNKEN,bd=5)
        self.f0.pack(side=TOP)
        self.sys_lbl =Label(self.f0,text="JESUS' POS SYSTEM", font=('arial',40,'bold'),bg='light blue')
        self.sys_lbl.place(x=330,y=1)
        self.localtime = time.asctime(time.localtime(time.time()))
        self.time_lbl = Label(self.f0,text="TIME INFO: " + self.localtime, font=('times new roman',12),bg='light blue')
        self.time_lbl.place(x=330,y=60)
        self.f1 = Frame(self.topframe,bg='light blue',width=675,height=575, relief=SUNKEN,bd=5)
        self.f1.pack(side=LEFT)
        self.f2 = Frame(self.topframe,bg='light blue',width=625,height=575,relief=SUNKEN,bd=5)
        self.f2.pack(side=RIGHT)
        #SALE_FRAME(moves the product tiles' position via pady and padx
        self.framepage = Frame(self.f1,bg='sky blue',width=643,height=450,pady=25,padx=14,relief=SUNKEN,bd=2)
        self.framepage.place(x=10,y=50)
     
        
        self.cart_lbl = Label(self.f2, text="CART" , font=('arial',12,'bold'),bg='light blue' )
        self.cart_lbl.place(x=50,y=50)
        self.addtocart_btn = Button(self.f1,text="Add to cart",relief=RAISED,font=('tahoma',12,'bold'),fg='white',bg='black',bd=5,command=self.add_to_cart,state='disable')
        self.addtocart_btn.place(x=520,y=510)
        
        self.itemprice_lbl = Label(self.f1, text="PRICE:" , font=('arial',12,'bold'),bg='light blue' )  
        self.itemquantity_lbl = Label(self.f1, text="QTY." , font=('arial',12,'bold'),bg='light blue' )
        self.itemprice_lbl.place(x=50,y=520)
        self.itemquantity_lbl.place(x=320,y=520)
        #===================item price and quantity
        self.price = IntVar()
        self.qty = IntVar()
        self.price.set("")
        self.qty.set("")
        self.itemprice_textbox = Text(self.f1 ,height = 1, width = 20,font=('arial' , 12,'bold'),state='disabled')
        self.itemquantity_entry = Entry(self.f1,textvariable = self.qty,font=('arial' , 12,'bold'),width=5,state='disabled')
        self.itemprice_textbox.place(x=120,y=520)
        self.itemquantity_entry.place(x=370,y=520)
        
        self.tree = ttk.Treeview(self.f2)
        self.scroll = ttk.Scrollbar(self.f2,orient="vertical",command=self.tree.yview)
        self.scroll.place(x=595,y=80)
        self.tree.configure(yscrollcommand=self.scroll.set)
        self.tree['show']="headings"
        self.tree['columns'] = ("1","2","3","4","5","6")
        self.tree.column("1", width=60)
        self.tree.column("2",width=60)
        self.tree.column("3",width=120)
        self.tree.column("4",width=120)
        self.tree.column("5",width=60)
        self.tree.column("6",width=120)
        self.tree.heading("1", text="Sales ID")
        self.tree.heading("2",text ="Prod ID")
        self.tree.heading("3",text ="Product Name")
        self.tree.heading("4",text ="Price")
        self.tree.heading("5",text ="Quantity")
        self.tree.heading("6",text ="Amount")
        self.tree.bind('<Button-1>', self.enable_removeitembtn)
        self.s = ttk.Style()
        self.s.configure('Treeview', rowheight=25)
        self.tree.place(x=50, y = 80)
      
        #buttons
        self.subtotalamount_lbl= Label(self.f2, text="SUB TOTAL " , font=('arial',12),bg='light blue' )
        self.vat_lbl= Label(self.f2, text="VAT (12%)" , font=('arial',12),bg='light blue' )
        self.cash_lbl= Label(self.f2, text="CASH" , font=('arial',12,'bold'),bg='light blue')
        self.totalsamount_lbl= Label(self.f2, text="TOTAL AMOUNT" , font=('arial',12,'bold'),bg='light blue')
        self.change_lbl= Label(self.f2, text="CHANGE" , font=('arial',12,'bold'),bg='light blue' )
        self.transact_btn  = Button(self.f2,text="TRANSACT",relief=RAISED,font=('tahoma',12,'bold'),fg='white',bg='black',bd=5,command=self.to_transact,state='disabled')    
        self.clear_btn  = Button(self.f2,text="CLEAR FIELDS", relief=RAISED,font=('tahoma',12,'bold'),fg='white',bg='black',bd=5,width=11,command=self.to_clearcart)
        self.removeitem_btn  = Button(self.f2,text="REMOVE ITEM",relief=RAISED,font=('tahoma',12,'bold'),fg='white',bg='black',bd=5,command=self.to_remove_item,state='disabled')
        self.clear_btn.place(x=285,y=525)
        self.removeitem_btn.place(x=120,y=525)
        self.transact_btn.place(x=435,y=525)
        self.subtotalamount_lbl.place(x=50,y=370)
        self.vat_lbl.place(x=50,y=400)
        self.totalsamount_lbl.place(x=50,y=430)
        self.cash_lbl.place(x=50,y=465)
        self.change_lbl.place(x=50,y=495)
       

        self.sales_id = 0 #some useful atributes
        self.date = datetime.datetime.now()#standard date of day php
        self.subtotalamount = 0.0
        self.totalsamount = 0.0
        self.vat = 0.0
        self.cash =0
        self.entered_quantity = 0
        self.change = 0.0
        self.newquantity =0
        self.image_list = []
        self.ids = []
        with open(r"D:\integprog\pos\sancheja_pos_system_finals\arrayofimages2.txt") as file:
            for line in file:
                imagepath = line.strip()
                self.image_list.append(imagepath)    

        
        #print(self.image_list[0])
        
        self.image = {} #dictionary created for variable iteration of images

        
        
        

          # output and vat and cash entry and subtotal and total amount
        self.cash = DoubleVar()
        self.subtotalamount_textbox = Text(self.f2,height = 1, width = 35,font=('arial' , 12),state='disabled')
        self.vat_textbox = Text(self.f2,height = 1, width = 35,font=('arial' , 12),state='disabled')
        self.counter = 1#salesid iterator
        self.cash_entry = Entry(self.f2,textvariable = self.cash,font=('arial' , 12,'bold'),width=35,state='disabled')
        self.change_textbox = Text(self.f2,height = 1,font=('arial' , 12,'bold'), width = 35,state='disabled')
        self.totalsamount_textbox = Text(self.f2,height = 1, width = 35,font=('arial' , 12,'bold'),state='disabled')
        self.totalsamount_textbox.place(x=200,y=430)  
        self.subtotalamount_textbox.place(x=200,y=370) 
        self.vat_textbox.place(x=200,y=400)  
        self.cash_entry.place(x=200,y=465)  
        self.change_textbox.place(x=200,y=495)

        self.mainmenu_btn = Button(self.f1,text="MAIN MENU",relief=RAISED,font=('tahoma',12,'bold'),fg='white',bg='black',bd=5,command = self.goto_mainmenu)
        self.mainmenu_btn.place(x=10,y=10)

        self.mainmenu_btn = Button(self.f1,text="REFRESH",relief=RAISED,font=('tahoma',12,'bold'),fg='white',bg='black',bd=5,command = self.goto_refresh)
        self.mainmenu_btn.place(x=250,y=10)
               
        self.myframe=Frame(self.framepage,relief=GROOVE,width=50,height=100,bd=1)#created a frame inside a frame called framepage
        self.myframe.place(x=10,y=10)

        self.canvas=Canvas(self.myframe,bg='white')#created canvas inside the frame that is inside to another frame
        self.frame=Frame(self.canvas,width=600,height=320)#created another frame inside the canvas
        self.myscrollbar=Scrollbar(self.myframe,orient="vertical",command=self.canvas.yview)#put the scrollbar inside the frame that is inside the topframe
        self.canvas.configure(yscrollcommand=self.myscrollbar.set)
        self.myscrollbar.pack(side="right",fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0),window=self.frame,anchor='nw')
        self.frame.bind("<Configure>",self.myfunction)
        self.data()#products in button with images

    def enable_removeitembtn(self,event=None):
        b = self.tree.get_children()

        if len(b) != 0:
            self.removeitem_btn.configure(state='normal')
        
        
    def to_clearcart(self):
        #self.modifyqty_btn.configure(state='normal')

        self.deleteall = messagebox.askyesno("system","clear all fields?")
        if self.deleteall > 0:
            self.removeitem_btn.configure(state='normal')
            self.transact_btn.configure(state='normal')
            self.addtocart_btn.configure(state='normal')
            self.subtotalamount_textbox.configure(state='normal')
            self.totalsamount_textbox.configure(state='normal')
            self.vat_textbox.configure(state='normal')
            self.itemquantity_entry.configure(state='normal')
            self.itemquantity_entry.delete(0,END)
            self.itemquantity_entry.configure(state='disabled')
            self.totalsamount =  0.0
            self.subtotalamount = 0.0
            self.vat  = 0.0
            self.totalsamount_textbox.delete(0.0,END)
            self.subtotalamount_textbox.delete(0.0,END)
            self.vat_textbox.delete(0.0,END)
            self.subtotalamount_textbox.configure(state='disabled')
            self.vat_textbox.configure(state='disabled')
            d = self.tree.get_children()

            c = self.tree.get_children()

            if len(c) != 0:
                for i in self.tree.get_children():
                    self.tree.delete(i)

            self.subtotalamount_textbox.delete(0.0,END)
            self.vat_textbox.delete(0.0,END)
            self.itemprice_textbox.configure(state='normal')
            self.itemprice_textbox.delete(0.0,END)
            self.itemprice_textbox.configure(state='disable')
            self.itemquantity_entry.delete(0,END)
            self.cash_entry.configure(state='normal')
            self.cash_entry.delete(0,END)
            self.cash_entry.configure(state='disabled')
            
           
            self.change_textbox.configure(state='normal')
            self.change_textbox.delete(0.0,END)
            self.change_textbox.configure(state='disabled')
            self.removeitem_btn.configure(state='disabled')
            self.transact_btn.configure(state='disabled')
            self.subtotalamount_textbox.configure(state='disabled')
            self.totalsamount_textbox.configure(state='disabled')
            self.vat_textbox.configure(state='disabled')
            self.itemquantity_entry.configure(state='disabled')
            self.addtocart_btn.configure(state='disabled')
        else:
            return
    
    def data(self):

        if not firebase_admin._apps:

            cred = credentials.Certificate("inventory-a40cc-firebase-adminsdk-p47zd-18b7b0c713.json")
            firebase_admin.initialize_app(cred)
            db = firestore.client()



        file = open("products1.txt","r+")
        file.truncate(0)
        file.close()

        item_ref = db.collection("products") #change this
        docs = item_ref.stream()
        for doc in docs:
            #print(f'{doc.id}')
    
            items_ref = db.collection(u'products').document(f'{doc.id}')
            get_name= items_ref.get({u'name'})
            get_price = items_ref.get({u'price'})
            get_qty = items_ref.get({u'quantity'})
            name = get_name.get('name')
            price = get_price.get('price')
            qty  = get_qty.get('quantity')
            
            print (f'{doc.id}'+','+name+','+price+','+qty)
            open('products1.txt','a').write( f'{doc.id}'+','+name+','+price+','+qty+ '\n')


        #-------------------
        db = open("products1.txt", "r")
        file = csv.reader(db, delimiter=',')
        
        self.b = {}     
        table = [[col[0],col[1],col[2],col[3]] for col in file]
        pos_x, pos_y, cntr = 1, 1, 0
        productcodecntr = 0
        for value in table:
            self.image[cntr] = PhotoImage(file=self.image_list[cntr])
            #print("heg",self.image_list[cntr])
            if cntr % 5 == 0:
                pos_x = pos_x + 1
                pos_y = 0
            #value[2] = price and value[0]= product code#heigh=6,width=15 actual
            self.b[cntr] = Button(self.frame,image=self.image[cntr],
                text = ("stocks:"+ value[3]+'\n'+value[1]+'\n'+"₱"+value[2]), height=98,width=106,compound=CENTER,
                bg='black',font=('tahoma',10,'bold'),bd=4,anchor=S,
                command=lambda cntr=cntr :
                self.select_product(table[cntr][0],table[cntr][1],table[cntr][2],table[cntr][3],cntr),relief=RAISED,fg='white' )
            self.b[cntr].grid(row=pos_x, column=pos_y)
            #print(self.b[productcodecntr])
           


            pos_y = pos_y + 1
            
            cntr = cntr + 1
       
    def select_product(self,product_id,product_name,product_price,product_stocks,cntr):
        self.b[cntr]['fg'] = 'red'
        self.b[cntr]['bg'] = 'red'
        try:
       
            self.new_qty = askinteger('SYSTEM', 'Please enter QTY', minvalue=0, maxvalue=100)
            
            if self.new_qty is not None:
                self.b[cntr]['fg'] = 'white'
                self.b[cntr]['bg'] = 'black'
                self.product_stocks  = int(product_stocks)
                self.product_stocks -= self.new_qty
                if self.product_stocks == 0:
                    self.b[cntr].configure(fg='red')
                    messagebox.showinfo("system","out of stock")
                    self.itemprice_textbox.configure(state='normal')
                    self.itemprice_textbox.delete(0.0,END)
                    self.itemprice_textbox.configure(state='disabled')
                    self.itemquantity_entry.configure(state='normal')
                    self.itemquantity_entry.delete(0,END)
                    self.itemquantity_entry.configure(state='disabled')
                    
            
                    
                self.b[cntr]['text'] = ("Stocks: " + str(self.product_stocks) + '\n' + str(product_name)+ '\n' + "₱" + str(product_price))
                self.addtocart_btn.configure(state='normal')
                self.itemprice_textbox.configure(state='normal')
                self.itemquantity_entry.configure(state='normal')
                self.itemquantity_entry.delete(0,END)
                self.itemquantity_entry.insert(END,self.new_qty)
                
                self.quantity = self.itemquantity_entry.get()
               

              
                #print(self.product_stocks)
                self.product_id = product_id
                self.product_name = product_name
                self.product_price = product_price
                self.itemprice_textbox.delete(0.0,END)
                self.itemprice_textbox.insert(END,self.product_price)
               # print(product_id,product_name,product_price)
                self.itemprice_textbox.configure(state='disabled')
                self.itemquantity_entry.configure(state='disabled')
            else:
                self.b[cntr]['fg'] = 'white'
                self.b[cntr]['bg'] = 'black'
                return
        except:
                self.b[cntr]['fg'] = 'white'
                self.b[cntr]['bg'] = 'black'
                messagebox.showinfo("system","invalid quantity")
                return

    def myfunction(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),width=590,height=400)

    
        
    def goto_mainmenu(self):
        x = messagebox.askyesno("system message","log out?")
        if x > 0:
            self.topframe.pack_forget()
            self.framepage.destroy()
            self.frame = Mainmenu(root)
        else:
            return

    def goto_refresh(self):
        os.execl(sys.executable, sys.executable, *sys.argv)
       
      

     
    def to_remove_item(self):
                
        try:

            self.clear = messagebox.askyesno('system message','Remove from cart?')
            if self.clear > 0:
                
                focused = self.tree.focus()
                row = self.tree.item(focused)
                print(row["values"][5])
                print(row["values"][4])
                self.subtotalamount_textbox.configure(state='normal')
                self.subtotalamount  -= float(row["values"][5])
                self.vat_textbox.configure(state='normal')
                self.totalsamount_textbox.configure(state='normal')
                self.vat = self.subtotalamount * 0.12
                self.totalsamount = self.subtotalamount + self.vat
                self.totalsamount_textbox.delete(0.0,END)
                self.totalsamount_textbox.insert(END,self.totalsamount)
                self.vat_textbox.delete(0.0,END)
                self.vat_textbox.insert(END,self.vat)
                self.vat_textbox.configure(state='disable')
                self.totalsamount_textbox.configure(state='disabled')

                
                c = self.tree.get_children()

                if len(c) == 0:
                    self.totalsamount =  0.0
                    self.subtotalamount = 0.0
                    self.vat  = 0.0
                    self.totalsamount_textbox.configure(state='normal')
                    self.totalsamount_textbox.delete(0.0,END)
                    self.totalsamount_textbox.configure(state='disabled')
                    self.subtotalamount_textbox.configure(state='normal')
                    self.subtotalamount_textbox.delete(0.0,END)
                    self.subtotalamount_textbox.configure(state='disabled')
                    self.vat_textbox.configure(state='normal')
                    self.vat_textbox.delete(0.0,END)
                    self.vat_textbox.configure(state='disabled')

                    self.itemquantity_entry.configure(state="normal")
                    self.itemquantity_entry.delete(0,END)
                    self.itemquantity_entry.configure(state="disabled")
                    self.itemprice_textbox.configure(state="normal")
                    self.itemprice_textbox.delete(0.0,END)
                    self.itemprice_textbox.configure(state="disabled")
                    self.addtocart_btn.configure(state='disabled')
                    self.removeitem_btn.configure(state='disabled')
                            
                
                

                self.subtotalamount_textbox.delete(0.0,END)
                self.subtotalamount_textbox.insert(END,self.subtotalamount)
                self.subtotalamount_textbox.configure(state='disabled')
                self.selected_item = self.tree.selection()
                self.tree.delete(self.selected_item)
                self.removeitem_btn.configure(state='disabled')
                return
        except:
                self.to_clearcart()
                messagebox.showinfo("system","check for errors")
    
        
    def add_to_cart(self):

       
        
        try:
            if self.qty.get() > 0 :
       
                #self.modifyqty_btn.configure(state='normal')
                self.removeitem_btn.configure(state='normal')
                self.transact_btn.configure(state='normal')
                self.subtotalamount_textbox.configure(state='normal')
                self.totalsamount_textbox.configure(state='normal')
                self.vat_textbox.configure(state='normal')
                self.change_textbox.configure(state='normal')
                #self.cash_entry.configure(state='normal')
                self.price= float(self.itemprice_textbox.get("1.0",END))#got the entry output from textbox of price
                self.quantity = self.qty.get()#got the entered value in quantity entry
                self.amount = self.price * self.quantity#multiplied price and quantity
                self.sales_id = self.counter #generated sales id per add to cart
                
                '''
               
                for line in self.tree.get_children(): #this block of codes  compares the product id if its the same then only the quantity is added in the treeview
                    for value in self.tree.item(line)['values']:
                        if value == self.product_id:
                            self.tree.delete(line)
                            self.entered_quantity  += self.new_qty
                '''
                               
                 

               
                self.tree.insert("", END, values=(self.sales_id,self.product_id,self.product_name,self.product_price,self.quantity,float(self.amount)))
                
             
                
                self.subtotalamount += self.amount
                self.subtotalamount_textbox.delete(0.0,END)
                self.subtotalamount_textbox.insert(END,self.subtotalamount)
                self.vat = self.subtotalamount * 0.12
                self.totalsamount = self.subtotalamount + self.vat
                self.totalsamount_textbox.delete(0.0,END)
                self.totalsamount_textbox.insert(0.0,self.totalsamount)
                self.vat_textbox.delete(0.0,END)
                self.vat_textbox.insert(END,self.vat)
                self.subtotalamount_textbox.configure(state='disabled')
                self.totalsamount_textbox.configure(state='disabled')
                self.vat_textbox.configure(state='disabled')
                self.change_textbox.configure(state='disabled')
                self.itemprice_textbox.configure(state='normal')
                self.itemprice_textbox.delete(0.0,END)
                self.itemprice_textbox.configure(state='disabled')
                self.itemquantity_entry.configure(state='normal')
                self.itemquantity_entry.delete(0,END)
                self.itemquantity_entry.configure(state='disabled')
                self.addtocart_btn.configure(state="disabled")
            else:
                messagebox.showinfo("SYSTEM","Invalid quantity")
                self.itemprice_textbox.configure(state='normal')
                self.itemprice_textbox.delete(0.0,END)
                self.itemprice_textbox.configure(state='disabled')
                self.itemquantity_entry.configure(state='normal')
                self.itemquantity_entry.delete(0,END)
                self.itemquantity_entry.configure(state='disabled')
                self.addtocart_btn.configure(state="disabled")
                self.addtocart_btn.configure(state="disabled")
                return
        
        except:
                self.itemprice_textbox.configure(state='normal')
                self.itemprice_textbox.delete(0.0,END)
                self.itemprice_textbox.configure(state='disabled')
                self.itemquantity_entry.configure(state='normal')
                self.itemquantity_entry.delete(0,END)
                self.itemquantity_entry.configure(state='disabled')
                self.addtocart_btn.configure(state="disabled")
                messagebox.showinfo("Error","Invalid Quantity")
                self.addtocart_btn.configure(state="disabled")
                return
        
 
                 
    def generate_salesID(self):
        self.counter += 1
        

    def get_product(self):
        pass
    
    def to_transact(self):
        
        global output
        #try:
        self.askcash = askfloat('SYSTEM', 'Please enter AMOUNT')
        if self.askcash > 0 and self.askcash >= float(self.totalsamount):

            self.subtotalamount_textbox.configure(state='normal')
            self.totalsamount_textbox.configure(state='normal')
            self.vat_textbox.configure(state='normal')
            self.change_textbox.configure(state='normal')

            self.generate_salesID()#calling sales id per transaction
            self.getcash =  self.askcash
            self.change = float(self.getcash)- float(self.totalsamount)
            self.change_textbox.delete(0.0,END)
            self.change_textbox.insert(END,float(self.change))


    
                
            #for child in self.tree.get_children():
                   
               # open('sales.txt', 'a').write( str(self.tree.item(child)["values"])+ '\n')

                
            self.monthvar = self.date.strftime("%Y-%m-%d")
            cntr=0
            for line in self.tree.get_children():#change to file write====to make it look like data,data,data
                for value in self.tree.item(line)['values']:
                    if cntr % 6 == 0:
                        open('sales.txt', 'a').write(self.monthvar + ',')
                    open('sales.txt', 'a').write(str(value)+',')
                
                    cntr += 1
                open('sales.txt','a').write('\n')


    

            

       



            file = io.StringIO()
            with redirect_stdout(file):

                print("============================================================\n")
                
                print("\t\t  JESUS' POS SYSTEM RECEIPT\n\n")
                print("Transaction Time:" , str(self.localtime))
                print("TRANSACTION DETAILS: receipt ID#",str(self.sales_id) + '\n')
                print("ITEM CODES\t\tNAME\t\tPRICE\t  QTY\t AMOUNT")
                for child in self.tree.get_children():
                    print(str(self.tree.item(child)["values"]))

                '''
                cntr=0
                for line in self.tree.get_children():#change to file write====to make it look like data,data,data,
                    if cntr % 3 == 0:
                        print('\n')
                    for value in self.tree.item(line)['values']:
                        if value == self.product_name or value == self.new_qty or value == self.product_price:
                            print(str(value),end="\t\t")
                        
                        cntr += 1
                 '''
                print("Transaction ID : ",str(self.tree.item(child)["values"][0]))
                print("ITEM CODE: ",str(self.tree.item(child)["values"][1]))
                print("Item name: ",str(self.tree.item(child)["values"][2]))
                print("Price: ",str(self.tree.item(child)["values"][3]))
                print("Qty: ",str(self.tree.item(child)["values"][4]))
                print("SUB TOTAL : " ,str(self.subtotalamount))
                print("vaT: " ,str(self.vat))
                print("TOTAL AMOUNT : " ,str(self.totalsamount))
                print("Cash: " ,str(self.getcash))
                print("Change: " ,str(self.change))




           

                
         
            print("\t\tTHANK YOU FOR BUYING...\n")
            print("============================================================\n")
                # here be all the commands whose print output
                # we want to capture.

            output = file.getvalue()
      
            #outputs = list(output)
            #for i in outputs:
                #outputs.append(i)
            
                    
            c  = self.tree.get_children()
            if len(c) != 0:
                for i in self.tree.get_children():
                    self.tree.delete(i)
                        
                    
            self.subtotalamount_textbox.delete(0.0,END)
            self.totalsamount_textbox.delete(0.0,END)
            self.vat_textbox.delete(0.0,END)
            self.itemprice_textbox.configure(state='normal')
            self.itemprice_textbox.delete(0.0,END)
            self.itemprice_textbox.configure(state='disable')
            self.itemquantity_entry.configure(state='normal')
            self.itemquantity_entry.delete(0,END)
            self.cash_entry.configure(state='disabled')
            self.change_textbox.configure(state='disable')
            messagebox.showinfo("Your change is ",self.change)
            
            self.clear = messagebox.askyesno('system message','WOULD YOU LIKE TO  BUY AGAIN?')
            if self.clear > 0:
                self.change_textbox.configure(state='normal')
                self.change_textbox.delete(0.0,END)
                self.change_textbox.configure(state='disabled')
                self.cash_entry.configure(state='normal')
                self.cash_entry.delete(0,END)
                self.cash_entry.configure(state='disabled')
                  
                #self.modifyqty_btn.configure(state='disable')
                self.removeitem_btn.configure(state='disable')
                self.transact_btn.configure(state='disable')
                self.addtocart_btn.configure(state='disable')
                    
                self.itemquantity_entry.configure(state='normal')
                self.itemquantity_entry.delete(0,END)
                self.itemquantity_entry.configure(state='disabled')
                self.vat_textbox.config(state='disabled')
                self.subtotalamount_textbox.config(state='disabled')
                self.totalsamount_textbox.config(state='disabled')

            else:
                messagebox.showinfo("sys","THANK YOU , PLS COME AGAIN!")
                self.topframe.pack_forget()
                self.topframe = receipt_window(root)
          
                    
        elif self.askcash < float(self.totalsamount):
            messagebox.showinfo("SYSTEM MESSAGE","Insufficient cash!")
            return
        else:
            return
    #except:
        #messagebox.showinfo("Invalid transaction")
        #return

class Mainmenu():
     def __init__(self,master):

        self.master =master
        self.frame = Frame(self.master,bg='light blue',width=1000,height=200,relief=RIDGE,bd=10)
        self.master.title("MAINMENU")
        self.master.geometry("880x200+280+200")
        self.goto_pos  = Button(self.frame,text="P.O.S",padx=45,pady=5,bd=10,relief=RAISED,font=('tahoma',12,'bold'),fg='white',bg='black',command=self.to_pos)
        self.goto_pos .place(x=50,y=50)
        self.goto_inventory  = Button(self.frame,text="INVENTORY",padx=15,pady=5,bd=10,relief=RAISED,font=('tahoma',12,'bold'),fg='white',bg='black',command=self.to_inventory)
        self.goto_inventory.place(x=250,y=50)
        self.exit_btn  = Button(self.frame,text="EXIT",padx=45,pady=5,bd=10,relief=RAISED,font=('tahoma',12,'bold'),fg='white',bg='red',command=self.exit2)
        self.exit_btn.place(x=450,y=50)
        self.salesreport_btn = Button(self.frame,text="SALES REPORT",padx=15,pady=5,bd=10,relief=RAISED,font=('tahoma',12,'bold'),fg='white',bg='black',command=self.to_salesreport)
        self.salesreport_btn.place(x=650,y=50)
        self.frame.pack()

     def to_salesreport(self):
        self.ask = messagebox.askyesno('SYSTEM','go to SALES REPORT?')
        if self.ask > 0:
            self.frame.pack_forget()
            self.frame = salesreport_window(root)
            return
            
     def to_pos(self):
        self.frame.pack_forget()
        self.frame = POS_window(root)
     def to_inventory(self):
        messagebox.showinfo("SYTEM","INVENTORY SYSTEM IS OFFLINE")
        return #put codes HERE to connect to inventory system==================================================
     def exit2(self):
        self.exit = messagebox.askyesno('SYSTEM','press yes to exit')
        if self.exit > 0:
            self.frame.pack_forget()
            self.frame = login_window(root)
            return


class salesreport_window():
    def __init__(self,master):

        self.master =master
        self.topsframe = Frame(self.master,bg='light blue',width=1000,height=500,relief=RIDGE,bd=10)
        self.secondtopframe  = Frame(self.topsframe,width =1000,height=1000,bg='light blue')
       
        self.framecont=Frame(self.secondtopframe,relief=GROOVE,width=500,height=1000,bd=1)
        self.master.title("MONTHLY SALES REPORT")
        self.master.geometry("880x500+280+150")
        self.varsmonth = StringVar()
        salesmonth_lbl = Label(self.topsframe,text='Sales report as of the month: ',font=('tahoma',12,'bold'),bg='light blue')
        salesmonth_lbl.place(x=150,y=50)
        self.cb = ttk.Combobox(self.secondtopframe, font=("tahoma",12,"bold"),text= self.varsmonth,values=("JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY","JUNE","JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"))
        self.cb.config(width=10)
        self.cb.set("SELECT")
        self.cb.config(state="readonly")
        
        self.cb.place(x=400,y=50)
        self.cb.bind('<<ComboboxSelected>>', self.on_select)

    

        self.canvas2=Canvas(self.framecont,bg='white')
        self.frameinside=Frame(self.canvas2,width=650,height=275)#to readjust tree2
        self.canvas2.pack(side="left")
        self.canvas2.create_window((0,0),window=self.frameinside,anchor='nw')

        #buttons
        self.mainmenu2_btn = Button(self.topsframe,text="MAINMENU",bd=5,relief=RAISED,font=('tahoma',10,'bold'),fg='white',bg='black',command=self.goto_mainmenu)
        self.mainmenu2_btn.place(x=620,y=50)

        self.totalsales_lbl = Label(self.topsframe,text='TOTAL SALES',font=('tahoma',15),bg='light blue')
        self.totalsales_lbl.place(x=150,y=400)
        self.totalsales_textbox = Text(self.topsframe ,height = 1, width = 20,font=('arial' , 12,'bold'),state="disabled")
        self.totalsales_textbox.place(x=350,y=400)

        self.tree2 = ttk.Treeview(self.frameinside)
        self.scroll2 = ttk.Scrollbar(self.framecont,orient="vertical",command=self.tree2.yview)
        self.scroll2.pack(side="left",fill='y')
        self.tree2.configure(yscrollcommand=self.scroll2.set)
        self.tree2['show']="headings"
        self.tree2['columns'] = ("1","2","3","4","5","6","7")
        self.tree2.column("1",width=120)
        self.tree2.column("2", width=60)
        self.tree2.column("3",width=60)
        self.tree2.column("4",width=120)
        self.tree2.column("5",width=120)
        self.tree2.column("6",width=60)
        self.tree2.column("7",width=120)
        
        self.tree2.heading("1",text ="Date Sold")
        self.tree2.heading("2", text="Sales ID")
        self.tree2.heading("3",text ="Prod ID")
        self.tree2.heading("4",text ="Product Name")
        self.tree2.heading("5",text ="Price")
        self.tree2.heading("6",text ="Quantity")
        self.tree2.heading("7",text ="Amount")

        #attributes added
        self.totalsales2 = 0.0

        self.s = ttk.Style()
        self.s.configure('Treeview', rowheight=25)
        self.tree2.place(x=0, y = 0)

        self.secondtopframe.pack()
        self.framecont.place(x=150,y=100)#to move the sales tree
        self.frameinside.pack()
        self.topsframe.pack()
    def on_select(self,event=None):
        
        self.month = self.varsmonth.get()
        self.totalsales2 = 0
        for i in self.tree2.get_children():
            self.tree2.delete(i)

        listofmonths = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY","JUNE","JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"]
        
              
        
        if  self.month == "MARCH":
         
            
            db2 = open(r"C:\Users\JUSUS CARL SANCHEJA\Desktop\sancheja\POS_FINAL\sales.txt", "r")
            file2 = csv.reader(db2, delimiter=',')
            
                  
            table2 = [[col[0],col[1],col[2],col[3],col[4],col[5],col[6],col[7]] for col in file2]
           
            cntr = 0
            start_date = datetime.date(2019, 3, 1)
            end_date   = datetime.date(2019, 4, 1)
            #print(str(end_date))
            for value2 in table2:
                if table2[cntr][0] != str(end_date):
                    self.tree2.insert("", END, values=(table2[cntr][0],table2[cntr][1],table2[cntr][2],table2[cntr][3],table2[cntr][4],table2[cntr][5],table2[cntr][6]))
                    self.totalsales2 += float(table2[cntr][6])
                else:
                    break
                cntr += 1
                

            self.totalsales_textbox.configure(state='normal')
            self.totalsales_textbox.delete(0.0,END)
            self.totalsales_textbox.insert(END,self.totalsales2)
            self.totalsales_textbox.configure(state='disabled')
        elif self.month == "APRIL":
         
            
            db2 = open(r"C:\Users\JUSUS CARL SANCHEJA\Desktop\sancheja\POS_FINAL\sales.txt", "r")
            file2 = csv.reader(db2, delimiter=',')
            
            
            table2 = [[col[0],col[1],col[2],col[3],col[4],col[5],col[6],col[7]] for col in file2]
           
            cntr = 0
            start_date = datetime.date(2019, 4, 1)
            end_date   = datetime.date(2019, 5, 1)
            for value2 in table2:
                if table2[cntr][0] != str(end_date)  and table2[cntr][0] == str(start_date):
                    self.tree2.insert("", END, values=(table2[cntr][0],table2[cntr][1],table2[cntr][2],table2[cntr][3],table2[cntr][4],table2[cntr][5],table2[cntr][6]))
                    self.totalsales2 += float(table2[cntr][6])
                cntr += 1
                

            self.totalsales_textbox.configure(state='normal')
            self.totalsales_textbox.delete(0.0,END)
            self.totalsales_textbox.insert(END,self.totalsales2)
            self.totalsales_textbox.configure(state='disabled')
            

        else:
            messagebox.showinfo("SYSTEM","No sales report yet for the month: "+ self.month)
            for i in self.tree2.get_children():
                self.tree2.delete(i)

            
            self.totalsales_textbox.configure(state='normal')
            self.totalsales_textbox.delete(0.0,END)
            self.totalsales_textbox.configure(state='disabled')
            


    def goto_mainmenu(self):
        x = messagebox.askyesno("system message","mainmenu?")
        if x > 0:
            self.topsframe.pack_forget()
            self.topsframe = Mainmenu(root)
        else:
            return


class receipt_window():
    def __init__(self,master):
        global output
        
      
        self.master =master
        self.master.title("RECEIPT")
        self.master.geometry("500x700+420+0")
        self.master.configure(bg='light blue')
        self.topsframe = Frame(self.master,bg='light blue',width=1000,height=500)
        


        self.receipt_textbox = Text(self.topsframe,height=500,width=300,relief=RIDGE)
        self.receipt_textbox.place(x=1,y=1)
        self.receipt_textbox.bind("<Button-1>", self.goto_pos)


        self.receipt_textbox.delete(0.0,END)
        self.receipt_textbox.insert(END,str(output))
        



        self.topsframe.pack(anchor='nw',expand=True,fill='y')

    def goto_pos(self,event=None):
        self.topsframe.pack_forget()
        self.topsframe = POS_window(root)
        self.receipt_textbox.delete(0.0,END)
        

        
root = Tk()


login_window(root)



root.mainloop()

