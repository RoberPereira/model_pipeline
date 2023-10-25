from app import build_app
# from etl import etl
# from train import train


app = build_app()

if __name__ == '__main__':
    # etl = etl.Etl()
    # etl.run()

    # train = train.Train()
    # train.run()
    app.run(debug=True, port=8081)
