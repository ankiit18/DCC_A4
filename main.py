from flask import Flask , render_template , request , session , redirect
from flask_sqlalchemy import SQLAlchemy
import json
from flask_mail import Mail
from datetime import datetime 

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Ankit%40123@localhost/ds"


db = SQLAlchemy(app)


class purchase_3(db.Model):
    sno = db.Column(db.String(10), primary_key=True)
    ref = db.Column(db.String(20),nullable = False)
    journal_date = db.Column(db.String(30),  nullable = False)
    date_of_purchase = db.Column(db.String(30), nullable = False)
    date_of_expiry = db.Column(db.String(30))
    name_purchaser = db.Column(db.String(120), nullable = False)
    prefix = db.Column(db.String(10), nullable = False)
    bond_no = db.Column(db.String(10), nullable = False)
    denominations = db.Column(db.String(40), nullable = False)
    issue_branch_code = db.Column(db.String(8), nullable = False)
    issue_teller = db.Column(db.String(14), nullable = False)
    status = db.Column(db.String(20), nullable = False)


class redemption_3(db.Model):
    sno = db.Column(db.String(10), primary_key=True)
    date_encashment = db.Column(db.String(40),nullable = False)
    party = db.Column(db.String(120),  nullable = False)
    acc_no = db.Column(db.String(30), nullable = False)
    prefix = db.Column(db.String(30))
    bond_no= db.Column(db.String(10), nullable = False)
    denominations = db.Column(db.String(40), nullable = False)
    pay_branch_code = db.Column(db.String(8), nullable = False)
    pay_teller = db.Column(db.String(20), nullable = False)



@app.route('/')
def index():
    parties = db.session.query(redemption_3.party).distinct().all()
    buyer = db.session.query(purchase_3.name_purchaser).distinct().all()

    return render_template('index.html' , parties = parties , buyer = buyer)

@app.route('/search', methods=['GET'])
def search():
    # Get the user's query, selected table, and selected column from the request parameters
    query = request.args.get('query')
    table = request.args.get('table')
    column = request.args.get('column')

    # Define the valid columns to search (excluding Sr. No. and Status)
    purchase_columns = ['sno','ref', 'journal_date', 'date_of_purchase', 'date_of_expiry', 'name_purchaser', 'prefix', 'bond_no', 'denominations', 'issue_branch_code', 'issue_teller']
    redemption_columns = ['sno' , 'date_encashment', 'party', 'acc_no', 'prefix', 'bond_no', 'denominations', 'pay_branch_code', 'pay_teller']

    # Check the selected table and validate the column
    if table == 'purchase':
        # Perform the search in the redemption table
        result = db.session.query(purchase_3).filter(getattr(purchase_3, column) == query).all()
    elif table == 'redemption':
        # Perform the search in the redemption table
        result = db.session.query(redemption_3).filter(getattr(redemption_3, column) == query).all()
    else:
        return "Invalid table selected for search.", 400

    # Render the search results in an HTML template (e.g., search_results.html)
    return render_template('search_results.html', results=result )

@app.route('/company', methods=['GET'])
def company():
    # Get the buyer parameter from the query string
    comp_name = request.args.get('comp')
    buyer = purchase_3.query.filter_by(name_purchaser=comp_name).all()
    
    year_totals = {
    year: {
        'total_sum': 0,
        'total_count': 0
    }
    for year in ['2019' , '2020', '2021', '2022', '2023' , '2024']  # Add the range of years you want to track
    }
    
    # Iterate through each purchase and calculate totals
    for buy in buyer:
        buys_date = buy.date_of_purchase
        
        if (buys_date[len(buys_date) - 1] == '9') :
            # if '2019' not in year_totals:
            #     year_totals['2019'] = {'total_sum': 0, 'total_count': 0}
        
            denominations_str = buy.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            year_totals['2019']['total_sum'] += denominations_int
            year_totals['2019']['total_count'] += 1

        if (buys_date[len(buys_date) - 1] == '0') :
            # if '2020' not in year_totals:
            #     year_totals['2020'] = {'total_sum': 0, 'total_count': 0}

            denominations_str = buy.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            year_totals['2020']['total_sum'] += denominations_int
            year_totals['2020']['total_count'] += 1

        if (buys_date[len(buys_date) - 1] == '1') :
            # if '2021' not in year_totals:
            #     year_totals['2021'] = {'total_sum': 0, 'total_count': 0}

            denominations_str = buy.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            year_totals['2021']['total_sum'] += denominations_int
            year_totals['2021']['total_count'] += 1

        if (buys_date[len(buys_date) - 1] == '2') :
            # if '2022' not in year_totals:
            #     year_totals['2022'] = {'total_sum': 0, 'total_count': 0}

            denominations_str = buy.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            year_totals['2022']['total_sum'] += denominations_int
            year_totals['2022']['total_count'] += 1

        if (buys_date[len(buys_date) - 1] == '3') :
            # if '2023' not in year_totals:
            #     year_totals['2023'] = {'total_sum': 0, 'total_count': 0}

            denominations_str = buy.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            year_totals['2023']['total_sum'] += denominations_int
            year_totals['2023']['total_count'] += 1

        if (buys_date[len(buys_date) - 1] == '4') :
            # if '2024' not in year_totals:
            #     year_totals['2024'] = {'total_sum': 0, 'total_count': 0}
            
            denominations_str = buy.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            year_totals['2024']['total_sum'] += denominations_int
            year_totals['2024']['total_count'] += 1
    
    # Render the template and pass the year_totals dictionary
    return render_template('company.html', year_totals=year_totals)

    

