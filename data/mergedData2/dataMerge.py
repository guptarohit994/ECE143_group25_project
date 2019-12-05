
##Data cleaning and combination
import pandas as pd


def merge(data1, set2, filename):
    """
    Merge CAPE dataset and UCOP dataset by instructors name
    :param data1: UCOP dataset
    :type panda dataframe
    :param set2: CAPE dataset(csv filename)
    :type String
    :param filename: saving path and name for merged file
    :type String
    :return: no return
    """
    count = 0
    data2 = pd.read_csv(set2)
    data2 = data2.dropna(subset=['Instructor'])
    name = data2.Instructor
    last = []
    first = []
    for i in name:
        last.append(i.split(',')[0])
        first.append(i.split(',')[1])
    lastN = ["".join(list(filter(str.isalnum, line))) for line in last]
    firstN = ["".join(list(filter(str.isalnum, line))) for line in first]
    lastN = [x.upper() for x in lastN]
    firstN = [x.upper() for x in firstN]

    data2['lastName'] = lastN
    data2['firstName'] = firstN
    inx = pd.Series(list(range(len(first))))
    data2 = data2.set_index(inx)

    Gp = list(data1.GrossPay)
    Rp = list(data1.RegularPay)
    Op = list(data1.OvertimePay)
    Otp = list(data1.OtherPay)
    title = list(data1.Title)
    Pay = []
    C1 = []
    C2 = []
    C3 = []
    C4 = []
    fName = []
    lName = []
    flag = False
    data = data2
    f1 = list(data1.firstName)
    f2 = list(data2.firstName)
    l1 = list(data1.lastName)
    l2 = list(data2.lastName)
    for n in range(len(l2)):
        flag = False
        for m in range(len(l1)):
            if l1[m] == l2[n]:

                if (f1[m] in f2[n]) or (f2[n] in f1[m]):
                    flag = True
                    payment = Gp[m]
                    fname2 = f1[m]
                    lname2 = l1[m]
                    p1 = Rp[m]
                    p2 = Op[m]
                    p3 = Otp[m]
                    t = title[m]
        if flag:
            Pay.append(payment)
            fName.append(fname2)
            lName.append(lname2)
            C1.append(p1)
            C2.append(p2)
            C3.append(p3)
            C4.append(t)

        else:
            temp = data
            data = temp.drop([n])

    data['fName2'] = fName
    data['lName2'] = lName
    data['GrossPay'] = Pay
    data['RegularPay'] = C1
    data['OvertimePay'] = C2
    data['OtherPay'] = C3
    data['Title'] = C4
    data.to_csv(filename, index=None, header=True)


def main():
    '''
    Merge CAPE dataset and UCOP dataset by same instructors name
    :return void
    '''
    df = pd.read_csv('ucop_sd_all.csv')
    df = df.dropna(subset=['FirstName'])
    df = df.dropna(subset=['LastName'])
    # Add full name and delete first name and last name
    # Clean Data
    df = df[df.FirstName != '*****']
    # Add full name and delete first name and last name
    first = df.FirstName
    last = df.LastName
    firstN = ["".join(list(filter(str.isalnum, line))) for line in first]
    lastN = ["".join(list(filter(str.isalnum, line))) for line in last]
    name = last + ',' + first
    fullName = ["".join(list(filter(str.isalnum, line))) for line in name]

    df['firstName'] = firstN
    df['lastName'] = lastN
    inx = pd.Series(list(range(len(first))))
    df = df.set_index(inx)
    csvList = ['ANTH', 'BENG', 'BIOL', 'CAT', 'CENG', 'CGS', 'CHEM', 'CHIN', 'COGS', 'COMM', 'CONT', 'CSE', 'DOC',
               'ECON', 'ECE', 'EDS', 'ENVR', 'ERC', 'ESYS', 'ETHN', 'FILM', 'FPMU', 'HDP', 'HIST', 'HMNR', 'HUM',
               'ICAM', 'INTL', 'JAPN', 'JUDA', 'LATI', 'LAWS', 'LING', 'LIT', 'MAE', 'MATH', 'MMW', 'MUIR', 'MUS',
               'NENG', 'PHIL', 'PHYS', 'POLI', 'PSYC', 'RELI', 'REV', 'RSM', 'SDCC', 'SE', 'SIO', 'SOC', 'SOE', 'STPA',
               'SXTH', 'THEA', 'TMC', 'TWS', 'USP', 'VIS', 'WARR', 'WCWP']
    for i in range(len(csvList)):
        print(i)
        csv = 'cape_' + csvList[i] + '_auto.csv'
        fname = 'D:\ECE143\ECE143_group25_project-master\data\Merged_' + csvList[i] + '.csv'
        merge(df, csv, fname)


if __name__ == "__main__":
    main()
