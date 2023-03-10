from registros_ig import app
from flask import jsonify, render_template,request,redirect,flash
from registros_ig.models import *
from datetime import date
from datetime import datetime


@app.route("/")
def index():
    registros=select_all()
   
    return render_template("index.html", pageTitle="Registro y movimientos de Criptomonedas",data=registros, page='Inicio')

@app.route("/purchase", methods=["GET","POST"])
def calcular():
    if request.method=="GET":
        return render_template("purchase.html", form={}, page='Purchase')
    
    else:
        if 'calcular' in request.form:
            value_to=request.form['from_q']
            value_to_q = request.form['value_to']
            value_from_qr=request.form['value_from']
            cambio=cambios(value_from_qr,value_to_q)
            valor_pu=float(value_to)*cambio
            
            list_request={
                "value_from":request.form['value_from'],
                "from_q":request.form['from_q'],
                "value_to":request.form['value_to'],
                "to_q":str(cambio),
                "value_pu":str(valor_pu)
            }
            return render_template("purchase.html",form=list_request)

        date=(datetime.today().strftime('%Y-%m-%d'))
        hora=(datetime.today().strftime('%H:%M'))


        if 'operacion' in request.form:
            errores=[]
            recur=recuperado()
            
            value_to=request.form['from_q']
            value_to_q = request.form['value_to']
            value_from_qr=request.form['value_from']
            cambio=cambios(value_from_qr,value_to_q)
            valor_pu=float(value_to)*cambio
            
            list_request={
                "value_from":request.form['value_from'],
                "from_q":request.form['from_q'],
                "value_to":request.form['value_to'],
                "to_q":str(cambio),
                "value_pu":str(valor_pu)
            } 
            
    
            if request.form['value_from'] != "EUR":
                errores.append("Moneda equivocada") 
                return render_template("purchase.html", msgError=errores, form=list_request)
            
            if float(request.form['from_q']) > float(recur) or float(request.form['from_q'])==False:
                errores.append("Fondos insuficientes ") 
                return render_template("purchase.html", msgError=errores, form=list_request)
                    
            if request.form['value_from'] == request.form['value_to']:
                errores.append("No sepuede operar con la misma moneda")
                return render_template("purchase.html", msgError=errores, form=list_request)
                
            if request.form['from_q'] <= "0":
                errores.append("solo puedes digitar cantidades mayores a 0 o iguales a 1")
                return render_template("purchase.html", msgError=errores, form=list_request)
                
            if request.form['value_from'] == "BTC":
                errores.append("No se puede vender una moneda diferente a BTC a EUR")
                return render_template("purchase.html", msgError=errores, form=list_request)

            else:
                
                insert([date,
                        hora,
                        request.form['value_from'],
                        request.form['from_q'],
                        request.form['value_to'],
                        request.form['to_q']
                ])  
                            
                flash('Movimiento registrado correctamente')
                return redirect("/")

    
    if 'cancelar' in request.form:
         return redirect("/")

@app.route("/status")
def status():
    if request.method == "GET":
       
        return render_template("status.html", adicion=invertido(), recovered=recuperado(), valorC=valorCompra(), page='Status')