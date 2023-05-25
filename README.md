# Dicord Token Checker cli

![Example Output](output.png)

Simple script made in python to check discord tokens for account data(total of 10 data points) and write it in csv format

Unlike other programs there are no 3rd party dependencies required; just python3 and a working internet connection
## Install 
Download discordTokenChecker.py

## Usage

Example usage `python3 discordTokenChecker.py --input input.txt --output.txt`

Use argument `-i` or `--input` to specifiy your input file(required)

Format should be 1 token per line, e.g:

- token0
- token1
- token2
- token3
- token4
- token5

Use argument `-o` or `--output` to specifiy your output file(required, output is .csv format)



The information we can get from discord with just a token is the following: 

- token
- username
- discriminator
- nickname
- email
- emailVerified
- phone
- locale
- nsfw
- linkedAccounts
- mfaStatus
- ID
- bio

## Planned Features:
- Server
- DM Count
- Last Activitiy 
- Account creation date
- Nitro status
- Flags (staff , verified, etc...)

## DISCLAIMER

THIS PROGRAM IS ONLY ALLOWED FOR LEGAL USE, ANY USAGE WHICH CAN BE CONSIDERED ILLEGAL IS FORBIDDEN BY THE CREATOR AND THEY ARE NOT RESPONSIBLE FOR ANY DAMAGE THAT MAY OCCUR; THIS MAY INCLUDE USING STOLEN TOKENS WHICH IS ALSO FOBIDDEN 
