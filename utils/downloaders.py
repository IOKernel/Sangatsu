import os
import requests
import zipfile
import tarfile

def download_stockfish(OS, script_dir):
    stockfish_path = os.path.join(script_dir, 'bin', 'stockfish')
    if OS == 'Windows':
        url = 'https://stockfishchess.org/files/stockfish_15_win_x64_avx2.zip'
        stockfish_path += '.exe'
        # download stockfish
        r = requests.get(url)
        # save stockfish.zip to bin folder and extract it then delete zip file
        with open(os.path.join(script_dir, 'bin', 'stockfish.zip'), 'wb') as f:
            f.write(r.content)
        # extract stockfish to bin folder
        with zipfile.ZipFile(os.path.join(script_dir, 'bin', 'stockfish.zip'), 'r') as zip_ref:
            zip_ref.extract('stockfish_15_win_x64_avx2/stockfish_15_x64_avx2.exe', os.path.join(script_dir, 'bin'))
        # rename stockfish_15_win_x64_avx2.exe to stockfish.exe
        os.rename(os.path.join(script_dir, 'bin', 'stockfish_15_win_x64_avx2', 'stockfish_15_x64_avx2.exe'), stockfish_path)
        # delete stockfish.zip
        os.remove(os.path.join(script_dir, 'bin', 'stockfish.zip'))
        # delete stockfish_15_win_x64_avx2 folder
        os.rmdir(os.path.join(script_dir, 'bin', 'stockfish_15_win_x64_avx2'))

    elif OS == 'Linux':
        url = 'https://stockfishchess.org/files/stockfish_15_linux_x64.zip'
        r = requests.get(url)
        # save stockfish.zip to bin folder and extract it then delete zip file
        with open(os.path.join(script_dir, 'bin', 'stockfish.zip'), 'wb') as f:
            f.write(r.content)
        # extract stockfish to bin folder
        with zipfile.ZipFile(os.path.join(script_dir, 'bin', 'stockfish.zip'), 'r') as zip_ref:
            # stockfish_15_linux_x64/stockfish_15_x64
            zip_ref.extract('stockfish_15_linux_x64/stockfish_15_x64', os.path.join(script_dir, 'bin'))
        # rename stockfish_15_x64_avx2 to stockfish
        os.rename(os.path.join(script_dir, 'bin', 'stockfish_15_linux_x64/stockfish_15_x64'), stockfish_path)
        # delete stockfish.zip
        os.remove(os.path.join(script_dir, 'bin', 'stockfish.zip'))
        # delete stockfish_15_linux_x64 folder
        os.rmdir(os.path.join(script_dir, 'bin', 'stockfish_15_linux_x64'))
        # make stockfish executable
        os.chmod(stockfish_path, 0o755)
    else:
        raise Exception('OS not supported')

    print('Stockfish downloaded')

def download_geckodriver(OS, script_dir):
    geckodriver_path = os.path.join(script_dir, 'bin', 'geckodriver')
    if OS == 'Windows':
        url = 'https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-win-aarch64.zip'
        geckodriver_path += '.exe'
        # download geckodriver
        r = requests.get(url)
        # save geckodriver.zip to bin folder and extract it then delete zip file
        with open(os.path.join(script_dir, 'bin', 'geckodriver.zip'), 'wb') as f:
            f.write(r.content)
        # extract geckodriver to bin folder
        with zipfile.ZipFile(os.path.join(script_dir, 'bin', 'geckodriver.zip'), 'r') as zip_ref:
            zip_ref.extract('geckodriver.exe', os.path.join(script_dir, 'bin'))
        # delete geckodriver.zip
        os.remove(os.path.join(script_dir, 'bin', 'geckodriver.zip'))
    elif OS == 'Linux':
        url = 'https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux64.tar.gz'
        # download geckodriver
        r = requests.get(url)
        # save geckodriver.tar.gz to bin folder and extract it then delete tar.gz file
        with open(os.path.join(script_dir, 'bin', 'geckodriver.tar.gz'), 'wb') as f:
            f.write(r.content)
        # extract geckodriver to bin folder
        with tarfile.open(os.path.join(script_dir, 'bin', 'geckodriver.tar.gz'), 'r:gz') as tar_ref:
            tar_ref.extract('geckodriver', os.path.join(script_dir, 'bin'))
        # delete geckodriver.tar.gz
        os.remove(os.path.join(script_dir, 'bin', 'geckodriver.tar.gz'))
        # make geckodriver executable
        os.chmod(geckodriver_path, 0o755)
    else:
        raise Exception('OS not supported')
