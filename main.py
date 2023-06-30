from tkinter import messagebox
from tkinter.ttk import Combobox
import mysql
from mysql.connector import Error
from tkinter import *
from tkinter.messagebox import showinfo
from functools import partial


def rgb_hack(rgb):
    return "#%02x%02x%02x" % rgb


def get_select_int(select_str_format):
    return int('{}'.format(select_str_format[0]))


def get_select_str(id_str_format):
    return str('{}'.format(id_str_format[0]))


def bank(conn, date, p_passport, p_date_money):
    passport = p_passport.get()
    print(date)
    date_money = p_date_money.get()
    print(date_money)
    with conn.cursor(buffered=True) as cursor:
        cursor.execute(f"SELECT `id_people` FROM `people` WHERE `pasport_number` = '{passport}'")
        ((people,),) = cursor.fetchall()
        print(people)
        cursor.execute(f"SELECT `id_fine` FROM `fine` WHERE `id_people` = '{people}' AND `fine_date` = '{date}'")
        fine = cursor.fetchone()
        fine = get_select_str(fine)
        cursor.execute("insert into bank_bank (id_fine, payment_date) values ('" + fine + "','" + date_money + "')")
        cursor.execute(
            f"Update `fine` set `payment` = '{date_money}' where `id_people` = '{people}' and `fine_date` = '{date}'")


def please_pasport(conn):
    root = Tk()
    root.geometry("400x400")
    lbl2 = Label(root, text="Номер паспорта")
    lbl2.place(x=20, y=60)
    p_passport = Entry(root)
    p_passport.place(x=180, y=60)
    btn1 = Button(root, text='далее', command=partial(banktest, conn, p_passport))
    btn1.place(x=180, y=180)


def banktest(conn, passport):
    p_passport = passport.get()
    root = Tk()
    root.geometry("400x400")
    with conn.cursor(buffered=True) as cursor:
        cursor.execute(f"SELECT `id_people` FROM `people` WHERE `pasport_number` = '{p_passport}'")
        ((id_person,),) = cursor.fetchall()
        print(id_person)
        cursor.execute(f"SELECT `fine_date` FROM `fine` WHERE `id_people` = '{id_person}'")
        money = cursor.fetchall()

    cmb = Combobox(root, width="10", values=money)

    class TableDropDown(Combobox):
        def __init__(self, parent):
            self.current_table = StringVar()
            Combobox.__init__(self, parent)
            self.config(textvariable=self.current_table, state="readonly",
                        values=["Customers", "Pets", "Invoices", "Prices"])
            self.current(0)
            self.place(x=50, y=50, anchor="w")

    def checkcmbo(conn, id_person):
        date = cmb.get()
        mes = "c вас "
        with conn.cursor() as cursor:
            cursor.execute(
                f"SELECT `actual_amount` FROM `fine` WHERE `id_people` = '{id_person}' AND `fine_date` = '{date}'")
            ((monn,),) = cursor.fetchall()
            mes += str(monn)
            window = Tk()
            window.geometry('1920x1080')
            window.title("оплата")

            lbl1 = Label(window, text=mes)
            lbl1.place(x=20, y=30)
            lbl2 = Label(window, text="Номер паспорта")
            lbl2.place(x=20, y=60)
            p_passport = Entry(window)
            p_passport.place(x=180, y=60)
            lbl3 = Label(window, text="Дата оплаты")
            lbl3.place(x=20, y=90)
            p_date = Entry(window)
            p_date.place(x=180, y=90)
            btn1 = Button(window, text='Оплатить', command=partial(bank, conn, date, p_passport, p_date))
            btn1.place(x=180, y=180)

    cmb.place(relx="0.1", rely="0.1")

    btn = Button(root, text="Get Value", command=partial(checkcmbo, conn, id_person))
    btn.place(relx="0.5", rely="0.1")

    root.mainloop()


def show_section(conn, p_info1):
    p_section = p_info1.get()
    if p_section == "":
        print("insert status. All fields are required")
    else:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT `name_violation` FROM `collection of violations` WHERE `section`='{p_section}'")
            ((violation,),) = cursor.fetchall()
    showinfo(title="Нарушение", message=violation)


