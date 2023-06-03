#IF YOU ARE SEEING THIS AND YOU HAVE PAID FOR THIS PROGRAM IT MEANS THAT YOU HAVE BEEN SCAMMED !!
#THE SOURCE CODE IS LOCATED AT: https://github.com/EmptyGateAhead/discordTokenCheckerCLI
#CURRENT VERSION IS V3.0.0
#THE DATE IS 03/06/2023
import requests, argparse, sys, os
from datetime import datetime
parser = argparse.ArgumentParser(description="simplistic discord token checker, no bells or whistles")
parser.add_argument('-o', '--output', action='store', dest='outputFileName', required=True, help='output file')
parser.add_argument('-i', '--input', action='store', dest='inputFileName', required=True, help='input file')
parser.add_argument('-a', '--avatars', action='store', dest='getAvatars', required=False, help='download avatars and save them to directory with the accounts name and discriminator')
parser.add_argument('-s', '--split', nargs=2, action='store', dest='splitOptions', required=False, help='change how the program handles line splitting')
parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', required=False, help='output user data on the current token to the terminal')
parser.add_argument('-se', '--saveErrorTokens', action='store', dest='saveErrorTokens', required=False, help='saved locked tokens')
args = parser.parse_args()
i = 0
hits = 0
count = 0
error = 0
locked = 0
invalid = 0
fileLength = 0
inputFileName = str(args.inputFileName)
outputFile = str(args.outputFileName)

