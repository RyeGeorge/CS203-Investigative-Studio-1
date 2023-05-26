from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

app.secret_key = 'nfe8shil3h29jlpj281rbjv'
    