def good_generation(conn):
    with conn.cursor() as cursor:
        cursor.execute(
            f"SELECT DISTINCT `id_people` FROM `fine` WHERE `fine_date` not between '2000-11-01' and '2001-11-01' ")
        person = cursor.fetchall()
        print(person)
        people = "Сообщения молодец отправлены: "
        namestr = ""
        for row in person:
            cursor.execute(f"SELECT  `full_name` FROM `people` WHERE `id_people` = '{row[0]}'")
            ((name,),) = cursor.fetchall()
            namestr += name
            namestr += ', '
        if namestr == "":
            showinfo(title="", message="Таких людей нет")
        else:
            people += namestr
            people += " "
            people += "все они проездили год без штрафов"
            showinfo(title="", message=people)


def bad_generation(conn):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT `id_people`, count(*) from `fine` where `payment` is null Group By `id_people`")
        people = "Повестки в суд отправлены: "
        count_fines = cursor.fetchall()
        for row in count_fines:
            if row[1] > 2:
                cursor.execute(f"SELECT `full_name` from `people` where `id_people`= '{row[0]}'")
                ((name,),) = cursor.fetchall()
                people += name
                people += ", "

        people += "они плохо ездили"
        showinfo(title="", message=people)


def show_name(conn, p_info1):
    p_passport = p_info1.get()
    print(p_passport)
    if p_passport == "":
        print("insert status. All fields are required")
    else:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT `full_name` FROM `people` "
                           f"WHERE `pasport_number`='{p_passport}'")
            person = cursor.fetchone()
            person = get_select_str(person)
    showinfo(title="ФИО", message=person)


def find_person_into_base(conn, p_info3):
    print(p_info3)
    p_passport = p_info3.get()
    print(p_passport)
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT `full_name` FROM `people` WHERE `pasport_number` ='{p_passport}'")
        person = cursor.fetchone()
        if person is None:
            showinfo(title="Извините!", message="Человек не найден! Добавьте в базу!")
        else:
            showinfo(title="ФИО", message=person)


def add_violation_btn_clicked(conn, p_info1, p_info2, p_info3):
    p_passport = p_info1.get()
    p_section = p_info2.get()
    p_date = p_info3.get()
    if p_passport == "":
        print("insert status. All fields are required")
    else:
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(f"SELECT `id_people` FROM `people` "
                           f"WHERE `pasport_number`='{p_passport}'")
            person = cursor.fetchone()
            person = get_select_str(person)
            print(person)
            cursor.execute(f"SELECT `id_violation` FROM `collection of violations`"
                           f"WHERE `section`='{p_section}'")
            violation = cursor.fetchone()
            violation = get_select_str(violation)
            cursor.execute(f"SELECT `amount_violation` FROM `collection of violations`"
                           f"WHERE `section`='{p_section}'")
            amount = cursor.fetchone()
            amount = get_select_int(amount)
            cursor.execute(
                f"SELECT `id_people` FROM `fine` WHERE DATEDIFF(CURDATE(), fine_date) < 366 AND `id_people`='{person}'")
            increase = cursor.fetchall()
            if increase:
                amount = amount * 1.1
            cursor.execute(
                "insert into fine (id_people, id_violation, fine_date, actual_amount) values ('" + person + "','" + violation + "','" + p_date + "','" + str(
                    amount) + "')")
            conn.commit()


