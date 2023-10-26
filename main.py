from website import create_app

app = create_app()

if __name__ == '__main__': # run web server only if file is ran directly
    app.run(debug=True) # every time you update code web server reruns automatically (turn off in production)

