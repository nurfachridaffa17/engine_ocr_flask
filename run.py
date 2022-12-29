from ktp_ocr_crop import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=7007, ssl_context=('fullchain.pem','privkey.pem'))