def add_violation_btm(conn):
    window = Tk()
    window.geometry('720x720')
    window['background'] = '#fed6da'
    window.title("Person registration")
    with conn.cursor() as cursor:
        cursor.execute(f"select `pasport_number` from `people`")
        people = cursor.fetchall()
        cmb = Combobox(window, width="10", values=people)
        cmb.place(x=180, y=30)
    with conn.cursor() as cursor:
        cursor.execute(f"select `section` from `collection of violations`")
        section = cursor.fetchall()
        combox = Combobox(window, width="10", values=section)
        combox.place(x=180, y=60)

    lbl1 = Label(window, text="pasport_people", background=rgb_hack((252, 123, 136)))
    lbl1.place(x=20, y=30)

    lbl2 = Label(window, text="section", background=rgb_hack((252, 123, 136)))
    lbl2.place(x=20, y=60)

    lbl3 = Label(window, text="violation_date", background=rgb_hack((252, 123, 136)))
    lbl3.place(x=20, y=90)

    p_date = Entry(window, background=rgb_hack((252, 123, 136)))
    p_date.place(x=180, y=90)

    btn1 = Button(window, text='Add violation into database',
                  command=partial(add_violation_btn_clicked, conn, cmb, combox, p_date),
                  background=rgb_hack((252, 123, 136)))
    btn1.place(x=180, y=180)

    add_full_name_messagebox = partial(show_name, conn, cmb)
    btn2 = Button(window, text='Show full name', command=add_full_name_messagebox, background=rgb_hack((252, 123, 136)))
    btn2.place(x=360, y=30)

    add_violation_messagebox = partial(show_section, conn, combox)
    btn3 = Button(window, text='Show violation', command=add_violation_messagebox, background=rgb_hack((252, 123, 136)))
    btn3.place(x=360, y=60)


def add_person_btn_clicked(conn, p_info1, p_info2, p_info3, p_info4):
    p_name = p_info1.get()
    p_birth = p_info2.get()
    p_passport = p_info3.get()
    p_liesince = p_info4.get()
    if p_name == "":
        print("insert status. All fields are required")
    else:
        query_is_in_db = (f"SELECT `id_people` FROM `people` WHERE `pasport_number` = '{p_passport}'")
        with conn.cursor(buffered=True) as cursor:
            cursor.execute(query_is_in_db)
            person = cursor.fetchone()
        if person is None:
            with conn.cursor() as cursor:
                cursor.execute(
                    "insert into people (full_name, birth_date, pasport_number, license_number) values ('" + p_name + "','" + p_birth + "','" + p_passport + "','" + p_liesince + "')")
                conn.commit()


