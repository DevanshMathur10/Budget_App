class Category():
    def __init__(self,category):
        self.category=category
        self.ledger=[]
        self.budget=0

    def deposit(self,amt,desc=""):
        self.amt=float(amt)
        self.desc=desc
        self.budget+=self.amt
        obj={"amount":self.amt,"description":self.desc}
        self.ledger.append(obj)
        
    def withdraw(self,amt,desc=""):
        self.amt=float(amt)
        self.desc=desc
        obj={"amount":self.amt*-1,"description":self.desc}
        if self.amt<=self.budget:
            self.budget-=self.amt
            self.ledger.append(obj)          
            return True
        else:
            return False
        
    def transfer(self,amt,category):
        if self.budget>=amt:
            transferamt=self.withdraw(amt,"Transfer to "+category.category)
            if transferamt:
                category.deposit(amt,"Transfer from "+self.category)
            return True
        else:
            return False

    def check_funds(self,checkamt):
        if checkamt<=self.budget:
            return True
        else:
            return False

    def get_balance(self):
        return self.budget

    def get_withdrawals(self):
        final=0
        for trans in self.ledger:
            if trans['amount']<0:
                final+=trans['amount']
        return final

    def __str__(self):
        info=str(self.category).center(30,"*")
        for i in self.ledger:
            chars=23-len(i["description"])
            if chars>0:
                descshow=i["description"]+" "*chars
            elif chars==0:
                descshow=i["description"]
            else:
                descshow=i["description"][:23]
            info+="\n"+descshow

            amtshow = f"{i['amount']:.2f}"
            chars=7-len(amtshow)
            if chars==0:
                info+=amtshow
            else:
                info+=" "*chars+amtshow

        info+="\nTotal: "+f"{self.budget}"
        return info

def create_spend_chart(categories):
    out="Percentage spent by category\n"
    x=len(categories)
    y=100
    percentages=[]
    totalspent=0
    for i in categories:
        totalspent+=i.get_withdrawals()
    for i in categories:
        each=i.get_withdrawals()/totalspent
        percentages.append(int((each//0.1)*10))

    while y >= 0:
        if y!=100:
            out+="\n"
        if y==100:
            out += str(y)+"| "
        elif y==0:
            out+="  "+str(y)+"| "
        else:
            out+=" "+str(y)+"| "

        col=0
        while col<x:
            if percentages[col]>=y:
                out+="o  "
            else:
                out+=" "*3
            col+=1
        y-=10
    out += "\n" + " "*4 +"-"+ "-"*x*3

    max_name_length=0
    for i in categories:
        if len(i.category)>max_name_length:
            max_name_length=len(i.category)

    xlab=0
    while xlab<max_name_length:
        out+="\n"+" "*5
        for i in categories:
            try:
                out+=i.category[xlab]+" "*2
            except:
                out+=" "*3
        xlab+=1

    return out