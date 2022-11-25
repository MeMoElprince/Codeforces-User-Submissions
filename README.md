# Codeforces-User-Submissions

## Requirements

### Linux User

```shell
# installing python
sudo apt install python3
```

```shell
# installing pip
sudo apt install python3-pip
```

### Windows User

1. **Windows user can install python3 from [here](https://www.python.org/downloads/)** and make sure that you will check the option `Add Python 3.x to PATH` while installing and .

2. **Install pip** from [here](https://pip.pypa.io/en/stable/installation/)

## Installing

```shell
# downloading the script
git clone https://github.com/MeMoElprince/Codeforces-User-Submissions.git
```

or you can download the script from [here](https://github.com/MeMoElprince/Codeforces-User-Submissions/archive/refs/heads/main.zip)

***open your terminal and run these commands***

```shell
# open the folder of the script
cd Codeforces-User-Submissions
```

```shell
# downloading the requirements and updating them
pip install --upgrade -r requirements.txt
```

***Install [Chorme Driver](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver/01fde32d0ed245141e24151f83b7c2db31d596a4#quick-installation)***

## Usage

1. Rename `.env.example` to `.env` and fill the data:
   1. HANDLE: your codeforces handle
   2. PASSWORD: your codeforces password

2. open folder `data`
   1. put your standing's links in `links.txt`
   2. put your trainees names and handles in `data.csv`

3. open your terminal and run this command:

    ```shell
    # run the script
    python3 main.py
    ```

4. your csv file will be in the folder `data` in `trainees.csv`

5. **Enjoy!**

## Demo Video

<https://user-images.githubusercontent.com/63050133/203844258-f325bc10-7dd2-43a8-920b-cc3686355b18.mp4>