def potential_profit(conn, p_date1, p_date2):
    date1 = p_date1.get()
    date2 = p_date2.get()
    text_message= 'Прибыль с ' + date1 + ' по ' + date2 + ' равна:\n'
    data1 = date1[8:10]
    print(data1)
    month1 = int(date1[5:7])
    print(month1)
    year1 = int(date1[0:4])
    print(year1)
    month2 = int(date2[5:7])
    print(month2)
    year2 = int(date2[0:4])
    print(year2)
    while (month1 != month2 or year1 != year2):
        print(text_message)
        with conn.cursor(buffered=True) as cursor:
            if month1 == 1:
                first_date = str(year1) + '-' + str(month1) + '-' + data1
                month1 += 1
                second_date = str(year1) + '-' + str(month1) + '-' + data1
                cursor.execute(
                    f"select sum(`actual_amount`) from `fine` where `fine_date` between '{first_date}' and '{second_date}'")
                ((amount,),) = cursor.fetchall()
                print(amount)
                if amount:
                    text_message += 'Январь ' + str(year1) + ' года: ' + str(amount) +'\n'
                else:
                    text_message += 'Январь ' + str(year1) + ' года: ' + str(0)+'\n'
                continue
            if month1 == 2:
                first_date = str(year1) + '-' + str(month1) + '-' + data1
                month1 += 1
                second_date = str(year1) + '-' + str(month1) + '-' + data1
                cursor.execute(
                    f"select sum(`actual_amount`) from `fine` where `fine_date` between '{first_date}' and '{second_date}'")
                ((amount,),) = cursor.fetchall()
                if amount:
                    text_message += 'Февраль ' + str(year1) + ' года: ' + str(amount)+'\n'
                else:
                    text_message += 'Февраль ' + str(year1) + ' года: ' + str(0)+'\n'
                continue

            if month1 == 3:
                first_date = str(year1) + '-' + str(month1) + '-' + data1
                month1 += 1
                second_date = str(year1) + '-' + str(month1) + '-' + data1
                cursor.execute(
                    f"select sum(`actual_amount`) from `fine` where `fine_date` between '{first_date}' and '{second_date}'")
                ((amount,),) = cursor.fetchall()
                if amount:
                    text_message += 'Март ' + str(year1) + ' года: ' + str(amount)+'\n'
                else:
                    text_message += 'Март ' + str(year1) + ' года: ' + str(0)+'\n'
                continue

            if month1 == 4:
                first_date = str(year1) + '-' + str(month1) + '-' + data1
                month1 += 1
                second_date = str(year1) + '-' + str(month1) + '-' + data1
                cursor.execute(
                    f"select sum(`actual_amount`) from `fine` where `fine_date` between '{first_date}' and '{second_date}'")
                ((amount,),) = cursor.fetchall()
                if amount:
                    text_message += 'Апрель ' + str(year1) + ' года: ' + str(amount)+'\n'
                else:
                    text_message += 'Апрель ' + str(year1) + ' года: ' + str(0)+'\n'
                continue

            if month1 == 5:
                first_date = str(year1) + '-' + str(month1) + '-' + data1
                month1 += 1
                second_date = str(year1) + '-' + str(month1) + '-' + data1
                cursor.execute(
                    f"select sum(`actual_amount`) from `fine` where `fine_date` between '{first_date}' and '{second_date}'")
                ((amount,),) = cursor.fetchall()
                if amount:
                    text_message += 'Май ' + str(year1) + ' года: ' + str(amount)+'\n'
                else:
                    text_message += 'Май ' + str(year1) + ' года: ' + str(0)+'\n'
                continue

            if month1 == 6:
                first_date = str(year1) + '-' + str(month1) + '-' + data1
                month1 += 1
                second_date = str(year1) + '-' + str(month1) + '-' + data1
                cursor.execute(
                    f"select sum(`actual_amount`) from `fine` where `fine_date` between '{first_date}' and '{second_date}'")
                ((amount,),) = cursor.fetchall()
                if amount:
                    text_message += 'Июнь ' + str(year1) + ' года: ' + str(amount)+'\n'
                else:
                    text_message += 'Июнь ' + str(year1) + ' года: ' + str(0)+'\n'
                continue
            if month1 == 7:
                first_date = str(year1) + '-' + str(month1) + '-' + data1
                month1 += 1
                second_date = str(year1) + '-' + str(month1) + '-' + data1
                cursor.execute(
                    f"select sum(`actual_amount`) from `fine` where `fine_date` between '{first_date}' and '{second_date}'")
                ((amount,),) = cursor.fetchall()
                if amount:
                    text_message += 'Июль ' + str(year1) + ' года: ' + str(amount) + '\n'
                else:
                    text_message += 'Июль ' + str(year1) + ' года: ' + str(0) + '\n'
                continue
            if month1 == 8:
                first_date = str(year1) + '-' + str(month1) + '-' + data1
                month1 += 1
                second_date = str(year1) + '-' + str(month1) + '-' + data1
                cursor.execute(
                    f"select sum(`actual_amount`) from `fine` where `fine_date` between '{first_date}' and '{second_date}'")
                ((amount,),) = cursor.fetchall()
                if amount:
                    text_message += 'Август ' + str(year1) + ' года: ' + str(amount) + '\n'
                else:
                    text_message += 'Август ' + str(year1) + ' года: ' + str(0) + '\n'
                continue
            if month1 == 9:
                first_date = str(year1) + '-' + str(month1) + '-' + data1
                month1 += 1
                second_date = str(year1) + '-' + str(month1) + '-' + data1
                cursor.execute(
                    f"select sum(`actual_amount`) from `fine` where `fine_date` between '{first_date}' and '{second_date}'")
                ((amount,),) = cursor.fetchall()
                if amount:
                    text_message += 'Сентябрь ' + str(year1) + ' года: ' + str(amount) + '\n'
                else:
                    text_message += 'Сентябрь ' + str(year1) + ' года: ' + str(0) + '\n'
                continue
            if month1 == 10:
                first_date = str(year1) + '-' + str(month1) + '-' + data1
                month1 += 1
                second_date = str(year1) + '-' + str(month1) + '-' + data1
                cursor.execute(
                    f"select sum(`actual_amount`) from `fine` where `fine_date` between '{first_date}' and '{second_date}'")
                ((amount,),) = cursor.fetchall()
                if amount:
                    text_message += 'Октябрь ' + str(year1) + ' года: ' + str(amount) + '\n'
                else:
                    text_message += 'Октябрь ' + str(year1) + ' года: ' + str(0) + '\n'
                continue
            if month1 == 11:
                first_date = str(year1) + '-' + str(month1) + '-' + data1
                month1 += 1
                second_date = str(year1) + '-' + str(month1) + '-' + data1
                cursor.execute(
                    f"select sum(`actual_amount`) from `fine` where `fine_date` between '{first_date}' and '{second_date}'")
                ((amount,),) = cursor.fetchall()
                if amount:
                    text_message += 'Ноябрь ' + str(year1) + ' года: ' + str(amount) + '\n'
                else:
                    text_message += 'Ноябрь ' + str(year1) + ' года: ' + str(0) + '\n'
                continue
            if month1 == 12:
                first_date = str(year1) + '-' + str(month1) + '-' + data1
                month1 = 1
                year1+=1
                second_date = str(year1) + '-' + str(month1) + '-' + data1
                cursor.execute(
                    f"select sum(`actual_amount`) from `fine` where `fine_date` between '{first_date}' and '{second_date}'")
                ((amount,),) = cursor.fetchall()
                if amount:
                    text_message += 'Декабрь ' + str(year1) + ' года: ' + str(amount) + '\n'
                else:
                    text_message += 'Декабрь ' + str(year1) + ' года: ' + str(0) + '\n'
                continue
    showinfo(title="Потенциальная прибыль", message=text_message)