def main():
    global hits, count, error, locked, invalid ,fileLength, inputFileName, outputFile
    try:
        if args.splitOptions == None:
            splitChar = ':'
            splitPosition = int(0)
        else:
            splitChar = args.splitOptions[0]
            splitPosition = int(args.splitOptions[1])
        if args.getAvatars != None:
            if not os.path.exists(args.getAvatars):
                os.makedirs(args.getAvatars)
        if args.saveErrorTokens != None: saveErrorTokens = open(args.saveErrorTokens, 'a')
        with open(inputFileName, 'r') as getFileLength:
            fileLength = sum(1 for _ in getFileLength)
            getFileLength.close
        if fileLength < 1: print(f'{colors.error}[!] Cannot use an empty input file{colors.end}'); exit()
        outFile = open(outputFile, 'a')
        outFile.write('token,username,nickname,email,email verified,phone,locale,nsfw,linked accounts,mfa status,ID,bio,creation date,user flags,nitro status,server count,dm count,friend count,card count,payment info,avatar URL'+'\n')
        with open(inputFileName, 'r') as inputFile:
            for line in inputFile:
                token = str(line).rstrip('\n').split(splitChar)[splitPosition]
                print(f"{colors.attempt}[+] Trying {token}{colors.end}")
                response = requests.get("https://discordapp.com/api/users/@me", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36","Authorization": token})
                responseData = response.text
                if response.status_code == 200:
                    print(f"{colors.success}[+] Successfully got account data!{colors.end}")
                    try: identifier = int(responseData.split('"id": "')[1].split('"')[0])
                    except IndexError: identifier = 'Null'; pass
                    try: username = responseData.split('"username": "')[1].split('"')[0]
                    except IndexError: username = 'Null'; pass
                    try: discrim = responseData.split('"discriminator": "')[1].split('"')[0]
                    except IndexError: discrim = 'Null'; pass
                    try: email = responseData.split('"email": "')[1].split('"')[0]
                    except IndexError: email = 'Null'; pass
                    try: verifiedMail = responseData.split('"verified": ')[1].split(',')[0]
                    except IndexError: verifiedMail = 'Null'; pass
                    try: locale = responseData.split('"locale": "')[1].split('"')[0]
                    except IndexError: locale = 'Null'; pass
                    try: nsfw = responseData.split('"nsfw_allowed": ')[1].split(',')[0]
                    except IndexError: nsfw = 'Null'; pass
                    try: mfaStatus = responseData.split('"mfa_enabled": ')[1].split(',')[0]
                    except IndexError: mfaStatus = 'Null'; pass
                    try: bio = responseData.split('"bio": "')[1].split('"')[0].replace(',','，')#unicode comma
                    except IndexError: bio = 'Null'; pass
                    try: phone = responseData.split('"phone": "')[1].split('"')[0]
                    except IndexError: phone = 'Null'; pass
                    try: nickname = responseData.split('"global_name": "')[1].split('"')[0]
                    except IndexError: nickname = 'Null'; pass
                    try: linkedAccounts = responseData.split('"linked_users": ["')[1].split(']')[0]
                    except IndexError: linkedAccounts = 'Null'; pass
                    try: avatarID = responseData.split('"avatar": "')[1].split('"')[0]
                    except IndexError: avatarID = 'Null'; pass
                    try: creationDateUtc = datetime.utcfromtimestamp((int(identifier >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC')#
                    except IndexError: creationDateUtc = 'Unknown'; pass
                    try:
                        flag = int(responseData.split('"public_flags": ')[1].split(',')[0])
                        userFlags = getUserFlags(flag)
                    except IndexError: flags = 'Null'; pass
                    try:
                        nitro = int(responseData.split('"premium_type": ')[1].split(',')[0])
                        nitroStatus = getNitroStatus(nitro)
                    except IndexError: nitroStatus = 'Null'; pass
                    try: serverCount = getServerCount(token)
                    except IndexError: serverCount = 'Null'; pass
                    try: dmCount = getDmCount(token)
                    except IndexError: dmCount = 'Null'; pass
                    try: friendCount = getFriendCount(token)
                    except IndexError: friendCount = 'Null'; pass
                    paymentData, cardCount = getPayments(token)
                    avatarLink = getAvatar(identifier,avatarID,username,discrim)
                    if args.verbose == True:
                        print(f"{colors.data}[+] Token: {token}\n[+] User: {username}#{discrim}\n[+] Nickname: {nickname}\n[+] Email: {email} Verified: {verifiedMail}\n[+] Phone: {phone}\n[+] Locale: {locale}\n[+] NSFW: {nsfw}\n[+] Linked accounts: {linkedAccounts}\n[+] MFA: {mfaStatus}\n[+] ID: {identifier}\n[+] Creation Time: {creationDateUtc}\n[+] Nitro Status: {nitroStatus}\n[+] User Flags: {userFlags}\n[+] Friends Count: {friendCount}\n[+] Server Count: {serverCount}\n[+] DM Count: {dmCount}\n[+] BIO: {bio}\n[+] Card count: {cardCount}\n[+] Payment Data: {paymentData}\n[+] Avatar URL: {avatarLink}{colors.end}")
                    outFile.write(f'{token},{username}#{discrim},{nickname},{email},{verifiedMail},{phone},{locale},{nsfw},{linkedAccounts},{mfaStatus},{identifier},{bio},{creationDateUtc},{userFlags},{nitroStatus},{serverCount},{dmCount},{friendCount},{cardCount},{paymentData},{avatarLink}\n')
                    hits += 1
                elif response.status_code == 403:
                    print(f"{colors.locked}[-] Token locked: {token}{colors.end}")
                    if args.saveErrorTokens != None: saveErrorTokens.write(f'Locked: {token}\n')
                    locked += 1
                else:
                    print(f"{colors.invalid}[-] Token invalid: {token}{colors.end}")
                    if args.saveErrorTokens != None: saveErrorTokens.write(f'Invalid: {token}\n')
                    invalid += 1
                count += 1
                if args.verbose == False: clear(39,12)
                print(f'{colors.stats}[+] Hits: {hits}|Invalid: {invalid}|Locked: {locked}|Error: {error}| ({count}/{fileLength}){colors.end}')
            outFile.close()
        doOsClear()
        print(f'{colors.stats}[+] Program complete saved {hits} valid tokens to {outputFile}\n └Stats:\n  └Hits: {hits}|Locked: {locked}|Invalid: {invalid}|Error: {error}{colors.end}')
    except KeyboardInterrupt:
        doOsClear()
        print(f'{colors.error}[!] Program exited unsafely on line: {count} on file: {inputFileName}{colors.end}')

def getAvatar(identifier,avatarID,username,discrim):
    if avatarID != 'Null':
        avatarLocation = (f'https://cdn.discordapp.com/avatars/{identifier}/{avatarID}.png')
    else:
        avatarLocation = (f'https://cdn.discordapp.com/embed/avatars/{int(discrim) % 5}.png')
    if args.getAvatars != None:
        avatarRequest = requests.get(avatarLocation)
        username = username.replace('/','∕')#unicode slash
        avatarFile = open(f'{args.getAvatars}/{username}#{discrim}_Avatar.png','wb').write(avatarRequest.content)
    return avatarLocation

def getPayments(token):
    def paymentData(paymentSource):
        try: cardBrand = paymentSource.split('"brand": "')[1].split('"')[0]
        except IndexError: cardBrand = 'Null'; pass
        try: last4 = paymentSource.split('"last_4": "')[1].split('"')[0]
        except IndexError: last4 = 'Null'; pass
        try: address = paymentSource.split('"billing_address": {')[1].split('}')[0].replace('"','')
        except IndexError: address = 'Null'; pass
        try: expiryMonth = paymentSource.split('"expires_month": ')[1].split(',')[0]
        except IndexError: expiryMonth = 'Null'; pass
        try: expiryYear = paymentSource.split('"expires_year": ')[1].split(',')[0]
        except IndexError: expiryYear = 'Null'; pass
        expiryDate = (expiryMonth+'/'+expiryYear)
        return cardBrand, last4, expiryDate, address
    paymentSources = requests.get('https://discordapp.com/api/users/@me/billing/payment-sources', headers = {'Authorization': token})
    paymentSourceResponse = str(paymentSources.text)
    userCCData = []
    if paymentSources.status_code == 200 and paymentSourceResponse != '[]':
        if paymentSourceResponse.count('"id":') > 1:
            paymentSourceResponse = str(paymentSourceResponse).split('}, {')
            numberOfCards = len(paymentSourceResponse)
            for i in range(len(paymentSourceResponse)):
                cardBrand, last4, expiryDate, address = paymentData(str(paymentSourceResponse[0]))
                data = (f'Card type: {cardBrand}|Last 4: {last4}|Expiry: {expiryDate}|Address: ({address})')
                userCCData.append(data)
                paymentSourceResponse.pop(0)
        else:
            cardBrand, last4, expiryDate, address = paymentData(str(paymentSourceResponse[0]))
            numberOfCards = 1
            data = (f'Card type: {cardBrand}|Last 4: {last4}|Expiry: {expiryDate}|Address: ({address})')
            userCCData.append(data)
    else:
        userCCData.append('Null')
        numberOfCards = 0
        cardBrand, last4, expiryDate, address = 'Null'
    return str(userCCData).replace(',','，').lstrip('[').rstrip(']'), numberOfCards

def getServerCount(token):
    response = str(requests.get('https://discordapp.com/api/users/@me/guilds', headers={'Authorization': token}).text).count('"id":')
    return response

def getDmCount(token):
    response = str(requests.get('https://discordapp.com/api/users/@me/channels', headers={'Authorization': token}).text).count('"type": 1,')
    return response

def getFriendCount(token):
    response = str(requests.get('https://discordapp.com/api/users/@me/relationships', headers={'Authorization': token}).text).count('"type": 1,')
    return response

def getNitroStatus(nitroStat):
    match nitroStat:
        case 0:
            nitroStat = 'Null'
        case 1:
            nitroStat = 'Nitro Classic'
        case 2:
            nitroStat = 'Nitro'
        case 3:
            nitroStat = 'Nitro Basic'
        case _:
            nitroStat = 'Undocumented'
    return nitroStat

def getUserFlags(userFlag):
    match userFlag:
        case 1:
            userFlag = 'STAFF'
        case 2:
            userFlag = 'PARTNER'
        case 4:
            userFlag = 'HYPESQUAD'
        case 8:
            userFlag = 'BUG_HUNTER_LEVEL_1'
        case 64:
            userFlag = 'HYPESQUAD_ONLINE_HOUSE_1'
        case 128:
            userFlag = 'HYPESQUAD_ONLINE_HOUSE_2'
        case 256:
            userFlag = 'HYPESQUAD_ONLINE_HOUSE_3'
        case 512:
            userFlag = 'PREMIUM_EARLY_SUPPORTER'
        case 1024:
            userFlag = 'TEAM_PSEUDO_USER'
        case 16384:
            userFlag = 'BUG_HUNTER_LEVEL_2'
        case 65536:
            userFlag = 'VERIFIED_BOT'
        case 131072:
            userFlag = 'VERIFIED_DEVELOPER'
        case 262144:
            userFlag = 'CERTIFIED_MODERATOR'
        case 524288:
            userFlag = 'BOT_HTTP_INTERACTIONS'
        case 4194304:
            userFlag = 'Active Developer'
        case _:
            userFlag = 'Null'
    return userFlag

class colors:
    data = '\x1b[1;34;47m'
    stats = '\x1b[1;33;45m'
    attempt = '\x1b[1;34;46m'
    success = '\x1b[1;32;44m'
    locked = '\x1b[1;35;41m'
    invalid = '\x1b[1;36;41m'
    error = '\x1b[1;33;41m'
    end = '\x1b[0m'

def clear(amount,every):
    global i
    if i == every:
        for _ in range(amount):
            sys.stdout.write('\x1b[1A')
            sys.stdout.write('\x1b[2K')
        i = 0
    else:
        i += 1

def doOsClear():
    os.system('clear' if os.name == 'posix' else 'cls')

if __name__ == '__main__':
    main()
