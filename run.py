from main_app import create_app

app = create_app('config.py')  # Charge la configuration

if __name__ == "__main__":
    app.run(debug=True)