def real_profit(conn, p_date1, p_date2):
    date1 = p_date1.get()
    date2 = p_date2.get()
    text = 'Прибыль с ' + date1 + ' по ' + date2 + ' равна: '

    with conn.cursor() as cursor:
        cursor.execute(f"select `id_fine` from `bank_bank` where `payment_date` between '{date1}' and '{date2}'")
        fine_id = cursor.fetchall()
        sum = 0
        if fine_id:
            for row in fine_id:
                cursor.execute(f"select `actual_amount` from `fine` where `id_fine` = '{row[0]}'")
                ((amount,),) = cursor.fetchall()
                print(amount)
                sum += int(amount)
        text += str(sum)
        showinfo(title="Реальная прибыль", message=text)


def real_profit_buttom(conn):
    window = Tk()
    window.geometry('720x720')
    window['background'] = '#fed6da'
    window.title("Прибль ГАИ")

    lbl1 = Label(window, text="Дата начала", background=rgb_hack((252, 123, 136)))
    lbl1.place(x=20, y=30)

    lbl2 = Label(window, text="Дата конца", background=rgb_hack((252, 123, 136)))
    lbl2.place(x=20, y=60)

    p_date1 = Entry(window, background=rgb_hack((252, 123, 136)))
    p_date1.place(x=180, y=30)

    p_date2 = Entry(window, background=rgb_hack((252, 123, 136)))
    p_date2.place(x=180, y=60)

    count_real_profit = partial(real_profit, conn, p_date1, p_date2)
    btn3 = Button(window, text='Расчитать реальную прибль', command=count_real_profit, background=rgb_hack((252, 123, 136)))
    btn3.place(x=20, y=120)
    count_pot_profit = partial(potential_profit, conn, p_date1, p_date2)
    btn3 = Button(window, text='Расчитать потенциальную прибыль', command=count_pot_profit, background=rgb_hack((252, 123, 136)))
    btn3.place(x=240, y=120)

def bad_people(conn):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT `id_people`, count(id_fine) as cid from `fine` Group By `id_people` ORDER BY `cid` DESC")
        people = "Cписок нарушителей: \n"
        count_fines = cursor.fetchall()
        for row in count_fines:
            cursor.execute(f"SELECT `full_name` from `people` where `id_people`= '{row[0]}'")
            ((name,),) = cursor.fetchall()
            people+=name+' количество штрафов: '+str(row[1])+'\n'
        showinfo(title="", message=people)
