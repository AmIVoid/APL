# APL - Anime Priority List

## What is APL?
APL is an automatic anime watch priority list maker.

## How does APL work?
APL uses AniList's API to gather a users completed and planning list which is then imported into a Google Sheet where the data can be sorted.

## What is the purpose of APL?
As I have over 250+ anime planning to watch I usually can't decide what to watch first so I created a spreadsheet by hand to sort which anime I should watch first. This program is just to add a quality of life change for me and stop me from staying up making spreadsheets by hand.

***

# Installing

As of now there are 2 ways to install APL, by git and by an installer. I plan to add APL to the AUR in the future.

## Releases
Download the [APL Installer](https://github.com/AmIVoid/APL/releases/download/1.2/APLSetup.exe) here or at the releases page.

## Git
`git clone https://github.com/AmIVoid/APL.git` `pip install -r requirements.txt`

***

# Video Tutorial
[Video Tutorial](https://youtu.be/BWv0Y20jnDA)

# Written tutorial
Before starting APL you will need to have a few things for Google sheets to work.
## APL Spreadsheet
You can make your own spreadsheet for APL but I encourage that you copy my [example spreadsheet](https://docs.google.com/spreadsheets/d/1mOCYbzkizOQam56_DgkN5rL_xn9BRLyKh4p3yjfb5qs/edit?usp=sharing) and use that. To make a copy, go to File > Make a Copy

![Make copy](https://puu.sh/H40dI.png)

## Enabling the API
To enable the Google sheets API go to the [Google developer console](https://console.developers.google.com/cloud-resource-manager) and create a new project.

![](https://puu.sh/H40hM.png)

Choose a name for your project and click `Create`.

Go to the search bar at the top and search for `Google Sheets API` and choose the first option. Once you're in the Google Sheets API menu enable the API.

It should redirect you to the API overview and show you a button to create credentials for the API.
![Create Credentials](https://puu.sh/H40m1.png)

Click the create credentials and fill out the form so it's like this.

![Credentials form 1](https://puu.sh/H40o3.png)

In the next section choose a name any for a service account and enable its role to be an Editor.
![Credentials form 2](https://puu.sh/H40p8.png)

After continuing you will be prompted with a JSON file which is how the bot edits your spreadsheet. Download this file and rename it to credentials.json and put it in the folder where APL is.

One last step is to copy the service account email and add it as an editor to your spreadsheet.

![Service account](https://puu.sh/H40se.png)
![Editor](https://puu.sh/H40uG.png)

## Running APL
Running APL will show you 3 input boxes and 3 button as well as an indicator to show if credentials.json is present in the folder. Fill out the boxes with your details like so.

![GUI](https://puu.sh/H40xH.png)

Your spreadsheet ID can be found in the URL of your spreadsheet e.g. (https://docs.google.com/spreadsheets/d/1mOCYbzkizOQam56_DgkN5rL_xn9BRLyKh4p3yjfb5qs/edit, `1mOCYbzkizOQam56_DgkN5rL_xn9BRLyKh4p3yjfb5qs` is my example spreadsheet's ID)
The sheet name you will want to use is `Raw Data` if you've copied the example spreadsheet.

With that everything is ready to be run, if you wish to save your data (AniList name, Spreadsheet ID and Sheet Name) the `Save data` button will keep that data in a local file to be used the next time you open APL.
### Note: Inputting the data to the google sheet can take a while, the program will create an alert box to tell you when it is done. When the program doesnt respond it doesn't mean it's crashed.

***

## APL Score v1
The APL Score is based on 3 factors:
1. Mean Score (M) - Base score of Anime.
2. B Factor (B) - Bingability of a series over 12 episodes long but less than 50 episodes long with a score over 75%. <img src="https://render.githubusercontent.com/render/math?math=B=(M-75)*10^-2">
3. P Factor (P) - If the previous season has been watched.
<img src="https://render.githubusercontent.com/render/math?math=APL%20Score%20=%20M%20\times%20(1%20%2B%20(B%20%2B%20P))">