@app.route('/party', methods=['GET'])
def party():
    
    par = request.args.get('party')
    parties = redemption_3.query.filter_by(party=par).all()
    
    year_totals = {
    year: {
        'total_sum': 0,
        'total_count': 0
    }
    for year in ['2019' , '2020', '2021', '2022', '2023' , '2024']  # Add the range of years you want to track
    }
    
    # Iterate through each purchase and calculate totals
    for pars in parties:
        buys_date = pars.date_encashment
        
        if (buys_date[len(buys_date) - 1] == '9') :
            # if '2019' not in year_totals:
            #     year_totals['2019'] = {'total_sum': 0, 'total_count': 0}
        
            denominations_str = pars.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            year_totals['2019']['total_sum'] += denominations_int
            year_totals['2019']['total_count'] += 1

        if (buys_date[len(buys_date) - 1] == '0') :
            # if '2020' not in year_totals:
            #     year_totals['2020'] = {'total_sum': 0, 'total_count': 0}

            denominations_str = pars.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            year_totals['2020']['total_sum'] += denominations_int
            year_totals['2020']['total_count'] += 1

        if (buys_date[len(buys_date) - 1] == '1') :
            # if '2021' not in year_totals:
            #     year_totals['2021'] = {'total_sum': 0, 'total_count': 0}

            denominations_str = pars.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            year_totals['2021']['total_sum'] += denominations_int
            year_totals['2021']['total_count'] += 1

        if (buys_date[len(buys_date) - 1] == '2') :
            # if '2022' not in year_totals:
            #     year_totals['2022'] = {'total_sum': 0, 'total_count': 0}

            denominations_str = pars.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            year_totals['2022']['total_sum'] += denominations_int
            year_totals['2022']['total_count'] += 1

        if (buys_date[len(buys_date) - 1] == '3') :
            # if '2023' not in year_totals:
            #     year_totals['2023'] = {'total_sum': 0, 'total_count': 0}

            denominations_str = pars.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            year_totals['2023']['total_sum'] += denominations_int
            year_totals['2023']['total_count'] += 1

        if (buys_date[len(buys_date) - 1] == '4') :
            # if '2024' not in year_totals:
            #     year_totals['2024'] = {'total_sum': 0, 'total_count': 0}
            
            denominations_str = pars.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            year_totals['2024']['total_sum'] += denominations_int
            year_totals['2024']['total_count'] += 1
    
    # Render the template and pass the year_totals dictionary
    return render_template('party.html', year_totals=year_totals)


@app.route('/ques', methods=['GET'])
def ques():
    par = request.args.get('party')
    parties = redemption_3.query.filter_by(party=par).all()
    dicto = {}
    sum = 0 

    for pars in parties :
        bno = pars.bond_no
        comp = purchase_3.query.filter_by(bond_no = bno).all()
        for co in comp :
            denominations_str = co.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            sum += denominations_int
            if co.name_purchaser not in dicto:
                dicto[co.name_purchaser] = denominations_int
            else :
                dicto[co.name_purchaser] += denominations_int
            

        
    return render_template('ques.html' , dicto = dicto , par = par , sum = sum)



@app.route('/ans', methods=['GET'])
def ans():
    comps = request.args.get('comp')
    print(f"Received comp parameter: {comps}")
    buyer = purchase_3.query.filter_by(name_purchaser=comps).all()
    print(f"Buyer query result: {buyer}")

    dicto = {}
    total_sum = 0 

    for buy in buyer:
        bno = buy.bond_no
        parties = redemption_3.query.filter_by(bond_no=bno).all()
        print(f"Parties query result for bond number {bno}: {parties}")

        for par in parties:
            denominations_str = par.denominations.replace(',', '')
            denominations_int = int(denominations_str)
            total_sum += denominations_int

            if par.party not in dicto:
                dicto[par.party] = denominations_int
            else:
                dicto[par.party] += denominations_int

    print(f"dicto dictionary: {dicto}")
    print(f"Total sum: {total_sum}")

    return render_template('ans.html', dicto=dicto, comps=comps, sum=total_sum)


app.run(debug = True)