def section_stat(conn):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT `id_violation`, count(id_fine) as cid from `fine` Group By `id_violation` ORDER BY `cid` DESC")
        people = "Статистика нарушений: \n"
        count_fines = cursor.fetchall()
        for row in count_fines:
            cursor.execute(f"SELECT `name_violation` from `collection of violations` where `id_violation`= '{row[0]}'")
            ((name,),) = cursor.fetchall()
            people += name + ' количество штрафов: ' + str(row[1]) + '\n'

    showinfo(title="", message=people)
def add_person_btn(connection):
    window = Tk()
    window.geometry('1920x1080')
    window.title("Person registration")

    lbl1 = Label(window, text="person's name")
    lbl1.place(x=20, y=30)

    lbl2 = Label(window, text="Date of birth")
    lbl2.place(x=20, y=60)

    lbl3 = Label(window, text="Passport")
    lbl3.place(x=20, y=90)

    lbl4 = Label(window, text="Driving licence")
    lbl4.place(x=20, y=120)

    p_name = Entry(window)
    p_name.place(x=170, y=30)

    p_birthday = Entry(window)
    p_birthday.place(x=170, y=60)

    p_pasport = Entry(window)
    p_pasport.place(x=170, y=90)

    p_liecense = Entry(window)
    p_liecense.place(x=170, y=120)

    btn0 = Button(window, text='Find person in database', command=partial(find_person_into_base, connection, p_pasport))
    btn0.place(x=20, y=180)

    add_person_btn_clicked_wo_arg = partial(add_person_btn_clicked, connection, p_name, p_birthday,
                                            p_pasport, p_liecense, )
    btn1 = Button(window, text='Add person into database', command=add_person_btn_clicked_wo_arg)
    btn1.place(x=170, y=180)

def report(connection):
    window = Tk()
    window.geometry("1920x1080")
    window.title("reports")
    lbl1 = Label(window, text="Выберите тип отчета.", font=("Montserrat", 18))
    lbl1.place(x=60, y=60)
    btn6 = Button(window, text="Прибыль Гаи", font=("Montserrat", 18),
                  command=partial(real_profit_buttom, connection))
    btn6.place(x=60, y=120)

    btn7 = Button(window, text="Список нарушителей", font=("Montserrat", 18),
                  command=partial(bad_people, connection))
    btn7.place(x=60, y=180)
    btn8 = Button(window, text="Статистика популярных штрафов", font=("Montserrat", 18),
                  command=partial(section_stat, connection))
    btn8.place(x=60, y=240)
def gui(connection):
    window = Tk()
    window.geometry("1920x1080")
    window.title("police database")
    lbl1 = Label(window, text="Welcome to police database.", font=("Montserrat", 18))
    lbl1.place(x=60, y=60)

    add_person_btn_wo_arg = partial(add_person_btn, connection)
    btn1 = Button(window, text="Register new person", font=("Montserrat", 18), command=add_person_btn_wo_arg)
    btn1.place(x=60, y=120)

    add_violation_btn_clicked_wo_arg = partial(add_violation_btm, connection)
    btn2 = Button(window, text="Register new violation", font=("Montserrat", 18),
                  command=add_violation_btn_clicked_wo_arg)
    btn2.place(x=60, y=180)

    btn3 = Button(window, text="Good generation", font=("Montserrat", 18),
                  command=partial(good_generation, connection))
    btn3.place(x=60, y=240)

    btn4 = Button(window, text="Bad generation", font=("Montserrat", 18),
                  command=partial(bad_generation, connection))
    btn4.place(x=60, y=300)

    btn5 = Button(window, text="Bank", font=("Montserrat", 18))
    btn5.place(x=60, y=360)

    btn6 = Button(window, text="Отчеты", font=("Montserrat", 18),
                  command=partial(report, conn))
    btn6.place(x=60, y=420)

    

    window.mainloop()


conn = mysql.connector.connect(user='root', password='lolkek', host='127.0.0.1', port='3306',
                               database='police')
conn.autocommit = True
gui(conn)
