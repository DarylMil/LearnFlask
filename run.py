from blog import create_app

app = create_app() # can pass in some other config.py files here

if __name__ == "__main__":
    app.run(debug=True)

     