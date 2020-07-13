import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec
from connection import database_connection
import matplotlib


def dashboard(date_from, date_to, userid):
    gs=gridspec.GridSpec(3, 3)

    fig = plt.figure(figsize=(10,8))
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0,2])
    ax3 = fig.add_subplot(gs[1,:])

    type_label =[]
    type_num = []

    cat_label = []
    cat_num =[]

    cat_amount_label= []
    cat_amount_num =[]

    #see income against expense

    database = "expense_tracker.db"
    conn = database_connection(database)
    c = conn.cursor()
    c.execute("SELECT income_expense, SUM(amount) from Expenses where Date(date) between ? and ? and userid=? GROUP BY income_expense", (date_from, date_to,userid))

    type_values = c.fetchall()

    for rows in type_values:
        label_value = rows[0]
        num_value = rows[1]

        type_label.append(label_value)
        type_num.append(num_value)

    ax1.bar(type_label, type_num, color=['red','green'])
    ax1.set_xlabel('Income/Expense')
    ax1.set_ylabel('Amount')

    #See catgories i pie chart by percentage
    c.execute("SELECT category, COUNT(*) from Expenses where Date(date) between ? and ? and userid=? and income_expense='Expense'  GROUP BY category", (date_from, date_to,userid))

    cat_values = c.fetchall()

    for rows in cat_values:
        cat_label_value = rows[0]
        cat_num_value = rows[1]

        cat_label.append(cat_label_value)
        cat_num.append(cat_num_value)

    ax2.pie(cat_num, labels=cat_label, autopct='%1.1f%%')

    c.execute("SELECT category, SUM(amount) from Expenses where Date(date) between ? and ? and userid=? and income_expense='Expense' GROUP BY category", (date_from, date_to,userid))

    cat_amount_values = c.fetchall()

    for rows in cat_amount_values:
        cat_amount_label_value = rows[0]
        cat_amount_num_value = rows[1]

        cat_amount_label.append(cat_amount_label_value)
        cat_amount_num.append(cat_amount_num_value)

    ax3.bar(cat_amount_label, cat_amount_num)
    ax3.set_xlabel('Category')
    ax3.set_ylabel('Amount')

    fig.tight_layout()

    return fig

