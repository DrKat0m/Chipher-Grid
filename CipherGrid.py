import webbrowser
from encoder import Encoder
from decoder import Decoder

def main():
    # Initializing encoder and decoder objects
    encoder = Encoder()
    decoder = Decoder()
    has_access=True
    # Examples
    #data = 'https://open.spotify.com/'
    #data = 'malware.exe'
    #data = 'https://uiverse.io/cards'
    #data = 'www.linkedin.com/in/drkat0m'
    #data = 'https://forms.gle/ydKy1PUFQumRPyR48'
    data = 'https://youtu.be/wDgQdr8ZkTw?si=-qZ_fE30123k3YE4'
    # Encoding the data

    qr_code, qr_text = encoder.encode(data)
    
    # Decoding the QR code to verify the process
    if has_access:
        decoded_data = decoder.decode(qr_code, qr_text)
        print("Original Data:", data)
        print("Decoded Data:", decoded_data)
        direct_url=decoded_data
        if direct_url[-4:len(direct_url)]=='.exe':
            print("Warning malware injection attempted!!!")
        elif direct_url[0:8]=='https://' or direct_url[0:7]=='http://':
            webbrowser.open(direct_url)
            print(f"Opening URL: {direct_url}")
        else:
            direct_url='https://' + direct_url
            webbrowser.open(direct_url)
            print(f"Opening URL: {direct_url}")
        
if __name__ == "__main__":
    main()