#IF YOU ARE SEEING THIS AND YOU HAVE PAID FOR THIS PROGRAM IT MEANS THAT YOU HAVE BEEN SCAMMED !!
#THE SOURCE CODE IS LOCATED AT: https://github.com/EmptyGateAhead/discordTokenCheckerCLI
#THE DATE IS 29/05/2023
import requests, argparse, sys, os
from datetime import datetime
parser = argparse.ArgumentParser(description="simplistic discord token checker, no bells or whistles")
parser.add_argument('-o','--output', action='store', dest='outputFileName', required=True, help='output file')
parser.add_argument('-i','--input', action='store', dest='inputFileName', required=True, help='input file')
parser.add_argument('--saveErrorTokens', action='store', dest='saveErrorTokens', required=False, help='saved locked tokens')
#parser.add_argument('-a','--avatars', action='store', dest='getAvatars', required=False, help='download avatars and save them to directory with names')soon ;)
args = parser.parse_args()
i = 0

def main():
    outputFile = str(args.outputFileName)
    inputFile = str(args.inputFileName)
    hits = 0
    locked = 0
    invalid = 0
    error = 0
    count = 0
    fileLength = 0
    with open(inputFile, 'r') as getFileLength:
        fileLength = sum(1 for _ in getFileLength)
        getFileLength.close
    if fileLength < 1: print(f'{colors.error}[!] Cannot use an empty input file{colors.end}'); exit()
    if args.saveErrorTokens != None: saveErrorTokens = open(args.saveErrorTokens, 'a')
    outFile = open(outputFile, 'a')
    outFile.write('token,username,nickname,email,email verified,phone,locale,nsfw,linked accounts,mfa status,ID,bio,creation date,user flags,nitro status,server count,dm count,friend count,payment data'+'\n')
    with open(inputFile, 'r') as inputFile:
        for line in inputFile:
            token = str(line).rstrip('\n')
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
                try: bio = responseData.split('"bio": "')[1].split('"')[0].replace(',','，')
                except IndexError: bio = 'Null'; pass
                try: phone = responseData.split('"phone": "')[1].split('"')[0]
                except IndexError: phone = 'Null'; pass
                try: nickname = responseData.split('"global_name": "')[1].split('"')[0]
                except IndexError: nickname = 'Null'; pass
                try: linkedAccounts = responseData.split('"linked_users": ["')[1].split(']')[0]
                except IndexError: linkedAccounts = 'Null'; pass
                try: creationDateUtc = datetime.utcfromtimestamp((int(identifier >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC')#
                except IndexError: creationDateUtc = 'Unknown'; pass
                try: flag = int(responseData.split('"public_flags": ')[1].split(',')[0])
                except IndexError: flags = 'Null'; pass
                userFlags = getUserFlags(flag)
                try: nitro = int(responseData.split('"premium_type": ')[1].split(',')[0])
                except IndexError: nitroStatus = 'Null'; pass
                nitroStatus = getNitroStatus(nitro)
                try: serverCount = str(requests.get('https://discordapp.com/api/users/@me/guilds', headers={'Authorization': token}).text).count('"id":')
                except IndexError: serverCount = 'Null'; pass
                try: dmCount = str(requests.get('https://discordapp.com/api/users/@me/channels', headers={'Authorization': token}).text).count('"type": 1,')
                except IndexError: dmCount = 'Null'; pass
                try: friendCount = str(requests.get('https://discordapp.com/api/users/@me/relationships', headers={'Authorization': token}).text).count('"type": 1,')
                except IndexError: friendCount = 'Null'; pass
                try:
                    payment = requests.get('https://discordapp.com/api/users/@me/billing/payment-sources', headers={'Authorization': token}).text
                    if payment != '[]': paymentData = 'True'
                    else: paymentData = 'Null'
                except IndexError: paymentData = 'Null'; pass

                outFile.write(f'{token},{username}#{discrim},{nickname},{email},{verifiedMail},{phone},{locale},{nsfw},{linkedAccounts},{mfaStatus},{identifier},{bio},{creationDateUtc},{userFlags},{nitroStatus},{serverCount},{dmCount},{friendCount},{paymentData}\n')
                hits += 1
            elif response.status_code == 403:#locked
                print(f"{colors.locked}[-] Token locked: {token}{colors.end}")
                if args.saveErrorTokens != None:
                    saveErrorTokens.write(f'Locked: {token}\n')
                locked += 1
            else:
                print(f"{colors.invalid}[-] Token invalid: {token}{colors.end}")
                if args.saveErrorTokens != None:
                    saveErrorTokens.write(f'Invalid: {token}\n')
                invalid += 1
            clear(50,6)#8:1
            print(f"{colors.data}[+] Token: {token}|User: {username}#{discrim}|Nickname: {nickname}|Email: {email} Verified: {verifiedMail}|Phone: {phone}\n[+] Locale: {locale}|NSFW: {nsfw}|Linked accounts: {linkedAccounts}| MFA: {mfaStatus}|ID: {identifier}\n[+] Creation Time: {creationDateUtc}|Nitro Status: {nitroStatus}|User Flags: {userFlags}|Friends Count: {friendCount}|Server Count: {serverCount}|DM Count: {dmCount}|Payment Data: {paymentData}\n[+] BIO: {bio}{colors.end}\n{colors.stats}[+] Hits: {hits}|Invalid: {invalid}|Locked: {locked}|Error: {error}| ({count}/{fileLength}){colors.end}")
            count += 1
    doOsClear()
    print(f'{colors.stats}[+] Program complete saved {hits} tokens to {outputFile}\n └Stats:\n  └Hits: {hits}|Locked: {locked}|Invalid: {invalid}|Error: {error}{colors.end}')


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
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        doOsClear()
        print(f'{colors.error}[!] Program Exited safely{colors.end}')
